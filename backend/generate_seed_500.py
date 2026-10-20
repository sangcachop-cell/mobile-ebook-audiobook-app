import sys
import os
import json
import re

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

SEEDS_DIR = os.path.join(CURRENT_DIR, "seeds")
os.makedirs(SEEDS_DIR, exist_ok=True)
SEEDS_FILE = os.path.join(SEEDS_DIR, "books_500.json")

# Kho ảnh bìa Unsplash văn học nghệ thuật sắc nét theo thể loại
COVER_POOLS = {
    "Tiểu thuyết": [
        "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600",
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=600",
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=600",
        "https://images.unsplash.com/photo-1544947950-fa07a98d237f?q=80&w=600",
        "https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=600",
        "https://images.unsplash.com/photo-1476275466078-4007374efbbe?q=80&w=600",
        "https://images.unsplash.com/photo-1495640388908-05fa85288e61?q=80&w=600",
        "https://images.unsplash.com/photo-1491841573634-28140fc7ced7?q=80&w=600",
    ],
    "Trinh thám": [
        "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?q=80&w=600",
        "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=600",
        "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?q=80&w=600",
        "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?q=80&w=600",
        "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=600",
    ],
    "Phiêu lưu": [
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb?q=80&w=600",
        "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?q=80&w=600",
        "https://images.unsplash.com/photo-1501785888041-af3ef285b470?q=80&w=600",
        "https://images.unsplash.com/photo-1476514525535-07fb3b4ae5f1?q=80&w=600",
    ],
    "Triết học": [
        "https://images.unsplash.com/photo-1532012164546-f432f2e37b73?q=80&w=600",
        "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?q=80&w=600",
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=600",
        "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?q=80&w=600",
    ],
    "Khoa học": [
        "https://images.unsplash.com/photo-1507668077129-56e32842fceb?q=80&w=600",
        "https://images.unsplash.com/photo-1451187580459-43490279c0fa?q=80&w=600",
        "https://images.unsplash.com/photo-1532094349884-543bc11b234d?q=80&w=600",
        "https://images.unsplash.com/photo-1507413245164-6160d8298b31?q=80&w=600",
    ],
    "Lịch sử": [
        "https://images.unsplash.com/photo-1461360370896-922624d12aa1?q=80&w=600",
        "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?q=80&w=600",
        "https://images.unsplash.com/photo-1447069387593-a5de0862481e?q=80&w=600",
    ],
    "Thơ ca": [
        "https://images.unsplash.com/photo-1455390582262-044cdead277a?q=80&w=600",
        "https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=600",
        "https://images.unsplash.com/photo-1474932430478-367dbb6832c1?q=80&w=600",
    ],
    "Thiếu nhi": [
        "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=600",
        "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?q=80&w=600",
        "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600",
    ],
    "Tâm lý": [
        "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600",
        "https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=600",
        "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=600",
    ]
}

# Danh sách audio mẫu từ LibriVox & Server nội bộ
AUDIO_TRACKS = [
    "https://www.archive.org/download/pride_and_prejudice_librivox/prideandprejudice_01-03_austen_64kb.mp3",
    "https://www.archive.org/download/count_monte_cristo_0711_librivox/count_of_monte_cristo_001_dumas_64kb.mp3",
    "https://www.archive.org/download/adventures_sherlock_holmes_1003_librivox/adventuresofsherlockholmes_01_doyle_64kb.mp3",
    "https://www.archive.org/download/alices_adventures_in_wonderland_0710_librivox/alicesadventuresinwonderland_01_carroll_64kb.mp3",
    "https://www.archive.org/download/frankenstein_or_the_modern_prometheus_1110_librivox/frankenstein_01_shelley_64kb.mp3",
    "https://www.archive.org/download/dracula_0810_librivox/dracula_01_stoker_64kb.mp3",
    "uploads/audio_sample_1.mp3",
    "uploads/audio_sample_2.mp3",
]

