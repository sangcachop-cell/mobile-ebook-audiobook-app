import os
import re
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# Đăng ký font tiếng Việt từ hệ thống Windows
FONT_REGULAR = 'Helvetica'
FONT_BOLD = 'Helvetica-Bold'
FONT_ITALIC = 'Helvetica-Oblique'

try:
    if os.path.exists('C:/Windows/Fonts/arial.ttf'):
        pdfmetrics.registerFont(TTFont('ArialVN', 'C:/Windows/Fonts/arial.ttf'))
        pdfmetrics.registerFont(TTFont('ArialVN-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
        if os.path.exists('C:/Windows/Fonts/ariali.ttf'):
            pdfmetrics.registerFont(TTFont('ArialVN-Italic', 'C:/Windows/Fonts/ariali.ttf'))
        else:
            pdfmetrics.registerFont(TTFont('ArialVN-Italic', 'C:/Windows/Fonts/arial.ttf'))
        FONT_REGULAR = 'ArialVN'
        FONT_BOLD = 'ArialVN-Bold'
        FONT_ITALIC = 'ArialVN-Italic'
except Exception as e:
    print(f"Lỗi nạp font tiếng Việt: {e}")

class BookCanvas(canvas.Canvas):
    """Canvas thông minh hỗ trợ 2 pass để tính tổng số trang và in Header/Footer đẹp mắt"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages):
        # Không vẽ header/footer trên trang bìa (trang 1)
        if self._pageNumber <= 1:
            return
        
        self.saveState()
        self.setFont(FONT_REGULAR, 8.5)
        self.setFillColor(colors.HexColor("#757575"))
        
        # Header đường kẻ mờ và tiêu đề sách
        self.setStrokeColor(colors.HexColor("#E0E0E0"))
        self.setLineWidth(0.5)
        self.line(54, 842 - 38, 595 - 54, 842 - 38)
        self.drawString(54, 842 - 32, getattr(self, 'doc_title', 'BookHub Reader'))
        
        # Footer đường kẻ và số trang
        self.line(54, 45, 595 - 54, 45)
        self.drawString(54, 32, "BookHub • Ứng dụng Sách & Sách nói điện tử")
        page_str = f"Trang {self._pageNumber} / {total_pages}"
        self.drawRightString(595 - 54, 32, page_str)
        
        self.restoreState()

def create_valid_pdf(output_path: str, title: str, author: str, chapters: list[dict], category: str = "Sách Tiêu Biểu"):
    """
    Tạo tệp PDF tiếng Việt nhiều trang hoàn chỉnh:
    - Bìa sách trang trọng, viền hoa văn hiện đại.
    - Trang Mục lục chi tiết.
    - Từng chương sách đầy đặn, các đoạn văn được dàn trang chuẩn sách in.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=54,
        leftMargin=54,
        topMargin=50,
        bottomMargin=55
    )
    
    # Gán tiêu đề cho canvas dùng trong header
    doc.doc_title = f"{title} — {author}"
    
    # Định nghĩa styles
    cover_title_style = ParagraphStyle(
        'CoverTitle',
        fontName=FONT_BOLD,
        fontSize=24,
        leading=32,
        alignment=1, # Căn giữa
        textColor=colors.HexColor('#D35400'),
        spaceAfter=15
    )
    
    cover_author_style = ParagraphStyle(
        'CoverAuthor',
        fontName=FONT_REGULAR,
        fontSize=14,
        leading=18,
        alignment=1,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=10
    )
    
    cover_cat_style = ParagraphStyle(
        'CoverCat',
        fontName=FONT_ITALIC,
        fontSize=11,
        leading=15,
        alignment=1,
        textColor=colors.HexColor('#7F8C8D'),
        spaceAfter=25
    )
    
    toc_heading_style = ParagraphStyle(
        'TOCHeading',
        fontName=FONT_BOLD,
        fontSize=16,
        leading=22,
        alignment=0,
        textColor=colors.HexColor('#C0392B'),
        spaceBefore=15,
        spaceAfter=15
    )
    
    toc_item_style = ParagraphStyle(
        'TOCItem',
        fontName=FONT_REGULAR,
        fontSize=11,
        leading=18,
        textColor=colors.HexColor('#34495E'),
        leftIndent=15,
        spaceAfter=6
    )
    
    chap_title_style = ParagraphStyle(
        'ChapTitle',
        fontName=FONT_BOLD,
        fontSize=16,
        leading=22,
        textColor=colors.HexColor('#C0392B'),
        spaceBefore=15,
        spaceAfter=12,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BookBody',
        fontName=FONT_REGULAR,
        fontSize=11,
        leading=18,
        textColor=colors.HexColor('#2C3E50'),
        firstLineIndent=20,
        spaceAfter=8,
        alignment=4 # Căn đều 2 bên
    )
    
    quote_style = ParagraphStyle(
        'BookQuote',
        fontName=FONT_ITALIC,
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor('#566573'),
        leftIndent=25,
        rightIndent=25,
        spaceBefore=6,
        spaceAfter=10
    )

    story = []
    
    # ---------------- 1. TRANG BÌA ----------------
    story.append(Spacer(1, 90))
    story.append(Paragraph(title.upper(), cover_title_style))
    story.append(Paragraph(f"Tác giả: <b>{author}</b>", cover_author_style))
    story.append(Paragraph(f"Thể loại: {category}", cover_cat_style))
    story.append(HRFlowable(width="60%", thickness=2, color=colors.HexColor('#E67E22'), spaceBefore=10, spaceAfter=25))
    story.append(Spacer(1, 40))
    
    intro_box = f"Ấn bản điện tử số hóa chính thức phục vụ trải nghiệm đọc & nghe sách đa phương tiện trên <b>BookHub</b>. Tác phẩm <i>{title}</i> của tác giả <b>{author}</b> là một trong những tác phẩm tiêu biểu mang giá trị văn hóa, tri thức và chiều sâu tư tưởng sâu sắc."
    story.append(Paragraph(intro_box, quote_style))
    story.append(Spacer(1, 60))
    story.append(Paragraph("<b>NHÀ XUẤT BẢN BOOKHUB DIGITAL</b>", ParagraphStyle('Publisher', fontName=FONT_BOLD, fontSize=10, alignment=1, textColor=colors.HexColor('#7F8C8D'))))
    story.append(PageBreak())
    
    # ---------------- 2. TRANG MỤC LỤC ----------------
    story.append(Spacer(1, 20))
    story.append(Paragraph("MỤC LỤC TÁC PHẨM", toc_heading_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#BDC3C7'), spaceBefore=5, spaceAfter=18))
    
    for idx, chap in enumerate(chapters, 1):
        clean_title = chap['title']
        story.append(Paragraph(f"<b>{idx}.</b> {clean_title}", toc_item_style))
    
    story.append(Spacer(1, 30))
    story.append(Paragraph("<i>Chúc bạn có những giờ phút thưởng thức tác phẩm thật nhiều cảm hứng và ý nghĩa!</i>", quote_style))
    story.append(PageBreak())
    
    # ---------------- 3. NỘI DUNG TỪNG CHƯƠNG ----------------
    for idx, chap in enumerate(chapters, 1):
        story.append(Spacer(1, 10))
        story.append(Paragraph(chap['title'], chap_title_style))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E74C3C'), spaceBefore=4, spaceAfter=14))
        
        # Làm sạch nội dung văn bản
        text_content = chap['content']
        # Thay thế các thẻ <p> hoặc ngắt dòng
        clean_text = text_content.replace('</p>', '\n').replace('<p>', '')
        clean_text = re.sub(r'<[^>]+>', '', clean_text)
        
        paragraphs = [p.strip() for p in clean_text.split('\n') if p.strip()]
        for p_text in paragraphs:
            # Nếu là đoạn trích thơ hoặc câu châm ngôn ngắn
            if p_text.startswith('"') or p_text.startswith('“') or p_text.startswith('—'):
                story.append(Paragraph(p_text, quote_style))
            else:
                story.append(Paragraph(p_text, body_style))
                
        if idx < len(chapters):
            story.append(PageBreak())
            
    # Tạo PDF sử dụng BookCanvas
    def make_canvas(*args, **kwargs):
        c = BookCanvas(*args, **kwargs)
        c.doc_title = f"{title} — {author}"
        return c

    doc.build(story, canvasmaker=make_canvas)
    return output_path

if __name__ == "__main__":
    test_pdf = "backend/uploads/test_book_sample.pdf"
    test_chaps = [
        {"title": "Chương 1: Mở đầu cuộc hành trình", "content": "<p>Đây là nội dung thử nghiệm một đoạn văn dài miêu tả cảnh sắc quê hương thanh bình buổi sớm mai.</p><p>Gió nhẹ lay động những rặng tre xanh ngát ven bờ sông Đáy.</p>"},
        {"title": "Chương 2: Thử thách và bài học", "content": "<p>Con đường phía trước còn nhiều chông gai và thử thách. Nhưng ý chí con người luôn mạnh mẽ hơn nghịch cảnh.</p>"}
    ]
    create_valid_pdf(test_pdf, "Tôi Thấy Hoa Vàng Trên Cỏ Xanh", "Nguyễn Nhật Ánh", test_chaps, "Văn học Việt Nam")
    print("PDF created, size:", os.path.getsize(test_pdf))
