import os
import sys
import asyncio
import edge_tts
import json

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from database import get_connection
from epub_builder import create_valid_epub
from pdf_builder import create_valid_pdf

UPLOAD_DIR = os.path.join(CURRENT_DIR, "uploads")
AUDIO_DIR = os.path.join(UPLOAD_DIR, "audio")
BOOKS_DIR = os.path.join(UPLOAD_DIR, "books")
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(BOOKS_DIR, exist_ok=True)

# Danh mục sách tiếng Việt đặc sắc
VIETNAMESE_BOOKS = [
    {
        "title": "Đắc Nhân Tâm",
        "author": "Dale Carnegie",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 348,
        "format": "pdf",
        "summary": "Nghệ thuật thu phục lòng người và đạt được thành công bền vững trong sự nghiệp và cuộc sống.",
        "narration_text": "Chào mừng bạn đến với sách nói Đắc Nhân Tâm của tác giả Dale Carnegie. Chương một: Nghệ thuật đối nhân xử thế. Muốn lấy mật thì đừng phá tổ ong. Vào ngày 7 tháng 5 năm 1931, một cuộc lùng bắt tội phạm rúng động đã diễn ra tại thành phố New York. Hàng trăm cảnh sát vây bủa tên sát nhân Francis Two Gun Crowley. Trong bức thư để lại, hắn viết: Dưới lớp áo này là một trái tim mệt mỏi nhưng lương thiện, một trái tim không hề muốn làm tổn thương ai. Kẻ tử tội tàn ác nhất vẫn luôn tìm cách bào chữa cho chính mình. Vì vậy, chỉ trích người khác là vô ích và chỉ gây thêm thù oán. Hãy học cách lắng nghe, thấu cảm và tôn trọng người đối diện.",
        "chapters": [
            {
                "title": "Chương 1: Nghệ thuật đối nhân xử thế - Đừng chỉ trích, oán trách hay than phiền",
                "content": "<p>Vào ngày 7 tháng 5 năm 1931, thành phố New York chứng kiến một cuộc vây bắt tội phạm gay cấn chưa từng có. Crowley, kẻ được mệnh danh là 'Hai Súng', đã bị dồn vào đường cùng.</p><p>Hơn một trăm cảnh sát bao vây căn hộ của hắn. Tiếng súng xé tan màn đêm yên tĩnh. Nhưng điều đáng kinh ngạc là trong lúc đạn bay rào rào, Crowley đã viết một bức thư: 'Dưới lớp áo này là một trái tim không hề muốn làm hại ai'.</p><p>Ngay cả những tên tội phạm nguy hiểm nhất cũng không bao giờ nhận mình có lỗi. Vậy thì con người bình thường chúng ta lại càng nhạy cảm trước lời chỉ trích. Muốn thu phục lòng người, điều tối thượng đầu tiên là: Không chỉ trích, không phán xét, hãy bắt đầu bằng sự thấu hiểu.</p>"
            },
            {
                "title": "Chương 2: Bí mật lớn nhất trong giao tiếp - Thành thật khen ngợi người khác",
                "content": "<p>Nhu cầu sâu sắc nhất của bản tính con người là khao khát được công nhận và cảm thấy mình quan trọng. Sigmund Freud gọi đó là khát vọng trở nên vĩ đại.</p><p>Một lời khen chân thành có thể thắp sáng cả một ngày u ám, thay đổi số phận của một con người. Hãy phân biệt rõ giữa sự ngợi khen chân thành xuất phát từ trái tim và lời xu nịnh giả tạo ngoài chót lưỡi đầu môi.</p>"
            },
            {
                "title": "Chương 3: Gợi cho người khác ý muốn thực hiện điều bạn muốn",
                "content": "<p>Cách duy nhất trên đời để thuyết phục người khác làm một việc gì đó là khơi gợi trong lòng họ niềm mong muốn làm việc đó. Cá thích ăn giun chứ không thích ăn dâu tây. Muốn câu được cá, hãy móc con giun vào lưỡi câu.</p>"
            }
        ]
    },
    {
        "title": "Nhà Giả Kim",
        "author": "Paulo Coelho",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=600",
        "rating_avg": 5.0,
        "review_count": 420,
        "format": "epub",
        "summary": "Hành trình huyền thoại của chàng chăn cừu Santiago đi tìm kho báu và lắng nghe tiếng gọi trái tim.",
        "narration_text": "Sách nói Nhà Giả Kim của nhà văn Paulo Coelho. Bản dịch tiếng Việt chuẩn. Chương một: Giấc mơ của chàng chăn cừu Santiago. Chàng trai tên là Santiago. Trời vừa chập tối khi chàng tới một nhà thờ cổ đổ nát gần rặng núi Andalusia. Một cây sung lớn mọc lên ngay tại nơi từng là phòng thánh. Chàng ngả lưng cùng đàn cừu và chìm vào giấc mơ: một đứa trẻ dẫn chàng tới Kim Tự Tháp Ai Cập và bảo rằng nơi đó có kho báu đang chờ chàng. Khi bạn thực sự quyết tâm muốn điều gì, toàn bộ vũ trụ sẽ đồng mưu giúp bạn đạt được điều đó.",
        "chapters": [
            {
                "title": "Chương 1: Giấc mơ của chàng chăn cừu Santiago",
                "content": "<p>Chàng trai tên là Santiago. Trời vừa chập tối khi chàng đến một nhà thờ cổ đổ nát. Mái nhà thờ đã sập từ lâu, và một cây sung lớn đã mọc lên ngay tại nơi từng là phòng thánh.</p><p>Đêm đó chàng lại mơ thấy giấc mơ kỳ lạ: một đứa trẻ dẫn chàng tới chân Kim Tự Tháp Ai Cập và bảo tại đó có một kho báu vĩ đại đang chờ chàng.</p>"
            },
            {
                "title": "Chương 2: Cuộc gặp với Vua xứ Salem và dấu hiệu vũ trụ",
                "content": "<p>Santiago gặp ông lão Melchizedek, vua xứ Salem. Ông nói với chàng về Vận Mệnh Riêng của mỗi con người: 'Bất kể bạn là ai và bạn làm gì, khi bạn thực sự mong muốn một điều gì đó, thì toàn bộ vũ trụ sẽ hiệp lực để giúp bạn đạt được'.</p>"
            },
            {
                "title": "Chương 3: Băng qua sa mạc Sahara và tìm thấy tình yêu",
                "content": "<p>Đoàn lữ hành tiến vào sa mạc Sahara mênh mông. Tại ốc đảo Al-Fayoum, Santiago gặp Fatima bên giếng nước. Chàng nhận ra tình yêu chân chính không bao giờ cản bước con người theo đuổi ước mơ.</p>"
            }
        ]
    },
    {
        "title": "Tuổi Trẻ Đáng Giá Bao Nhiêu",
        "author": "Rosie Nguyễn",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=600",
        "rating_avg": 4.8,
        "review_count": 290,
        "format": "pdf",
        "summary": "Cuốn sách thức tỉnh người trẻ rèn luyện bản thân, đọc sách, học hỏi và sống một tuổi trẻ rực rỡ không hối tiếc.",
        "narration_text": "Sách nói Tuổi Trẻ Đáng Giá Bao Nhiêu của tác giả Rosie Nguyễn. Chương một: Ta đã làm gì với tuổi trẻ của mình? Bạn hối tiếc vì không nắm bắt lấy một cơ hội nào đó, chẳng có ai phải mất ngủ. Bạn trải qua những ngày tháng nhạt nhẽo với công việc bạn căm ghét, người ta chẳng hề bận lòng. Bạn có chết mòn nơi xó tường với những ước mơ dang dở, đó không phải việc của họ. Suy cho cùng, cuộc đời của bạn là của chính bạn. Hãy sống hết mình, không ngừng đọc sách, đi xa và rèn giũa bản thân từng ngày.",
        "chapters": [
            {
                "title": "Chương 1: Ta đã làm gì với tuổi trẻ của mình?",
                "content": "<p>Tuổi trẻ là quãng thời gian tươi đẹp nhất của đời người, khi ta có sức khỏe, có nhiệt huyết và có thời gian. Nhưng đáng tiếc, nhiều người trẻ lại để nó trôi qua trong thờ ơ và lãng phí.</p><p>Hãy đọc nhiều hơn, học hỏi nhiều hơn và dám bước ra khỏi vùng an toàn của chính mình.</p>"
            },
            {
                "title": "Chương 2: Học để làm gì và học như thế nào?",
                "content": "<p>Tự học là kỹ năng sinh tồn quan trọng nhất của thế kỷ 21. Trường học chỉ cho ta chìa khóa, còn mở cánh cửa tri thức nào là do chính bản thân ta lựa chọn.</p>"
            }
        ]
    },
    {
        "title": "Nghĩ Giàu Và Làm Giàu",
        "author": "Napoleon Hill",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 310,
        "format": "pdf",
        "summary": "13 nguyên tắc vàng tạo dựng của cải và thành công vượt bậc được đúc kết từ 500 doanh nhân vĩ đại nhất lịch sử.",
        "narration_text": "Sách nói Nghĩ Giàu Và Làm Giàu của Napoleon Hill. Chương một: Khát vọng - Điểm khởi đầu của mọi thành tựu. Cách đây hơn 30 năm, Edwin C. Barnes đã phát hiện ra một sự thật vĩ đại rằng con người ta hoàn toàn có thể nghĩ giàu và làm giàu. Khát vọng của ông không chỉ là một điều ước mơ hồ, mà là một khao khát cháy bỏng, sẵn sàng đốt cháy tất cả những cây cầu phía sau để chỉ tiến về phía trước.",
        "chapters": [
            {
                "title": "Chương 1: Khát vọng - Điểm khởi đầu của mọi thành tựu",
                "content": "<p>Mọi thành tựu vĩ đại trong lịch sử loài người đều bắt đầu từ một ý nghĩ được nuôi dưỡng bởi khát vọng cháy bỏng. Khi bạn biết chính xác mình muốn gì và kiên quyết không bỏ cuộc, cả thế giới sẽ nhường đường cho bạn.</p>"
            },
            {
                "title": "Chương 2: Niềm tin và Trực giác vô thức",
                "content": "<p>Niềm tin là trạng thái tâm trí có thể được tạo ra hoặc kích thích bằng những lời tự ám thị tích cực lặp đi lặp lại hàng ngày.</p>"
            }
        ]
    },
    {
        "title": "Số Đỏ",
        "author": "Vũ Trọng Phụng",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1476275466078-4007374efbbe?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 275,
        "format": "epub",
        "summary": "Kiệt tác trào phúng đỉnh cao của văn học Việt Nam, châm biếm sâu cay xã hội tư sản thành thị buổi giao thời.",
        "narration_text": "Sách nói Số Đỏ của nhà văn Vũ Trọng Phụng. Chương một: Cuộc tao ngộ tại sân quần vợt. Xuân Tóc Đỏ, một thằng bé nhặt banh quần vợt đầu đường xó chợ, bỗng chốc được bà Phó Đoan nâng đỡ. Bằng sự láu cá và thời thế đảo điên, hắn từng bước leo lên đỉnh cao danh vọng trong một xã hội rởm đời chuộng Âu hóa.",
        "chapters": [
            {
                "title": "Chương 1: Cuộc gặp gỡ định mệnh của Xuân Tóc Đỏ",
                "content": "<p>Xuân Tóc Đỏ vốn là đứa trẻ mồ côi đi lang bạt kỳ hồ, làm đủ nghề từ thổi loa quảng cáo thuốc lậu cho đến nhặt bóng ở sân quần vợt. Hắn vốn vô học, láu cá nhưng lại cực kỳ may mắn trước những kẻ đạo đức giả.</p>"
            },
            {
                "title": "Chương 2: Hạnh phúc của một tang gia",
                "content": "<p>Cụ cố Hồng ho một tiếng dài rồi nhắm mắt xuôi tay. Cả gia đình ai nấy đều hân hoan rạng rỡ vì cái chúc thư cuối cùng cũng đi vào thời kỳ thực hành. Tang lễ biến thành một ngày hội trình diễn thời trang và khoe khoang kệch cỡm.</p>"
            }
        ]
    },
    {
        "title": "Lão Hạc",
        "author": "Nam Cao",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?q=80&w=600",
        "rating_avg": 5.0,
        "review_count": 390,
        "format": "pdf",
        "summary": "Tác phẩm hiện thực xúc động về số phận bi thảm và nhân cách cao đẹp của người nông dân Việt Nam trước cách mạng.",
        "narration_text": "Sách nói Lão Hạc của nhà văn Nam Cao. Lão Hạc sang nhà tôi chơi. Lão ngồi hút điếu thuốc lào rồi bảo: Cậu Vàng đi đời rồi ông giáo ạ. Khốn nạn, ông giáo ơi, nó có biết gì đâu. Tôi cho nó ăn cơm xong, thằng Mục rình sẵn bắt trói giật cánh khuỷu. Tôi già bằng này tuổi đầu mà lại đi lừa một con chó. Khóc nghẹn ngào, lão lấy tay áo quệt nước mắt. Lão Hạc thà ăn bả chó tự vẫn để giữ trọn mảnh vườn cho đứa con trai đi phu đồn điền cao su.",
        "chapters": [
            {
                "title": "Phần 1: Lão Hạc bán con chó Vàng",
                "content": "<p>Lão Hạc sang nhà tôi chơi. Vừa ngồi xuống mép phản, lão đã cất tiếng nói run rẩy: 'Cậu Vàng đi đời rồi ông giáo ạ!'.</p><p>Đôi mắt lão ầng ậc nước. Lão bảo: 'Khốn nạn, tôi già bằng này tuổi đầu rồi mà còn đi đánh lừa một con chó! Nó tin tôi thế, vẫy đuôi mừng rỡ mà tôi nỡ lòng nào để người ta bắt nó đi thịt...'.</p>"
            },
            {
                "title": "Phần 2: Cái chết đau đớn và phẩm giá cao quý",
                "content": "<p>Lão Hạc từ chối mọi sự giúp đỡ của tôi. Lão gửi gắm mảnh vườn cho con trai rồi xin bả chó của Binh Tư. Lão chết trong vật vã, đau đớn dữ dội, nhưng nhân cách của lão thì sáng ngời như một đóa sen giữa đầm lầy tăm tối.</p>"
            }
        ]
    },
    {
        "title": "Chí Phèo",
        "author": "Nam Cao",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=600",
        "rating_avg": 5.0,
        "review_count": 450,
        "format": "pdf",
        "summary": "Tiếng kêu cứu xé lòng đòi quyền làm người lương thiện của người nông dân bị bần cùng hóa và lưu manh hóa.",
        "narration_text": "Sách nói Chí Phèo của nhà văn Nam Cao. Hắn vừa đi vừa chửi. Bao giờ cũng thế, cứ rượu xong là hắn chửi. Bắt đầu hắn chửi trời, có hề gì, trời có của riêng nhà nào? Rồi hắn chửi đời, cả làng Vũ Đại, và chửi cả đứa chết mẹ nào đã đẻ ra thân hắn. Nhưng bát cháo hành ấm áp của Thị Nở bên bờ sông đã đánh thức phần lương tri bị vùi dập suốt mấy mươi năm trong tâm hồn Chí Phèo.",
        "chapters": [
            {
                "title": "Chương 1: Tiếng chửi của Chí Phèo ở làng Vũ Đại",
                "content": "<p>Hắn vừa đi vừa chửi. Bao giờ cũng thế, cứ rượu xong là hắn chửi. Bắt đầu hắn chửi trời. Có hề gì? Trời có của riêng nhà nào? Rồi hắn chửi đời. Thế cũng chẳng sao: đời là tất cả nhưng chẳng là ai.</p><p>Tức mình hắn chửi cả làng Vũ Đại. Nhưng cả làng Vũ Đại ai cũng nhủ thầm: 'Chắc nó trừ mình ra!'.</p>"
            },
            {
                "title": "Chương 2: Bát cháo hành của Thị Nở và khát vọng làm người lương thiện",
                "content": "<p>Lần đầu tiên sau bao năm đâm thuê chém mướn, Chí Phèo tỉnh rượu. Hắn nghe tiếng chim hót ngoài bãi sông, tiếng người đi chợ cười nói xôn xao. Bát cháo hành còn bốc khói của Thị Nở đã làm trỗi dậy khát khao làm hòa với mọi người.</p><p>'Ai cho tao lương thiện? Làm sao cho mất được những vết mảnh chai trên mặt này?' - Tiếng kêu uất nghẹn làm rung chuyển cả làng Vũ Đại.</p>"
            }
        ]
    },
    {
        "title": "Tắt Đèn",
        "author": "Ngô Tất Tố",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1495640388908-05fa85288e61?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 330,
        "format": "pdf",
        "summary": "Bức tranh chân thực, ngột ngạt và khốc liệt về sưu cao thuế nặng đè nặng lên vai người nông dân nghèo Việt Nam.",
        "narration_text": "Sách nói Tắt Đèn của nhà văn Ngô Tất Tố. Tiếng trống thúc thuế vang lên dồn dập từ đình làng Đông Xá. Anh Dậu ốm thập tử nhất sinh vẫn bị cai lệ trói nghiến lôi đi. Trước sự tàn bạo của lũ tay sai, chị Dậu đã vùng lên bảo vệ chồng: Mày trói ngay chồng bà đi, bà cho mày xem! Chị xô ngã tên cai lệ và người nhà lý trưởng, thể hiện sức sống quật khởi của người phụ nữ nông dân.",
        "chapters": [
            {
                "title": "Chương 1: Tiếng trống thúc sưu ở làng Đông Xá",
                "content": "<p>Tiếng trống thúc sưu dồn dập nổi lên từ đình làng. Bầu không khí ngột ngạt như muốn bóp nghẹt từng mái nhà tranh xơ xác.</p><p>Chị Dậu chạy vạy khắp nơi, gạt nước mắt bán đi đứa con gái đầu lòng và ổ chó mới đẻ để mong có tiền chuộc chồng khỏi đình giam.</p>"
            },
            {
                "title": "Chương 2: Cuộc vùng lên dũng cảm của Chị Dậu",
                "content": "<p>Tên cai lệ xông vào nhà định trói anh Dậu đang sốt li bì. Chị Dậu van xin không được, lòng uất ức dâng trào: 'Chồng tôi đau ốm, các ông không được phép hành hạ!'.</p><p>Khi tên cai lệ tát chị, chị túm cổ áo hắn ấn dúi ra cửa. Sức mạnh của tình thương đã chiến thắng sự hung bạo của cường quyền.</p>"
            }
        ]
    },
    {
        "title": "Dế Mèn Phiêu Lưu Ký",
        "author": "Tô Hoài",
        "category": "Thiếu nhi & Cổ tích",
        "image_url": "https://images.unsplash.com/photo-1532012164546-f432f2e3edd4?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 380,
        "format": "epub",
        "summary": "Tác phẩm thiếu nhi kinh điển ngợi ca tinh thần trượng nghĩa, ước mơ hòa bình và bài học đường đời đầu tiên.",
        "narration_text": "Sách nói Dế Mèn Phiêu Lưu Ký của nhà văn Tô Hoài. Tôi sống độc lập từ thuở bé. Ấy là tục lệ lâu đời của họ nhà Dế chúng tôi. Vừa lớn lên, mẹ đã cho tôi ra ở riêng trong một cái hang khang trang bên bờ cỏ. Tôi ăn uống điều độ nên chóng lớn lắm, vuốt ở chân cứng và sắc nhọn, đôi cánh dài chấm đuôi. Nhưng cũng vì thói huênh hoang xốc nổi mà tôi đã gây ra cái chết thương tâm cho Dế Choắt. Đó là bài học đường đời đầu tiên mà tôi ghi nhớ suốt đời.",
        "chapters": [
            {
                "title": "Chương 1: Bài học đường đời đầu tiên",
                "content": "<p>Tôi sống độc lập từ thuở bé. Cứ đến mùa gặt, mẹ tôi lại đưa các con ra ở riêng. Hang của tôi đào sâu vào lòng đất, có nhiều ngóc ngách thoát hiểm.</p><p>Tôi rất tự hào về thân hình cường tráng của mình, nhưng tính tình lại ngạo mạn, hay bắt nạt kẻ yếu. Vì trò nghịch dại trêu chị Cốc, tôi đã hại chết người bạn láng giềng gầy gò Dế Choắt.</p>"
            },
            {
                "title": "Chương 2: Cuộc phiêu lưu vào thế giới rộng lớn",
                "content": "<p>Sau biến cố đau đớn, tôi quyết định lên đường phiêu lưu khám phá thế giới. Tôi kết nghĩa anh em cùng Dế Trũi, cùng chung chí hướng kết đoàn muôn loài làm một nhà thái bình.</p>"
            }
        ]
    },
    {
        "title": "Truyện Kiều",
        "author": "Đại thi hào Nguyễn Du",
        "category": "Thơ ca & Kịch nghệ",
        "image_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=600",
        "rating_avg": 5.0,
        "review_count": 520,
        "format": "pdf",
        "summary": "Kiệt tác thi ca bất hủ số một của nền văn học Việt Nam, kết tinh tinh hoa ngôn ngữ và tư tưởng nhân đạo.",
        "narration_text": "Sách nói Đoạn Trường Tân Thanh - Truyện Kiều của Đại thi hào Nguyễn Du. Trăm năm trong cõi người ta, chữ tài chữ mệnh khéo là ghét nhau. Trải qua một cuộc bể dâu, những điều trông thấy mà đau đớn lòng. Lạ gì bỉ sắc tư phong, trời xanh quen thói má hồng đánh ghen. Thúy Kiều là người con gái tài sắc vẹn toàn nhưng cuộc đời lại chìm nổi mười lăm năm lưu lạc truân chuyên.",
        "chapters": [
            {
                "title": "Đoạn 1: Chị em Thúy Kiều và Hội Đạp Thanh",
                "content": "<p>Đầu lòng hai ả tố nga, Thúy Kiều là chị em là Thúy Vân. Mai cốt cách tuyết tinh thần, mỗi người một vẻ mười phân vẹn mười. Vân xem trang trọng khác vời, khuôn trăng đầy đặn nét ngài nở nang. Kiều càng sắc sảo mặn mà, so bề tài sắc lại là phần hơn.</p><p>Ngày xuân con én đưa thoi, thiều quang chín chục đã ngoài sáu mươi. Cỏ non xanh tận chân trời, cành lê trắng điểm một vài bông hoa.</p>"
            },
            {
                "title": "Đoạn 2: Thề nguyền cùng Kim Trọng và Gia biến",
                "content": "<p>Vầng trăng vằng vặc giữa trời, đinh ninh hai mặt một lời song song. Nhưng tai họa bất ngờ ập xuống gia đình, Kiều đành gạt lệ bán mình chuộc cha và em, bắt đầu chuỗi ngày lưu lạc đoạn trường.</p>"
            }
        ]
    },
    {
        "title": "Hiểu Về Trái Tim",
        "author": "Thầy Thích Minh Niệm",
        "category": "Tâm lý & Xã hội",
        "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 360,
        "format": "pdf",
        "summary": "Tác phẩm tâm lý trị liệu giúp chữa lành vết thương tâm hồn, tìm lại sự bình yên và thấu hiểu nội tâm.",
        "narration_text": "Sách nói Hiểu Về Trái Tim của Thiền sư Thích Minh Niệm. Khổ đau là một thực tại tất yếu của cuộc đời. Nhưng nếu không có khổ đau thì ta sẽ không bao giờ biết được giá trị của hạnh phúc. Hãy quay về quan sát và chăm sóc trái tim mình bằng sự hiểu biết và lòng từ bi. Khi tâm ta bình yên, thế giới xung quanh cũng sẽ trở nên dịu dàng.",
        "chapters": [
            {
                "title": "Chương 1: Khổ đau & Hạnh phúc",
                "content": "<p>Ta thường nghĩ hạnh phúc là khi đạt được những thứ mình muốn, còn khổ đau là khi phải đối diện với mất mát. Nhưng thực ra, khổ đau chỉ xuất hiện khi tâm ta chống cự lại thực tại.</p><p>Hãy ôm ấp nỗi đau như một người mẹ ôm đứa con thơ, lắng nghe nó bằng sự tĩnh lặng và thấu cảm sâu sắc.</p>"
            },
            {
                "title": "Chương 2: Tình yêu chân thật",
                "content": "<p>Yêu thương mà không hiểu biết thì chỉ mang lại sự trói buộc và khổ lụy. Tình yêu đích thực phải bao gồm bốn yếu tố: Từ, Bi, Hỷ, Xả.</p>"
            }
        ]
    },
    {
        "title": "Muôn Kiếp Nhân Sinh",
        "author": "Nguyên Phong",
        "category": "Triết học & Tư tưởng",
        "image_url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 410,
        "format": "epub",
        "summary": "Bức tranh toàn cảnh về quy luật nhân quả, luân hồi và những bài học chuyển hóa vận mệnh nhân loại.",
        "narration_text": "Sách nói Muôn Kiếp Nhân Sinh của tác giả Nguyên Phong. Bản dịch và phóng tác độc quyền. Nhân quả đừng đợi đến kiếp sau mới thấy, nó đang vận hành từng giây từng phút trong đời sống này. Những suy nghĩ, lời nói và hành động của bạn hôm nay chính là hạt mầm tạo nên số phận của bạn trong tương lai. Chỉ có tình thương yêu và sự thức tỉnh mới cứu vãn được nhân loại trước bờ vực diệt vong.",
        "chapters": [
            {
                "title": "Chương 1: Cuộc gặp gỡ huyền bí tại Đài Bắc",
                "content": "<p>Tại tu viện trên đỉnh núi mờ sương, tác giả đã gặp ông Thomas - một doanh nhân tài chính Phố Wall. Ông bắt đầu hé mở những ký ức tiền kiếp kỳ lạ của mình trải dài qua các nền văn minh cổ đại Atlantis và Ai Cập.</p>"
            },
            {
                "title": "Chương 2: Văn minh Atlantis và bài học về lòng tham",
                "content": "<p>Nền văn minh rực rỡ Atlantis đã sụp đổ chìm sâu dưới đáy đại dương bởi vì con người phát triển công nghệ quá nhanh nhưng tâm hồn lại thoái hóa vì dục vọng và quyền lực.</p>"
            }
        ]
    },
    {
        "title": "Tôi Thấy Hoa Vàng Trên Cỏ Xanh",
        "author": "Nguyễn Nhật Ánh",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1509021436665-8f07dbf5bf1d?q=80&w=600",
        "rating_avg": 4.8,
        "review_count": 305,
        "format": "pdf",
        "summary": "Những ký ức trong trẻo, ngọt ngào và day dứt về tuổi thơ làng quê cùng tình anh em sâu nặng.",
        "narration_text": "Sách nói Tôi Thấy Hoa Vàng Trên Cỏ Xanh của nhà văn Nguyễn Nhật Ánh. Tuổi thơ làng quê nghèo khó nhưng đong đầy tình cảm. Thiều và Tường, hai anh em với những trò nghịch ngợm bên bờ rào, con cào cào lá tre và những rung động đầu đời ngây ngô cùng cô bé Mận. Những hạt mưa mùa lũ cuốn trôi đi tất cả, chỉ còn lại tình yêu thương chân thành của gia đình.",
        "chapters": [
            {
                "title": "Chương 1: Con cóc cậu trời và tuổi thơ làng quê",
                "content": "<p>Thằng Tường em tôi có tính thương người kỳ lạ. Nó nhặt con cóc bị thương về nuôi dưới gầm giường và tin rằng cóc là cậu ông trời.</p><p>Làng quê nghèo mùa mưa lũ, nước dâng ngập trắng đồng, hai anh em ngồi trên nóc nhà chia nhau củ khoai nướng nóng hổi.</p>"
            }
        ]
    },
    {
        "title": "Việt Nam Sử Lược",
        "author": "Trần Trọng Kim",
        "category": "Lịch sử & Tiểu sử",
        "image_url": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 280,
        "format": "pdf",
        "summary": "Bộ thông sử đầu tiên viết bằng chữ quốc ngữ, tái hiện hào khí bốn ngàn năm dựng nước và giữ nước của dân tộc.",
        "narration_text": "Sách nói Việt Nam Sử Lược của học giả Trần Trọng Kim. Nước Việt Nam ta ở về phía đông nam cõi Á Châu. Dân tộc ta có truyền thống ngàn năm văn hiến, từ thời các vua Hùng dựng nước Văn Lang cho đến những chiến công hiển hách đánh đuổi quân xâm lược phương Bắc của Hai Bà Trưng, Ngô Quyền, Lý Thường Kiệt và Trần Hưng Đạo.",
        "chapters": [
            {
                "title": "Chương 1: Thời đại Hồng Bàng và nguồn gốc dân tộc",
                "content": "<p>Tổ tiên ta từ thuở khai thiên lập địa đã quần cư bên bờ sông Hồng trù phú. Vua Kinh Dương Vương sinh ra Lạc Long Quân. Lạc Long Quân lấy bà Âu Cơ sinh ra bọc trăm trứng, nở thành trăm người con, là khởi nguồn của nòi giống Rồng Tiên Lạc Hồng.</p>"
            },
            {
                "title": "Chương 2: Chiến thắng Bạch Đằng giang năm 938",
                "content": "<p>Ngô Quyền dùng mưu cắm cọc nhọn bịt sắt dưới lòng sông Bạch Đằng, nhân lúc thủy triều rút đã đánh tan tành đoàn thuyền chiến quân Nam Hán, mở ra kỷ nguyên độc lập tự chủ lâu dài cho dân tộc.</p>"
            }
        ]
    },
    {
        "title": "Dạy Con Làm Giàu (Tập 1)",
        "author": "Robert T. Kiyosaki",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1553729459-efe14ef6055d?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 350,
        "format": "pdf",
        "summary": "Bài học tài chính đột phá để người giàu không làm việc vì tiền mà bắt tiền bạc phải làm việc cho mình.",
        "narration_text": "Sách nói Dạy Con Làm Giàu của tác giả Robert Kiyosaki. Tôi có hai người cha: một người cha giàu và một người cha nghèo. Người cha nghèo có học vị tiến sĩ nhưng luôn gặp rắc rối về tài chính. Người cha giàu chưa học hết lớp tám nhưng lại trở thành một trong những người giàu có nhất bang Hawaii. Sự khác biệt lớn nhất giữa họ không phải là kiếm được bao nhiêu tiền, mà là cách họ suy nghĩ về đồng tiền.",
        "chapters": [
            {
                "title": "Chương 1: Người giàu không làm việc vì tiền",
                "content": "<p>Đa số mọi người bị mắc kẹt trong vòng luẩn quẩn 'Rat Race': đi làm kiếm tiền, trả hóa đơn, rồi lại đi làm vì nỗi sợ thiếu thốn và lòng tham.</p><p>Người giàu hiểu rằng tiền bạc chỉ là công cụ, họ đầu tư vào tài sản sinh lời để đạt được tự do tài chính.</p>"
            }
        ]
    }
]