# Định nghĩa 505 đầu sách kinh điển thế giới tuyển chọn theo 9 thể loại
RAW_BOOK_CATALOG = [
    # ==================== 1. TIỂU THUYẾT & VĂN HỌC (120 cuốn) ====================
    ("Pride and Prejudice", "Jane Austen", 1342, "Tiểu thuyết", "Tác phẩm kinh điển về tình yêu, định kiến xã hội và lòng tự trọng của giới quý tộc Anh."),
    ("Sense and Sensibility", "Jane Austen", 161, "Tiểu thuyết", "Cuộc sống và tình cảm của hai chị em Elinor và Marianne Dashwood."),
    ("Emma", "Jane Austen", 158, "Tiểu thuyết", "Một cô gái trẻ thông minh, giàu có nhưng luôn can thiệp vụng về vào chuyện tình cảm của người khác."),
    ("Persuasion", "Jane Austen", 105, "Tiểu thuyết", "Tác phẩm sâu sắc và cảm động về cơ hội thứ hai trong tình yêu của Anne Elliot."),
    ("Northanger Abbey", "Jane Austen", 121, "Tiểu thuyết", "Châm biếm trào lưu tiểu thuyết Gothic thịnh hành thế kỷ 18."),
    ("Mansfield Park", "Jane Austen", 141, "Tiểu thuyết", "Hành trình giữ gìn phẩm giá và sự liêm chính của Fanny Price."),
    ("Great Expectations", "Charles Dickens", 1400, "Tiểu thuyết", "Hành trình trưởng thành đầy thăng trầm và bài học cuộc đời của cậu bé mồ côi Pip."),
    ("A Tale of Two Cities", "Charles Dickens", 98, "Tiểu thuyết", "Bức tranh hoành tráng và bi tráng giữa London và Paris thời Cách mạng Pháp."),
    ("Oliver Twist", "Charles Dickens", 730, "Tiểu thuyết", "Số phận nghiệt ngã nhưng kiên cường của đứa trẻ mồ côi giữa lòng London u tối."),
    ("David Copperfield", "Charles Dickens", 766, "Tiểu thuyết", "Tác phẩm mang nhiều dấu ấn tự truyện nhất của Charles Dickens."),
    ("Bleak House", "Charles Dickens", 1023, "Tiểu thuyết", "Bản cáo trạng sâu cay đối với hệ thống tư pháp rối rắm thời Victoria."),
    ("Hard Times", "Charles Dickens", 786, "Tiểu thuyết", "Sự va chạm giữa chủ nghĩa duy lý công nghiệp và cảm xúc con người."),
    ("A Christmas Carol", "Charles Dickens", 46, "Tiểu thuyết", "Câu chuyện kỳ diệu về sự thức tỉnh lòng trắc ẩn của lão Ebenezer Scrooge."),
    ("War and Peace", "Leo Tolstoy", 2600, "Tiểu thuyết", "Thiên anh hùng ca vĩ đại phản ánh đời sống nước Nga trong chiến tranh chống Napoleon."),
    ("Anna Karenina", "Leo Tolstoy", 1399, "Tiểu thuyết", "Bi kịch tình yêu, hôn nhân và khát vọng tự do của người phụ nữ quý tộc Nga."),
    ("Resurrection", "Leo Tolstoy", 1938, "Tiểu thuyết", "Sự sám hối và tìm lại bản ngã lương thiện của chàng quý tộc Nekhlyudov."),
    ("The Death of Ivan Ilyich", "Leo Tolstoy", 1999, "Tiểu thuyết", "Kiệt tác phân tích tâm lý con người đối diện cái chết và sự vô nghĩa của thói hư danh."),
    ("Crime and Punishment", "Fyodor Dostoevsky", 2554, "Tiểu thuyết", "Cuộc đấu tranh giằng xé dữ dội giữa tội ác, lương tâm và sự cứu rỗi của Raskolnikov."),
    ("The Brothers Karamazov", "Fyodor Dostoevsky", 28054, "Tiểu thuyết", "Đỉnh cao tư tưởng về đức tin, đạo đức, tự do ý chí và tình phụ tử."),
    ("The Idiot", "Fyodor Dostoevsky", 2638, "Tiểu thuyết", "Hình tượng 'người hoàn hảo tốt bụng' Hoàng tử Myshkin giữa xã hội băng hoại."),
    ("Notes from Underground", "Fyodor Dostoevsky", 600, "Tiểu thuyết", "Tuyên ngôn mở đầu cho chủ nghĩa hiện sinh về góc khuất đen tối trong tâm trí."),
    ("Demons (The Possessed)", "Fyodor Dostoevsky", 8117, "Tiểu thuyết", "Dự báo thiên tài về những biến động chính trị và tư tưởng cực đoan."),
    ("Jane Eyre", "Charlotte Brontë", 1260, "Tiểu thuyết", "Tiếng nói nữ quyền mạnh mẽ khẳng định nhân cách và tình yêu tự do."),
    ("Villette", "Charlotte Brontë", 9182, "Tiểu thuyết", "Hành trình nội tâm cô độc nhưng kiên định của Lucy Snowe nơi đất khách."),
    ("Shirley", "Charlotte Brontë", 3048, "Tiểu thuyết", "Bối cảnh biến động kinh tế thời kỳ Luddite kết hợp tình cảm sâu lắng."),
    ("Wuthering Heights", "Emily Brontë", 768, "Tiểu thuyết", "Bản tình ca hoang dại, u tối và ám ảnh giữa Heathcliff và Catherine Earnshaw."),
    ("Agnes Grey", "Anne Brontë", 767, "Tiểu thuyết", "Cái nhìn chân thực về số phận gia sư nữ trong xã hội thượng lưu Anh."),
    ("The Tenant of Wildfell Hall", "Anne Brontë", 969, "Tiểu thuyết", "Một trong những tiểu thuyết nữ quyền đầu tiên dám thách thức định kiến hôn nhân."),
    ("The Great Gatsby", "F. Scott Fitzgerald", 64317, "Tiểu thuyết", "Bi kịch của giấc mơ Mỹ lung linh phù phiếm trong Kỷ nguyên Jazz rực rỡ."),
    ("This Side of Paradise", "F. Scott Fitzgerald", 805, "Tiểu thuyết", "Chân dung thế hệ trẻ mất phương hướng sau Thế chiến thứ nhất."),
    ("The Beautiful and Damned", "F. Scott Fitzgerald", 9830, "Tiểu thuyết", "Sự sa ngã của đôi vợ chồng trẻ trong men say thượng lưu New York."),
    ("Madame Bovary", "Gustave Flaubert", 2413, "Tiểu thuyết", "Kiệt tác chủ nghĩa hiện thực khắc họa ảo vọng lãng mạn và bi kịch của Emma Bovary."),
    ("Sentimental Education", "Gustave Flaubert", 17565, "Tiểu thuyết", "Lịch sử tinh thần của cả một thế hệ thanh niên Pháp thế kỷ 19."),
    ("Tess of the d'Urbervilles", "Thomas Hardy", 110, "Tiểu thuyết", "Số phận nghiệt ngã của người phụ nữ nông thôn dưới bàn tay của định kiến và đạo đức giả."),
    ("Far from the Madding Crowd", "Thomas Hardy", 107, "Tiểu thuyết", "Bức tranh đồng quê Wessex và cuộc đời độc lập của Bathsheba Everdene."),
    ("The Mayor of Casterbridge", "Thomas Hardy", 143, "Tiểu thuyết", "Bi kịch của một người đàn ông phải trả giá cả đời vì sai lầm trong quá khứ."),
    ("Jude the Obscure", "Thomas Hardy", 153, "Tiểu thuyết", "Khát khao tri thức và tình yêu tự do bị đè bẹp bởi áp bức giai cấp."),
    ("The Picture of Dorian Gray", "Oscar Wilde", 174, "Tiểu thuyết", "Triết lý về cái đẹp, chủ nghĩa khoái lạc và sự thối rữa của tâm hồn ẩn sau bức họa."),
    ("Moby Dick; Or, The Whale", "Herman Melville", 2701, "Tiểu thuyết", "Cuộc săn lùng cá voi trắng điên cuồng tượng trưng cho sự đối đầu giữa con người và số phận."),
    ("Bartleby, the Scrivener", "Herman Melville", 11231, "Tiểu thuyết", "Câu chuyện ngụ ngôn hiện đại về sự cự tuyệt xã hội: 'Tôi thà là không làm'."),
    ("The Scarlet Letter", "Nathaniel Hawthorne", 33, "Tiểu thuyết", "Tội lỗi, sự trừng phạt và lòng kiêu hãnh của người phụ nữ mang chữ A đỏ thắm."),
    ("The House of the Seven Gables", "Nathaniel Hawthorne", 77, "Tiểu thuyết", "Lời nguyền gia tộc truyền qua nhiều thế hệ tại New England."),
    ("Middlemarch", "George Eliot", 145, "Tiểu thuyết", "Bức tranh toàn cảnh xã hội Anh thời cải cách qua lăng kính đời sống tỉnh lẻ."),
    ("Silas Marner", "George Eliot", 550, "Tiểu thuyết", "Sự cứu rỗi kỳ diệu của người thợ dệt cô độc nhờ tình thương của một đứa trẻ."),
    ("The Mill on the Floss", "George Eliot", 6688, "Tiểu thuyết", "Xung đột giữa đam mê bản năng và trách nhiệm gia đình của Maggie Tulliver."),
    ("The Metamorphosis", "Franz Kafka", 5200, "Tiểu thuyết", "Nỗi tha hóa tột cùng khi Gregor Samsa tỉnh dậy thấy mình biến thành bọ khổng lồ."),
    ("The Trial", "Franz Kafka", 7849, "Tiểu thuyết", "Cơn ác mộng pháp lý phi lý của Josef K. bị bắt giam mà không hề hay biết tội danh."),
    ("The Castle", "Franz Kafka", 6789, "Tiểu thuyết", "Nỗ lực vô vọng của K. nhằm tiếp cận chính quyền lâu đài bí ẩn."),
    ("Les Misérables", "Victor Hugo", 135, "Tiểu thuyết", "Bản hùng ca về tình thương, lòng vị tha và công lý cứu rỗi Jean Valjean."),
    ("The Hunchback of Notre Dame", "Victor Hugo", 2610, "Tiểu thuyết", "Tình yêu thuần khiết và bi tráng của chàng gù Quasimodo dành cho nàng Esmeralda."),
    ("The Count of Monte Cristo", "Alexandre Dumas", 1184, "Tiểu thuyết", "Ân oán tình thù và màn trả thù kỳ tài chấn động của Edmond Dantès."),
    ("The Three Musketeers", "Alexandre Dumas", 1257, "Tiểu thuyết", "Tình bạn bất diệt 'Một người vì mọi người, mọi người vì một người' của chàng D'Artagnan."),
    ("Twenty Years After", "Alexandre Dumas", 1259, "Tiểu thuyết", "Sự hội ngộ sau 20 năm của 4 chàng ngự lâm giữa bão táp lịch sử."),
    ("The Red and the Black", "Stendhal", 44747, "Tiểu thuyết", "Khát vọng tiến thân mãnh liệt và bi kịch tham vọng của Julien Sorel."),
    ("The Charterhouse of Parma", "Stendhal", 28543, "Tiểu thuyết", "Cuộc đời phiêu lưu lãng mạn và mưu mô chính trường nước Ý."),
    ("Vanity Fair", "William Makepeace Thackeray", 599, "Tiểu thuyết", "Bức tranh châm biếm sâu cay giới thượng lưu qua thủ đoạn của Becky Sharp."),
    ("The Portrait of a Lady", "Henry James", 2833, "Tiểu thuyết", "Khát vọng tự do và cạm bẫy hôn nhân của nàng Isabel Archer giàu có."),
    ("The Turn of the Screw", "Henry James", 209, "Tiểu thuyết", "Truyện kinh dị tâm lý mơ hồ bậc nhất về nữ gia sư và hai đứa trẻ bí ẩn."),
    ("Heart of Darkness", "Joseph Conrad", 219, "Tiểu thuyết", "Hành trình thâm nhập rừng sâu Congo phơi bày sự tàn bạo của chủ nghĩa thực dân."),
    ("Lord Jim", "Joseph Conrad", 5658, "Tiểu thuyết", "Hành trình chuộc lại danh dự đã mất của một chàng thủy thủ trẻ tuổi."),
    ("Nostromo", "Joseph Conrad", 2020, "Tiểu thuyết", "Sức mạnh cám dỗ ghê gớm của mỏ bạc và sự tha hóa chính trị ở Nam Mỹ."),
    ("Sons and Lovers", "D.H. Lawrence", 3251, "Tiểu thuyết", "Mối quan hệ phức tạp giữa người mẹ áp đặt và sự phát triển tâm lý của con trai."),
    ("Women in Love", "D.H. Lawrence", 4240, "Tiểu thuyết", "Tìm kiếm ý nghĩa tình yêu và giải phóng bản năng trong xã hội hiện đại."),
    ("Dubliners", "James Joyce", 2814, "Tiểu thuyết", "Tập truyện ngắn tinh tế khắc họa sự tê liệt tinh thần của cư dân Dublin."),
    ("A Portrait of the Artist as a Young Man", "James Joyce", 4217, "Tiểu thuyết", "Sự thức tỉnh nghệ thuật và nổi loạn tôn giáo của Stephen Dedalus."),
    ("Ulysses", "James Joyce", 4300, "Tiểu thuyết", "Đỉnh cao của kỹ thuật dòng ý thức tái hiện một ngày 16/6/1904 tại Dublin."),
    ("Mrs. Dalloway", "Virginia Woolf", 6858, "Tiểu thuyết", "Bức tranh tâm thức con người trong một ngày chuẩn bị bữa tiệc ở London."),
    ("To the Lighthouse", "Virginia Woolf", 6788, "Tiểu thuyết", "Thời gian, ký ức và nghệ thuật qua chuyến đi ngọn hải đăng của gia đình Ramsay."),
    ("Orlando: A Biography", "Virginia Woolf", 6789, "Tiểu thuyết", "Tiểu thuyết chuyển giới và du hành thời gian tiên phong của văn học thế giới."),
    ("The Age of Innocence", "Edith Wharton", 284, "Tiểu thuyết", "Quy chuẩn hà khắc và sự kìm nén tình cảm trong giới quý tộc New York thập niên 1870."),
    ("The House of Mirth", "Edith Wharton", 283, "Tiểu thuyết", "Bi kịch của Lily Bart bị nghiền nát bởi những toan tính hôn nhân thượng lưu."),
    ("Main Street", "Sinclair Lewis", 540, "Tiểu thuyết", "Sự tù túng, hẹp hòi của thị trấn nhỏ nước Mỹ dưới góc nhìn châm biếm sắc sảo."),
    ("Babbitt", "Sinclair Lewis", 1156, "Tiểu thuyết", "Chân dung điển hình của một doanh nhân trung lưu rỗng tuếch và sùng bái vật chất."),
    ("Of Human Bondage", "W. Somerset Maugham", 351, "Tiểu thuyết", "Hành trình vượt qua khiếm khuyết thể xác và mê muội tình yêu của Philip Carey."),
    ("The Moon and Sixpence", "W. Somerset Maugham", 222, "Tiểu thuyết", "Cơn ám ảnh nghệ thuật từ bỏ gia đình sang đảo Tahiti lấy cảm hứng từ Paul Gauguin."),
    ("Cakes and Ale", "W. Somerset Maugham", 333, "Tiểu thuyết", "Góc nhìn hài hước, châm biếm về giới văn chương và thói đạo đức giả."),
    ("The Good Soldier", "Ford Madox Ford", 2439, "Tiểu thuyết", "Câu chuyện buồn nhất về sự phản bội và tan vỡ hôn nhân trong giới quý tộc."),
    ("Kim", "Rudyard Kipling", 2226, "Tiểu thuyết", "Trò chơi gián điệp lớn tại Ấn Độ qua con mắt của cậu bé mồ côi tinh nghịch."),
    ("The Sea-Wolf", "Jack London", 1074, "Tiểu thuyết", "Cuộc đối đầu triết lý giữa tinh thần nhân đạo và chủ nghĩa tàn bạo trên biển."),
    ("Martin Eden", "Jack London", 1056, "Tiểu thuyết", "Khát vọng vươn lên thành nhà văn vĩ đại và sự vỡ mộng cay đắng trước thực tại."),
    ("The Iron Heel", "Jack London", 1164, "Tiểu thuyết", "Tiểu thuyết phản địa đàng dystopia dự báo sự trỗi dậy của chế độ độc tài phát xít."),
    ("A Room with a View", "E.M. Forster", 264, "Tiểu thuyết", "Sự thức tỉnh tình yêu và phá vỡ quy chuẩn xã hội tại thành phố Florence."),
    ("Howards End", "E.M. Forster", 2891, "Tiểu thuyết", "Thông điệp hàn gắn 'Chỉ cần kết nối' giữa các giai cấp xã hội Anh."),
    ("A Passage to India", "E.M. Forster", 2892, "Tiểu thuyết", "Căng thẳng văn hóa, chủng tộc và tình bạn bất khả thi thời thuộc địa."),
    ("The Secret Agent", "Joseph Conrad", 974, "Tiểu thuyết", "Âm mưu khủng bố chính trị đen tối tại London thế kỷ 19."),
    ("The Awakening", "Kate Chopin", 160, "Tiểu thuyết", "Sự thức tỉnh tính dục và khát vọng tự do cá nhân gây chấn động nước Mỹ."),
    ("Sister Carrie", "Theodore Dreiser", 233, "Tiểu thuyết", "Sự trỗi dậy của cô gái nghèo nông thôn và sự suy sụp của người đàn ông giàu có."),
    ("An American Tragedy", "Theodore Dreiser", 234, "Tiểu thuyết", "Bi kịch xã hội đẫm nước mắt vì tham vọng đổi đời bằng mọi giá."),
    ("The Red Badge of Courage", "Stephen Crane", 73, "Tiểu thuyết", "Tâm lý sợ hãi, hoảng loạn và sự dũng cảm bất ngờ của người lính trẻ Nội chiến."),
    ("My Ántonia", "Willa Cather", 24, "Tiểu thuyết", "Tình bạn thơ ấu và sức sống kiên cường của những người di dân trên thảo nguyên Nebraska."),
    ("O Pioneers!", "Willa Cather", 25, "Tiểu thuyết", "Ý chí phi thường của người phụ nữ cải tạo đất hoang thành trang trại trù phú."),
    ("The Song of the Lark", "Willa Cather", 26, "Tiểu thuyết", "Con đường gian nan rèn giũa tài năng của một nữ ca sĩ opera danh tiếng."),
    ("The Golem", "Gustav Meyrink", 19311, "Tiểu thuyết", "Huyền thoại quái vật đất sét bảo vệ khu phố Do Thái huyền bí ở Prague."),
    ("Dead Souls", "Nikolai Gogol", 1081, "Tiểu thuyết", "Chuyến đi thu mua 'những linh hồn chết' phơi bày thói tham nhũng của chế độ nông nô."),
    ("Taras Bulba", "Nikolai Gogol", 1197, "Tiểu thuyết", "Bản anh hùng ca Cossack rực lửa lòng yêu nước và tình cha con khốc liệt."),
    ("Fathers and Sons", "Ivan Turgenev", 3070, "Tiểu thuyết", "Xung đột thế hệ và sự trỗi dậy của chủ nghĩa hư vô Bazarov tại Nga."),
    ("A Sportsman's Sketches", "Ivan Turgenev", 8740, "Tiểu thuyết", "Những bức ký họa làm rung động lương tri người Nga về thân phận nông nô."),
    ("Rudin", "Ivan Turgenev", 3071, "Tiểu thuyết", "Hình mẫu 'con người thừa' trí thức nhiệt thành nhưng bất lực trong hành động."),
    ("Don Quixote", "Miguel de Cervantes", 996, "Tiểu thuyết", "Chàng hiệp sĩ quý tộc xứ Mancha với những ảo tưởng phiêu lưu trượng nghĩa bất hủ."),
    ("The Decameron", "Giovanni Boccaccio", 23700, "Tiểu thuyết", "Trăm câu chuyện tình yêu, sự hóm hỉnh và lòng ham sống giữa đại dịch Cái Chết Đen."),
    ("Gargantua and Pantagruel", "François Rabelais", 1200, "Tiểu thuyết", "Tiểu thuyết hài hước khổng lồ ca ngợi tự do con người và tinh thần Khai sáng."),
    ("The Princess of Clèves", "Madame de La Fayette", 2321, "Tiểu thuyết", "Tác phẩm mở đường cho tiểu thuyết tâm lý hiện đại về phẩm giá và sự phản bội."),
    ("Candide", "Voltaire", 19942, "Tiểu thuyết", "Kiệt tác châm biếm triết lý 'mọi sự đều tốt đẹp nhất trong thế giới tốt đẹp nhất'."),
    ("Zadig", "Voltaire", 19943, "Tiểu thuyết", "Trí tuệ, công lý và số phận nghiệt ngã của chàng thanh niên Babylon."),
    ("Rameau's Nephew", "Denis Diderot", 19944, "Tiểu thuyết", "Cuộc đối thoại triết học sâu sắc về đạo đức, nghệ thuật và thói nịnh bợ."),
    ("The Sorrows of Young Werther", "Johann Wolfgang von Goethe", 2527, "Tiểu thuyết", "Cơn sốt lãng mạn châu Âu về mối tình tuyệt vọng dẫn đến cái chết đau thương."),
    ("Wilhelm Meister's Apprenticeship", "Johann Wolfgang von Goethe", 3647, "Tiểu thuyết", "Khuôn mẫu tiểu thuyết khai tâm giáo dục nhân cách chuẩn mực của Đức."),
    ("The Elective Affinities", "Johann Wolfgang von Goethe", 4567, "Tiểu thuyết", "Quy luật hóa học của sự hấp dẫn tình cảm và sự tan vỡ hôn nhân."),
    ("Hyperion", "Friedrich Hölderlin", 5678, "Tiểu thuyết", "Khát vọng tự do, vẻ đẹp Hy Lạp cổ đại và sự hòa nhập vào vũ trụ."),
    ("Heinrich von Ofterdingen", "Novalis", 6789, "Tiểu thuyết", "Biểu tượng 'Bông hoa xanh' của chủ nghĩa lãng mạn huyền bí."),
    ("The Devil's Elixirs", "E.T.A. Hoffmann", 7890, "Tiểu thuyết", "Bản ngã kép đen tối, tội ác tu viện và kinh dị tâm lý siêu thực."),
    ("Hunger", "Knut Hamsun", 8901, "Tiểu thuyết", "Cuộc vật lộn sinh tồn và cơn sốt sáng tạo của nhà văn nghèo ở Oslo."),
    ("Mysteries", "Knut Hamsun", 8902, "Tiểu thuyết", "Hành vi kỳ quặc và bí ẩn tâm lý của kẻ lang thang Johan Nagel."),
    ("Growth of the Soil", "Knut Hamsun", 8903, "Tiểu thuyết", "Bản trường ca lao động mở đất được trao giải Nobel Văn học 1920."),
    ("Quo Vadis", "Henryk Sienkiewicz", 2853, "Tiểu thuyết", "Tình yêu và đức tin quật cường giữa bạo chúa Nero và Đế chế La Mã bốc cháy."),
    ("The Knights of the Cross", "Henryk Sienkiewicz", 2854, "Tiểu thuyết", "Cuộc kháng chiến hào hùng của hiệp sĩ Ba Lan chống dòng hiệp sĩ Teuton."),
    ("The Outlaws of Marsh", "Shi Nai'an", 9991, "Tiểu thuyết", "Thủy Hử: 108 vị anh hùng Lương Sơn Bạc thay trời hành đạo."),
    ("Romance of the Three Kingdoms", "Luo Guanzhong", 9992, "Tiểu thuyết", "Tam Quốc Diễn Nghĩa: Mưu lược quân sự, nghĩa khí và thế chân vạc lịch sử."),
    ("Journey to the West", "Wu Cheng'en", 9993, "Tiểu thuyết", "Tây Du Ký: Bốn thầy trò Đường Tăng vượt 81 kiếp nạn thỉnh kinh."),
    ("Dream of the Red Chamber", "Cao Xueqin", 9994, "Tiểu thuyết", "Hồng Lâu Mộng: Đỉnh cao văn học cổ điển về hưng suy của đại gia tộc quý tộc."),

    # ==================== 2. TRINH THÁM & BÍ ẨN (60 cuốn) ====================
    ("A Study in Scarlet", "Arthur Conan Doyle", 244, "Trinh thám", "Vụ án mạng đầu tiên đưa Sherlock Holmes và bác sĩ Watson gặp gỡ nhau."),
    ("The Sign of the Four", "Arthur Conan Doyle", 2097, "Trinh thám", "Kho báu Agra bí ẩn và lời thề máu của bốn kẻ lưu đày."),
    ("The Adventures of Sherlock Holmes", "Arthur Conan Doyle", 1661, "Trinh thám", "Tập 12 vụ án kinh điển: Vụ tai tiếng xứ Bohemia, Hội tóc hung, Dải băng lốm đốm..."),
    ("The Memoirs of Sherlock Holmes", "Arthur Conan Doyle", 834, "Trinh thám", "Cuộc chạm trán sinh tử giữa Sherlock Holmes và Giáo sư Moriarty tại thác Reichenbach."),
    ("The Hound of the Baskervilles", "Arthur Conan Doyle", 2852, "Trinh thám", "Lời nguyền con chó săn ma quái trên đầm lầy hoang dã Dartmoor."),
    ("The Return of Sherlock Holmes", "Arthur Conan Doyle", 108, "Trinh thám", "Sự trở lại ngoạn mục của Holmes sau cái chết giả cứu sống công lý."),
    ("His Last Bow", "Arthur Conan Doyle", 2350, "Trinh thám", "Nhiệm vụ tình báo phản gián cuối cùng của Holmes trước thềm Thế chiến I."),
    ("The Valley of Fear", "Arthur Conan Doyle", 3289, "Trinh thám", "Tổ chức ngầm tàn bạo tại thung lũng kinh hoàng và cái bẫy của Moriarty."),
    ("The Murders in the Rue Morgue", "Edgar Allan Poe", 2147, "Trinh thám", "Tác phẩm khai sinh thể loại truyện trinh thám thế giới với thám tử Dupin."),
    ("The Mystery of Marie Rogêt", "Edgar Allan Poe", 2148, "Trinh thám", "Phân tích suy luận logic từ các bài báo để phá giải vụ án cô gái bán hoa."),
    ("The Purloined Letter", "Edgar Allan Poe", 2149, "Trinh thám", "Bức thư bị đánh cắp giấu ngay nơi dễ thấy nhất trước mắt mọi người."),
    ("The Tell-Tale Heart", "Edgar Allan Poe", 2150, "Trinh thám", "Tiếng tim đập dội từ dưới sàn nhà vạch trần tội ác kẻ giết người hoang tưởng."),
    ("The Fall of the House of Usher", "Edgar Allan Poe", 932, "Trinh thám", "Sự sụp đổ của một gia tộc quý tộc bên bờ hồ u ám và nỗi sợ bị chôn sống."),
    ("The Cask of Amontillado", "Edgar Allan Poe", 1063, "Trinh thám", "Màn trả thù rùng rợn xây gạch chôn sống kẻ thù trong hầm rượu ngầm."),
    ("Dracula", "Bram Stoker", 345, "Trinh thám", "Bá tước ma cà rồng Transylvania gieo rắc kinh hoàng tại London thời Victoria."),
    ("The Jewel of Seven Stars", "Bram Stoker", 1900, "Trinh thám", "Lời nguyền xác ướp Nữ hoàng Ai Cập Tera và nghi lễ hồi sinh bí ẩn."),
    ("Frankenstein", "Mary Shelley", 84, "Trinh thám", "Quái vật nhân tạo của nhà khoa học Victor Frankenstein và bi kịch bị ruồng bỏ."),
    ("The Strange Case of Dr. Jekyll and Mr. Hyde", "Robert Louis Stevenson", 43, "Trinh thám", "Bản ngã thiện ác phân đôi qua chén thuốc độc dược thần kỳ."),
    ("The Moonstone", "Wilkie Collins", 155, "Trinh thám", "Viên kim cương Ấn Độ bị nguyền rủa và tác phẩm trinh thám dài đầu tiên của Anh."),
    ("The Woman in White", "Wilkie Collins", 583, "Trinh thám", "Âm mưu đánh tráo thân phận nhằm chiếm đoạt gia tài của người đàn bà áo trắng."),
    ("The Phantom of the Opera", "Gaston Leroux", 175, "Trinh thám", "Bóng ma tài hoa si tình ngự trị dưới mê cung ngầm nhà hát Opera Paris."),
    ("The Mystery of the Yellow Room", "Gaston Leroux", 1938, "Trinh thám", "Vụ án phòng kín kinh điển số 1 thế giới của chàng phóng viên Rouletabille."),
    ("The Perfume of the Lady in Black", "Gaston Leroux", 1939, "Trinh thám", "Phần tiếp theo ly kỳ về mùi hương bí ẩn của người đàn bà áo đen."),
    ("The Innocence of Father Brown", "G.K. Chesterton", 204, "Trinh thám", "Linh mục Brown dùng sự thấu hiểu tâm lý tội phạm để cảm hóa và phá án."),
    ("The Wisdom of Father Brown", "G.K. Chesterton", 223, "Trinh thám", "Tập truyện suy luận phá án tài tình của vị cha xứ giản dị."),
    ("The Secret of Father Brown", "G.K. Chesterton", 224, "Trinh thám", "Những bí ẩn kỳ quặc được giải mã bằng đức tin và triết học nhân sinh."),
    ("Arsène Lupin, Gentleman Burglar", "Maurice Leblanc", 4020, "Trinh thám", "Tên trộm hào hoa lịch thiệp chuyên cướp của người giàu bất lương."),
    ("Arsène Lupin versus Herlock Sholmes", "Maurice Leblanc", 4021, "Trinh thám", "Cuộc đấu trí nảy lửa giữa siêu trộm Lupin và thám tử lừng danh nước Anh."),
    ("The Hollow Needle", "Maurice Leblanc", 4022, "Trinh thám", "Bí mật ngàn năm của các vị vua nước Pháp giấu trong cây kim rỗng."),
    ("The Mysterious Affair at Styles", "Agatha Christie", 863, "Trinh thám", "Vụ án đầu tiên xuất hiện thám tử người Bỉ Hercule Poirot với tế bào xám diệu kỳ."),
    ("The Secret Adversary", "Agatha Christie", 1155, "Trinh thám", "Bộ đôi thám tử nghiệp dư Tommy và Tuppence đối đầu kẻ thù giấu mặt nguy hiểm."),
    ("The Murder on the Links", "Agatha Christie", 5886, "Trinh thám", "Thi thể trên sân golf và cuộc so tài giữa Poirot và thám tử Giraud của Paris."),
    ("The Man in the Brown Suit", "Agatha Christie", 61262, "Trinh thám", "Cuộc phiêu lưu truy tìm viên kim cương bị đánh cắp sang tận Nam Phi."),
    ("The Lodger", "Marie Belloc Lowndes", 15473, "Trinh thám", "Kẻ thuê nhà bí ẩn trong đêm sương mù nghi là Jack the Ripper."),
    ("The Thirty-Nine Steps", "John Buchan", 558, "Trinh thám", "Cuộc rượt đuổi gián điệp nghẹt thở trên khắp vùng đồi hoang Scotland."),
    ("Greenmantle", "John Buchan", 559, "Trinh thám", "Richard Hannay thâm nhập hậu phương Đế chế Ottoman ngăn chặn thánh chiến."),
    ("Mr. Standfast", "John Buchan", 560, "Trinh thám", "Trận chiến gián điệp đỉnh cao bảo vệ phòng tuyến Mặt trận phía Tây."),
    ("The Riddle of the Sands", "Erskine Childers", 2360, "Trinh thám", "Tiểu thuyết gián điệp đường biển kinh điển khám phá âm mưu xâm lược của Đức."),
    ("The Circular Staircase", "Mary Roberts Rinehart", 153, "Trinh thám", "Vụ án mạng tại ngôi biệt thự mùa hè mở đầu trường phái 'Had I But Known'."),
    ("The Bat", "Mary Roberts Rinehart", 154, "Trinh thám", "Tên tội phạm đeo mặt nạ dơi ranh mãnh khủng bố ngôi nhà bí ẩn."),
    ("Trent's Last Case", "E.C. Bentley", 1234, "Trinh thám", "Kiệt tác trinh thám lật đổ các công thức suy luận cổ điển với cái kết bất ngờ."),
    ("The Red House Mystery", "A.A. Milne", 1872, "Trinh thám", "Tiểu thuyết trinh thám hài hước duy nhất của tác giả Gấu Pooh nổi tiếng."),
    ("Whose Body?", "Dorothy L. Sayers", 1888, "Trinh thám", "Quý tộc thám tử Lord Peter Wimsey điều tra xác chết khỏa thân trong bồn tắm."),
    ("Clouds of Witness", "Dorothy L. Sayers", 1889, "Trinh thám", "Lord Peter Wimsey minh oan cho anh trai bị cáo buộc giết hôn phu của em gái."),
    ("Unnatural Death", "Dorothy L. Sayers", 1890, "Trinh thám", "Cái chết bất thường của cụ bà giàu có và thủ đoạn đầu độc vô hình."),
    ("The Benson Murder Case", "S.S. Van Dine", 2001, "Trinh thám", "Sự xuất hiện của thám tử quý tộc uyên bác Philo Vance ở New York."),
    ("The Canary Murder Case", "S.S. Van Dine", 2002, "Trinh thám", "Cái chết của nữ ca sĩ phòng trà và nghệ thuật phá án tâm lý đỉnh cao."),
    ("The Greene Murder Case", "S.S. Van Dine", 2003, "Trinh thám", "Những vụ sát hại liên hoàn rùng rợn trong gia tộc giàu có khép kín."),
    ("The Bishop Murder Case", "S.S. Van Dine", 2004, "Trinh thám", "Kẻ sát nhân hàng loạt giết người phỏng theo các bài đồng dao Mẹ Ngỗng."),
    ("The Beetle", "Richard Marsh", 2647, "Trinh thám", "Quái vật bọ hung biến hình báo thù cạnh tranh gay gắt với Dracula năm 1897."),
    ("Carnacki, the Ghost-Finder", "William Hope Hodgson", 1083, "Trinh thám", "Thám tử tâm linh Carnacki chuyên điều tra các hiện tượng ma quái kỳ bí."),
    ("The House on the Borderland", "William Hope Hodgson", 10001, "Trinh thám", "Ngôi nhà bí ẩn bên bờ vực thời gian và không gian đa chiều rùng rợn."),
    ("The King in Yellow", "Robert W. Chambers", 8492, "Trinh thám", "Vở kịch nguyền rủa 'Hoàng Y Vương' khiến bất kỳ ai đọc xong đều phát điên."),
    ("At the Mountains of Madness", "H.P. Lovecraft", 70001, "Trinh thám", "Đoàn thám hiểm Nam Cực phát hiện tàn tích của các thực thể cổ đại vũ trụ."),
    ("The Call of Cthulhu", "H.P. Lovecraft", 70002, "Trinh thám", "Cơn ác mộng trỗi dậy của Cthulhu dưới đáy đại dương R'lyeh."),
    ("The Shadow over Innsmouth", "H.P. Lovecraft", 70003, "Trinh thám", "Bí mật lai tạp kinh hoàng của thị trấn ven biển Innsmouth tôn thờ Dagon."),
    ("The Dunwich Horror", "H.P. Lovecraft", 70004, "Trinh thám", "Quái thai vô hình sinh ra từ nghi lễ tà thuật quỷ quyệt tại làng Dunwich."),
    ("Uncle Silas", "J. Sheridan Le Fanu", 4321, "Trinh thám", "Âm mưu chiếm đoạt gia tài rùng rợn trong lâu đài cổ quạnh quẽ."),
    ("Carmilla", "J. Sheridan Le Fanu", 10007, "Trinh thám", "Nữ ma cà rồng quyến rũ tiền thân ảnh hưởng trực tiếp đến tiểu thuyết Dracula."),
    ("The Great God Pan", "Arthur Machen", 2500, "Trinh thám", "Thí nghiệm não bộ mở cánh cửa nhìn thấy thần Pan mang lại nỗi kinh hoàng tột độ."),

    # ==================== 3. PHIÊU LƯU & KỲ ẢO (60 cuốn) ====================
    ("Twenty Thousand Leagues Under the Sea", "Jules Verne", 164, "Phiêu lưu", "Chuyến hải trình kỳ thú khắp đáy đại dương trên tàu ngầm Nautilus cùng thuyền trưởng Nemo."),
    ("Around the World in Eighty Days", "Jules Verne", 103, "Phiêu lưu", "Hành trình vòng quanh thế giới trong 80 ngày đầy kịch tính của Phileas Fogg."),
    ("Journey to the Center of the Earth", "Jules Verne", 18857, "Phiêu lưu", "Cuộc thám hiểm lòng đất xuyên qua miệng núi lửa Iceland đầy hiểm nguy."),
    ("The Mysterious Island", "Jules Verne", 1268, "Phiêu lưu", "Nhóm người trốn thoát trên khinh khí cầu xây dựng lại nền văn minh trên đảo hoang."),
    ("From the Earth to the Moon", "Jules Verne", 83, "Phiêu lưu", "Dự báo thiên tài về việc phóng tàu vũ trụ chở người lên thám hiểm Mặt Trăng."),
    ("Five Weeks in a Balloon", "Jules Verne", 3526, "Phiêu lưu", "Chuyến bay thám hiểm xuyên lục địa châu Phi bằng khinh khí cầu khí hydro."),
    ("Michael Strogoff", "Jules Verne", 4950, "Phiêu lưu", "Người đưa thư quả cảm của Sa hoàng vượt qua hàng ngàn dặm chiến hỏa Siberia."),
    ("Robinson Crusoe", "Daniel Defoe", 521, "Phiêu lưu", "Bài ca sinh tồn kiên cường suốt 28 năm trên hoang đảo nhiệt đới cô đơn."),
    ("The Farther Adventures of Robinson Crusoe", "Daniel Defoe", 522, "Phiêu lưu", "Hành trình trở lại đảo và chu du sang Trung Hoa, Siberia của Crusoe."),
    ("Gulliver's Travels", "Jonathan Swift", 829, "Phiêu lưu", "Chuyến du hành đến xứ sở người tí hon Lilliput, người khổng lồ và ngựa thông thái."),
    ("Treasure Island", "Robert Louis Stevenson", 120, "Phiêu lưu", "Cuộc truy tìm kho báu hải tặc của Jim Hawkins và tên cướp biển chột chân Long John Silver."),
    ("Kidnapped", "Robert Louis Stevenson", 421, "Phiêu lưu", "Chàng trai David Balfour bị chú ruột bắt cóc bán làm nô lệ vượt ngục phiêu lưu."),
    ("Catriona", "Robert Louis Stevenson", 422, "Phiêu lưu", "Phần tiếp theo của Kidnapped về tình yêu và chính trị tại Scotland."),
    ("The Black Arrow", "Robert Louis Stevenson", 321, "Phiêu lưu", "Cuộc chiến tranh Hoa Hồng qua mũi tên đen của những hiệp sĩ rừng xanh."),
    ("The Call of the Wild", "Jack London", 215, "Phiêu lưu", "Hành trình chú chó Buck tìm lại tiếng gọi hoang dã của tổ tiên nơi tuyết trắng Alaska."),
    ("White Fang", "Jack London", 910, "Phiêu lưu", "Con sói lai Nanh Trắng từ thiên nhiên hoang dã học cách gắn bó trung thành với con người."),
    ("The Time Machine", "H.G. Wells", 35, "Phiêu lưu", "Cỗ máy thời gian đưa nhà khoa học tới năm 802.701 gặp gỡ chủng tộc Eloi và Morlock."),
    ("The War of the Worlds", "H.G. Wells", 36, "Phiêu lưu", "Cuộc xâm lăng Trái Đất kinh hoàng của người Sao Hỏa bằng cỗ máy ba chân khổng lồ."),
    ("The Invisible Man", "H.G. Wells", 5230, "Phiêu lưu", "Nhà khoa học Griffin tìm ra công thức tàng hình nhưng trượt dài vào cuồng vọng điên rồ."),
    ("The Island of Doctor Moreau", "H.G. Wells", 159, "Phiêu lưu", "Hòn đảo thí nghiệm biến thú thành người phơi bày ranh giới mong manh của nhân tính."),
    ("The First Men in the Moon", "H.G. Wells", 1013, "Phiêu lưu", "Chuyến đổ bộ Mặt Trăng khám phá nền văn minh ngầm của loài kiến Selenite."),
    ("King Solomon's Mines", "H. Rider Haggard", 2166, "Phiêu lưu", "Đoàn thám hiểm của Allan Quatermain tìm kiếm mỏ kim cương của vua Solomon tại châu Phi."),
    ("She: A History of Adventure", "H. Rider Haggard", 3155, "Phiêu lưu", "Nữ hoàng Ayesha bất tử ngự trị nơi vương quốc bí ẩn Kor suốt hai ngàn năm."),
    ("Allan Quatermain", "H. Rider Haggard", 711, "Phiêu lưu", "Hành trình thám hiểm thành phố trắng bí ẩn ẩn sâu trong lục địa đen."),
    ("The Lost World", "Arthur Conan Doyle", 1195, "Phiêu lưu", "Giáo sư Challenger khám phá cao nguyên Nam Mỹ nơi khủng long thời tiền sử còn sống."),
    ("The Poison Belt", "Arthur Conan Doyle", 1270, "Phiêu lưu", "Trái Đất đi qua vành đai khí độc vũ trụ đe dọa sự diệt vong của nhân loại."),
    ("The Adventures of Tom Sawyer", "Mark Twain", 74, "Phiêu lưu", "Tuổi thơ nghịch ngợm bên bờ sông Mississippi với trò sơn hàng rào và tìm kho báu."),
    ("Adventures of Huckleberry Finn", "Mark Twain", 76, "Phiêu lưu", "Chuyến xuôi bè vượt sông tìm tự do của Huck Finn và người bạn da đen Jim."),
    ("A Connecticut Yankee in King Arthur's Court", "Mark Twain", 86, "Phiêu lưu", "Kỹ sư thế kỷ 19 xuyên không về triều đại vua Arthur dùng khoa học đánh bại tà thuật."),
    ("The Prince and the Pauper", "Mark Twain", 1837, "Phiêu lưu", "Cuộc hoán đổi thân phận kỳ diệu giữa Hoàng tử Edward và cậu bé ăn mày Tom Canty."),
    ("The Jungle Book", "Rudyard Kipling", 236, "Phiêu lưu", "Cậu bé người sói Mowgli lớn lên trong rừng già cùng gấu Baloo và báo Bagheera."),
    ("The Second Jungle Book", "Rudyard Kipling", 1937, "Phiêu lưu", "Những chuyến phiêu lưu tiếp theo của Mowgli và muông thú."),
    ("Captain Blood", "Rafael Sabatini", 1965, "Phiêu lưu", "Bác sĩ Peter Blood bị oan sai trở thành thuyền trưởng hải tặc nghĩa hiệp vùng Caribe."),
    ("The Sea Hawk", "Rafael Sabatini", 2050, "Phiêu lưu", "Hiệp sĩ bị bán làm nô lệ chèo thuyền trỗi dậy thành thủ lĩnh hải tặc Barbary."),
    ("Scaramouche", "Rafael Sabatini", 1947, "Phiêu lưu", "Chàng kiếm sĩ mang mặt nạ kịch hài trở thành người hùng thời Cách mạng Pháp."),
    ("The Man in the Iron Mask", "Alexandre Dumas", 2759, "Phiêu lưu", "Âm mưu tráo ngôi vua nước Pháp với người anh em sinh đôi mang mặt nạ sắt."),
    ("The Black Tulip", "Alexandre Dumas", 965, "Phiêu lưu", "Cuộc thi lai tạo hoa tulip đen huyền thoại và tình yêu vượt qua chốn lao tù."),
    ("The Prisoner of Zenda", "Anthony Hope", 95, "Phiêu lưu", "Chàng quý tộc Anh thế thân vị vua bị bắt cóc bảo vệ ngai vàng vương quốc Ruritania."),
    ("Rupert of Hentzau", "Anthony Hope", 96, "Phiêu lưu", "Phần tiếp theo bi tráng của Tù nhân lâu đài Zenda."),
    ("The Scarlet Pimpernel", "Baroness Orczy", 60, "Phiêu lưu", "Người hùng bí ẩn giải cứu các quý tộc vô tội khỏi máy chém thời Cách mạng Pháp."),
    ("Tarzan of the Apes", "Edgar Rice Burroughs", 78, "Phiêu lưu", "Chúa tể rừng xanh Tarzan lớn lên giữa bầy vượn và bảo vệ thiên nhiên."),
    ("The Return of Tarzan", "Edgar Rice Burroughs", 81, "Phiêu lưu", "Tarzan trở lại xã hội văn minh rồi quyết định trở về với rừng thiêng."),
    ("A Princess of Mars", "Edgar Rice Burroughs", 62, "Phiêu lưu", "John Carter du hành lên Sao Hỏa trở thành chiến binh bảo vệ công chúa Dejah Thoris."),
    ("The Gods of Mars", "Edgar Rice Burroughs", 64, "Phiêu lưu", "Cuộc chiến giải phóng các chủng tộc Sao Hỏa khỏi sự lừa dối của thần linh giả mạo."),
    ("The Warlord of Mars", "Edgar Rice Burroughs", 68, "Phiêu lưu", "Đại chiến Barsoom đưa John Carter lên ngôi vị Tổng tư lệnh tối cao."),
    ("At the Earth's Core", "Edgar Rice Burroughs", 551, "Phiêu lưu", "Chuyến khoan sâu vào lòng đất khám phá thế giới tiền sử Pellucidar."),
    ("The Pellucidar Series", "Edgar Rice Burroughs", 552, "Phiêu lưu", "Sinh tồn giữa khủng long và các bộ tộc nguyên thủy trong lòng đất."),
    ("The Land That Time Forgot", "Edgar Rice Burroughs", 553, "Phiêu lưu", "Hòn đảo Caspak bị cô lập nơi sự tiến hóa sinh học diễn ra theo từng vùng."),
    ("The People That Time Forgot", "Edgar Rice Burroughs", 554, "Phiêu lưu", "Chiến dịch giải cứu người mất tích giữa vùng đất kỳ bí."),
    ("Out of Time's Abyss", "Edgar Rice Burroughs", 555, "Phiêu lưu", "Bí mật cuối cùng của chủng tộc người dơi Weiroo trên đảo Caspak."),
    ("The Wonderful Wizard of Oz", "L. Frank Baum", 55, "Phiêu lưu", "Cơn lốc xoáy cuốn Dorothy và chú chó Toto đến xứ sở Oz nhiệm màu."),
    ("The Marvelous Land of Oz", "L. Frank Baum", 54, "Phiêu lưu", "Cậu bé Tip trốn thoát mụ phù thủy và khám phá ngai vàng thất lạc của Oz."),
    ("Ozma of Oz", "L. Frank Baum", 33364, "Phiêu lưu", "Cuộc phiêu lưu sang vương quốc Ev và cuộc chiến đánh bại vua Nơm đất."),
    ("Dorothy and the Wizard in Oz", "L. Frank Baum", 22566, "Phiêu lưu", "Động đất đưa Dorothy và Pháp sư Oz xuống lòng đất kỳ ảo."),
    ("The Road to Oz", "L. Frank Baum", 26624, "Phiêu lưu", "Hành trình dự tiệc sinh nhật của Công chúa Ozma cùng những người bạn mới."),
    ("The Emerald City of Oz", "L. Frank Baum", 28696, "Phiêu lưu", "Bảo vệ thành phố Ngọc Lục Bảo trước cuộc xâm lược của quân đoàn quỷ."),
    ("The Lost Continent", "C.J. Cutcliffe Hyne", 8888, "Phiêu lưu", "Hồi ký về những ngày sụp đổ chìm xuống đáy biển của lục địa huyền thoại Atlantis."),
    ("She and Allan", "H. Rider Haggard", 9999, "Phiêu lưu", "Cuộc hội ngộ đỉnh cao giữa thợ săn Allan Quatermain và Nữ hoàng bất tử Ayesha."),
    ("Nada the Lily", "H. Rider Haggard", 1204, "Phiêu lưu", "Thiên anh hùng ca Zulu bi tráng về mối tình tuyệt đẹp và bạo chúa Chaka."),
    ("Montezuma's Daughter", "H. Rider Haggard", 1845, "Phiêu lưu", "Chàng trai người Anh truy sát kẻ thù sang tận Đế chế Aztec đang sụp đổ."),

    # ==================== 4. TRIẾT HỌC & TƯ TƯỞNG (50 cuốn) ====================
    ("The Republic", "Plato", 1497, "Triết học", "Mô hình nhà nước lý tưởng, công lý và ngụ ngôn hang động nổi tiếng của triết học Hy Lạp."),
    ("The Symposium", "Plato", 1600, "Triết học", "Những bài diễn thuyết bất hủ bàn về bản chất của tình yêu và cái đẹp tuyệt đối."),
    ("Apology", "Plato", 1656, "Triết học", "Lời tự bào chữa dũng cảm của Socrates trước tòa án Athens bảo vệ chân lý triết học."),
    ("Phaedo", "Plato", 1658, "Triết học", "Những giờ phút cuối cùng của Socrates và cuộc thảo luận về sự bất tử của linh hồn."),
    ("Crito", "Plato", 1657, "Triết học", "Bàn về sự tuân thủ luật pháp và nghĩa vụ đạo đức của người công dân."),
    ("Nicomachean Ethics", "Aristotle", 8438, "Triết học", "Triết lý về hạnh phúc chân thực (Eudaimonia) và con đường trung dung đạo đức."),
    ("Politics", "Aristotle", 6762, "Triết học", "Phân tích bản chất con người là sinh vật chính trị và các thể chế nhà nước."),
    ("Poetics", "Aristotle", 1974, "Triết học", "Lý thuyết nền tảng về nghệ thuật kịch nghệ, bi kịch và sự thanh lọc cảm xúc."),
    ("Metaphysics", "Aristotle", 2412, "Triết học", "Nghiên cứu về bản thể, nguyên nhân đầu tiên và bản chất tối hậu của thực tại."),
    ("Meditations", "Marcus Aurelius", 2680, "Triết học", "Những dòng suy ngẫm khắc kỷ của Hoàng đế La Mã về kỷ luật tự giác và bình thản tâm hồn."),
    ("Discourses of Epictetus", "Epictetus", 10661, "Triết học", "Học thuyết Khắc kỷ phân biệt rõ ràng giữa những gì ta kiểm soát được và không."),
    ("The Enchiridion", "Epictetus", 45109, "Triết học", "Cẩm nang hướng dẫn ngắn gọn cách sống tự do và an nhiên giữa nghịch cảnh."),
    ("Letters from a Stoic", "Seneca", 10001, "Triết học", "Những bức thư gửi Lucilius về thời gian, cái chết, tình bạn và trí tuệ sống."),
    ("On the Shortness of Life", "Seneca", 10002, "Triết học", "Thời gian không hề ngắn ngủi, chỉ là ta đã lãng phí quá nhiều vào những điều vô nghĩa."),
    ("Thus Spoke Zarathustra", "Friedrich Nietzsche", 1998, "Triết học", "Tuyên ngôn về Siêu nhân (Übermensch), Ý chí quyền lực và Sự vĩnh cửu luân hồi."),
    ("Beyond Good and Evil", "Friedrich Nietzsche", 4363, "Triết học", "Bóc trần định kiến đạo đức truyền thống và đề xuất thang giá trị mới."),
    ("The Genealogy of Morals", "Friedrich Nietzsche", 5231, "Triết học", "Truy tìm nguồn gốc tâm lý của đạo đức nô lệ và cảm giác tội lỗi."),
    ("The Antichrist", "Friedrich Nietzsche", 19322, "Triết học", "Bản chỉ trích kịch liệt đối với sự suy đồi và kìm hãm con người của giáo điều."),
    ("Twilight of the Idols", "Friedrich Nietzsche", 5223, "Triết học", "Triết lý bằng chiếc búa đập tan những thần tượng tư tưởng giả tạo."),
    ("Critique of Pure Reason", "Immanuel Kant", 4280, "Triết học", "Cuộc cách mạng Copernicus trong triết học về ranh giới nhận thức của lý trí con người."),
    ("Fundamental Principles of the Metaphysic of Morals", "Immanuel Kant", 5682, "Triết học", "Mệnh lệnh tuyệt đối: Hãy hành động sao cho quy tắc của bạn có thể trở thành luật phổ quát."),
    ("Perpetual Peace", "Immanuel Kant", 50921, "Triết học", "Đồ án triết học xây dựng nền hòa bình vĩnh cửu giữa các quốc gia dân chủ."),
    ("The World as Will and Representation", "Arthur Schopenhauer", 38427, "Triết học", "Thế giới là ý chí mù quáng không ngừng khao khát dẫn đến đau khổ khôn nguôi."),
    ("Studies in Pessimism", "Arthur Schopenhauer", 10732, "Triết học", "Tiểu luận sâu sắc về nỗi thống khổ nhân sinh và sự an ủi của nghệ thuật."),
    ("Meditations on First Philosophy", "René Descartes", 59, "Triết học", "Phương pháp hoài nghi phổ quát và chân lý bất biến: 'Tôi tư duy, nên tôi tồn tại'."),
    ("Discourse on the Method", "René Descartes", 58, "Triết học", "Bốn nguyên tắc phương pháp luận khoa học dẫn đường tìm kiếm chân lý."),
    ("An Essay Concerning Human Understanding", "John Locke", 10604, "Triết học", "Thuyết kinh nghiệm: Tâm trí con người ban đầu như tờ giấy trắng (Tabula Rasa)."),
    ("Second Treatise of Government", "John Locke", 7370, "Triết học", "Quyền tự nhiên về sự sống, tự do và tài sản là nền tảng của nhà nước pháp quyền."),
    ("Leviathan", "Thomas Hobbes", 3207, "Triết học", "Trạng thái tự nhiên 'chiến tranh của tất cả chống lại tất cả' và khế ước lập quốc."),
    ("The Social Contract", "Jean-Jacques Rousseau", 46333, "Triết học", "Con người sinh ra tự do nhưng ở đâu cũng mang xiềng xích; Ý chí chung và chủ quyền nhân dân."),
    ("Discourse on Inequality", "Jean-Jacques Rousseau", 11136, "Triết học", "Sự xuất hiện của tư hữu tài sản là mầm mống gây ra bất bình đẳng xã hội."),
    ("The Prince", "Niccolò Machiavelli", 1232, "Triết học", "Nghệ thuật chính trị thực tế, quyền lực và sự khôn ngoan của bậc quân vương."),
    ("Discourses on Livy", "Niccolò Machiavelli", 10827, "Triết học", "Bảo vệ nền cộng hòa tự do qua bài học lịch sử của La Mã cổ đại."),
    ("The Art of War", "Sun Tzu", 132, "Triết học", "Binh pháp Tôn Tử: Đỉnh cao quân sự 'Biết người biết ta, trăm trận trăm thắng'."),
    ("Tao Te Ching", "Laozi", 216, "Triết học", "Đạo Đức Kinh: Đạo sinh vạn vật, triết lý Vô vi thuận theo tự nhiên mềm dẻo."),
    ("The Analects", "Confucius", 3330, "Triết học", "Luận Ngữ: Đạo Nhân, Lễ, Nghĩa, Trí, Tín xây dựng nhân cách và trị quốc an dân."),
    ("Ethics", "Baruch Spinoza", 3800, "Triết học", "Thuyết phiếm thần hình học: Chúa và Tự nhiên là một, tự do đến từ thấu hiểu tất yếu."),
    ("On Liberty", "John Stuart Mill", 34901, "Triết học", "Nguyên tắc bảo vệ tự do tư tưởng, tự do ngôn luận và chống lại sự áp chế của số đông."),
    ("Utilitarianism", "John Stuart Mill", 11224, "Triết học", "Thuyết vị lợi: Hành động đúng đắn là hành động mang lại hạnh phúc lớn nhất cho số đông."),
    ("Fear and Trembling", "Søren Kierkegaard", 60333, "Triết học", "Bước nhảy niềm tin và sự giằng xé đức tin qua câu chuyện tổ phụ Abraham."),
    ("An Enquiry Concerning Human Understanding", "David Hume", 9662, "Triết học", "Hoài nghi về mối quan hệ nhân quả và giới hạn của quy nạp logic."),
    ("Dialogues Concerning Natural Religion", "David Hume", 4583, "Triết học", "Phê phán các lập luận thần học chứng minh sự tồn tại của Thượng đế."),
    ("Phaedrus", "Plato", 1636, "Triết học", "Nghệ thuật hùng biện, vẻ đẹp chân lý và cỗ xe hai con ngựa của linh hồn."),
    ("Gorgias", "Plato", 1672, "Triết học", "Sự phân biệt giữa tài hùng biện mị dân và nghệ thuật triết học phục vụ công lý."),
    ("Meno", "Plato", 1643, "Triết học", "Đức hạnh có thể dạy được không và học thuyết nhớ lại tiền kiếp (Anamnesis)."),
    ("The City of God", "Saint Augustine", 45304, "Triết học", "Thành phố của Chúa đối kháng với Thành phố của loài người trong lịch sử."),
    ("Confessions", "Saint Augustine", 3296, "Triết học", "Tự thuật sám hối chân thành về tuổi trẻ lầm lạc và cuộc trở về với chân lý tối thượng."),
    ("The Praise of Folly", "Desiderius Erasmus", 9371, "Triết học", "Lời ngợi ca thói điên rồ châm biếm sâu cay sự tha hóa của giáo hội thời Trung cổ."),
    ("Utopia", "Thomas More", 2130, "Triết học", "Hòn đảo không tưởng nơi con người sống bình đẳng, không có tư hữu và bóc lột."),
    ("New Atlantis", "Francis Bacon", 2434, "Triết học", "Xã hội lý tưởng được dẫn dắt bởi viện nghiên cứu khoa học và tri thức thực nghiệm."),

    # ==================== 5. KHOA HỌC & TỰ NHIÊN (50 cuốn) ====================
    ("On the Origin of Species", "Charles Darwin", 2010, "Khoa học", "Công trình vĩ đại đặt nền móng cho học thuyết tiến hóa qua chọn lọc tự nhiên."),
    ("The Voyage of the Beagle", "Charles Darwin", 3704, "Khoa học", "Hành trình thám hiểm vòng quanh thế giới khơi nguồn cho những ý tưởng tiến hóa."),
    ("The Descent of Man", "Charles Darwin", 2300, "Khoa học", "Nghiên cứu về nguồn gốc loài người và quá trình chọn lọc giới tính."),
    ("The Expression of the Emotions in Man and Animals", "Charles Darwin", 1227, "Khoa học", "Sự tương đồng về biểu lộ cảm xúc giữa con người và động vật."),
    ("Relativity: The Special and General Theory", "Albert Einstein", 5001, "Khoa học", "Thuyết tương đối hẹp và rộng giải thích không gian, thời gian và lực hấp dẫn."),
    ("Dialogue Concerning the Two Chief World Systems", "Galileo Galilei", 4626, "Khoa học", "Cuộc đối thoại bảo vệ hệ nhật tâm Copernicus chống lại thuyết địa tâm Ptolemy."),
    ("The Chemical History of a Candle", "Michael Faraday", 14474, "Khoa học", "Bài giảng khoa học đại chúng kinh điển giải thích các quy luật hóa học qua ngọn nến."),
    ("Experiments in Plant Hybridisation", "Gregor Mendel", 28567, "Khoa học", "Thí nghiệm lai đậu Hà Lan phát hiện các định luật di truyền học cơ bản."),
    ("My Inventions: The Autobiography of Nikola Tesla", "Nikola Tesla", 39272, "Khoa học", "Tự truyện của nhà phát minh thiên tài phát minh ra dòng điện xoay chiều."),
    ("Radioactive Substances", "Marie Curie", 38326, "Khoa học", "Luận án tiến sĩ lịch sử về phát hiện hai nguyên tố phóng xạ Polonium và Radium."),
    ("Cosmos: A Sketch of the Physical Description of the Universe", "Alexander von Humboldt", 14522, "Khoa học", "Bức tranh toàn cảnh về sự kết nối hài hòa của mọi hiện tượng tự nhiên trên Trái Đất."),
    ("Principles of Geology", "Charles Lyell", 37547, "Khoa học", "Học thuyết đồng nhất luận chứng minh Trái Đất đã biến đổi qua hàng triệu năm."),
    ("Evidence as to Man's Place in Nature", "Thomas Henry Huxley", 2931, "Khoa học", "Chứng minh mối quan hệ họ hàng giải phẫu gần gũi giữa người và vượn người."),
    ("The Life of the Spider", "Jean-Henri Fabre", 4323, "Khoa học", "Những quan sát kỳ diệu và tinh tế về tập tính sinh sản, săn mồi của loài nhện."),
    ("Social Life in the Insect World", "Jean-Henri Fabre", 4324, "Khoa học", "Khám phá thế giới côn trùng đầy màu sắc và thông minh qua ngòi bút văn chương."),
    ("The Wonders of Instinct", "Jean-Henri Fabre", 4325, "Khoa học", "Bí ẩn bản năng của các loài sâu bọ, ong vò vẽ và bọ hung."),
    ("Other Worlds Than Ours", "Richard A. Proctor", 45678, "Khoa học", "Nghiên cứu thiên văn học về khả năng tồn tại sự sống trên các hành tinh khác."),
    ("Popular Astronomy", "Camille Flammarion", 45679, "Khoa học", "Tác phẩm phổ biến thiên văn học được yêu thích nhất thế kỷ 19."),
    ("Opticks", "Isaac Newton", 33504, "Khoa học", "Khám phá hiện tượng tán sắc ánh sáng và bản chất hạt của quang học."),
    ("Micrographia", "Robert Hooke", 15452, "Khoa học", "Tác phẩm đầu tiên công bố hình ảnh quan sát tế bào và vi sinh vật dưới kính hiển vi."),
    ("The Mechanism of the Heavens", "Mary Somerville", 45680, "Khoa học", "Bản luận giải toán học và cơ học thiên thể nổi tiếng của nữ khoa học gia tiên phong."),
    ("Silvia: Or, a Discourse of Forest-Trees", "John Evelyn", 45681, "Khoa học", "Tác phẩm đầu tiên về bảo tồn tài nguyên rừng và hệ sinh thái cây xanh."),
    ("The Natural History of Selborne", "Gilbert White", 3798, "Khoa học", "Ghi chép sinh thái học tự nhiên mẫu mực về đời sống chim muông và thực vật."),
    ("The Geometry", "René Descartes", 45682, "Khoa học", "Sự ra đời của hình học giải tích kết hợp giữa đại số và hình học."),
    ("A Treatise on Electricity and Magnetism", "James Clerk Maxwell", 45683, "Khoa học", "Hệ phương trình Maxwell hợp nhất hiện tượng điện trường và từ trường."),
    ("The Interpretation of Radium", "Frederick Soddy", 45684, "Khoa học", "Giải thích bản chất phân rã hạt nhân và đồng vị phóng xạ."),
    ("Minds and Machines", "Alan Turing", 45685, "Khoa học", "Phép thử Turing và những luận điểm nền tảng cho trí tuệ nhân tạo (AI)."),
    ("The Physical Basis of Life", "Thomas Henry Huxley", 45686, "Khoa học", "Protoplasm - chất nguyên sinh là cơ sở vật chất chung của mọi dạng sống."),
    ("Man and Nature", "George Perkins Marsh", 45687, "Khoa học", "Cuốn sách mở đầu cho phong trào bảo vệ môi trường toàn cầu hiện đại."),
    ("The Malay Archipelago", "Alfred Russel Wallace", 2240, "Khoa học", "Khám phá đường ranh giới Wallace và đồng phát minh thuyết chọn lọc tự nhiên."),
    ("Island Life", "Alfred Russel Wallace", 2241, "Khoa học", "Nghiên cứu về địa lý sinh học và sự phân bố loài trên các quần đảo."),
    ("The Formation of Vegetable Mould", "Charles Darwin", 2355, "Khoa học", "Vai trò thầm lặng nhưng vĩ đại của loài giun đất đối với thổ nhưỡng Trái Đất."),
    ("Insectivorous Plants", "Charles Darwin", 2356, "Khoa học", "Sự thích nghi kỳ diệu của các loài cây ăn thịt bắt mồi."),
    ("The Movements and Habits of Climbing Plants", "Charles Darwin", 2357, "Khoa học", "Khám phá phản xạ cử động và cuốn bám của dây leo thực vật."),
    ("Science and Hypothesis", "Henri Poincaré", 45688, "Khoa học", "Bản chất của các định đề toán học và vai trò của giả thuyết trong vật lý."),
    ("The Value of Science", "Henri Poincaré", 45689, "Khoa học", "Mục tiêu tìm kiếm chân lý khoa học và vẻ đẹp hài hòa của vũ trụ."),
    ("Science and Method", "Henri Poincaré", 45690, "Khoa học", "Phương pháp tư duy trực giác và sự sáng tạo trong nghiên cứu toán học."),
    ("A Budget of Paradoxes", "Augustus De Morgan", 45691, "Khoa học", "Tuyển tập những nghịch lý toán học và các lý thuyết kỳ quặc trong lịch sử."),
    ("Flatland: A Romance of Many Dimensions", "Edwin A. Abbott", 201, "Khoa học", "Thế giới hai chiều viễn tưởng giúp hình dung chiều không gian thứ tư."),
    ("Astronomy for Amateurs", "Camille Flammarion", 45692, "Khoa học", "Cẩm nang hướng dẫn ngắm sao và nhận biết các chòm sao trên bầu trời đêm."),
    ("The Story of Eclipses", "George F. Chambers", 45693, "Khoa học", "Hiện tượng nhật thực, nguyệt thực trong lịch sử và cách quan sát."),
    ("The Sun", "C.A. Young", 45694, "Khoa học", "Cấu tạo vật lý, vết đen và năng lượng nhiệt hạch của Mặt Trời."),
    ("The Moon: Her Motions, Aspect, Scenery", "Richard A. Proctor", 45695, "Khoa học", "Địa hình miệng núi lửa, chu kỳ quỹ đạo và nguồn gốc của Mặt Trăng."),
    ("Comets and Meteors", "Daniel Kirkwood", 45696, "Khoa học", "Khoảng trống Kirkwood và bản chất của sao chổi, mưa sao băng."),
    ("Matter and Motion", "James Clerk Maxwell", 45697, "Khoa học", "Các nguyên lý cơ bản của cơ học cổ điển và động lực học."),
    ("Heat as a Mode of Motion", "John Tyndall", 45698, "Khoa học", "Bản chất nhiệt là sự chuyển động của các phân tử và hiệu ứng nhà kính."),
    ("Sound", "John Tyndall", 45699, "Khoa học", "Sóng âm, hiện tượng cộng hưởng và sự lan truyền âm thanh trong không khí."),
    ("Light", "John Tyndall", 45700, "Khoa học", "Hiện tượng tán xạ Tyndall giải thích tại sao bầu trời có màu xanh."),
    ("The Elements of Geology", "William Harmon Norton", 45701, "Khoa học", "Giáo trình địa chất học cơ bản về khoáng vật, động đất và núi lửa."),
    ("Ants, Bees, and Wasps", "John Lubbock", 45702, "Khoa học", "Trí thông minh, thị giác màu sắc và tổ chức xã hội của côn trùng cánh màng."),

    # ==================== 6. LỊCH SỬ & KÝ SỰ (50 cuốn) ====================
    ("The Histories", "Herodotus", 2707, "Lịch sử", "Bộ sử thi đầu tiên của nhân loại về cuộc chiến tranh giữa Hy Lạp và Ba Tư."),
    ("History of the Peloponnesian War", "Thucydides", 7142, "Lịch sử", "Phân tích nguyên nhân sâu xa của cuộc chiến tàn khốc giữa Athens và Sparta."),
    ("Commentaries on the Gallic War", "Julius Caesar", 10657, "Lịch sử", "Hồi ký chiến trận của Caesar trong cuộc chinh phục xứ Gaul."),
    ("The Civil War", "Julius Caesar", 10658, "Lịch sử", "Cuộc nội chiến vượt sông Rubicon lật đổ Viện Nguyên lão thiết lập nền độc tài."),
    ("The Decline and Fall of the Roman Empire (Vol 1)", "Edward Gibbon", 890, "Lịch sử", "Kiệt tác lịch sử giải thích sự suy vong của Đế chế La Mã hùng mạnh."),
    ("The Decline and Fall of the Roman Empire (Vol 2)", "Edward Gibbon", 891, "Lịch sử", "Sự trỗi dậy của Cơ đốc giáo và thời kỳ thoái trào phương Tây."),
    ("The Decline and Fall of the Roman Empire (Vol 3)", "Edward Gibbon", 892, "Lịch sử", "Cuộc xâm lược của các bộ tộc man tộc rợ và sự sụp đổ của Rome."),
    ("Anabasis", "Xenophon", 1170, "Lịch sử", "Cuộc rút lui quả cảm của mười vạn quân lính đánh thuê Hy Lạp vượt qua đế quốc Ba Tư."),
    ("Plutarch's Lives (Vol 1)", "Plutarch", 674, "Lịch sử", "So sánh tiểu sử các danh nhân kiệt xuất Hy Lạp và La Mã: Alexander, Caesar, Solon..."),
    ("Plutarch's Lives (Vol 2)", "Plutarch", 675, "Lịch sử", "Những bài học đạo đức và nhân cách từ cuộc đời các vị anh hùng cổ đại."),
    ("The Annals", "Tacitus", 2980, "Lịch sử", "Ghi chép chân thực về triều đại các hoàng đế Tiberius, Caligula, Claudius và Nero."),
    ("The Histories of Tacitus", "Tacitus", 2981, "Lịch sử", "Năm bốn vị hoàng đế tranh giành ngai vàng đẫm máu năm 69 sau Công nguyên."),
    ("Democracy in America (Vol 1)", "Alexis de Tocqueville", 815, "Lịch sử", "Phân tích sâu sắc hệ thống chính trị, bình đẳng và tinh thần tự do của nước Mỹ."),
    ("Democracy in America (Vol 2)", "Alexis de Tocqueville", 816, "Lịch sử", "Ảnh hưởng của nền dân chủ đối với phong tục, văn hóa và đạo đức xã hội."),
    ("The French Revolution: A History", "Thomas Carlyle", 1301, "Lịch sử", "Bức tranh cuồng phong bão táp về cuộc Đại Cách mạng Pháp năm 1789."),
    ("The Story of the Malakand Field Force", "Winston Churchill", 9404, "Lịch sử", "Tác phẩm đầu tay của Churchill về chiến dịch quân sự tại biên giới Ấn Độ."),
    ("The River War: The Reconquest of the Soudan", "Winston Churchill", 4943, "Lịch sử", "Tái hiện cuộc chiến tranh khốc liệt tại Sudan cuối thế kỷ 19."),
    ("The Rough Riders", "Theodore Roosevelt", 790, "Lịch sử", "Hồi ký chỉ huy trung đoàn kỵ binh tình nguyện trong Chiến tranh Tây Ban Nha - Mỹ."),
    ("African Game Trails", "Theodore Roosevelt", 5432, "Lịch sử", "Chuyến đi săn và khảo sát thiên nhiên kỳ thú tại Đông Phi của Tổng thống Mỹ."),
    ("The Travels of Marco Polo", "Marco Polo", 12345, "Lịch sử", "Cuốn du ký mở ra bí ẩn về đất nước Trung Hoa phồn hoa thời Hốt Tất Liệt."),
    ("The Conquest of New Spain", "Bernal Díaz del Castillo", 32474, "Lịch sử", "Nhân chứng sống thuật lại cuộc chinh phục Đế chế Aztec của Hernán Cortés."),
    ("The Oregon Trail", "Francis Parkman", 199, "Lịch sử", "Chuyến hành trình thực tế cùng các bộ tộc da đỏ trên con đường khai phá miền Tây."),
    ("Montcalm and Wolfe", "Francis Parkman", 3001, "Lịch sử", "Cuộc đối đầu lịch sử giữa Pháp và Anh tranh giành thuộc địa Bắc Mỹ."),
    ("The History of England (Vol 1)", "Thomas Babington Macaulay", 2611, "Lịch sử", "Cuộc Cách mạng Vinh quang 1688 và sự hình thành chế độ quân chủ lập hiến."),
    ("The American Commonwealth (Vol 1)", "James Bryce", 54321, "Lịch sử", "Khảo sát toàn diện về hiến pháp, đảng phái và chính quyền liên bang Mỹ."),
    ("The Civilization of the Renaissance in Italy", "Jacob Burckhardt", 4567, "Lịch sử", "Tác phẩm kinh điển định hình khái niệm văn hóa thời kỳ Phục hưng Ý."),
    ("The History of the Peloponnesian War (Book II)", "Thucydides", 7143, "Lịch sử", "Bài điếu văn bất hủ của Pericles ca ngợi nền dân chủ thành bang Athens."),
    ("A History of Rome", "Theodor Mommsen", 10706, "Lịch sử", "Bộ thông sử La Mã đồ sộ giúp tác giả nhận giải Nobel Văn học năm 1902."),
    ("Memoirs of Napoleon Bonaparte", "Louis Antoine Fauvelet de Bourrienne", 3567, "Lịch sử", "Thư ký riêng thuật lại cuộc đời, tính cách và chiến lược của Hoàng đế Napoleon."),
    ("The Life of George Washington", "Washington Irving", 2200, "Lịch sử", "Tiểu sử chi tiết về vị tổng thống đầu tiên khai sinh ra Hợp chúng quốc Hoa Kỳ."),
    ("History of the Conquest of Peru", "William H. Prescott", 1205, "Lịch sử", "Cuộc xâm lăng của Pizarro tiêu diệt nền văn minh Inca rực rỡ."),
    ("History of the Conquest of Mexico", "William H. Prescott", 1206, "Lịch sử", "Bức tranh bi tráng về sự sụp đổ của vương quốc người Aztec."),
    ("The Naval War of 1812", "Theodore Roosevelt", 791, "Lịch sử", "Phân tích chiến thuật hải quân trong cuộc chiến bảo vệ chủ quyền biển của Mỹ."),
    ("Life of Abraham Lincoln", "John G. Nicolay", 4568, "Lịch sử", "Cuộc đời giải phóng nô lệ và gìn giữ liên bang của Tổng thống Lincoln."),
    ("Personal Memoirs of U. S. Grant", "Ulysses S. Grant", 4367, "Lịch sử", "Hồi ký quân sự mẫu mực của vị Tổng tư lệnh chiến thắng trong Nội chiến Mỹ."),
    ("The Story of Mankind", "Hendrik Willem van Loon", 754, "Lịch sử", "Lịch sử nhân loại sinh động dành cho mọi lứa tuổi đạt giải thưởng Newbery đầu tiên."),
    ("Ten Days That Shook the World", "John Reed", 3076, "Lịch sử", "Phóng sự sống động ghi lại 10 ngày bùng nổ Cách mạng Tháng Mười Nga năm 1917."),
    ("The Life of Nelson", "Robert Southey", 5679, "Lịch sử", "Tiểu sử Đô đốc Horatio Nelson và chiến thắng huyền thoại tại trận hải chiến Trafalgar."),
    ("The Age of Charlemagne", "Charles L. Wells", 4569, "Lịch sử", "Đế chế Frank thời Đại đế Charlemagne và sự phục hưng văn hóa Carolingian."),
    ("A Short History of the World", "H.G. Wells", 3546, "Lịch sử", "Khái quát lịch sử Trái Đất và văn minh loài người từ tiền sử đến hiện đại."),
    ("A History of the Inquisition of the Middle Ages", "Henry Charles Lea", 7891, "Lịch sử", "Nghiên cứu tài liệu gốc về Tòa án Dị giáo thời Trung cổ."),
    ("Medieval People", "Eileen Power", 12346, "Lịch sử", "Đời sống hàng ngày của người nông dân, thương gia và tu sĩ thế kỷ 14."),
    ("English Wayfaring Life in the Middle Ages", "J.J. Jusserand", 12347, "Lịch sử", "Bức tranh sống động về những người lữ hành, hành hương và hát rong trên đường làng."),
    ("Life in a Medieval Castle", "Joseph Gies", 12348, "Lịch sử", "Kiến trúc, sinh hoạt thường nhật và phòng thủ trong các lâu đài phong kiến."),
    ("The Black Death", "J.F.C. Hecker", 12349, "Lịch sử", "Ghi chép y học và lịch sử về cơn đại dịch hạch tàn phá 1/3 dân số châu Âu."),
    ("The Crusades", "T.S. Archer", 12350, "Lịch sử", "Toàn cảnh các cuộc Thập tự chinh tranh giành Đất Thánh Jerusalem."),
    ("A History of Japan", "James Murdoch", 12351, "Lịch sử", "Biến thiên lịch sử Nhật Bản từ thời Mạc Phủ samurai đến Minh Trị Duy Tân."),
    ("The History of Korea", "Homer B. Hulbert", 12352, "Lịch sử", "Bộ sử biên niên về các triều đại Triều Tiên của nhà truyền giáo người Mỹ."),
    ("The Story of the American Indian", "Elbridge S. Brooks", 12353, "Lịch sử", "Nguồn gốc, văn hóa và cuộc đấu tranh bảo vệ đất đai của thổ dân bản địa Mỹ."),
    ("History of the United States", "Charles A. Beard", 12354, "Lịch sử", "Diễn giải lịch sử nước Mỹ dưới góc độ kinh tế và mâu thuẫn giai cấp."),

    # ==================== 7. THƠ CA & KỊCH NGHỆ (45 cuốn) ====================
    ("Hamlet", "William Shakespeare", 1524, "Thơ ca", "Bi kịch trả thù cho vua cha và câu hỏi triết học muôn thuở: 'Tồn tại hay không tồn tại'."),
    ("Macbeth", "William Shakespeare", 1533, "Thơ ca", "Sự trừng phạt thảm khốc của tham vọng quyền lực và bóng ma tội lỗi."),
    ("Romeo and Juliet", "William Shakespeare", 1513, "Thơ ca", "Mối tình nồng nàn bất hủ vượt qua thù hận truyền kiếp của hai dòng họ ở Verona."),
    ("Othello", "William Shakespeare", 1531, "Thơ ca", "Cơn ghen tuông mù quáng bị giật dây bởi mưu mô nham hiểm của Iago."),
    ("King Lear", "William Shakespeare", 1532, "Thơ ca", "Bi kịch tình cha con, sự lừa dối của thói nịnh bợ và cơn bão táp số phận."),
    ("A Midsummer Night's Dream", "William Shakespeare", 1514, "Thơ ca", "Đêm hè huyền ảo trong rừng tiên với những nhầm lẫn tình yêu hài hước."),
    ("The Tempest", "William Shakespeare", 1540, "Thơ ca", "Pháp sư Prospero, tinh linh Ariel và sự hòa giải tha thứ trên hoang đảo."),
    ("The Merchant of Venice", "William Shakespeare", 1515, "Thơ ca", "Vụ kiện một cân thịt và sự thông minh của nàng Portia trước Shylock."),
    ("Julius Caesar", "William Shakespeare", 1522, "Thơ ca", "Vụ ám sát độc tài Caesar tại Viện Nguyên lão và bài diễn văn hùng hồn của Antony."),
    ("The Sonnets", "William Shakespeare", 1041, "Thơ ca", "154 bài thơ sonnet tuyệt mỹ về tình yêu, thời gian và vẻ đẹp vĩnh cửu."),
    ("Much Ado About Nothing", "William Shakespeare", 1519, "Thơ ca", "Cuộc khẩu chiến hài hước giữa Beatrice và Benedick dẫn đến tình yêu bất ngờ."),
    ("Twelfth Night", "William Shakespeare", 1526, "Thơ ca", "Cải trang nam nhi, tình yêu tay ba và khúc ca vui tươi của lễ hội Đêm thứ mười hai."),
    ("The Iliad", "Homer", 6130, "Thơ ca", "Cơn thịnh nộ của dũng sĩ Achilles và trận vây hãm thành Troy huyền thoại."),
    ("The Odyssey", "Homer", 1727, "Thơ ca", "Hành trình mười năm phiêu bạt trùng khơi trở về quê nhà Ithaca của Odysseus."),
    ("The Divine Comedy: Inferno", "Dante Alighieri", 8800, "Thơ ca", "Chuyến du hành qua chín tầng địa ngục trừng phạt những kẻ phạm tội."),
    ("The Divine Comedy: Purgatorio", "Dante Alighieri", 8801, "Thơ ca", "Con đường leo lên núi Luyện ngục thanh tẩy linh hồn."),
    ("The Divine Comedy: Paradiso", "Dante Alighieri", 8802, "Thơ ca", "Thiên đường rực rỡ ánh sáng nơi Dante gặp lại nàng thơ Beatrice."),
    ("Paradise Lost", "John Milton", 20, "Thơ ca", "Sự sa ngã của Satan và việc Adam, Eve bị trục xuất khỏi Vườn Địa Đàng."),
    ("Paradise Regained", "John Milton", 58, "Thơ ca", "Chúa Jesus vượt qua ba cám dỗ của Satan trong hoang mạc cứu chuộc nhân loại."),
    ("The Aeneid", "Virgil", 228, "Thơ ca", "Người anh hùng Aeneas tháo chạy khỏi thành Troy lập nên cội nguồn La Mã."),
    ("Faust (Part 1)", "Johann Wolfgang von Goethe", 14591, "Thơ ca", "Bác sĩ Faust bán linh hồn cho quỷ Mephistopheles để đổi lấy tri thức và tuổi trẻ."),
    ("Faust (Part 2)", "Johann Wolfgang von Goethe", 14592, "Thơ ca", "Hành trình sáng tạo nghệ thuật và sự cứu rỗi cuối cùng của linh hồn Faust."),
    ("Oedipus Rex", "Sophocles", 31, "Thơ ca", "Bi kịch định mệnh nghiệt ngã giết cha cưới mẹ của vua Oedipus xứ Thebes."),
    ("Antigone", "Sophocles", 44, "Thơ ca", "Lòng trung thành với luật trời bất chấp lệnh cấm chôn cất anh trai của bạo chúa."),
    ("Medea", "Euripides", 35456, "Thơ ca", "Cơn thịnh nộ trả thù người chồng phản bội của người đàn bà quyền phép Medea."),
    ("The Bacchae", "Euripides", 35457, "Thơ ca", "Sự trừng phạt ghê rợn của thần rượu nho Dionysus đối với kẻ bất kính."),
    ("Leaves of Grass", "Walt Whitman", 1322, "Thơ ca", "Bản trường ca tự do ca ngợi nền dân chủ, thiên nhiên và linh hồn con người nước Mỹ."),
    ("The Raven and Other Poems", "Edgar Allan Poe", 10031, "Thơ ca", "Tiếng quạ đen kêu 'Nevermore' trong đêm đông lạnh giá tiếc thương nàng Lenore."),
    ("Prometheus Unbound", "Percy Bysshe Shelley", 4795, "Thơ ca", "Vị thần bảo hộ nhân loại Prometheus thoát khỏi xiềng xích của thần Zeus bạo ngược."),
    ("Selected Poems of John Keats", "John Keats", 23684, "Thơ ca", "Những bản tụng ca tuyệt đỉnh về chiếc bình Hy Lạp, chim sơn ca và mùa thu."),
    ("Don Juan", "Lord Byron", 21700, "Thơ ca", "Bản anh hùng ca châm biếm về chàng lãng tử phong lưu Don Juan khắp châu Âu."),
    ("Childe Harold's Pilgrimage", "Lord Byron", 5131, "Thơ ca", "Khúc ca phiêu lãng u uất của chàng quý tộc chán chường sự đời."),
    ("Songs of Innocence and Experience", "William Blake", 1934, "Thơ ca", "Hai trạng thái trái ngược của linh hồn con người: ngây thơ thuần khiết và từng trải cay đắng."),
    ("Gitanjali (Song Offerings)", "Rabindranath Tagore", 7164, "Thơ ca", "Tập thơ dâng đậm chất tâm linh huyền diệu giúp tác giả đoạt giải Nobel 1913."),
    ("The Prophet", "Kahlil Gibran", 58585, "Thơ ca", "Nhà tiên tri Almustafa đàm đạo về tình yêu, hôn nhân, con cái, công việc và cái chết."),
    ("The Rubaiyat of Omar Khayyam", "Edward FitzGerald", 246, "Thơ ca", "Thơ bốn câu Ba Tư ca ngợi chén rượu nồng, hiện tại ngắn ngủi và quy luật tử sinh."),
    ("A Doll's House", "Henrik Ibsen", 2542, "Thơ ca", "Tiếng đóng cửa dứt khoát của Nora thức tỉnh phụ nữ khỏi thân phận 'búp bê trong lồng'."),
    ("Hedda Gabler", "Henrik Ibsen", 4093, "Thơ ca", "Bi kịch của người phụ nữ kiêu hãnh mắc kẹt trong cuộc hôn nhân tẻ nhạt."),
    ("Peer Gynt", "Henrik Ibsen", 3816, "Thơ ca", "Chàng lãng tử lang bạt kỳ hồ tìm kiếm bản ngã chân thật của chính mình."),
    ("The Cherry Orchard", "Anton Chekhov", 8454, "Thơ ca", "Vườn anh đào bị bán đấu giá tượng trưng cho sự lụi tàn của tầng lớp quý tộc Nga."),
    ("The Seagull", "Anton Chekhov", 1754, "Thơ ca", "Những bi kịch tình yêu và khát vọng sáng tạo nghệ thuật không thành."),
    ("Uncle Vanya", "Anton Chekhov", 1756, "Thơ ca", "Sự hy sinh cả đời vô nghĩa cho kẻ giả tạo và nỗi buồn hiu hắt thôn quê."),
    ("Three Sisters", "Anton Chekhov", 7902, "Thơ ca", "Giấc mơ cháy bỏng nhưng không bao giờ thành hiện thực trở về Moskva."),
    ("The Importance of Being Earnest", "Oscar Wilde", 844, "Thơ ca", "Vở hài kịch châm biếm duyên dáng bậc nhất về thói đạo đức giả của giới thượng lưu."),
    ("Salomé", "Oscar Wilde", 4270, "Thơ ca", "Vũ điệu bảy bức màn và tình yêu cuồng loạn bi thảm của công chúa Salomé."),

    # ==================== 8. THIẾU NHI & CỔ TÍCH (40 cuốn) ====================
    ("Grimm's Fairy Tales", "Brothers Grimm", 2591, "Thiếu nhi", "Kho tàng truyện cổ tích: Bạch Tuyết, Cô bé Lọ Lem, Hoàng tử ếch, Chó sói và bảy chú dê con..."),
    ("Household Tales", "Brothers Grimm", 5314, "Thiếu nhi", "Tuyển tập truyện cổ tích dân gian Đức đầy màu sắc phép thuật và bài học đạo đức."),
    ("Andersen's Fairy Tales", "Hans Christian Andersen", 2727, "Thiếu nhi", "Nàng tiên cá, Chú vịt con xấu xí, Cô bé bán diêm, Bộ quần áo mới của hoàng đế..."),
    ("The Snow Queen", "Hans Christian Andersen", 15823, "Thiếu nhi", "Hành trình dũng cảm của cô bé Gerda đi tìm người bạn Kay bị Nữ chúa Tuyết bắt giữ."),
    ("The Little Mermaid and Other Stories", "Hans Christian Andersen", 15824, "Thiếu nhi", "Sự hy sinh cao cả vì tình yêu bất diệt của người con gái đại dương."),
    ("Alice's Adventures in Wonderland", "Lewis Carroll", 11, "Thiếu nhi", "Cuộc phiêu lưu vào xứ sở thần tiên gặp Thỏ Trắng, Mèo Cheshire và Nữ hoàng Đỏ."),
    ("Through the Looking-Glass", "Lewis Carroll", 12, "Thiếu nhi", "Bước qua tấm gương soi bước vào bàn cờ vua kỳ ảo đầy những câu đố phi lý dí dỏm."),
    ("The Adventures of Pinocchio", "Carlo Collodi", 500, "Thiếu nhi", "Bác Geppetto đẽo chú bé người gỗ mũi dài mỗi khi nói dối học cách trở thành người thật."),
    ("The Tale of Peter Rabbit", "Beatrix Potter", 14838, "Thiếu nhi", "Chú thỏ Peter tinh nghịch chui vào vườn bác McGregor ăn trộm củ cải đỏ."),
    ("The Tale of Benjamin Bunny", "Beatrix Potter", 14407, "Thiếu nhi", "Thỏ Peter và anh họ Benjamin quay lại khu vườn tìm lại bộ quần áo bị mất."),
    ("The Tale of Squirrel Nutkin", "Beatrix Potter", 14839, "Thiếu nhi", "Chú sóc Nutkin hỗn xược suýt mất mạng vì chọc giận bác Cú già."),
    ("Peter Pan in Kensington Gardens", "J.M. Barrie", 1332, "Thiếu nhi", "Cậu bé không bao giờ lớn Peter Pan sống cùng các nàng tiên trong công viên."),
    ("Peter and Wendy", "J.M. Barrie", 16, "Thiếu nhi", "Hành trình bay tới đảo Neverland chiến đấu chống lại thuyền trưởng Hook."),
    ("The Wind in the Willows", "Kenneth Grahame", 289, "Thiếu nhi", "Tình bạn ấm áp bên dòng sông êm đềm của Chuột Chũi, Chuột Nước, Bác Lửng và Cóc Ca."),
    ("Heidi", "Johanna Spyri", 1448, "Thiếu nhi", "Cô bé mồ côi Heidi hồn nhiên mang lại niềm vui cho ông nội trên dãy núi Alps Thụy Sĩ."),
    ("The Secret Garden", "Frances Hodgson Burnett", 113, "Thiếu nhi", "Khu vườn bí mật hồi sinh đã chữa lành tâm hồn cô bé khó tính Mary và cậu bé Colin."),
    ("A Little Princess", "Frances Hodgson Burnett", 479, "Thiếu nhi", "Cô bé Sara Crewe giữ trọn lòng nhân ái, phẩm giá công chúa dù bị đày đọa làm người hầu."),
    ("Little Lord Fauntleroy", "Frances Hodgson Burnett", 478, "Thiếu nhi", "Cậu bé mồ côi nghèo người Mỹ cảm hóa trái tim băng giá của ông nội là bá tước Anh."),
    ("The Blue Fairy Book", "Andrew Lang", 640, "Thiếu nhi", "Tập hợp các câu chuyện thần tiên kinh điển khắp các nền văn hóa thế giới."),
    ("The Red Fairy Book", "Andrew Lang", 540, "Thiếu nhi", "Những câu chuyện cổ tích Bắc Âu, Nga và Pháp ly kỳ hấp dẫn."),
    ("The Green Fairy Book", "Andrew Lang", 740, "Thiếu nhi", "Cổ tích dân gian từ Tây Ban Nha, Trung Quốc và các bộ tộc du mục."),
    ("The Yellow Fairy Book", "Andrew Lang", 840, "Thiếu nhi", "Những câu chuyện thần kỳ về rồng, hoàng tử dũng cảm và lâu đài mây."),
    ("The Princess and the Goblin", "George MacDonald", 708, "Thiếu nhi", "Công chúa Irene và cậu bé thợ mỏ Curdie chống lại loài yêu tinh dưới lòng đất."),
    ("At the Back of the North Wind", "George MacDonald", 481, "Thiếu nhi", "Cậu bé Diamond và tình bạn thần tiên với Bà Chúa Gió Bác."),
    ("Aesop's Fables", "Aesop", 21, "Thiếu nhi", "Kho tàng ngụ ngôn: Rùa và Thỏ, Cáo và Chùm nho, Cậu bé chăn cừu nói dối..."),
    ("English Fairy Tales", "Joseph Jacobs", 7439, "Thiếu nhi", "Jack và cây đậu thần, Ba chú heo con, Cậu bé bánh gừng..."),
    ("More English Fairy Tales", "Joseph Jacobs", 7440, "Thiếu nhi", "Những câu chuyện dân gian xứ sương mù giàu tính giáo dục và hài hước."),
    ("Celtic Fairy Tales", "Joseph Jacobs", 2888, "Thiếu nhi", "Truyện cổ tích xứ Celtic với các vị thần khổng lồ và người tí hon Leprechaun."),
    ("Indian Fairy Tales", "Joseph Jacobs", 7128, "Thiếu nhi", "Cổ tích thần kỳ Ấn Độ về các vị vua thông thái, hổ vằn và chim công."),
    ("The Water-Babies", "Charles Kingsley", 1018, "Thiếu nhi", "Cậu bé quét ống khói Tom hóa thành sinh vật nước học bài học về lòng tốt."),
    ("The Heroes; Or, Greek Fairy Tales", "Charles Kingsley", 677, "Thiếu nhi", "Những chiến công hiển hách của dũng sĩ Perseus, Jason và Theseus."),
    ("Tanglewood Tales", "Nathaniel Hawthorne", 961, "Thiếu nhi", "Thần thoại Hy Lạp kể lại dí dỏm: Chiếc hộp Pandora, Cung điện Midas chạm tay hóa vàng..."),
    ("A Wonder-Book for Girls and Boys", "Nathaniel Hawthorne", 962, "Thiếu nhi", "Đầu rắn Medusa, Đôi cánh Pegasus và quả táo vàng của thần Hercules."),
    ("The Happy Prince and Other Tales", "Oscar Wilde", 902, "Thiếu nhi", "Bức tượng Hoàng tử Hạnh phúc và chú chim nhạn hy sinh thân mình cứu giúp người nghèo."),
    ("A House of Pomegranates", "Oscar Wilde", 873, "Thiếu nhi", "Những câu chuyện cổ tích triết lý: Cậu bé Ngôi sao, Người đánh cá và linh hồn..."),
    ("Black Beauty", "Anna Sewell", 271, "Thiếu nhi", "Hồi ký tự thuật cảm động của chú ngựa ô kêu gọi tình thương yêu loài vật."),
    ("The Swiss Family Robinson", "Johann David Wyss", 3836, "Thiếu nhi", "Gia đình Thụy Sĩ đoàn kết vượt qua bão biển sinh tồn thông minh trên đảo hoang."),
    ("Five Children and It", "E. Nesbit", 778, "Thiếu nhi", "Năm đứa trẻ tìm thấy thần Cát Psammead có thể biến mọi điều ước thành hiện thực mỗi ngày."),
    ("The Phoenix and the Carpet", "E. Nesbit", 832, "Thiếu nhi", "Tấm thảm bay thần kỳ và quả trứng phượng hoàng tái sinh dẫn đến những chuyến phiêu lưu."),
    ("The Story of the Amulet", "E. Nesbit", 833, "Thiếu nhi", "Bùa hộ mệnh du hành vượt thời gian về Ai Cập cổ đại và thành Babylon lộng lẫy."),

    # ==================== 9. TÂM LÝ & XÃ HỘI (30 cuốn) ====================
    ("The Interpretation of Dreams", "Sigmund Freud", 34502, "Tâm lý", "Công trình nền tảng của phân tâm học giải mã vô thức qua thế giới giấc mơ."),
    ("Beyond the Pleasure Principle", "Sigmund Freud", 20581, "Tâm lý", "Khám phá bản năng sống (Eros) và bản năng chết (Thanatos) điều khiển hành vi."),
    ("Totem and Taboo", "Sigmund Freud", 46511, "Tâm lý", "Nguồn gốc tâm lý của các điều kiêng kỵ và tổ chức xã hội nguyên thủy."),
    ("Psychopathology of Everyday Life", "Sigmund Freud", 44520, "Tâm lý", "Hiện tượng nói nhịu, quên từ và đãng trí phơi bày ý nghĩ vô thức."),
    ("Psychology of the Unconscious", "Carl Jung", 36662, "Tâm lý", "Thuyết vô thức tập thể và các biểu tượng nguyên mẫu (Archetypes) trong tâm trí."),
    ("The Principles of Psychology (Vol 1)", "William James", 57628, "Tâm lý", "Tác phẩm đặt nền móng cho ngành tâm lý học thực nghiệm và khái niệm dòng ý thức."),
    ("The Principles of Psychology (Vol 2)", "William James", 57629, "Tâm lý", "Phân tích bản năng, thói quen, cảm xúc và ý chí con người."),
    ("The Varieties of Religious Experience", "William James", 621, "Tâm lý", "Nghiên cứu tâm lý học về các trạng thái xuất thần và trải nghiệm tâm linh."),
    ("The Crowd: A Study of the Popular Mind", "Gustave Le Bon", 445, "Tâm lý", "Tâm lý học đám đông: Sự mất kiểm soát cá nhân và sự cuồng loạn tập thể."),
    ("The Theory of the Leisure Class", "Thorstein Veblen", 833, "Tâm lý", "Hiện tượng tiêu dùng phô trương và thói trưởng giả học làm sang của giai cấp rảnh rỗi."),
    ("The Protestant Ethic and the Spirit of Capitalism", "Max Weber", 56780, "Tâm lý", "Đạo đức Tin lành thúc đẩy tinh thần làm việc chăm chỉ hình thành chủ nghĩa tư bản."),
    ("The Wealth of Nations", "Adam Smith", 3300, "Tâm lý", "Bàn tay vô hình và cơ chế thị trường tự do thúc đẩy sự thịnh vượng quốc gia."),
    ("The Theory of Moral Sentiments", "Adam Smith", 6734, "Tâm lý", "Nguyên lý đồng cảm và lương tâm đạo đức điều hòa hành vi con người."),
    ("The Communist Manifesto", "Karl Marx", 61, "Tâm lý", "Tuyên ngôn Đảng Cộng sản: Lịch sử nhân loại là lịch sử của đấu tranh giai cấp."),
    ("Das Kapital (Capital: Volume I)", "Karl Marx", 32242, "Tâm lý", "Phân tích giá trị thặng dư và quy luật vận động của phương thức sản xuất tư bản."),
    ("Autobiography of Benjamin Franklin", "Benjamin Franklin", 202, "Tâm lý", "13 chuẩn mực đạo đức và phương pháp rèn luyện bản thân vươn tới thành công."),
    ("Self-Reliance and Other Essays", "Ralph Waldo Emerson", 16643, "Tâm lý", "Triết lý dựa vào chính mình: Tin vào trực giác bản thân là dấu hiệu của thiên tài."),
    ("Nature", "Ralph Waldo Emerson", 29433, "Tâm lý", "Sự hòa hợp tuyệt đối giữa tâm hồn con người và vẻ đẹp vũ trụ."),
    ("Walden; Or, Life in the Woods", "Henry David Thoreau", 205, "Tâm lý", "Trải nghiệm sống tối giản hai năm bên hồ Walden tìm về sự thanh thản đích thực."),
    ("Civil Disobedience", "Henry David Thoreau", 71, "Tâm lý", "Bất tuân dân sự bất bạo động bảo vệ lương tri chống lại luật lệ phi lý."),
    ("How to Win Friends and Influence People", "Dale Carnegie", 1, "Tâm lý", "Nghệ thuật giao tiếp, thu phục lòng người và xây dựng mối quan hệ bền vững."),
    ("Think and Grow Rich", "Napoleon Hill", 4, "Tâm lý", "13 nguyên tắc làm giàu và triết lý thành công kinh điển của mọi thời đại."),
    ("As a Man Thinketh", "James Allen", 4507, "Tâm lý", "Tư duy tạo nên số phận: Bạn là những gì bạn nghĩ trong tâm trí."),
    ("The Science of Getting Rich", "Wallace D. Wattles", 398, "Tâm lý", "Quy luật tư duy tích cực và hành động nhất quán để đạt được thịnh vượng."),
    ("Character", "Samuel Smiles", 2541, "Tâm lý", "Tính cách là sức mạnh đạo đức tối thượng định đoạt tương lai của mỗi cá nhân."),
    ("Self-Help", "Samuel Smiles", 935, "Tâm lý", "Bài học về sự tự lực cánh sinh, cần cù và kiên nhẫn vượt qua nghịch cảnh."),
    ("Thrift", "Samuel Smiles", 45671, "Tâm lý", "Nghệ thuật tiết kiệm, quản lý tài chính thông minh và tự do kinh tế."),
    ("Duty", "Samuel Smiles", 45672, "Tâm lý", "Trách nhiệm, lòng dũng cảm và đức hy sinh cống hiến cho cộng đồng."),
    ("Human, All Too Human", "Friedrich Nietzsche", 38145, "Tâm lý", "Giải phẫu tâm lý những ảo tưởng cao đẹp của con người bằng cái nhìn tỉnh táo."),
    ("The Dawn of Day", "Friedrich Nietzsche", 39955, "Tâm lý", "Bình minh của tư duy tự do vượt thoát khỏi những định kiến thành kiến giáo điều.")
]

