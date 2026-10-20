# -*- coding: utf-8 -*-
import os
import zipfile
import re
import html

def format_content_to_xhtml_paragraphs(raw_content: str) -> str:
    """
    Chuyển đổi mọi loại nội dung (văn bản thô, html, markdown) thành
    các thẻ <p class="paragraph">...</p> chuẩn XHTML 1.1 để tương thích
    100% với cơ chế parse DOM Element của epub_view trong Flutter.
    """
    if not raw_content or not raw_content.strip():
        return '<p class="paragraph">Nội dung chương đang được cập nhật...</p>'

    content = raw_content.strip()

    # Nếu văn bản chứa thẻ <p>
    if "<p>" in content or "<p " in content:
        raw_paras = re.findall(r'<p[^>]*>(.*?)</p>', content, re.DOTALL | re.IGNORECASE)
        if raw_paras:
            result = []
            for p in raw_paras:
                clean_p = re.sub(r'<[^>]+>', '', p).strip()
                if clean_p:
                    escaped = html.escape(clean_p)
                    result.append(f'<p class="paragraph">{escaped}</p>')
            if result:
                return "\n    ".join(result)

    # Nếu văn bản thô theo đoạn văn
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', content) if p.strip()]
    if len(paragraphs) <= 1:
        # Thử ngắt theo từng dòng nếu không có dòng trống kép
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

    result = []
    for p in paragraphs:
        # Loại bỏ các tag HTML lạ nếu có sót
        clean_text = re.sub(r'<[^>]+>', '', p).strip()
        if not clean_text:
            continue
        escaped = html.escape(clean_text)
        result.append(f'<p class="paragraph">{escaped}</p>')

    if not result:
        return '<p class="paragraph">Nội dung đang được cập nhật...</p>'

    return "\n    ".join(result)

def create_valid_epub(output_path: str, title: str, author: str, chapters: list[dict]):
    """
    Tạo tệp EPUB 2/3 chuẩn quốc tế (IDPF), chia chương sạch đẹp,
    tương thích hoàn hảo với epub_view của Flutter, Apple Books, Google Play Books và Kobo.
    chapters: [{'title': 'Chương 1', 'content': 'Nội dung hoặc các đoạn văn...'}]
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    safe_title = html.escape(title.strip())
    safe_author = html.escape(author.strip()) if author else "Nhiều tác giả"

    with zipfile.ZipFile(output_path, 'w') as z:
        # 1. mimetype PHẢI là file đầu tiên và KHÔNG được nén (STORED) theo chuẩn EPUB OCF
        z.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        # 2. META-INF/container.xml
        container_xml = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>'''
        z.writestr('META-INF/container.xml', container_xml, compress_type=zipfile.ZIP_DEFLATED)

        # 3. CSS định dạng văn bản chuẩn, hỗ trợ cả sáng, sepia và tối
        css_content = '''@charset "utf-8";
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.7;
    margin: 1.5em 1.2em;
    padding: 0;
}
h1.chapter-title {
    color: #e65100;
    font-size: 1.45em;
    font-weight: bold;
    border-bottom: 2px solid #ff9800;
    padding-bottom: 0.35em;
    margin-top: 0.4em;
    margin-bottom: 0.6em;
    text-align: left;
}
.author-meta {
    font-style: italic;
    color: #888888;
    margin-bottom: 1.8em;
    font-size: 0.9em;
}
p.paragraph {
    margin-top: 0;
    margin-bottom: 1.1em;
    text-align: justify;
    text-indent: 1.5em;
    line-height: 1.7;
}
'''
        z.writestr('OEBPS/stylesheet.css', css_content, compress_type=zipfile.ZIP_DEFLATED)

        manifest_items = [
            '<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>',
            '<item id="css" href="stylesheet.css" media-type="text/css"/>'
        ]
        spine_items = []
        nav_points = []

        # 4. Tạo từng file chương XHTML
        for i, chap in enumerate(chapters, 1):
            chap_filename = f"chapter_{i}.xhtml"
            item_id = f"chap_{i}"
            manifest_items.append(f'<item id="{item_id}" href="{chap_filename}" media-type="application/xhtml+xml"/>')
            spine_items.append(f'<itemref idref="{item_id}"/>')

            raw_chap_title = chap.get("title", f"Chương {i}")
            safe_chap_title = html.escape(raw_chap_title.strip())

            nav_points.append(f'''    <navPoint id="navPoint-{i}" playOrder="{i}">
      <navLabel><text>{safe_chap_title}</text></navLabel>
      <content src="{chap_filename}"/>
    </navPoint>''')

            # Chuyển đổi nội dung thành các thẻ <p class="paragraph">
            formatted_paragraphs = format_content_to_xhtml_paragraphs(chap.get("content", ""))

            chap_html = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="vi">
<head>
    <title>{safe_chap_title}</title>
    <link rel="stylesheet" type="text/css" href="stylesheet.css"/>
</head>
<body>
    <h1 class="chapter-title">{safe_chap_title}</h1>
    <div class="author-meta">Tác phẩm: {safe_title} | Tác giả: {safe_author}</div>
    {formatted_paragraphs}
</body>
</html>'''
            z.writestr(f'OEBPS/{chap_filename}', chap_html.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)

        # 5. OEBPS/content.opf
        unique_book_id = abs(hash(f"{title}_{author}"))
        content_opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookID" version="2.0">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>{safe_title}</dc:title>
    <dc:creator>{safe_author}</dc:creator>
    <dc:language>vi</dc:language>
    <dc:identifier id="BookID">urn:bookhub:{unique_book_id}</dc:identifier>
  </metadata>
  <manifest>
    {''.join(manifest_items)}
  </manifest>
  <spine toc="ncx">
    {''.join(spine_items)}
  </spine>
</package>'''
        z.writestr('OEBPS/content.opf', content_opf.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)

        # 6. OEBPS/toc.ncx (Mục lục tiêu chuẩn EPUB 2)
        toc_ncx = f'''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta name="dtb:uid" content="urn:bookhub:{unique_book_id}"/>
    <meta name="dtb:depth" content="1"/>
    <meta name="dtb:totalPageCount" content="0"/>
    <meta name="dtb:maxPageNumber" content="0"/>
  </head>
  <docTitle><text>{safe_title}</text></docTitle>
  <docAuthor><text>{safe_author}</text></docAuthor>
  <navMap>
{''.join(nav_points)}
  </navMap>
</ncx>'''
        z.writestr('OEBPS/toc.ncx', toc_ncx.encode('utf-8'), compress_type=zipfile.ZIP_DEFLATED)

if __name__ == "__main__":
    test_path = "uploads/test_fixed.epub"
    test_chapters = [
        {"title": "Chương 1: Mở đầu", "content": "Đây là đoạn văn 1.\n\nĐây là đoạn văn 2."},
        {"title": "Chương 2: Diễn biến", "content": "Nội dung tiếp theo...\nNhiều chi tiết hấp dẫn."}
    ]
    create_valid_epub(test_path, "Kiểm Thử Sách", "Tác Giả Việt Nam", test_chapters)
    print("EPUB test file created successfully.")