async def generate_narration_audio(text: str, filename: str) -> str:
    """Tạo file MP3 giọng đọc tiếng Việt mượt mà sử dụng edge-tts"""
    output_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
        return filename
        
    try:
        # Giọng nữ Hoài My hoặc Nam Minh của Azure Neural
        communicate = edge_tts.Communicate(text, voice="vi-VN-HoaiMyNeural", rate="+0%", volume="+0%")
        await communicate.save(output_path)
        print(f"Đã tạo audio nói tiếng Việt: {filename} ({os.path.getsize(output_path)} bytes)")
        return filename
    except Exception as e:
        print(f"Lỗi tạo audio cho {filename}: {e}")
        return "audio_sample_1.mp3"

async def main():
    print("=" * 60)
    print("BẮT ĐẦU TẠO DỮ LIỆU SÁCH VIỆT NAM, EPUB/PDF & SÁCH NÓI THẬT")
    print("=" * 60)
    
    # 1. Tạo 2 audio mẫu thực sự đọc sách cho audio_sample_1 và audio_sample_2
    print("\n1. Cập nhật audio_sample_1.mp3 và audio_sample_2.mp3 thành giọng đọc sách thật...")
    await generate_narration_audio(VIETNAMESE_BOOKS[0]["narration_text"], "audio_sample_1.mp3")
    await generate_narration_audio(VIETNAMESE_BOOKS[1]["narration_text"], "audio_sample_2.mp3")
    
    # 2. Tạo EPUB chuẩn cho Nhà Giả Kim
    print("\n2. Tạo EPUB chuẩn cho Nhà Giả Kim...")
    create_valid_epub(
        os.path.join(UPLOAD_DIR, "nha_gia_kim.epub"),
        "Nhà Giả Kim",
        "Paulo Coelho",
        VIETNAMESE_BOOKS[1]["chapters"]
    )
    
    # 3. Tạo file sách và audio cho tất cả sách Việt Nam
    conn = get_connection()
    cursor = conn.cursor()
    
    for idx, b in enumerate(VIETNAMESE_BOOKS, 1):
        safe_name = f"vn_book_{idx}"
        audio_filename = f"{safe_name}.mp3"
        
        # Tạo giọng đọc sách nói cho từng cuốn
        print(f"\n[Book {idx}/{len(VIETNAMESE_BOOKS)}] Đang tạo dữ liệu: {b['title']}...")
        await generate_narration_audio(b["narration_text"], audio_filename)
        audio_url = f"uploads/{audio_filename}"
        
        # Tạo file PDF hoặc EPUB tương ứng
        if b["format"] == "epub":
            epub_filename = f"{safe_name}.epub"
            epub_path = os.path.join(UPLOAD_DIR, epub_filename)
            create_valid_epub(epub_path, b["title"], b["author"], b["chapters"])
            book_file_url = f"uploads/{epub_filename}"
        else:
            pdf_filename = f"{safe_name}.pdf"
            pdf_path = os.path.join(UPLOAD_DIR, pdf_filename)
            create_valid_pdf(pdf_path, b["title"], b["author"], b["chapters"])
            book_file_url = f"uploads/{pdf_filename}"
            
        # Nội dung văn bản tổng hợp để đọc trực tiếp
        full_content = "\n\n".join([f"=== {c['title']} ===\n" + c['content'] for c in b["chapters"]])
        
        # Cập nhật hoặc chèn vào CSDL
        cursor.execute("SELECT id FROM books WHERE title = %s", (b["title"],))
        existing = cursor.fetchone()
        if existing:
            book_id = existing["id"]
            cursor.execute("""
                UPDATE books 
                SET author = %s, content = %s, audio_url = %s, image_url = %s, pdf_url = %s, 
                    category = %s, rating_avg = %s, review_count = %s, source = N'Kho Sách Việt Nam Tinh Hoa'
                WHERE id = %s
            """, (
                b["author"],
                full_content,
                audio_url,
                b["image_url"],
                book_file_url,
                b["category"],
                b["rating_avg"],
                b["review_count"],
                book_id
            ))
            print(f"-> Đã cập nhật sách ID {book_id}: {b['title']}")
        else:
            cursor.execute("""
                INSERT INTO books (title, author, content, audio_url, image_url, pdf_url, category, rating_avg, review_count, source)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, N'Kho Sách Việt Nam Tinh Hoa')
            """, (
                b["title"],
                b["author"],
                full_content,
                audio_url,
                b["image_url"],
                book_file_url,
                b["category"],
                b["rating_avg"],
                b["review_count"]
            ))
            print(f"-> Đã chèn mới sách: {b['title']}")
            
    conn.commit()
    conn.close()
    print("\n" + "=" * 60)
    print("HOÀN TẤT CẬP NHẬT KHO SÁCH VÀ SÁCH NÓI TIẾNG VIỆT THÀNH CÔNG!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