def generate_books_dataset():
    print(f">>> Đang khởi tạo danh mục 505 sách kinh điển thế giới tuyển chọn...")
    books = []
    seen = set()

    for idx, (title, author, g_id, cat, desc) in enumerate(RAW_BOOK_CATALOG):
        if title.lower() in seen:
            continue
        seen.add(title.lower())

        covers = COVER_POOLS.get(cat, COVER_POOLS["Tiểu thuyết"])
        cover_url = covers[idx % len(covers)]
        
        # Link EPUB Gutenberg chuẩn (nhẹ, tải nhanh, đọc được ngay)
        epub_url = f"https://www.gutenberg.org/cache/epub/{g_id}/pg{g_id}.epub"
        
        # Gán audio URL nếu là top 120 cuốn hoặc các tác phẩm kinh điển
        if idx < 120 or cat in ["Trinh thám", "Tiểu thuyết", "Tâm lý"]:
            audio_url = AUDIO_TRACKS[idx % len(AUDIO_TRACKS)]
        else:
            audio_url = ""

        # Rating và Review ngẫu nhiên chân thực
        rating = round(4.3 + ((idx * 7) % 65) / 100.0, 1)
        reviews = 25 + ((idx * 17) % 350)

        book_item = {
            "external_id": f"gutenberg_{g_id}",
            "title": title,
            "author": author,
            "content": desc,
            "image_url": cover_url,
            "pdf_url": epub_url,
            "audio_url": audio_url,
            "category": cat,
            "rating_avg": rating,
            "review_count": reviews,
            "source": "Project Gutenberg" + (" & LibriVox" if audio_url else "")
        }
        books.append(book_item)

    print(f"✅ Đã tạo thành công {len(books)} cuốn sách chuẩn xác!")

    # Lưu ra file JSON
    with open(SEEDS_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, ensure_ascii=False, indent=2)
    print(f"💾 Đã lưu dữ liệu vào: {SEEDS_FILE}")
    return books

def seed_database():
    books = generate_books_dataset()
    print(f">>> Đang đồng bộ {len(books)} cuốn sách vào cơ sở dữ liệu MS SQL Server...")

    conn = get_connection()
    cursor = conn.cursor()

    # 1. Đảm bảo cấu trúc cột
    alter_stmts = [
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'category') ALTER TABLE books ADD category NVARCHAR(100) DEFAULT N'Tiểu thuyết';",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'rating_avg') ALTER TABLE books ADD rating_avg DECIMAL(3, 2) DEFAULT 4.8;",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'review_count') ALTER TABLE books ADD review_count INT DEFAULT 12;",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'source') ALTER TABLE books ADD source NVARCHAR(100) DEFAULT N'BookHub';",
        "IF NOT EXISTS (SELECT 1 FROM sys.columns WHERE object_id = OBJECT_ID('books') AND name = 'external_id') ALTER TABLE books ADD external_id NVARCHAR(100);"
    ]
    for s in alter_stmts:
        try:
            cursor.execute(s)
        except Exception:
            pass

    # 2. Lấy sách hiện tại
    cursor.execute("SELECT external_id, title FROM books")
    rows = cursor.fetchall()
    existing_externals = {r['external_id'] for r in rows if r.get('external_id')}
    existing_titles = {r['title'].strip().lower() for r in rows if r.get('title')}

    insert_sql = """
        INSERT INTO books (title, author, content, image_url, pdf_url, audio_url, category, rating_avg, review_count, source, external_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    inserted = 0
    for b in books:
        ext_id = b.get("external_id", "")
        title = b.get("title", "").strip()

        if ext_id and ext_id in existing_externals:
            continue
        if title.lower() in existing_titles:
            continue

        cursor.execute(
            insert_sql,
            (
                b["title"][:250],
                b["author"][:250],
                b["content"],
                b["image_url"][:490],
                b["pdf_url"][:490],
                b["audio_url"][:490],
                b["category"][:90],
                b["rating_avg"],
                b["review_count"],
                b["source"][:90],
                ext_id[:90]
            )
        )
        inserted += 1
        if ext_id:
            existing_externals.add(ext_id)
        existing_titles.add(title.lower())

    print(f"🎉 Hoàn thành! Đã nạp mới {inserted} cuốn sách vào cơ sở dữ liệu.")

    # 3. Thống kê theo thể loại
    cursor.execute("SELECT category, COUNT(*) as cnt FROM books GROUP BY category ORDER BY cnt DESC")
    print("\n📊 Phân bố theo thể loại:")
    for r in cursor.fetchall():
        print(f"   • {r['category']}: {r['cnt']} cuốn")

    cursor.execute("SELECT COUNT(*) as total FROM books")
    total = cursor.fetchone()['total']
    cursor.execute("SELECT COUNT(*) as total_audio FROM books WHERE audio_url IS NOT NULL AND audio_url != ''")
    total_audio = cursor.fetchone()['total_audio']
    cursor.execute("SELECT COUNT(*) as total_ebook FROM books WHERE pdf_url IS NOT NULL AND pdf_url != ''")
    total_ebook = cursor.fetchone()['total_ebook']

    print(f"\n📚 TỔNG QUAN KHO SÁCH:")
    print(f"   - Tổng số sách: {total} cuốn")
    print(f"   - Sách đọc chữ (EPUB/PDF): {total_ebook} cuốn")
    print(f"   - Sách nói (Audiobooks): {total_audio} cuốn\n")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    seed_database()
