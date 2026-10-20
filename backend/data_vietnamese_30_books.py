# -*- coding: utf-8 -*-
"""
Dữ liệu 30 cuốn sách Việt Nam & Tác phẩm tinh hoa kinh điển
Được biên soạn đầy đủ nội dung, nhiều chương, văn bản phong phú và chuẩn hóa.
"""

BOOKS_DATA = [
    # ---------------- 1. VĂN HỌC VIỆT NAM KINH ĐIỂN ----------------
    {
        "slug": "so_do",
        "title": "Số Đỏ",
        "author": "Vũ Trọng Phụng",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1476275466078-4007374efbbe?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 520,
        "format": "epub",
        "summary": "Kiệt tác văn học trào phúng đỉnh cao của Vũ Trọng Phụng, phơi bày tấn bi hài kịch của xã hội tư sản thành thị buổi giao thời Âu hóa rởm đời.",
        "narration_text": "Chào mừng bạn đến với sách nói Số Đỏ của nhà văn Vũ Trọng Phụng. Chương một: Cuộc gặp gỡ định mệnh của Xuân Tóc Đỏ. Một buổi sáng đẹp trời tại sân quần vợt Hội Khai Trí Tiến Đức, Xuân - một gã nhặt banh hạ lưu đầu đường xó chợ - vô tình lọt vào mắt xanh của bà Phó Đoan, một góa phụ giàu có và chuộng tân thời. Nhờ miệng lưỡi lém lỉnh, thói láu cá và thời thế đảo điên, Xuân bước chân vào thế giới thượng lưu, mở đầu cho chuỗi ngày thăng tiến kỳ dị chưa từng có trong lịch sử.",
        "chapters": [
            {
                "title": "Chương 1: Cuộc gặp gỡ định mệnh của Xuân Tóc Đỏ",
                "content": """Xuân Tóc Đỏ vốn là một đứa trẻ mồ côi, kiếm sống bằng đủ thứ nghề hạ lưu: từ chân chạy cờ, nhặt banh ở sân quần vợt, đến người thổi loa quảng cáo cho tiệm thuốc lậu. Hắn không biết chữ, không gia đình, nhưng lại có sẵn bản tính láu cá và khuôn mặt vênh váo bẩm sinh.

Một buổi trưa hè tại sân quần vợt của Hội Khai Trí Tiến Đức, Xuân Tóc Đỏ vô tình trèo lên cây me nhìn trộm cô đầm tắm. Vụ việc bị phát giác, hắn bị đuổi việc ngay tại trận. Nhưng trớ trêu thay, bà Phó Đoan - một phụ nữ góa chồng giàu có, nổi danh đoan chính và sùng bái phong trào Âu hóa - lại tình cờ chứng kiến sự việc và cảm thấy gã thanh niên này có một 'sức hút hoang dã' khác thường.

Bà Phó Đoan quyết định ra tay cứu vớt Xuân Tóc Đỏ. Bà dẫn hắn về giới thiệu với ông bà Văn Minh, chủ nhân của tiệm may Âu Hóa danh tiếng đất Hà thành. Tại đây, Xuân bước vào một thế giới hoàn toàn xa lạ: thế giới của những bộ y phục tân thời mang tên Ngây Thơ, Lời Hứa Dở Dang, Chinh Phục, và những triết lý cải cách xã hội nửa mùa.

Từ một kẻ mạt hạng không tấc đất cắm dùi, chỉ sau một đêm, Xuân Tóc Đỏ được khoác lên mình bộ âu phục bóng lộn, tóc xức sáp thơm lừng, sẵn sàng bước vào hành trình đổi vận ngoạn mục."""
            },
            {
                "title": "Chương 2: Tiệm may Âu Hóa và trào lưu giải phóng phụ nữ",
                "content": """Tiệm may Âu Hóa lúc bấy giờ là trung tâm văn minh của giới thượng lưu Hà Nội. Ông Văn Minh, một trí thức du học Pháp về (thực chất chỉ thi trượt bằng tú tài), luôn mở miệng là 'văn minh hóa xã hội', 'giải phóng nữ quyền' và 'thể thao cứu quốc'.

Nhà thiết kế chính của tiệm là cụ TYPN - người chuyên sáng tạo ra những kiểu váy áo khoét sâu, xẻ tà táo bạo. Khi nhìn thấy Xuân Tóc Đỏ, cụ TYPN reo lên như bắt được vàng: 'Đây rồi! Một thân hình hoàn mỹ của người lao động tự do! Chú em sẽ là ma-nơ-canh sống cho các bộ y phục nam tính tân tiến!'.

Xuân Tóc Đỏ nhanh chóng học lỏm được những câu nói cửa miệng của giới thượng gia: 'Nước mẹ Đại Pháp', 'văn minh tiến bộ', 'khoa học nhân văn'. Mỗi khi ai hỏi điều gì vượt quá hiểu biết, hắn liền trợn mắt phán một câu: 'Mẹ kiếp! Nước đời là thế!'. Đáng kinh ngạc là những lời nói thô bỉ ấy lại được các quý bà quý cô tán thưởng nhiệt liệt, coi đó là sự thẳng thắn, bộc trực của một bậc 'thiên tài chưa gặp thời'.

Tiếng tăm của Xuân bắt đầu lan rộng khắp các phòng trà và biệt thự sang trọng, đưa hắn từng bước leo cao trong mắt gia đình cụ cố Hồng."""
            },
            {
                "title": "Chương 3: Hạnh phúc của một tang gia",
                "content": """Cụ tổ hơn tám mươi tuổi đang ốm nặng. Cả gia đình cụ cố Hồng đều mong mỏi cụ mau chết để bản di chúc đi vào thời kỳ thực hành. Cái chết của cụ tổ không đem lại nỗi buồn rầu, mà trái lại, mang đến niềm hân hoan rạng rỡ cho từng thành viên trong gia đình.

Cụ cố Hồng mơ màng nghĩ đến lúc được mặc áo sô gai, chống gậy, ho khạc và gục gặc đầu để thiên hạ trầm trồ khen ngợi là một người con có hiếu. Ông Văn Minh hí hửng vì đây là dịp quảng bá bộ sưu tập tang phục tân thời của tiệm may. Cô Tuyết được diện bộ y phục 'Ngây Thơ' bằng voan trắng mỏng tang để khoe vẻ đẹp ngây thơ lãng mạn.

Đám ma diễn ra rình rang chưa từng thấy. Đi đầu là hai vòng hoa lớn của bạn bè, theo sau là hàng chục chiếc xe hơi sang trọng, kèn ta, kèn Tây, kèn Tàu thi nhau thổi những điệu vui tươi rộn rã. Khách đi đưa tang cười nói râm ran, liếc mắt đưa tình, bàn tán về bất động sản, đồ trang sức và những mối tình vụng trộm.

Một cảnh tượng trào phúng bi đát đến tột cùng: một xã hội đạo đức suy đồi, nơi tình thâm ruột thịt bị chôn vùi dưới lòng tham lam và thói khoe mẽ kệch cỡm."""
            },
            {
                "title": "Chương 4: Đỉnh cao danh vọng và danh hiệu Anh Hùng Cứu Quốc",
                "content": """Đỉnh điểm của sự lố bịch là trận chung kết quần vợt giữa đội Việt Nam và đội quán quân Xiêm La (Thái Lan). Xuân Tóc Đỏ được cử ra sân thi đấu vì tay vợt số một bị ốm. Bằng một chuỗi may mắn không tưởng và sự can thiệp bí mật vì lý do ngoại giao giữa hai nước, Xuân Tóc Đỏ đã 'nhường' phần thắng cho đối phương để giữ gìn hòa bình hữu nghị.

Đám đông cổ động viên cuồng nhiệt từ thất vọng chuyển sang tung hô hắn như một đấng cứu thế. Đứng trước hàng vạn người đang hô vang tên mình, Xuân Tóc Đỏ giơ tay dõng dạc tuyên bố: 'Hỡi quần chúng nông nổi! Ta đã cứu vãn nền hòa bình cho các ngươi!'.

Tiếng vỗ tay vang dội như sấm dậy. Nhà chức trách trao tặng hắn huân chương cao quý, các quý tộc tranh nhau gả con gái cho hắn. Xuân Tóc Đỏ - kẻ lưu manh mù chữ ngày nào - đã chính thức bước lên đỉnh cao danh vọng của một thời đại đảo lộn giá trị."""
            }
        ]
    },
    {
        "slug": "lao_hac",
        "title": "Lão Hạc",
        "author": "Nam Cao",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1457369804613-52c61a468e7d?q=80&w=600",
        "rating_avg": 5.0,
        "review_count": 680,
        "format": "pdf",
        "summary": "Bức tranh hiện thực xúc động về số phận bi thảm cùng phẩm giá trong sạch, cao cả của người nông dân Việt Nam trước cách mạng.",
        "narration_text": "Sách nói Lão Hạc của nhà văn Nam Cao. Lão Hạc sang nhà tôi chơi. Vừa ngồi xuống mép phản, lão đã cất tiếng nói run rẩy: Cậu Vàng đi đời rồi ông giáo ạ. Khốn nạn, tôi già bằng này tuổi đầu rồi mà còn đi lừa một con chó. Nó tin tôi thế, vẫy đuôi mừng rỡ mà tôi nỡ lòng nào để người ta bắt nó đi thịt. Hai hàng nước mắt lão ầng ậc chảy dài trên gò má nhăn nheo. Đằng sau sự hy sinh đau đớn ấy là một tấm lòng người cha bao la, thà chết trong nghèo khổ chứ nhất quyết không phạm vào mảnh vườn của đứa con trai.",
        "chapters": [
            {
                "title": "Chương 1: Lão Hạc và con chó Vàng",
                "content": """Lão Hạc là một người nông dân góa vợ sống thui thủi một mình nơi góc làng. Gia tài của lão chỉ có mảnh vườn nhỏ vài sào và đứa con trai duy nhất. Nhưng vì không đủ tiền cưới vợ, con trai lão đã phẫn chí bỏ làng đi phu đồn điền cao su biền biệt nhiều năm không về.

Niềm an ủi duy nhất của lão Hạc là con chó Vàng - kỷ vật đứa con để lại. Lão gọi nó là 'cậu Vàng' như một người bà con thân thiết. Có miếng gì ngon lão cũng nhường cho nó, bắt rận, tắm rửa và trò chuyện với nó như một con người: 'Cậu Vàng của ông có đói không? Khi nào thằng bố mày về thì mày sướng nhé!'.

Thế nhưng, sau trận ốm nặng kéo dài hai tháng ròng rã, lão Hạc kiệt quệ hoàn toàn. Hoa màu trong vườn bị bão tàn phá, giá gạo ngày một đắt đỏ. Mỗi ngày lão không đi làm được thuê mướn thì lại phải tiêu lẹm vào số tiền dành dụm. Lão nhận ra rằng nuôi cậu Vàng mỗi ngày tốn kém, mà lão thì không muốn bán đi dù chỉ một thước đất trong mảnh vườn vốn thuộc về đứa con trai.

Ý nghĩ bán cậu Vàng nhen nhóm trong đầu lão như một nỗi dằn vặt xé nát tâm can."""
            },
            {
                "title": "Chương 2: Cậu Vàng đi đời rồi, ông giáo ạ!",
                "content": """Lão Hạc sang nhà tôi chơi. Vừa ngồi xuống mép phản, lão đã cất tiếng run rẩy: 'Cậu Vàng đi đời rồi ông giáo ạ!'.
Tôi giật mình hỏi: 'Bán rồi à lão?'.
'Bán rồi! Họ vừa bắt xong!'.

Lão cố làm ra vẻ vui vẻ, nhưng nụ cười của lão méo mó, hai mắt ầng ậc nước. Lão bảo: 'Khốn nạn... Tôi già bằng này tuổi đầu rồi mà còn đi đánh lừa một con chó! Nó có biết gì đâu! Tôi cho nó ăn cơm no nê trong chậu, đang lúc nó cắm cúi ăn thì thằng Mục với thằng Xiên rình sẵn nhảy vào quăng lưới túm lấy... Nó kêu ư ử, đôi mắt nó nhìn tôi như muốn trách móc: A! Lão già tệ lắm! Tôi ăn ở với lão như thế mà lão nỡ đối xử với tôi thế này ư?'.

Đến đây, lão Hạc không kìm được nữa, lão hu hu khóc. Đầu lão ngoẹo về một bên, cái miệng móm mém mếu máo như con nít, những giọt nước mắt nóng hổi lăn dài qua những nếp nhăn xô lại trên khuôn mặt già nua khắc khổ. Tôi ôm lấy vai lão mà nghẹn ngào, không biết nói lời nào để an ủi một trái tim vừa tự xé rách chính mình vì lòng tự trọng."""
            },
            {
                "title": "Chương 3: Bàn giao gia tài và bức thư gửi con",
                "content": """Sau hôm bán chó, lão Hạc thu xếp mọi việc một cách cẩn thận và tĩnh lặng lạ thường. Lão mang toàn bộ số tiền bán chó cùng với số tiền dành dụm được bấy lâu - tổng cộng được ba mươi đồng bạc hoa xòe - sang gửi tôi.

Lão bảo: 'Tôi gửi ông giáo số tiền này. Nếu chẳng may tôi có mệnh hệ nào thì nhờ ông giáo đứng ra lo liệu ma chay giúp tôi, đừng phiền lụy đến hàng xóm láng giềng. Còn mảnh vườn, tôi xin gửi lại ông giáo trông nom, đợi ngày con trai tôi về thì giao tận tay nó, bảo rằng bố nó đã giữ trọn cho nó đến hơi thở cuối cùng'.

Tôi cảm động muốn ứa nước mắt trước nhân cách của lão. Trong xã hội bần cùng khốn khó này, biết bao kẻ dẫm đạp lên nhau để giành giật sự sống, vậy mà người nông dân nghèo ấy vẫn nâng niu phẩm giá của mình trong sạch như một đóa sen giữa bùn lầy."""
            },
            {
                "title": "Chương 4: Cái chết dữ dội và sự bất tử của lương tri",
                "content": """Vài hôm sau, Binh Tư - một gã trộm cắp trong làng - rỉ tai tôi rằng lão Hạc vừa sang xin hắn ít bả chó. Tôi sững sờ thất vọng: 'Chẳng lẽ lão Hạc cũng đến bước đường cùng mà tha hóa như thế sao?'. Nhưng tôi đã lầm, một sự lầm lẫn đau đớn.

Sáng hôm ấy, một tiếng kêu thét thất thanh phát ra từ nhà lão Hạc. Tôi chạy sang thì cảnh tượng trước mắt làm tôi rụng rời: Lão Hạc đang quằn quại trên giường, đầu tóc rũ rượi, quần áo xộc xệch, hai mắt trợn ngược, miệng sùi bọt mép, người co giật liên hồi như bị ai bóp nghẹt cổ họng.

Lão Hạc đã ăn chính liều bả chó ấy để tự kết liễu đời mình. Lão chọn cái chết đau đớn và ghê gớm nhất như con chó Vàng đã chết để tự trừng phạt bản thân, và để giữ trọn vẹn số tiền cùng mảnh vườn cho con trai.

Cái chết của lão Hạc làm rung chuyển cả làng quê nghèo. Cuộc đời có thể nghiền nát thân xác một con người, nhưng không bao giờ có thể vùi dập được thiên lương cao đẹp của họ."""
            }
        ]
    },
    {
        "slug": "chi_pheo",
        "title": "Chí Phèo",
        "author": "Nam Cao",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=600",
        "rating_avg": 5.0,
        "review_count": 890,
        "format": "pdf",
        "summary": "Tiếng kêu cứu xé lòng đòi quyền làm người lương thiện của người nông dân bị tha hóa tột cùng dưới bàn tay cường hào phong kiến.",
        "narration_text": "Sách nói Chí Phèo của nhà văn Nam Cao. Hắn vừa đi vừa chửi. Bao giờ cũng thế, cứ rượu xong là hắn chửi. Bắt đầu hắn chửi trời, có hề gì, trời có của riêng nhà nào? Rồi hắn chửi đời, cả làng Vũ Đại, và chửi cả đứa chết mẹ nào đã đẻ ra thân hắn. Nhưng bát cháo hành ấm nóng của Thị Nở bên bờ sông đã đánh thức ngọn lửa lương tri ngỡ đã tàn lụi suốt mấy mươi năm trong lồng ngực người đàn ông bất hạnh.",
        "chapters": [
            {
                "title": "Chương 1: Tiếng chửi của Chí Phèo làng Vũ Đại",
                "content": """Hắn vừa đi vừa chửi. Bao giờ cũng thế, cứ rượu xong là hắn chửi. Bắt đầu hắn chửi trời. Có hề gì? Trời có của riêng nhà nào? Rồi hắn chửi đời. Thế cũng chẳng sao: đời là tất cả nhưng chẳng là ai. Tức mình, hắn chửi ngay tất cả làng Vũ Đại. Nhưng cả làng Vũ Đại ai cũng nhủ thầm: 'Chắc nó trừ mình ra!'.

Không ai thèm lên tiếng, thế là hắn tức. Hắn chửi cả đứa chết mẹ nào đã đẻ ra thân hắn cho hắn khổ thế này. Nhưng đứa nào đẻ ra hắn? Chính hắn cũng không biết, cả làng Vũ Đại cũng chẳng ai hay. Người ta chỉ biết một buổi sáng mùa đông nọ, một người đi thả ống lươn thấy một đứa bé đỏ hỏn trần truồng nằm khóc oe oe bên một lò gạch cũ bỏ hoang.

Đứa bé ấy lớn lên trong sự nuôi nấng của dân làng, đi làm canh điền hiền lành như cục đất cho nhà Bá Kiến. Tuổi đôi mươi, hắn từng biết xấu hổ khi bà ba nhà Bá Kiến bắt bóp chân. Thế nhưng lòng ghen tuông vô cớ của cụ Bá đã đẩy người thanh niên lương thiện vào chốn lao tù tăm tối."""
            },
            {
                "title": "Chương 2: Từ người nông dân hiền lành thành con quỷ dữ",
                "content": """Bảy tám năm sau, Chí Phèo trở về làng với một diện mạo hoàn toàn khác lạ. Hắn trông đặc như một thằng sắng cá: cái đầu cạo trọc lốc, cái răng cạo trắng hớn, cái mặt thì đen mà rất câng câng, hai mắt gườm gườm trông gớm chết. Hắn mặc cái quần nái đen với cái áo tây vàng, ngực phanh ra phơi những nét xăm trổ rồng phượng vằn vện.

Về hôm trước, hôm sau hắn đã ngồi uống rượu ở quán bà bán nước từ sáng đến trưa. Say khướt, hắn xách vỏ chai xộc thẳng vào nhà cụ Bá Kiến rạch mặt ăn vạ. Bá Kiến - một tay cường hào cáo già khét tiếng làng Vũ Đại - thay vì báo quan lại đem tiền ra dỗ dành, mời rượu và biến Chí Phèo thành công cụ đâm thuê chém mướn.

Từ đó, Chí Phèo trở thành con quỷ dữ của làng Vũ Đại. Hắn sống bằng máu và nước mắt của người dân lương thiện. Hắn đập đầu, rạch mặt, chém giết, đốt quán để đổi lấy mấy hào mua rượu. Hắn triền miên trong những cơn say, say vô tận từ ngày này sang tháng khác, không biết mình bao nhiêu tuổi và đã đánh mất linh hồn từ lúc nào."""
            },
            {
                "title": "Chương 3: Bát cháo hành của Thị Nở và tình yêu bên bờ sông",
                "content": """Một đêm trăng sáng vằng vặc trên bãi dâu ven sông, Chí Phèo uống rượu say khướt rồi đi về căn lều hoang tàn của mình. Tại đây, hắn tình cờ gặp Thị Nở - một người đàn bà xấu ma chê quỷ hờn, dở hơi lại nghèo đói - đang ngủ quên dưới bụi chuối.

Trận ốm thập tử nhất sinh đêm ấy đã đưa hai con người khốn cùng lại gần nhau. Sáng hôm sau tỉnh dậy, lần đầu tiên sau bao năm tháng đọa đày, Chí Phèo hoàn toàn tỉnh rượu. Hắn lắng nghe được những âm thanh bình dị của cuộc sống quanh mình: tiếng chim hót ngoài bãi sông ríu rít, tiếng cười nói của những người đàn bà đi chợ về, tiếng anh thuyền chài gõ mái chèo đuổi cá trên sông...

Những âm thanh ấy như những mũi kim đâm vào tâm can hắn, nhắc hắn nhớ về ước mơ giản dị thời trai trẻ: một ngôi nhà tranh ấm cúng, chồng cày thuê cuốc mướn, vợ dệt vải, nuôi một con lợn làm vốn.

Đang lúc ngổn ngang tâm sự thì Thị Nở bưng vào một bát cháo hành còn bốc khói nghi ngút. Bát cháo hành dung dị ấy chứa đựng tình thương ấm áp đầu tiên mà Chí Phèo được nhận trong suốt cuộc đời. Hắn húp cháo và thấy mắt mình ươn ướt. Hắn muốn làm hòa với mọi người, hắn khao khát được trở lại làm người lương thiện."""
            },
            {
                "title": "Chương 4: Tiếng kêu đòi lương thiện và nhát dao kết liễu",
                "content": """Nhưng cánh cửa hoàn lương vừa hé mở đã vội vàng khép lại tàn nhẫn. Bà cô của Thị Nở - đại diện cho những định kiến hẹp hòi của làng quê phong kiến - kiên quyết cấm đoán cháu gái lấy một thằng không cha không mẹ, chỉ biết rạch mặt ăn vạ.

Thị Nở chạy sang trút tất cả những lời cay độc lên mặt Chí Phèo rồi ngoúng ngoảy bỏ đi. Chí Phèo ngồi ngẩn người ra như pho tượng đá. Hắn lại với lấy chai rượu, nhưng càng uống hắn lại càng tỉnh, và thoang thoảng đâu đây vẫn phảng phất hương vị bát cháo hành của Thị Nở.

Nỗi uất hận dâng trào tột độ. Hắn giắt con dao nhọn vào cạp quần, đi thẳng đến nhà Bá Kiến. Trước mặt kẻ thù truyền kiếp đã cướp đoạt cả cuộc đời mình, Chí Phèo dõng dạc đòi lại điều thiêng liêng nhất:
'Tao không muốn làm một thằng lưu manh nữa! Tao muốn làm người lương thiện! Nhưng ai cho tao lương thiện? Làm sao cho mất được những vết mảnh chai trên mặt này?'.

Nói đoạn, Chí Phèo vung dao đâm chết Bá Kiến rồi tự kết liễu đời mình. Tiếng kêu xé ruột của hắn mãi vang vọng như một lời kết án đanh thép đối với một xã hội tàn bạo đã đẩy con người vào ngõ cụt bi thương."""
            }
        ]
    },
    {
        "slug": "tat_den",
        "title": "Tắt Đèn",
        "author": "Ngô Tất Tố",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1495640388908-05fa85288e61?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 480,
        "format": "pdf",
        "summary": "Tác phẩm hiện thực phê phán sắc bén, vạch trần tội ác của chế độ sưu thuế thực dân phong kiến và ngợi ca phẩm chất kiên cường của người phụ nữ nông dân.",
        "narration_text": "Sách nói Tắt Đèn của nhà văn Ngô Tất Tố. Tiếng trống thúc thuế vang lên dồn dập từ đình làng Đông Xá như muốn xé toạc bầu trời xám xịt. Anh Dậu đang ốm thập tử nhất sinh vẫn bị bọn tay sai trói nghiến mang ra đình cùm kẹp. Chị Dậu gạt nước mắt bán đi đứa con gái đầu lòng và ổ chó mới đẻ để nộp sưu, nhưng bóng tối bất công vẫn không ngừng bủa vây.",
        "chapters": [
            {
                "title": "Chương 1: Tiếng trống thúc sưu ở làng Đông Xá",
                "content": """Tiếng trống thúc sưu từ sáng sớm đã dồn dập nổi lên ở đình làng Đông Xá. Âm thanh khô khốc, đe dọa ấy len lỏi qua từng bờ tre, mái rạ xơ xác, gieo rắc nỗi kinh hoàng cho những người nông dân nghèo đói. Bầu không khí ngột ngạt bao trùm khắp xóm làng.

Gia đình chị Dậu thuộc diện bần cùng nhất xóm. Vụ mùa thất bát, anh Dậu lại mắc bệnh sốt rét nằm liệt giường, da bọc xương. Để có tiền nộp hai suất sưu cho anh Dậu và cho người em trai đã chết từ năm ngoái, chị Dậu đã chạy vạy vạy mượn khắp nơi nhưng chỉ nhận được những cái lắc đầu lạnh lùng.

Bọn lý trưởng và cai lệ sầm sập xông vào nhà, lôi anh Dậu đang run rẩy vì cơn sốt ra đình đánh đập dã man rồi cùm chân lại. Tiếng gào khóc thảm thiết của đàn con thơ dại xé lòng người mẹ trẻ."""
            },
            {
                "title": "Chương 2: Bán con, bán chó chuộc chồng",
                "content": """Không còn con đường nào khác để cứu mạng chồng, chị Dậu đành phải gạt nước mắt đem cái Tý - đứa con gái đầu lòng mới lên bảy tuổi ngoan ngoãn, hiểu chuyện - cùng đàn chó con mới đẻ sang bán cho nhà Nghị Quế bên thôn Đoài.

Cái Tý vừa đi vừa khóc lóc van xin: 'Mẹ ơi, mẹ đừng bán con! Con ở nhà con làm đỡ mẹ, con bế em, con không ăn cơm của mẹ đâu!'. Từng lời nói ngây thơ của đứa trẻ như xát muối vào tim chị Dậu. Chị chỉ biết cắn chặt môi, nước mắt ròng ròng chảy xuống ngực áo rách tươm.

Tại nhà Nghị Quế, chị Dậu phải chịu đựng sự mặc cả bủn xỉn, khinh bỉ và tàn nhẫn của vợ chồng tên địa chủ keo kiệt. Chúng ép giá cả đứa bé lẫn đàn chó xuống mức rẻ mạt, chỉ vừa đủ để đóng suất thuế thân bất nhân."""
            },
            {
                "title": "Chương 3: Sự vùng lên của người đàn bà nông dân",
                "content": """Được tha về nhà, anh Dậu vừa húp được mấy thìa cháo loãng do bà lão hàng xóm thương tình mang cho thì tên cai lệ và người nhà lý trưởng lại sầm sập xông vào với roi song, tay thước và dây thừng.

Chúng đòi trói nghiến anh Dậu mang đi tiếp vì thiếu tiền thuế của người chết. Chị Dậu run rẩy van xin tha thiết: 'Hai ông làm phúc tha cho nhà cháu! Nhà cháu vừa mới tỉnh lại...'. Nhưng tên cai lệ trợn trừng mắt tát đánh bốp vào mặt chị rồi nhảy xổ vào anh Dậu.

Tình thương chồng vô bờ và lòng căm thù bị đè nén bấy lâu bỗng bùng cháy dữ dội. Chị Dậu nghiến răng: 'Mày trói ngay chồng bà đi, bà cho mày xem!'. Chị túm cổ áo tên cai lệ, ấn dúi một cái khiến hắn ngã chổng vó ra thềm. Tên người nhà lý trưởng sấn sổ bước tới cũng bị chị túm tóc lẳng ra cổng. Sức mạnh quật khởi của người phụ nữ bảo vệ tổ ấm đã đánh bại sự hung hăng hèn hạ của cường quyền."""
            },
            {
                "title": "Chương 4: Đêm tối tiền đồ mịt mù",
                "content": """Sau cuộc phản kháng ấy, chị Dậu bị bắt giải lên huyện. Tại công đường, quan huyện Tri phủ Tư Ân hiện nguyên hình là một tên dâm quan đốn mạt, toan giở trò sàm sỡ với chị giữa đêm khuya. Chị Dậu vứt nắm bạc vào mặt hắn rồi liều mình trốn thoát ra ngoài.

Chị được giới thiệu đi làm vú em cho nhà một cụ cố trên tỉnh. Tưởng chừng đã tìm được lối thoát, nhưng gã quan cụ già nua đồi bại lại mò vào phòng chị toan làm nhục. Chị Dậu giằng tay hắn ra, xô cửa chạy thục mạng ra đường phố trong đêm tối mịt mùng.

Trời tối đen như mực. Đêm tối dày đặc bao phủ khắp không gian, đen tối như chính tiền đồ mịt mùng và bế tắc của cuộc đời chị dưới ách thống trị tàn bạo của chế độ cũ."""
            }
        ]
    },
    {
        "slug": "vo_nhat",
        "title": "Vợ Nhặt",
        "author": "Kim Lân",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600",
        "rating_avg": 5.0,
        "review_count": 610,
        "format": "pdf",
        "summary": "Khúc ca ca ngợi vẻ đẹp tình người, khát vọng sống và niềm tin vào tương lai tươi sáng giữa thảm họa nạn đói năm 1945.",
        "narration_text": "Sách nói Vợ Nhặt của nhà văn Kim Lân. Giữa nạn đói năm Ất Dậu khủng khiếp, người chết như ngả rạ, không khí vẩn lên mùi ẩm mốc của rác rưởi và mùi tử khí của xác người. Ấy vậy mà anh cu Tràng - một người đàn ông nghèo xơ xác lại nhặt được vợ chỉ bằng bốn bát bánh đúc và vài câu hò đùa bông phèng bên kho thóc. Một đám cưới kỳ lạ giữa bờ vực cái chết đã thắp lên ngọn lửa hy vọng ấm áp cho cả gia đình.",
        "chapters": [
            {
                "title": "Chương 1: Người đàn bà lạ theo về xóm ngụ cư",
                "content": """Cái đói đã tràn đến xóm ngụ cư tự lúc nào. Những gia đình dắt díu nhau bồng bế, đói lả ngồi la liệt khắp các góc chợ. Mỗi buổi sáng sớm, tiếng quạ kêu từng hồi thê thiết trên những ngọn cây gạo trụi lá, dưới lòng đường thỉnh thoảng lại thấy vài ba cái xác người nằm còng queo bên bờ rào.

Trong hoàn cảnh chết chóc ấy, anh Tràng - một người dân ngụ cư thô kệch, nghèo khổ - bỗng dẫn một người đàn bà lạ về nhà vào lúc hoàng hôn chạng vạng. Người đàn bà mặc áo quần rách rưới như tổ đỉa, khuôn mặt lưỡi cày xám xịt chỉ còn hai con mắt trũng sâu, ngượng ngùng bước theo sau Tràng.

Cả xóm ngụ cư ngạc nhiên nhìn theo. Người ta bàn tán thì thầm: 'Giời đất này còn rước cái nợ đời về! Không biết có nuôi nổi nhau qua cái thì này không...'. Nhưng trên khuôn mặt Tràng lại rạng ngời một niềm hãnh diện và hạnh phúc kín đáo."""
            },
            {
                "title": "Chương 2: Bốn bát bánh đúc và mối duyên kỳ lạ",
                "content": """Mối nhân duyên ấy bắt đầu thật tình cờ bên cổng kho thóc của tỉnh. Hôm đó Tràng kéo xe thóc lên dốc, mệt quá bèn cất tiếng hò đùa vui:
'Muốn ăn cơm trắng mấy giò này
Lại đây mà đẩy xe bò với anh, nỉ!'.

Thế là cô ả ton ton chạy lại đẩy xe phụ Tràng. Vài hôm sau gặp lại ở chợ, người đàn bà gầy sọp hẳn đi vì đói khát. Tràng hào phóng mời: 'Có ăn gì thì ăn!'. Người đàn bà sà xuống ăn liền một chặp bốn bát bánh đúc chẳng thèm chuyện trò.

Ăn xong, Tràng nói nửa đùa nửa thật: 'Này nói đùa chứ có về với tớ thì ra khuân đồ lên xe rồi cùng về!'. Không ngờ người đàn bà đồng ý thật. Giữa ranh giới mong manh của sự sống và cái chết, người ta bám lấy nhau không phải vì vụ lợi, mà vì khát khao được sống, được nương tựa vào một mái ấm gia đình."""
            },
            {
                "title": "Chương 3: Nỗi lòng người mẹ già",
                "content": """Bà cụ Tứ - mẹ Tràng - lếch thếch bước về nhà trong ánh chiều tà. Nhìn thấy người đàn bà lạ chào mình bằng u, bà cụ sững sờ ngạc nhiên. Sau khi nghe con trai giải thích ngọn ngành, bà hiểu ra tất cả.

Lòng người mẹ nghèo xót xa vừa thương vừa tủi. Bà khóc vì thương cho con trai thiệt thòi phải lấy vợ trong cảnh đói khổ túng quẫn, thương cho người đàn bà khốn nạn vì bước đường cùng mới phải theo con mình. Nhìn người con dâu cúi gằm mặt e lệ, bà cụ cất tiếng nhẹ nhàng: 'Ừ thôi, các con đã phải duyên phải kiếp với nhau thì u cũng mừng lòng...'.

Lời nói ấm áp của mẹ già đã xóa tan nỗi e ngại, mặc cảm trong lòng người vợ nhặt, thắp lên hơi ấm tình thân trong căn nhà tranh xiêu vẹo."""
            },
            {
                "title": "Chương 4: Bữa cơm ngày đói và niềm tin tương lai",
                "content": """Sáng hôm sau, mặt trời lên cao sưởi ấm cả khoảng sân. Nhà cửa được quét dọn sạch sẽ, ang nước đầy ắp, vườn tược phong quang. Khung cảnh ấy khiến Tràng cảm thấy mình đã trưởng thành, có trách nhiệm với gia đình.

Bữa cơm đón dâu đầu tiên diễn ra thật cảm động: chỉ có một đĩa muối hạt, một lùm rau chuối thái rối và một nồi cháo loãng. Đến cuối bữa, bà cụ Tứ bưng ra một nồi cháo cám đặc sệt, mỉm cười bảo: 'Chè khoán đấy, ngon đáo để cơ!'. Dù vị cháo cám đắng chát nghẹn ứ cổ họng, nhưng cả ba người đều cố nuốt trong niềm vui sum họp.

Bên ngoài, tiếng trống thúc thuế dồn dập vang lên. Người vợ nhặt kể lại chuyện trên mạn Thái Nguyên, Bắc Giang người ta đã phá kho thóc Nhật chia cho dân nghèo, và đi theo Việt Minh. Trong tâm trí Tràng hiện lên hình ảnh đoàn người đi phá kho thóc với lá cờ đỏ sao vàng bay phấp phới, mở ra chân trời tự do và hy vọng."""
            }
        ]
    },
    {
        "slug": "de_men_phieu_luu_ky",
        "title": "Dế Mèn Phiêu Lưu Ký",
        "author": "Tô Hoài",
        "category": "Thiếu nhi & Cổ tích",
        "image_url": "https://images.unsplash.com/photo-1532012164546-f432f2e3edd4?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 750,
        "format": "epub",
        "summary": "Tác phẩm thiếu nhi kinh điển ngợi ca tinh thần trượng nghĩa, lý tưởng hòa bình và bài học đường đời đầu tiên đầy sâu sắc.",
        "narration_text": "Sách nói Dế Mèn Phiêu Lưu Ký của nhà văn Tô Hoài. Tôi sống độc lập từ thuở bé. Ấy là tục lệ lâu đời của họ nhà Dế chúng tôi. Vừa lớn lên, mẹ đã cho tôi ra ở riêng trong một cái hang khang trang bên bờ cỏ. Tôi ăn uống điều độ nên chóng lớn lắm, đôi càng mẫm bóng, vuốt ở chân cứng ngắc và nhọn hoắt. Nhưng cũng vì tính hiếu thắng xốc nổi của tuổi trẻ mà tôi đã gây ra cái chết thương tâm cho Dế Choắt - người bạn láng giềng gầy gò ốm yếu.",
        "chapters": [
            {
                "title": "Chương 1: Bài học đường đời đầu tiên",
                "content": """Tôi sống độc lập từ thuở bé. Cứ đến mùa gặt, mẹ tôi lại dắt các con ra ở riêng. Hang của tôi được đào sâu vào lòng đất ven một bờ cỏ xanh um, có nhiều ngóc ngách thoát hiểm kiên cố. Tôi ăn uống điều độ và làm việc có chừng mực nên chóng lớn lắm.

Chẳng bao lâu tôi đã trở thành một chàng dế thanh niên cường tráng: đôi càng mẫm bóng, vuốt ở chân cứng ngắc và nhọn hoắt, đôi cánh dài chấm đuôi, râu ria dài uốn cong hùng dũng. Tôi rất tự hào về vẻ đẹp của mình, đi đứng oai phong lẫm liệt.

Nhưng thói đời kiêu căng tự phụ thường dẫn đến tai họa. Cạnh hang tôi là Dế Choắt, một anh chàng gầy gò, ốm yếu như gã nghiện thuốc phiện. Thay vì giúp đỡ bạn, tôi luôn coi thường và giễu cợt Choắt. Chính sự xốc nổi ấy đã đẩy tôi vào một lỗi lầm không thể nào tha thứ."""
            },
            {
                "title": "Chương 2: Trò đùa tai hại và cái chết của Dế Choắt",
                "content": """Một buổi chiều mát mẻ, thấy chị Cốc béo tròn đang đứng rỉa cánh bên bờ đầm, tôi nảy ra ý định trêu chọc để khoe khoang tài nghệ với Dế Choắt. Mặc cho Choắt hết lời can ngăn, tôi vẫn cất giọng hát vang bài vè chế giễu chị Cốc rồi chui tọt vào hang sâu nằm khoái chí.

Chị Cốc nổi giận lôi đình, nhìn quanh không thấy ai bèn trút cơn thịnh nộ lên Dế Choắt đang run rẩy ngoài cửa hang. Mỏ chị Cốc như dùi sắt giáng xuống liên tiếp vào lưng Choắt khiến chú gãy đôi lưng, nằm quằn quại trên vũng máu.

Khi chị Cốc bay đi rồi, tôi mới dám bò ra ôm lấy Dế Choắt. Trước lúc trút hơi thở cuối cùng, Choắt thều thào nói: 'Ở đời mà có thói hung hăng bậy bạ, có óc mà không biết nghĩ, sớm muộn rồi cũng mang vạ vào mình đấy!'. Đó là bài học đường đời đầu tiên đẫm nước mắt mà tôi khắc cốt ghi tâm suốt đời."""
            },
            {
                "title": "Chương 3: Bị bắt làm đồ chơi và cuộc trốn thoát ngoạn mục",
                "content": """Sau khi chôn cất Dế Choắt dưới gốc cỏ xanh, tôi quyết định rời bỏ quê hương lên đường đi ngao du thiên hạ để mở rộng tầm mắt. Nhưng trên đường đi, tôi không may bị hai cậu bé bắt sống nhốt vào lồng tre làm đồ chơi chọi dế.

Trong những ngày bị giam cầm, tôi phải chứng kiến cảnh những chú dế hung dữ cắn xé lẫn nhau chỉ để mua vui cho con người. Tôi kiên quyết không khuất phục, nung nấu ý chí tự do và tìm mọi cơ hội để đào thoát.

Nhờ sự mưu trí và sức bật dẻo dai của đôi càng, một đêm mưa gió, tôi đã phá vỡ then cài lồng tre, phóng mình ra ngoài bãi cỏ bao la, hít thở bầu không khí tự do lồng lộng."""
            },
            {
                "title": "Chương 4: Kết nghĩa cùng Dế Trũi và chí nguyện bốn phương",
                "content": """Trên chặng đường phiêu lưu tiếp theo, tôi tình cờ cứu thoát Dế Trũi khỏi nanh vuốt của bầy châu chấu kiêu ngạo. Cảm kích trước nghĩa cử trượng nghĩa ấy, Dế Trũi đã xin kết nghĩa anh em đồng cam cộng khổ cùng tôi.

Hai chúng tôi cùng nhau kết bè bằng lá sen bồng bềnh xuôi theo dòng sông lớn, kết bạn với muôn loài côn trùng hiền lành: từ bác Xiến Tóc, bọ ngựa đến họ nhà chuồn chuồn. Chúng tôi cùng nhau truyền bá thông điệp hòa bình: 'Muôn loài kết đoàn làm một nhà, không áp bức, không chia rẽ!'.

Hành trình của Dế Mèn không chỉ là chuyến phiêu lưu kỳ thú qua những miền đất lạ, mà còn là hành trình hoàn thiện nhân cách từ một gã trai huênh hoang trở thành một trang trượng phu giàu lòng nhân ái."""
            }
        ]
    },
    {
        "slug": "toi_thay_hoa_vang_tren_co_xanh",
        "title": "Tôi Thấy Hoa Vàng Trên Cỏ Xanh",
        "author": "Nguyễn Nhật Ánh",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1509021436665-8f07dbf5bf1d?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 820,
        "format": "pdf",
        "summary": "Cuốn nhật ký tuổi thơ trong veo, ngọt ngào và day dứt về tình anh em, tình làng nghĩa xóm cùng những rung động đầu đời bình dị nơi làng quê miền Trung nghèo khó.",
        "narration_text": "Sách nói Tôi Thấy Hoa Vàng Trên Cỏ Xanh của nhà văn Nguyễn Nhật Ánh. Tuổi thơ làng quê nghèo khó mà đong đầy kỷ niệm. Thằng Tường em tôi có tính thương người kỳ lạ, nó nhặt con cóc bị thương về nuôi dưới gầm giường và tin rằng cóc là cậu ông trời. Giữa những trò nghịch ngợm bên bờ rào, con diều giấy bay lượn và bóng dáng cô bé Mận nép sau gốc cây, những ký ức hồn nhiên ấy sẽ mãi là bông hoa vàng rực rỡ sưởi ấm tâm hồn mỗi chúng ta.",
        "chapters": [
            {
                "title": "Chương 1: Con cóc cậu trời và tình thương thơ dại",
                "content": """Thằng Tường em tôi có tính thương người kỳ lạ, mà nói đúng hơn là thương muôn loài. Một hôm đi học về qua bờ mương, thấy một con cóc bị gãy chân nằm ngửa bụng thở thoi thóp, nó cẩn thận bọc vào vạt áo đem về giấu dưới gầm giường để chữa trị.

Tôi bảo: 'Cóc là loài gớm ghiếc, mày đem về nhà lỡ bố mắng thì sao?'. Nó phụng phịu cãi: 'Cóc là cậu ông trời đấy anh hai! Cậu ông trời bị đau thì mình phải băng bó cho cậu chứ!'. Thế là ngày nào nó cũng đi bắt sâu, bắt kiến đút cho con cóc ăn, tối tối lại thì thầm trò chuyện với con cóc như hai người bạn tâm giao.

Tuổi thơ của hai anh em tôi trôi qua bên góc sân đất, những buổi trưa trốn bố mẹ đi câu cá bống, những trận cười vỡ bụng khi bắt ve sầu dán cánh giấy. Làng quê nghèo miền Trung đầy nắng và gió, nhưng trong mắt những đứa trẻ như chúng tôi, đó là cả một vương quốc thần tiên rực rỡ sắc màu."""
            },
            {
                "title": "Chương 2: Căn nhà gỗ của chú Đàn và nàng Trinh mù",
                "content": """Trong làng tôi có chú Đàn, chú bị mất một cánh tay trong một tai nạn thuở nhỏ nhưng lại đàn ghi-ta rất hay. Những đêm trăng sáng, thanh niên trong làng thường tụ tập trước sân nhà chú để nghe tiếng đàn thánh thót và những khúc hát dân ca da diết.

Chú Đàn yêu thầm chị Trinh, một cô gái xinh đẹp nhưng không may bị mù đôi mắt. Tình yêu của họ trong sáng và bình dị như dòng suối trong rừng, nhưng lại gặp phải sự cấm đoán gay gắt từ gia đình chị Trinh vì chú Đàn tàn tật.

Mỗi lần chị Trinh đi ngang qua con đường làng rợp bóng tre, chú Đàn lại lặng lẽ gảy lên khúc nhạc quen thuộc để chị nhận ra phương hướng. Tình yêu không lời ấy đã gieo vào tâm hồn non nớt của anh em tôi những rung cảm đầu đời về sự hy sinh và lòng chung thủy."""
            },
            {
                "title": "Chương 3: Cô bạn Mận và những rung động đầu đời",
                "content": """Mận là con gái của chú Năm Tần. Mận có đôi mắt tròn xoe, đen láy và nụ cười e ấp khiến tôi mỗi lần nhìn thấy đều bối rối lạ thường. Một ngày nọ, biến cố ập đến: nhà Mận bị cháy rụi, bố Mận bị bệnh tâm thần bỏ trốn đi đâu không rõ.

Mẹ tôi thương tình đón Mận về nhà nuôi dưỡng cùng hai anh em tôi. Có Mận ở chung nhà, tôi vừa vui mừng lại vừa lo sợ. Tôi vụng về thể hiện tình cảm của mình bằng cách nhường phần cơm nhiều hơn cho Mận, trèo lên cây cao hái quả thị thơm lừng tặng bạn.

Nhưng tôi cũng bắt đầu biết ghen tị. Mỗi khi thấy Mận tíu tít chơi đùa cùng thằng Tường, chia sẻ những bí mật tuổi thơ, lòng tôi lại cuộn lên một cảm giác ấm ức khó tả - thứ cảm xúc vị kỷ đầu tiên của tuổi mới lớn."""
            },
            {
                "title": "Chương 4: Cơn lũ trắng đồng và chiếc nẹp bằng củi gai",
                "content": """Mùa mưa năm ấy hung bạo chưa từng thấy. Nước sông dâng cao cuồn cuộn tràn qua đê, nhấn chìm toàn bộ làng mạc trong biển nước trắng xóa. Cả nhà tôi phải trèo lên gác xép tránh lũ, chia nhau từng củ khoai nướng và bát cháo muối cầm hơi.

Giữa lúc đói khát, con gà mái của nhà tôi đẻ được mấy quả trứng. Thằng Tường lén giấu trứng đi để dành cho con cóc của nó. Tôi vô tình phát hiện ra, cơn giận dữ và đói khát bùng lên khiến tôi mất hết lý trí: tôi vớ lấy thanh củi gai giáng mạnh vào lưng thằng Tường.

Cú đánh oan nghiệt ấy khiến Tường bị chấn thương cột sống nằm liệt giường suốt nhiều tháng trời. Nhìn em đau đớn mà không một lời oán trách anh hai, ngày ngày vẫn mỉm cười gượng gạo, lòng tôi ngập tràn ân hận và cắn rứt khôn nguôi. Tôi nhận ra sự ích kỷ của mình tàn nhẫn đến dường nào."""
            },
            {
                "title": "Chương 5: Bông hoa vàng trên bãi cỏ xanh ngát",
                "content": """Nhờ sự chăm sóc kiên trì của cả gia đình và sự xuất hiện kỳ diệu của một vị thầy thuốc già, đôi chân thằng Tường dần dần hồi phục. Buổi sáng hôm ấy, bầu trời sau cơn mưa bỗng trong xanh lạ kỳ, gió xuân mơn man thổi qua những cánh đồng đang hồi sinh.

Tôi dìu Tường bước ra bãi cỏ sau nhà. Trước mắt chúng tôi là một thảm cỏ xanh mướt trải dài tít tắp, điểm xuyết muôn vàn bông hoa cúc dại màu vàng rực rỡ lung linh dưới ánh nắng mai. Thằng Tường reo lên thích thú, dang rộng hai tay đón lấy luồng gió mát lành.

Nhìn nụ cười hồn nhiên của em bên những đóa hoa vàng trên cỏ xanh, tôi hiểu rằng tuổi thơ dẫu có những vết thương và vấp ngã, nhưng tình yêu thương ruột thịt sẽ luôn là chiếc cầu vồng chữa lành mọi nỗi đau, dẫn lối ta trở về với sự thiện lương trong trẻo nhất."""
            }
        ]
    },
    {
        "slug": "mat_biec",
        "title": "Mắt Biếc",
        "author": "Nguyễn Nhật Ánh",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 910,
        "format": "pdf",
        "summary": "Bản tình ca da diết, đượm buồn về mối tình đơn phương khắc cốt ghi tâm của Ngạn dành cho Hà Lan - cô gái có đôi mắt biếc biếc như ngọc.",
        "narration_text": "Sách nói Mắt Biếc của nhà văn Nguyễn Nhật Ánh. Làng Đo Đo mùa quả chín ngập tràn kỷ niệm tuổi thơ. Ngạn lớn lên bên cạnh Hà Lan, cô bạn gái cùng làng có đôi mắt long lanh như hồ nước mùa thu. Suốt những năm tháng ấu thơ cho đến khi bước vào thị thành phồn hoa, trái tim Ngạn chỉ hướng về một bóng hình duy nhất. Dù dòng đời đưa đẩy Hà Lan trôi dạt vào những cuộc tình cay đắng, Ngạn vẫn mãi ở lại làng quê, gìn giữ mối tình si vụng dại đến tận cuối cuộc đời.",
        "chapters": [
            {
                "title": "Chương 1: Làng Đo Đo và đôi mắt biếc tuổi thơ",
                "content": """Tôi sinh ra và lớn lên ở làng Đo Đo, một ngôi làng nhỏ yên bình nép mình bên rặng tre và những cánh đồng lúa xanh ngát. Tuổi thơ tôi gắn liền với chợ Đo Đo, cây thị đầu làng và những buổi chiều trốn ngủ đi hái sim rừng.

Nhưng điều tuyệt vời nhất trong cuộc đời tôi là Hà Lan. Hà Lan bằng tuổi tôi, nhà ở cạnh nhà tôi. Cô bé có một đôi mắt đặc biệt: đôi mắt to tròn, trong veo và đượm một nỗi buồn mơ màng mà sau này ông nội tôi gọi đó là 'Mắt Biếc'. Ông bảo: 'Đôi mắt ấy sau này sẽ khổ lắm đấy con ạ'.

Thuở nhỏ, tôi thường trèo lên cây dâu hái những quả chín mọng ném xuống cho Hà Lan hứng, hoặc ngồi tỉ mẩn khắc tên hai đứa lên thân cây thị. Tôi đàn ghi-ta cho Hà Lan hát, những bài đồng dao mộc mạc nuôi dưỡng tâm hồn chúng tôi lớn lên từng ngày."""
            },
            {
                "title": "Chương 2: Rời làng ra thành phố và những ngã rẽ",
                "content": """Lớn lên, cả hai chúng tôi cùng rời làng Đo Đo ra thành phố để theo học trung học. Thành phố mở ra trước mắt chúng tôi một thế giới hoàn toàn khác: những con đường trải nhựa thênh thang, ánh đèn điện lung linh rực rỡ và những thú vui xa hoa.

Trong khi tôi vẫn giữ nguyên tính cách trầm lặng, yêu thích những nếp xưa cũ của làng quê thì Hà Lan nhanh chóng bị cuốn vào lối sống hiện đại nơi thị thành. Hà Lan làm quen với Dũng - một công tử nhà giàu, đi xe máy xịn, sành điệu và giỏi võ thuật.

Tôi nhìn thấy Hà Lan dần dần xa rời tầm tay mình mà bất lực. Mỗi lần ngồi quán nước ngắm nhìn Dũng đón Hà Lan đi dạo phố, lòng tôi đau nhói như có ngàn mũi kim châm. Tôi biết Dũng chỉ coi Hà Lan như một món đồ chơi qua đường, nhưng tình yêu mù quáng đã khiến đôi mắt biếc không còn nhìn thấy hiểm nguy phía trước."""
            },
            {
                "title": "Chương 3: Nỗi đau của Hà Lan và sự xuất hiện của Trà Long",
                "content": """Bi kịch cuối cùng cũng ập đến. Sau khi làm Hà Lan mang thai, Dũng đã nhẫn tâm phủi tay rũ bỏ trách nhiệm để đi cưới một cô gái giàu có khác theo sự sắp đặt của gia đình.

Hà Lan đau đớn gục ngã, sinh ra một bé gái đặt tên là Trà Long rồi gửi về làng cho bà ngoại nuôi dưỡng. Trong những ngày tháng tăm tối nhất ấy của Hà Lan, tôi vẫn luôn ở bên cạnh chăm sóc, động viên và thậm chí muốn cưới Hà Lan để làm cha cho đứa trẻ. Nhưng Hà Lan kiên quyết từ chối: 'Ngạn tốt quá, em không xứng đáng với Ngạn!'.

Tôi trở về làng Đo Đo làm thầy giáo trường làng, tận tụy chăm sóc bé Trà Long như con gái ruột. Trà Long lớn lên giống mẹ như đúc: cũng khuôn mặt thanh tú, cũng giọng nói ngọt ngào và đặc biệt là đôi mắt biếc trong veo của Hà Lan năm nào."""
            },
            {
                "title": "Chương 4: Chuyến tàu cuối cùng chia tay Đo Đo",
                "content": """Trà Long lớn lên trong tình thương yêu và sự dạy dỗ ân cần của tôi. Cô bé yêu làng Đo Đo da diết, yêu từng rặng tre, giếng nước và yêu chính người thầy giáo đã nuôi nấng mình từ thuở ấu thơ.

Khi Trà Long trưởng thành và bày tỏ tình cảm với tôi, tôi bỗng giật mình thức tỉnh. Tôi nhận ra rằng hình bóng mà tôi yêu thương suốt bao năm qua không phải là Trà Long, mà là mẹ của cô bé - Hà Lan của những ngày thơ dại. Nếu tôi ở lại bên Trà Long, tôi sẽ chỉ biến cô thành một chiếc bóng thay thế cho mối tình si không trọn vẹn.

Trong một đêm mưa lạnh, tôi viết một bức thư từ biệt để lại cho Trà Long rồi lặng lẽ xách va-li bước ra ga xe lửa. Khi chuyến tàu đêm từ từ chuyển bánh xé toang màn đêm rời khỏi Đo Đo, tôi nhìn qua khung cửa sổ mà nước mắt tuôn rơi. Tạm biệt Đo Đo, tạm biệt mối tình ngây thơ khắc khoải cả một đời người."""
            }
        ]
    },
    {
        "slug": "cho_toi_xin_mot_ve_di_tuoi_tho",
        "title": "Cho Tôi Xin Một Vé Đi Tuổi Thơ",
        "author": "Nguyễn Nhật Ánh",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 670,
        "format": "pdf",
        "summary": "Tác phẩm đoạt Giải thưởng Văn học ASEAN, đưa độc giả quay ngược bánh xe thời gian trở về thế giới tuổi thơ kỳ diệu và tinh nghịch.",
        "narration_text": "Sách nói Cho Tôi Xin Một Vé Đi Tuổi Thơ của nhà văn Nguyễn Nhật Ánh. Bạn có bao giờ ước ao được quay trở lại những năm tháng lên tám, lên mười để nhìn ngắm thế giới bằng đôi mắt trong trẻo lạ kỳ? Hãy cùng cu Mùi, Hải cò, Tủn và Tí sún mở phiên tòa phán xử người lớn, đảo lộn trật tự thế giới và tìm lại chiếc vé diệu kỳ đã thất lạc nơi ký ức.",
        "chapters": [
            {
                "title": "Chương 1: Chiếc vé thông hành về miền ký ức",
                "content": """Tôi viết cuốn sách này không phải dành riêng cho trẻ em, mà là dành cho những ai từng là trẻ em. Cuộc đời người lớn đôi khi quá tẻ nhạt, phẳng lặng và gò bó bởi hàng trăm thứ quy tắc phiền toái mà họ tự đặt ra.

Năm lên tám tuổi, tôi - thằng cu Mùi - cùng với ba người bạn chí cốt: Hải cò, con Tủn và con Tí sún, cảm thấy cuộc sống xung quanh mình đơn điệu đến mức không thể chịu nổi. Ngày nào cũng phải rửa mặt, đi học, làm bài tập về nhà, vâng lời cha mẹ và đi ngủ đúng giờ.

Chúng tôi quyết định phải làm một cuộc cách mạng: thay đổi thế giới bằng cách thay đổi cách nhìn nhận về mọi thứ xung quanh mình."""
            },
            {
                "title": "Chương 2: Cuộc nổi loạn thay đổi tên gọi thế giới",
                "content": """Ý tưởng đầu tiên của chúng tôi là thay đổi tên gọi của các đồ vật. Tại sao cái nón lại phải gọi là cái nón mà không gọi là cái quạt? Tại sao con gà lại gọi là con gà mà không gọi là con vịt?

Thế là chúng tôi lập ra một cuốn từ điển mới: gọi quả chuối là quả ớt, gọi cây chổi là khẩu súng, gọi cô giáo là bà tiên. Cả nhóm hào hứng trò chuyện với nhau bằng thứ ngôn ngữ bí mật mà không một người lớn nào hiểu nổi.

Hậu quả là trong bữa cơm, khi tôi dõng dạc bảo mẹ: 'Mẹ ơi xới cho con bát đất!', mẹ tôi đã tưởng tôi bị ma ám và suýt nữa đưa tôi đi viện tâm thần. Nhưng trò nghịch ngợm ngây ngô ấy đã đem lại cho chúng tôi những trận cười nghiêng ngả vô giá."""
            },
            {
                "title": "Chương 3: Phiên tòa phán xử người lớn",
                "content": """Đỉnh cao của sự phản kháng là phiên tòa giả định do bốn đứa chúng tôi tổ chức dưới gốc cây bàng. Chúng tôi đóng vai thẩm phán và luật sư, đưa bố mẹ lên ghế bị cáo để phán xét những 'tội ác' của họ.

Tội của người lớn nhiều vô kể: ép trẻ con ăn những món chúng ghét như mướp đắng và rau má, bắt ngủ trưa trong khi ngoài trời gió mát lộng tha hồ thả diều, hay hứa mua đồ chơi rồi lại quên bẵng mất.

Nhưng khi phiên tòa kết thúc, chúng tôi nhận ra rằng đằng sau sự nghiêm khắc và những lời mắng mỏ ấy là một tình yêu thương bao la vô bờ bến mà khi còn nhỏ chúng tôi chưa thể thấu hiểu trọn vẹn."""
            },
            {
                "title": "Chương 4: Bài học về lòng bao dung và sự trưởng thành",
                "content": """Thời gian trôi qua như bóng câu qua cửa sổ. Những đứa trẻ ngây thơ năm nào giờ đã trở thành những người lớn bận rộn với công việc, gia đình và những nỗi lo toan cơm áo gạo tiền.

Nhưng thỉnh thoảng, trong những phút giây tĩnh lặng giữa cuộc sống ồn ã, tôi lại lục tìm trong ngăn kéo ký ức chiếc vé đi tuổi thơ kỳ diệu. Chiếc vé ấy nhắc nhở chúng ta rằng: Dù khôn lớn đến đâu, hãy luôn giữ trong tim một khoảng trời trong trẻo, một tấm lòng bao dung và nụ cười rạng rỡ của đứa trẻ năm nào."""
            }
        ]
    },
    {
        "slug": "dat_rung_phuong_nam",
        "title": "Đất Rừng Phương Nam",
        "author": "Đoàn Giỏi",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 590,
        "format": "epub",
        "summary": "Bức tranh hoành tráng, kỳ vĩ và đậm đà bản sắc hào sảng về thiên nhiên hoang sơ cùng con người Nam Bộ kiên cường đánh giặc.",
        "narration_text": "Sách nói Đất Rừng Phương Nam của nhà văn Đoàn Giỏi. Theo chân cậu bé An lưu lạc khắp các vùng đất Nam Bộ trong những năm kháng chiến chống Pháp. Từ rừng tràm bạt ngàn U Minh, những dòng sông đỏ nặng phù sa đến những con người trượng nghĩa như ba nuôi, má nuôi và chú bé Cò gan dạ. Một thiên anh hùng ca tràn đầy sức sống của đất và người phương Nam trù phú.",
        "chapters": [
            {
                "title": "Chương 1: Bước chân lưu lạc của cậu bé An",
                "content": """Chiến tranh bùng nổ, thực dân Pháp nổ súng đánh chiếm Nam Bộ. Cậu bé An trong cơn loạn lạc đã bị lạc mất gia đình, bước vào cuộc đời phiêu bạt qua những cánh đồng mênh mông, những làng mạc cháy rụi và những khu rừng ngập mặn hoang sơ.

An may mắn được một gia đình nông dân hiền lành nhận nuôi: tía nuôi, má nuôi và thằng Cò - một chú bé đen nhẻm, hoạt bát và lanh lợi như con sóc rừng. Từ một công tử thành thị quen sống trong nhung lụa, An bắt đầu học cách chèo xuồng, bắt ốc, giăng câu và thích nghi với cuộc sống hào sảng nơi sông nước phương Nam."""
            },
            {
                "title": "Chương 2: Đi lấy mật ong trong rừng U Minh",
                "content": """Một buổi sáng tinh sương, tía nuôi dẫn An và thằng Cò chèo xuồng vào sâu trong rừng U Minh để thu hoạch kèo ong. Rừng tràm bạt ngàn tỏa hương thơm ngát của hoa tràm trắng muốt, tiếng ong rừng bay vo ve như một bản hợp xướng vĩ đại của thiên nhiên.

Tía nuôi dạy An cách xem hướng gió, cách hun khói bằng bó đuốc xơ dừa để đàn ong bay đi mà không đốt người, và cách cắt những bánh sáp ong vàng óng nặng trĩu mật ngọt. Từng giọt mật ong rừng nguyên chất sánh vàng như ngọc hổ phách, mang vị ngọt đậm đà của tinh hoa đất trời."""
            },
            {
                "title": "Chương 3: Cuộc chiến đấu với cá sấu khổng lồ",
                "content": """Vùng đầm lầy phương Nam ẩn chứa nhiều hiểm nguy khôn lường. Một buổi chiều đi câu cá trên kênh, An và Cò chạm trán với một con cá sấu khổng lồ - chúa tể đầm lầy với bộ da xù xì như khúc gỗ mục và hàm răng sắc nhọn gớm ghiếc.

Bằng sự bình tĩnh và kinh nghiệm săn bắt lão luyện của người dân sông nước, tía nuôi cùng các thợ săn trong làng đã dùng lưỡi câu sắt móc mồi vịt sống, dũng cảm đối đầu và hạ gục con thủy quái, bảo vệ an toàn cho xóm ấp."""
            },
            {
                "title": "Chương 4: Hào khí kháng chiến và tình yêu quê hương",
                "content": """Rừng U Minh không chỉ là nguồn sống trù phú mà còn là căn cứ địa kháng chiến kiên cường của quân và dân Nam Bộ. Dưới sự lãnh đạo của cách mạng, những người nông dân chân chất như tía nuôi, anh em du kích đã biến từng con rạch, gốc tràm thành cạm bẫy chôn vùi quân giặc ngoại xâm.

An lớn lên giữa tình yêu thương đùm bọc của đồng bào, hiểu được giá trị thiêng liêng của độc lập, tự do và nguyện cống hiến tuổi xuân cho mảnh đất phương Nam anh dũng."""
            }
        ]
    },
    {
        "slug": "truyen_kieu",
        "title": "Truyện Kiều",
        "author": "Đại thi hào Nguyễn Du",
        "category": "Thơ ca & Kịch nghệ",
        "image_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=600",
        "rating_avg": 5.0,
        "review_count": 1200,
        "format": "pdf",
        "summary": "Đỉnh cao chói lọi của nền thi ca cổ điển Việt Nam, khúc ca đoạn trường đớn đau về thân phận người phụ nữ tài hoa bạc mệnh trong xã hội phong kiến.",
        "narration_text": "Sách nói Đoạn Trường Tân Thanh - Truyện Kiều của Đại thi hào Nguyễn Du. Trăm năm trong cõi người ta, chữ tài chữ mệnh khéo là ghét nhau. Trải qua một cuộc bể dâu, những điều trông thấy mà đau đớn lòng. Lạ gì bỉ sắc tư phong, trời xanh quen thói má hồng đánh ghen. Thúy Kiều là người con gái tài sắc vẹn toàn nhưng cuộc đời lại chìm nổi suốt mười lăm năm lưu lạc truân chuyên giữa dòng đời bão táp.",
        "chapters": [
            {
                "title": "Đoạn 1: Chị em Thúy Kiều và Hội Đạp Thanh",
                "content": """Đầu lòng hai ả tố nga, Thúy Kiều là chị em là Thúy Vân. Mai cốt cách tuyết tinh thần, mỗi người một vẻ mười phân vẹn mười. Vân xem trang trọng khác vời, khuôn trăng đầy đặn nét ngài nở nang. Hoa cười ngọc thốt đoan trang, mây thua nước tóc tuyết nhường màu da.

Kiều càng sắc sảo mặn mà, so bề tài sắc lại là phần hơn: làn thu thủy nét xuân sơn, hoa ghen thua thắm liễu hờn kém xanh. Thông minh vốn sẵn tính trời, pha nghề thi họa đủ mùi ca ngâm. Cung thương lầu bậc ngũ âm, nghề riêng ăn đứt hồ cầm một trương.

Nhân tiết Thanh minh trong tiết tháng ba, chị em sắm sửa đi tảo mộ du xuân. Cỏ non xanh tận chân trời, cành lê trắng điểm một vài bông hoa. Tại đây, Kiều đã viếng nấm mồ vô chủ của Đạm Tiên và tao ngộ chàng thư sinh Kim Trọng tài hoa phong nhã."""
            },
            {
                "title": "Đoạn 2: Thề nguyền cùng Kim Trọng và Gia biến bán mình",
                "content": """Tình yêu giữa Kim Trọng và Thúy Kiều nảy nở đẹp đẽ và trong sáng. Dưới vầng trăng vằng vặc giữa trời, đôi lứa đã cùng nhau cắt tóc thề bồi: 'Đinh ninh hai mặt một lời song song'.

Nhưng chữ tình chưa trọn thì tai họa bất ngờ ập xuống gia đình Vương ông do sự vu oan giá họa của tên bán tơ gian ác. Cha và em trai bị bắt giam, tra tấn dã man.

Đứng trước sự lựa chọn nghiệt ngã giữa chữ tình và chữ hiếu, Kiều đã gạt nước mắt trao duyên lại cho em gái là Thúy Vân để thay mình đền đáp tấm lòng chàng Kim, còn bản thân nàng chấp nhận bán mình chuộc cha, bắt đầu chuỗi ngày lưu lạc mười lăm năm cay đắng."""
            },
            {
                "title": "Đoạn 3: Nanh vuốt Mã Giám Sinh và lầu xanh cay đắng",
                "content": """Rơi vào tay Mã Giám Sinh và mụ mối Tú Bà, Kiều mới bàng hoàng nhận ra mình bị lừa vào chốn lầu xanh nhơ bẩn. Nàng toan tự vẫn để giữ gìn trinh tiết nhưng không thành.

Bị giam lỏng nơi Lầu Ngưng Bích, Kiều trải qua những ngày tháng cô đơn, xót xa nhớ về cha mẹ già yếu không người phụng dưỡng và người yêu cũ nơi phương trời xa xăm:
'Buồn trông cửa bể chiều hôm
Thuyền ai thấp thoáng cánh buồm xa xa?
Buồn trông ngọn nước mới sa
Hoa trôi man mác biết là về đâu?'.

Cuộc đời nàng tiếp tục bị xô đẩy qua tay Sở Khanh, Thúc Sinh, chịu đựng cơn ghen tuông tàn nhẫn của Hoạn Thư trước khi tìm được bến đỗ bên người anh hùng Từ Hải."""
            },
            {
                "title": "Đoạn 4: Trùng phùng đoàn viên và khúc ca tri âm",
                "content": """Từ Hải - bậc trượng phu đội trời đạp đất - đã chuộc Kiều khỏi chốn lầu xanh, giúp nàng báo ân báo oán rạng rỡ. Nhưng vì mắc mưu quan tổng đốc Hồ Tôn Hiến, Từ Hải bị hãm hại chết đứng giữa trận tiền.

Đau đớn tột cùng, Kiều trèo lên cầu gieo mình xuống dòng sông Tiền Đường tự vẫn. Nhờ sư giác Duyên giăng lưới cứu vớt, Kiều được nương náu nơi cửa Phật thanh tịnh.

Sau mười lăm năm lưu lạc đoạn trường, chàng Kim Trọng vẫn một lòng son sắt đi tìm người yêu. Ngày đoàn tụ trùng phùng, hai người xem nhau như bạn tri âm tri kỷ, khép lại bản trường ca bất hủ về số phận và phẩm giá con người."""
            }
        ]
    },
    # ---------------- 2. KỸ NĂNG SỐNG & PHÁT TRIỂN BẢN THÂN ----------------
    {
        "slug": "dac_nhan_tam",
        "title": "Đắc Nhân Tâm",
        "author": "Dale Carnegie",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 1540,
        "format": "pdf",
        "summary": "Cuốn sách nghệ thuật sống bán chạy nhất mọi thời đại, hướng dẫn phương pháp thu phục lòng người, xây dựng mối quan hệ chân thành và lãnh đạo xuất chúng.",
        "narration_text": "Chào mừng bạn đến với sách nói Đắc Nhân Tâm của tác giả Dale Carnegie. Nguyên tắc số một: Không chỉ trích, oán trách hay than phiền. Muốn lấy mật thì đừng phá tổ ong. Con người vốn dĩ là sinh vật của cảm xúc, tự ái và định kiến chứ không đơn thuần hành động theo lý trí. Một lời chỉ trích gay gắt chỉ làm tổn thương lòng tự trọng và khơi dậy sự thù oán. Hãy học cách lắng nghe, bao dung và đặt mình vào vị trí của người khác.",
        "chapters": [
            {
                "title": "Chương 1: Muốn lấy mật thì đừng phá tổ ong",
                "content": """Vào ngày 7 tháng 5 năm 1931, thành phố New York chứng kiến một cuộc vây bắt tội phạm rúng động lịch sử. Francis 'Two Gun' Crowley - tên sát nhân nguy hiểm khét tiếng - đã bị dồn vào đường cùng trong căn hộ của người tình.

Hơn một trăm cảnh sát trang bị súng máy và lựu đạn cay đã bao vây tòa nhà. Trong làn mưa đạn xé toạc căn phòng, Crowley đã viết một bức thư đẫm máu: 'Dưới lớp áo này là một trái tim mệt mỏi nhưng lương thiện, một trái tim không hề muốn làm hại bất cứ ai'.

Ngay cả những kẻ giết người man rợ nhất còn không bao giờ nhận mình có lỗi, huống chi là những con người bình thường quanh ta. Chỉ trích là vô ích vì nó đặt người khác vào thế phòng thủ và khiến họ tìm mọi cách để biện minh cho bản thân. Muốn thu phục lòng người, điều tối thượng đầu tiên là: Đừng chỉ trích, oán trách hay than phiền."""
            },
            {
                "title": "Chương 2: Bí mật lớn nhất trong giao tiếp - Thành thật khen ngợi",
                "content": """Nhu cầu sâu sắc nhất trong bản tính con người là khao khát được công nhận và cảm thấy mình quan trọng. Nhà tâm lý học vĩ đại William James từng khẳng định: 'Nguyên lý sâu xa nhất trong bản tính con người là sự thèm khát được tán thưởng'.

Charles Schwab, người từng được tỷ phú thép Andrew Carnegie trả mức lương kỷ lục một triệu đô la mỗi năm, chia sẻ bí quyết thành công của mình: 'Tôi coi khả năng khơi dậy lòng nhiệt tình ở nhân viên là tài sản quý nhất. Cách duy nhất để phát huy những gì tốt nhất ở một con người là thông qua sự ngợi khen và khích lệ'.

Hãy phân biệt rõ ràng giữa lời khen ngợi chân thành xuất phát từ đáy lòng và lời xu nịnh dối trá ngoài đầu môi chót lưỡi. Lời khen thành thật đem lại nguồn năng lượng tích cực nuôi dưỡng tâm hồn người nhận suốt cả cuộc đời."""
            },
            {
                "title": "Chương 3: Nói về điều người khác quan tâm - Câu cá bằng mồi giun",
                "content": """Mùa hè nào tôi cũng đi câu cá ở Maine. Cá nhân tôi rất thích ăn dâu tây dầm kem tươi, nhưng kỳ lạ là loài cá lại chỉ thích ăn giun đất. Do đó, khi đi câu, tôi không móc dâu tây vào lưỡi câu, mà móc một con giun béo ngậy trước mũi cá và hỏi: 'Mày có muốn ăn cái này không?'.

Tại sao chúng ta không áp dụng nguyên lý hiển nhiên ấy vào cách đối nhân xử thế hàng ngày? Con người ai cũng chỉ quan tâm đến ước mơ, lợi ích và nhu cầu của chính họ. Cách duy nhất trên đời để thuyết phục người khác làm một việc gì đó là hãy nói về điều họ muốn và chỉ cho họ cách đạt được điều đó."""
            },
            {
                "title": "Chương 4: Nghệ thuật lắng nghe và mỉm cười chân thành",
                "content": """Một nụ cười không tốn một xu nhưng đem lại giá trị vô giá. Nó làm giàu cho người nhận mà không làm nghèo đi người trao tặng. Một nụ cười rạng rỡ từ ánh mắt xóa tan mọi khoảng cách xa lạ và mở toang cánh cửa tâm hồn của người đối diện.

Bên cạnh nụ cười, kỹ năng lắng nghe chăm chú là lời khen ngợi tinh tế nhất mà bạn có thể dành cho ai đó. Hãy lắng nghe bằng cả tấm lòng, không ngắt lời, khuyến khích họ chia sẻ về thành tựu và cuộc sống của họ. Bạn sẽ trở thành người trò chuyện thú vị nhất mà không cần phải nói quá nhiều."""
            }
        ]
    },
    {
        "slug": "tuoi_tre_dang_gia_bao_nhieu",
        "title": "Tuổi Trẻ Đáng Giá Bao Nhiêu",
        "author": "Rosie Nguyễn",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1497633762265-9d179a990aa6?q=80&w=600",
        "rating_avg": 4.8,
        "review_count": 930,
        "format": "pdf",
        "summary": "Cuốn sách gối đầu giường truyền cảm hứng mạnh mẽ cho hàng triệu người trẻ Việt Nam rèn luyện thói quen tự học, đọc sách, xách ba lô lên và đi để tỏa sáng.",
        "narration_text": "Sách nói Tuổi Trẻ Đáng Giá Bao Nhiêu của tác giả Rosie Nguyễn. Bạn hối tiếc vì không nắm bắt lấy một cơ hội nào đó, chẳng có ai phải mất ngủ. Bạn trải qua những ngày tháng nhạt nhẽo với công việc bạn căm ghét, người ta chẳng hề bận lòng. Bạn có chết mòn nơi xó tường với những ước mơ dang dở, đó không phải việc của họ. Suy cho cùng, cuộc đời của bạn là của chính bạn. Hãy sống hết mình, không ngừng học hỏi và rèn luyện bản thân mỗi ngày.",
        "chapters": [
            {
                "title": "Chương 1: Ta đã làm gì với những năm tháng thanh xuân?",
                "content": """Tuổi trẻ là quãng thời gian rực rỡ nhất của đời người, khi bạn sở hữu ba tài sản quý giá nhất: sức khỏe dồi dào, thời gian thênh thang và một trái tim đầy nhiệt huyết. Thế nhưng, đáng buồn thay, nhiều bạn trẻ lại lãng phí tuổi trẻ vào những cuộc nhậu thâu đêm, những trận game vô bổ hay những giờ lướt mạng xã hội vô định.

Cuộc đời bạn là một tác phẩm nghệ thuật do chính bạn vẽ nên. Bạn không thể đổ lỗi cho hoàn cảnh, cho gia đình hay cho nền giáo dục. Nếu bạn không tự tay thiết kế tương lai của mình, sẽ có người khác thuê bạn xây dựng giấc mơ của họ."""
            },
            {
                "title": "Chương 2: Tự học - Kỹ năng sinh tồn của thế kỷ 21",
                "content": """Trường học chỉ trao cho bạn tấm bằng tốt nghiệp và những kiến thức cơ bản nhất, còn trường đời mới là nơi quyết định bạn là ai. Kỹ năng quan trọng nhất mà bất kỳ người trẻ nào cũng phải thành thạo là kỹ năng tự học.

Tự học bắt đầu từ thói quen đọc sách mỗi ngày. Đọc sách là cách nhanh nhất và rẻ nhất để bạn trò chuyện cùng những bộ óc vĩ đại nhất của nhân loại. Mỗi trang sách mở ra là một chân trời tri thức mới, giúp bạn nâng cao tư duy phản biện, mở rộng thế giới quan và không bị tụt hậu trước sự biến đổi chóng mặt của công nghệ."""
            },
            {
                "title": "Chương 3: Xách ba lô lên và đi để trưởng thành",
                "content": """Du lịch trải nghiệm không đơn thuần là việc đi chụp vài bức ảnh check-in rồi về khoe lên mạng xã hội. Đi là để dấn thân, để bước ra khỏi vùng an toàn chật hẹp, để đối diện với những bất trắc và học cách tự chăm sóc bản thân giữa một vùng đất xa lạ.

Khi bạn đứng trước sự hùng vĩ của núi non hay sự bao la của đại dương, bạn sẽ nhận ra cái tôi của mình nhỏ bé đến nhường nào, từ đó biết sống khiêm nhường, yêu thương đồng loại và trân quý từng khoảnh khắc của thực tại."""
            },
            {
                "title": "Chương 4: Tỏa sáng rực rỡ theo cách của riêng bạn",
                "content": """Mỗi người sinh ra đều mang trong mình một sứ mệnh và một thế mạnh độc nhất vô nhị. Đừng bao giờ so sánh chương một của cuộc đời bạn với chương hai mươi của cuộc đời người khác.

Hãy kiên trì theo đuổi đam mê, không ngừng trau dồi chuyên môn và sống một cuộc đời trung thực với chính mình. Khi bạn nỗ lực hết mình để trở thành phiên bản tốt nhất của bản thân, thành công và hạnh phúc sẽ tự khắc tìm đến gõ cửa."""
            }
        ]
    },
    {
        "slug": "nghi_giau_va_lam_giau",
        "title": "Nghĩ Giàu Và Làm Giàu",
        "author": "Napoleon Hill",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 870,
        "format": "pdf",
        "summary": "13 nguyên tắc vàng tạo dựng của cải và thành công vượt bậc được đúc kết từ cuộc đời của hơn 500 doanh nhân vĩ đại nhất lịch sử nước Mỹ.",
        "narration_text": "Sách nói Nghĩ Giàu Và Làm Giàu của Napoleon Hill. Khát vọng là điểm khởi đầu của mọi thành tựu. Cách đây hơn 30 năm, Edwin C. Barnes đã phát hiện ra một sự thật vĩ đại rằng con người ta hoàn toàn có thể nghĩ giàu và làm giàu. Khát vọng của ông không phải là một điều ước mơ hồ, mà là một khao khát cháy bỏng, sẵn sàng đốt cháy tất cả những cây cầu phía sau để chỉ tiến về phía trước.",
        "chapters": [
            {
                "title": "Chương 1: Sức mạnh của ý nghĩ và Khát vọng cháy bỏng",
                "content": """Ý nghĩ là vật chất, và là thứ vật chất có sức mạnh vô song khi được kết hợp với một mục đích rõ ràng, sự kiên định và một khát vọng cháy bỏng chuyển hóa thành của cải vật chất.

Edwin C. Barnes khi còn là một chàng trai nghèo không một xu dính túi đã khao khát trở thành đối tác kinh doanh của nhà sáng chế vĩ đại Thomas Edison. Ông không muốn làm việc CHO Edison, mà muốn làm việc CÙNG Edison. Bằng sự kiên trì phục vụ suốt nhiều năm từ những công việc nhỏ nhất, cuối cùng ông đã nắm bắt được cơ hội và trở thành nhà phân phối độc quyền máy đọc Edison trên toàn nước Mỹ."""
            },
            {
                "title": "Chương 2: Tự ám thị - Cầu nối đến tiềm thức",
                "content": """Tự ám thị là thuật ngữ chỉ tất cả các hình thức tự kích thích và truyền tải thông điệp qua các giác quan đến tâm trí tiềm thức của bạn. Tiềm thức không phân biệt được suy nghĩ tích cực hay tiêu cực, nó tiếp nhận tất cả mệnh lệnh được nuôi dưỡng bằng cảm xúc mãnh liệt.

Để biến khát vọng giàu có thành hiện thực, bạn phải viết ra số tiền chính xác mình muốn sở hữu, thời hạn đạt được và những gì bạn sẵn sàng đánh đổi. Đọc to bản tuyên ngôn ấy hai lần mỗi ngày vào buổi sáng khi thức dậy và buổi tối trước khi đi ngủ với một niềm tin tuyệt đối."""
            },
            {
                "title": "Chương 3: Nhóm trí tuệ ưu tú và Kế hoạch kiên trì",
                "content": """Không một cá nhân nào có thể tích lũy được khối tài sản khổng lồ nếu chỉ dựa vào sức lực đơn độc của mình. Khái niệm 'Nhóm trí tuệ ưu tú' (Master Mind) là sự phối hợp hài hòa giữa kiến thức và nỗ lực của hai hay nhiều người hướng về một mục đích chung.

Khi hai bộ óc hợp tác cùng nhau, một nguồn năng lượng thứ ba vô hình sẽ được hình thành, kích thích khả năng sáng tạo và giải quyết mọi bài toán hóc búa nhất của thương trường."""
            },
            {
                "title": "Chương 4: Chiến thắng sáu bóng ma sợ hãi",
                "content": """Kẻ thù lớn nhất cản bước con người trên con đường vươn tới vinh quang không phải là sự thiếu hụt vốn liếng, mà là nỗi sợ hãi ẩn sâu trong tâm trí. Có sáu nỗi sợ cơ bản: sợ nghèo khó, sợ bị chỉ trích, sợ ốm đau, sợ mất đi tình yêu, sợ tuổi già và sợ cái chết.

Hãy làm chủ tâm trí mình bằng cách dứt khoát xóa bỏ mọi nghi ngờ và lưỡng lự. Can đảm không phải là không sợ hãi, mà là hành động bất chấp nỗi sợ hãi."""
            }
        ]
    },
    {
        "slug": "kheo_an_noi_se_co_duoc_thien_ha",
        "title": "Khéo Ăn Nói Sẽ Có Được Thiên Hạ",
        "author": "Trác Nhã",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1553729459-efe14ef6055d?q=80&w=600",
        "rating_avg": 4.8,
        "review_count": 760,
        "format": "pdf",
        "summary": "Cẩm nang giao tiếp thực chiến giúp bạn làm chủ lời ăn tiếng nói, chinh phục lòng người trong công việc, tình cảm và cuộc sống hàng ngày.",
        "narration_text": "Sách nói Khéo Ăn Nói Sẽ Có Được Thiên Hạ của tác giả Trác Nhã. Lời nói chẳng mất tiền mua, lựa lời mà nói cho vừa lòng nhau. Giao tiếp là chiếc cầu nối gắn kết con người với thế giới. Người khéo ăn nói không phải là người ba hoa khoác lác, mà là người biết nói đúng lúc, đúng chỗ, đúng người và bằng một thái độ chân thành nhất.",
        "chapters": [
            {
                "title": "Chương 1: Dũng cảm mở lời - Bước đầu tiên để phá vỡ băng giá",
                "content": """Nhiều người bỏ lỡ những cơ hội quý báu trong sự nghiệp chỉ vì sự nhút nhát và sợ sai khi giao tiếp trước đám đông. Nỗi sợ hãi nói chuyện thực chất bắt nguồn từ sự thiếu tự tin và lo lắng thái quá về đánh giá của người khác.

Muốn thành công, bạn phải tập thói quen chủ động cất lời chào hỏi. Một câu mở đầu tự nhiên về thời tiết, một lời khen tinh tế về trang phục của đối phương hay một câu hỏi thăm chân tình có thể ngay lập tức phá vỡ bầu không khí ngột ngạt và mở ra một cuộc trò chuyện thú vị."""
            },
            {
                "title": "Chương 2: Nói chuyện hợp ngữ cảnh và đúng đối tượng",
                "content": """Cổ nhân có câu: 'Nhìn mặt gửi vàng, nhìn người tiếp chuyện'. Đối với người lớn tuổi, cần thể hiện sự lễ phép và tôn trọng kinh nghiệm sống của họ. Đối với đồng nghiệp, cần sự thẳng thắn, hợp tác và tôn trọng lẫn nhau. Đối với cấp dưới, cần sự khích lệ và đồng cảm.

Biết lắng nghe nhiều hơn nói là đỉnh cao của nghệ thuật giao tiếp. Người thông minh luôn dành 70% thời gian để lắng nghe và chỉ 30% thời gian để đưa ra những phản hồi đắt giá."""
            },
            {
                "title": "Chương 3: Nghệ thuật từ chối khéo léo không làm mất lòng",
                "content": """Biết nói 'Không' đúng lúc là một năng lực sống còn để bảo vệ thời gian và năng lượng của chính mình. Tuy nhiên, từ chối thẳng thừng có thể làm tổn thương mối quan hệ.

Hãy áp dụng kỹ thuật 'Đồng cảm trước - Từ chối sau': trước tiên hãy công nhận thiện chí của đối phương, sau đó đưa ra lý do khách quan một cách chân thành và nếu có thể, hãy đề xuất một giải pháp thay thế hợp lý."""
            }
        ]
    },
    {
        "slug": "quang_ganh_lo_di_va_vui_song",
        "title": "Quẳng Gánh Lo Đi Và Vui Sống",
        "author": "Dale Carnegie",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 810,
        "format": "pdf",
        "summary": "Phương thuốc kỳ diệu giúp bạn đập tan nỗi lo âu, giải tỏa căng thẳng thần kinh và tận hưởng trọn vẹn từng ngày an vui của cuộc sống.",
        "narration_text": "Sách nói Quẳng Gánh Lo Đi Và Vui Sống của Dale Carnegie. Lo lắng giống như một chiếc ghế bập bênh: nó cho bạn việc gì đó để làm nhưng chẳng đưa bạn đến đâu cả. Hãy sống trong những ngăn kín của từng ngày một. Đừng nhìn về quá khứ với sự nuối tiếc, cũng đừng lo sợ tương lai với những điều chưa xảy ra. Hạnh phúc đích thực chỉ hiện diện trong giây phút hiện tại này mà thôi.",
        "chapters": [
            {
                "title": "Chương 1: Sống trong từng ngăn kín của thời gian",
                "content": """Bác sĩ William Osler - một trong những người sáng lập Bệnh viện danh tiếng Johns Hopkins - đã chia sẻ bí quyết sống an vui của mình: 'Hãy đóng chặt các cánh cửa ngăn cách quá khứ đã qua và tương lai chưa tới. Hãy sống trọn vẹn trong khoang kín của ngày hôm nay'.

Mỗi ngày mới là một cuộc đời thu nhỏ. Việc lo lắng cho gánh nặng của ngày mai cộng dồn với sự hối tiếc của ngày hôm qua chỉ khiến chúng ta kiệt quệ và sụp đổ ngay trong ngày hôm nay."""
            },
            {
                "title": "Chương 2: Công thức thần kỳ giải quyết nỗi lo của Willis Carrier",
                "content": """Kỹ sư Willis Carrier đã phát minh ra một công thức ba bước đơn giản nhưng vô cùng hiệu quả để đối phó với những tình huống tồi tệ nhất:
Bước 1: Tự hỏi bản thân điều tồi tệ nhất có thể xảy ra trong chuyện này là gì?
Bước 2: Chuẩn bị tinh thần sẵn sàng chấp nhận điều tồi tệ nhất đó nếu nó xảy ra.
Bước 3: Bình tĩnh tìm mọi cách để cải thiện tình hình từ điểm đáy tồi tệ đó."""
            },
            {
                "title": "Chương 3: Quy luật bình quân và xóa bỏ lo âu vô cớ",
                "content": """Hầu hết những điều chúng ta lo lắng suốt cả cuộc đời đều chưa bao giờ xảy ra trong thực tế. Nhà tâm lý học William James từng chỉ ra rằng tâm trí con người có xu hướng phóng đại nguy cơ vượt xa quy luật xác suất bình quân.

Hãy nhìn thẳng vào thực tế, kiểm tra số liệu khách quan và tự hỏi: 'Theo quy luật bình quân, khả năng sự việc này xảy ra là bao nhiêu phần trăm?'. Bạn sẽ thấy phần lớn nỗi sợ đều tự tan biến như bong bóng xà phòng."""
            }
        ]
    },
    {
        "slug": "doc_vi_bat_ky_ai",
        "title": "Đọc Vị Bất Kỳ Ai",
        "author": "David J. Lieberman",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=600",
        "rating_avg": 4.8,
        "review_count": 640,
        "format": "pdf",
        "summary": "Khoa học giải mã ngôn ngữ cơ thể, tâm lý học hành vi giúp bạn thấu hiểu suy nghĩ và động cơ thật sự của người đối diện trong nháy mắt.",
        "narration_text": "Sách nói Đọc Vị Bất Kỳ Ai của Tiến sĩ David Lieberman. Con người có thể nói dối bằng lời nói, nhưng cơ thể của họ thì không bao giờ biết nói dối. Từ ánh mắt né tránh, đôi vai co rúm đến giọng điệu run rẩy, mọi chuyển động vi mô đều hé lộ sự thật ẩn giấu trong tiềm thức. Nắm vững nghệ thuật đọc vị sẽ giúp bạn tự tin làm chủ mọi cuộc đàm phán và giao tiếp xã hội.",
        "chapters": [
            {
                "title": "Chương 1: Giải mã ngôn ngữ cơ thể và dấu hiệu nói dối",
                "content": """Khi một người nói dối, não bộ của họ phải hoạt động với cường độ cao gấp đôi so với khi nói sự thật: họ vừa phải bịa ra câu chuyện hư cấu, vừa phải ghi nhớ các tình tiết và vừa phải kiểm soát hành vi để không bị phát giác.

Các dấu hiệu nhận biết kẻ nói dối bao gồm: chớp mắt liên tục, lấy tay chạm vào mũi hoặc che miệng, chân hướng về phía cửa thoát hiểm và giọng nói có xu hướng cao vút bất thường. Hãy chú ý đến sự bất tương xứng giữa lời nói và cử chỉ nét mặt."""
            },
            {
                "title": "Chương 2: Nhận biết mức độ tự tin và cảm xúc thật",
                "content": """Người tự tin thực sự luôn có dáng đi đĩnh đạc, lưng thẳng, hai bàn tay mở rộng và tiếp xúc ánh mắt tự nhiên với người đối diện. Ngược lại, người mang tâm lý bất an thường có xu hướng khoanh tay trước ngực như một bức tường tự vệ vô hình hoặc liên tục mân mê các đồ vật như nhẫn, bút, đồng hồ."""
            },
            {
                "title": "Chương 3: Đọc vị động cơ trong đàm phán và kinh doanh",
                "content": """Trong một cuộc đàm phán thương mại, ai là người sốt ruột chốt hợp đồng thì người đó nắm thế hạ phong. Bằng cách đặt những câu hỏi mở bất ngờ và quan sát phản ứng chậm trễ của đối tác, bạn có thể dễ dàng đoán biết được mức giá đáy thực sự mà họ có thể chấp nhận."""
            }
        ]
    },
    # ---------------- 3. KINH DOANH & TÀI CHÍNH CÁ NHÂN ----------------
    {
        "slug": "day_con_lam_giau_1",
        "title": "Dạy Con Làm Giàu (Tập 1)",
        "author": "Robert T. Kiyosaki",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1553729459-efe14ef6055d?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 1120,
        "format": "pdf",
        "summary": "Cuốn sách thay đổi tư duy tài chính của hàng chục triệu người trên thế giới: Người giàu không làm việc vì tiền mà bắt tiền bạc phải làm việc cho mình.",
        "narration_text": "Sách nói Dạy Con Làm Giàu Tập 1 của tác giả Robert Kiyosaki. Tôi có hai người cha: một người cha giàu và một người cha nghèo. Người cha nghèo có học vị tiến sĩ nhưng luôn gặp rắc rối về tiền bạc. Người cha giàu chưa học hết lớp tám nhưng lại trở thành một trong những người giàu có nhất bang Hawaii. Sự khác biệt lớn nhất giữa họ không phải là kiếm được bao nhiêu tiền, mà là cách họ tư duy về đồng tiền và tài sản.",
        "chapters": [
            {
                "title": "Chương 1: Người giàu không làm việc vì tiền",
                "content": """Đa số mọi người bị mắc kẹt trong vòng luẩn quẩn mà tôi gọi là 'Rat Race' (vòng quay chuột chạy): đi học lấy điểm cao, kiếm một công việc ổn định, nhận lương, trả tiền hóa đơn, rồi lại đi làm cật lực vì nỗi sợ thiếu thốn và lòng tham lam những thứ xa xỉ.

Người cha giàu dạy tôi bài học đầu tiên: 'Nếu con làm việc vì tiền, con sẽ bị đồng tiền làm chủ suốt đời. Người giàu không làm việc vì tiền, người giàu bắt tiền bạc phải làm việc chăm chỉ phục vụ cho mình'."""
            },
            {
                "title": "Chương 2: Phân biệt rõ Tài sản và Tiêu sản",
                "content": """Quy tắc tài chính quan trọng nhất trên đời vô cùng đơn giản: Bạn phải biết sự khác biệt giữa Tài sản và Tiêu sản, và chỉ mua Tài sản mà thôi.
- Tài sản là những thứ đưa tiền vào túi của bạn (bất động sản cho thuê, cổ phiếu sinh lời, bản quyền tác giả).
- Tiêu sản là những thứ rút tiền ra khỏi túi của bạn (xe hơi trả góp, nhà ở chịu lãi vay lớn, đồ hiệu xa xỉ).

Người nghèo chỉ có chi phí; người trung lưu mua tiêu sản mà cứ ngỡ là tài sản; chỉ có người giàu mới kiên trì xây dựng cột tài sản sinh lời."""
            },
            {
                "title": "Chương 3: Tập trung vào công việc kinh doanh của chính bạn",
                "content": """Nghề nghiệp chuyên môn của bạn là thứ giúp bạn trang trải cuộc sống hiện tại, nhưng công việc kinh doanh cột tài sản mới là thứ đem lại cho bạn sự tự do tài chính bền vững.

Hãy giữ vững công việc hàng ngày của bạn, nhưng hãy sống tiết kiệm và dùng số tiền dư thừa ấy để đầu tư vào những tài sản sinh lời thực thụ thay vì chi tiêu phung phí."""
            },
            {
                "title": "Chương 4: Trí thông minh tài chính - Sức mạnh của sự hiểu biết",
                "content": """Trí thông minh tài chính được cấu thành từ bốn trụ cột chính:
1. Kế toán: Khả năng đọc hiểu các con số và báo cáo tài chính.
2. Đầu tư: Khoa học về việc bắt tiền sinh ra tiền.
3. Hiểu biết thị trường: Khoa học về cung và cầu.
4. Luật pháp: Tận dụng các lợi thế về thuế và công ty để bảo vệ tài sản."""
            }
        ]
    },
    {
        "slug": "day_con_lam_giau_2",
        "title": "Dạy Con Làm Giàu (Tập 2: Kim Tứ Đồ)",
        "author": "Robert T. Kiyosaki",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 890,
        "format": "pdf",
        "summary": "Mô hình Kim Tứ Đồ kinh điển phân loại 4 nhóm người tạo ra thu nhập và lộ trình chuyển đổi từ người làm công sang chủ doanh nghiệp và nhà đầu tư chuyên nghiệp.",
        "narration_text": "Sách nói Dạy Con Làm Giàu Tập 2 của Robert Kiyosaki. Kim Tứ Đồ chia thế giới kiếm tiền thành bốn góc: Nhóm L - Người làm công; Nhóm T - Người làm tư; Nhóm C - Chủ doanh nghiệp có hệ thống; và Nhóm Đ - Nhà đầu tư. Để đạt được tự do tài chính thực sự, bạn phải học cách bước qua nửa bên phải của Kim Tứ Đồ.",
        "chapters": [
            {
                "title": "Chương 1: Bốn góc của Kim Tứ Đồ",
                "content": """Kim Tứ Đồ mô tả bốn cách khác nhau để tạo ra dòng tiền trong xã hội:
- Nhóm L (Làm công): Đổi thời gian và sức lao động lấy tiền lương cố định.
- Nhóm T (Tự làm chủ): Bạn sở hữu một công việc, nhưng nếu bạn nghỉ làm thì thu nhập cũng dừng lại.
- Nhóm C (Chủ doanh nghiệp): Bạn sở hữu một hệ thống vận hành tự động và có những con người tài giỏi làm việc cho bạn.
- Nhóm Đ (Đầu tư): Tiền bạc tự sinh sôi nảy nở ra tiền mà không cần bạn phải can thiệp trực tiếp."""
            },
            {
                "title": "Chương 2: Tư duy khác biệt giữa bên trái và bên phải",
                "content": """Người ở bên trái Kim Tứ Đồ luôn tìm kiếm sự an toàn và ổn định, nhưng thực chất họ lại là nhóm người chịu nhiều rủi ro nhất khi nền kinh tế suy thoái và phải đóng thuế cao nhất.

Người ở bên phải tìm kiếm sự tự do. Họ sẵn sàng đối mặt với rủi ro có tính toán, xây dựng quy trình kinh doanh và tận dụng đòn bẩy tài chính để nhân rộng quy mô."""
            },
            {
                "title": "Chương 3: Bảy cấp độ đầu tư tài chính",
                "content": """Từ cấp độ 0 (những người không có tiền để đầu tư) đến cấp độ 6 (nhà đầu tư thực sự), mỗi bậc thang đòi hỏi sự nâng cao về kiến thức, khả năng quản trị cảm xúc và tầm nhìn chiến lược. Nhà đầu tư thực sự tạo ra cơ hội đầu tư chứ không chỉ chờ đợi người khác mang cơ hội đến."""
            }
        ]
    },
    {
        "slug": "khoi_nghiep_tinh_gon",
        "title": "Khởi Nghiệp Tinh Gọn",
        "author": "Eric Ries",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=600",
        "rating_avg": 4.8,
        "review_count": 580,
        "format": "pdf",
        "summary": "Phương pháp luận khởi nghiệp cách mạng thung lũng Silicon: Xây dựng - Đo lường - Học hỏi giúp doanh nghiệp đổi mới sáng tạo nhanh chóng mà không lãng phí nguồn lực.",
        "narration_text": "Sách nói Khởi Nghiệp Tinh Gọn của Eric Ries. Hầu hết các công ty khởi nghiệp thất bại không phải vì sản phẩm của họ dở, mà vì họ đã dành quá nhiều thời gian và tiền bạc để xây dựng một thứ mà không một khách hàng nào thực sự cần. Tinh thần tinh gọn dạy chúng ta cách thử nghiệm giả thuyết nhanh nhất với sản phẩm khả dụng tối thiểu MVP.",
        "chapters": [
            {
                "title": "Chương 1: Bản chất của Khởi nghiệp trong điều kiện bất định",
                "content": """Khởi nghiệp là một thể chế con người được lập ra nhằm tạo ra sản phẩm hoặc dịch vụ mới trong điều kiện hoàn toàn bất định cực đoan. Lập kế hoạch kinh doanh truyền thống dài hạn hoàn toàn vô dụng trước những thị trường chưa từng tồn tại."""
            },
            {
                "title": "Chương 2: Vòng phản hồi Xây dựng - Đo lường - Học hỏi",
                "content": """Trái tim của phương pháp tinh gọn là vòng lặp ba bước: Biến ý tưởng thành Sản phẩm khả dụng tối thiểu (MVP), Đo lường phản hồi thực tế của khách hàng bằng dữ liệu định lượng, và Học hỏi được kiểm chứng để quyết định tiếp tục kiên trì hay xoay trục chiến lược."""
            },
            {
                "title": "Chương 3: Nghệ thuật xoay trục (Pivot)",
                "content": """Xoay trục là sự điều chỉnh chiến lược có cấu trúc nhằm kiểm tra một giả thuyết cơ bản mới về sản phẩm, mô hình kinh doanh hoặc động cơ tăng trưởng mà không làm thay đổi tầm nhìn cốt lõi của công ty."""
            }
        ]
    },
    {
        "slug": "nha_dau_tu_thong_minh",
        "title": "Nhà Đầu Tư Thông Minh",
        "author": "Benjamin Graham",
        "category": "Kinh doanh & Phát triển",
        "image_url": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 920,
        "format": "pdf",
        "summary": "Kinh thánh của phương pháp đầu tư giá trị, cuốn sách gối đầu giường được tỷ phú Warren Buffett ca ngợi là tác phẩm hay nhất về đầu tư từng được viết.",
        "narration_text": "Sách nói Nhà Đầu Tư Thông Minh của Benjamin Graham. Hoạt động đầu tư là một hoạt động mà qua phân tích kỹ lưỡng, hứa hẹn sự an toàn của vốn gốc và một mức sinh lời thỏa đáng. Hãy coi cổ phiếu là một phần sở hữu của doanh nghiệp thực thụ, và luôn ghi nhớ nguyên tắc tối thượng: Biên độ an toàn.",
        "chapters": [
            {
                "title": "Chương 1: Phân biệt Đầu tư và Đầu cơ",
                "content": """Đầu tư thực thụ đòi hỏi sự phân tích chuyên sâu về giá trị nội tại của doanh nghiệp, khả năng bảo toàn vốn gốc và mức sinh lời hợp lý. Đầu cơ là hành vi đánh cược vào sự biến động giá ngắn hạn của thị trường dựa trên tâm lý bầy đàn."""
            },
            {
                "title": "Chương 2: Quý ngài Thị Trường (Mr. Market)",
                "content": """Hãy tưởng tượng thị trường chứng khoán như một người đối tác kinh doanh kỳ quặc tên là Quý ngài Thị Trường. Mỗi ngày ông ta gõ cửa đưa ra một mức giá để mua lại cổ phần của bạn hoặc bán thêm cổ phần cho bạn. Đừng bao giờ để sự thất thường của ông ta chi phối lý trí của bạn."""
            },
            {
                "title": "Chương 3: Nguyên tắc Biên độ An toàn (Margin of Safety)",
                "content": """Bí quyết đầu tư thành công nằm gọn trong bốn chữ: Biên độ an toàn. Chỉ mua một tài sản khi giá thị trường của nó thấp hơn đáng kể so với giá trị nội tại được định giá thận trọng."""
            }
        ]
    },
    # ---------------- 4. TÂM LÝ, TRIẾT HỌC & CHỮA LÀNH TÂM HỒN ----------------
    {
        "slug": "hieu_ve_trai_tim",
        "title": "Hiểu Về Trái Tim",
        "author": "Thầy Thích Minh Niệm",
        "category": "Tâm lý & Xã hội",
        "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=600",
        "rating_avg": 5.0,
        "review_count": 1420,
        "format": "pdf",
        "summary": "Tác phẩm tâm lý trị liệu sâu sắc của thiền sư Minh Niệm, giúp người đọc thấu suốt bản chất của khổ đau, chữa lành những vết thương tâm hồn và tìm về an lạc nội tại.",
        "narration_text": "Sách nói Hiểu Về Trái Tim của Thầy Thích Minh Niệm. Khổ đau là một thực tại tất yếu của cuộc đời. Nhưng nếu không có khổ đau thì ta sẽ không bao giờ cảm nhận được vị ngọt ngào của hạnh phúc. Hãy quay về chăm sóc và ôm ấp trái tim mình bằng sự hiểu biết và lòng từ bi. Khi tâm ta bình yên, thế giới xung quanh cũng sẽ tự khắc trở nên dịu dàng.",
        "chapters": [
            {
                "title": "Chương 1: Khổ đau & Nghệ thuật chuyển hóa",
                "content": """Khổ đau không phải là kẻ thù, mà là một phần tự nhiên của đời sống. Chúng ta đau khổ không phải vì nghịch cảnh bên ngoài quá lớn, mà vì tâm ta đang chống cự lại thực tại và đòi hỏi mọi thứ phải diễn ra theo ý muốn ích kỷ của mình.

Hãy học cách đối diện với nỗi đau như một người mẹ ôm đứa con thơ đang khóc. Đừng xua đuổi, đừng trốn tránh. Nhìn sâu vào bản chất của nỗi đau bằng sự tĩnh lặng, bạn sẽ thấy nó chính là chất liệu quý giá tôi luyện nên sự kiên cường và lòng trắc ẩn."""
            },
            {
                "title": "Chương 2: Tình yêu chân thật - Từ, Bi, Hỷ, Xả",
                "content": """Yêu thương mà không hiểu biết thì chỉ đem lại sự trói buộc và làm tổn thương lẫn nhau. Tình yêu đích thực trong đạo Phật phải hội tụ đủ bốn yếu tố:
- Từ: Khả năng đem lại niềm vui và bình an cho người mình yêu.
- Bi: Khả năng chia sẻ và làm vơi đi nỗi khổ niềm đau của họ.
- Hỷ: Niềm vui thanh thoát khi thấy người kia hạnh phúc.
- Xả: Sự bao dung, không chiếm hữu và tôn trọng tự do của nhau."""
            },
            {
                "title": "Chương 3: Tha thứ để giải phóng tâm hồn",
                "content": """Ôm giữ lòng oán hận cũng giống như việc bạn uống thuốc độc mà lại mong người khác chết. Kẻ thù lớn nhất cướp đi bình yên của bạn chính là sự cố chấp trong tâm trí.

Tha thứ không phải là dung túng cho cái ác, mà là hành động dũng cảm giải phóng chính mình khỏi gông cùm của quá khứ để bước tiếp nhẹ nhàng trong hiện tại."""
            },
            {
                "title": "Chương 4: Bình yên giữa dòng đời biến động",
                "content": """Bình yên không phải là một nơi chốn không có tiếng ồn ào hay không có sóng gió. Bình yên là khi ta đứng giữa muôn trùng bão táp mà tâm trí vẫn lắng đọng như mặt hồ mùa thu. Trở về với hơi thở chánh niệm, nhận biết giây phút hiện tại chính là chìa khóa mở cánh cửa thiên đường nơi trần thế."""
            }
        ]
    },
    {
        "slug": "muon_kiep_nhan_sinh",
        "title": "Muôn Kiếp Nhân Sinh",
        "author": "Nguyên Phong",
        "category": "Triết học & Tư tưởng",
        "image_url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 1350,
        "format": "epub",
        "summary": "Bức tranh toàn cảnh kỳ vĩ về quy luật nhân quả, luân hồi và những bài học thức tỉnh tâm linh sâu sắc cho nhân loại trước những biến động thời đại.",
        "narration_text": "Sách nói Muôn Kiếp Nhân Sinh của tác giả Nguyên Phong. Nhân quả đừng đợi đến kiếp sau mới thấy, nó đang vận hành từng giây từng phút trong đời sống này. Những suy nghĩ, lời nói và hành động của bạn hôm nay chính là hạt mầm kiến tạo nên số phận của bạn trong tương lai. Chỉ có tình thương yêu vô điều kiện và sự thức tỉnh lương tri mới cứu vãn được nhân loại trước bờ vực tự hủy diệt.",
        "chapters": [
            {
                "title": "Chương 1: Cuộc hội ngộ kỳ bí tại Đài Bắc",
                "content": """Tại một tu viện thanh tịnh trên đỉnh núi mờ sương ở Đài Bắc, tác giả Nguyên Phong đã có cuộc gặp gỡ định mệnh với ông Thomas - một doanh nhân tài chính Phố Wall quyền lực.

Ông Thomas bắt đầu trải lòng về những ký ức tiền kiếp kỳ lạ của mình thông qua thuật thôi miên hồi quy. Những ký ức ấy trải dài qua hàng ngàn năm, từ nền văn minh rực rỡ đã chìm sâu dưới đáy đại dương Atlantis cho đến những kim tự tháp huyền bí của Ai Cập cổ đại."""
            },
            {
                "title": "Chương 2: Nền văn minh Atlantis và sự hủy diệt bởi lòng tham",
                "content": """Atlantis từng là một nền văn minh siêu việt với công nghệ năng lượng tinh thể vượt xa thế giới hiện đại ngày nay. Thế nhưng, bi kịch xảy ra khi sự phát triển của khoa học công nghệ không đi đôi với sự trưởng thành về đạo đức và tâm linh.

Lòng tham quyền lực, sự ngạo mạn muốn thay thế đấng sáng tạo và thói dâm ô trụy lạc đã dẫn đến thảm họa đại hồng thủy vùi lấp toàn bộ lục địa Atlantis xuống đáy biển sâu trong một đêm kinh hoàng."""
            },
            {
                "title": "Chương 3: Đền đài Ai Cập và Luật Nhân Quả",
                "content": """Tái sinh vào thời kỳ Ai Cập cổ đại, linh hồn Thomas lại tiếp tục bài học về nghiệp báo giữa quyền lực tôn giáo và luân hồi. Quy luật Nhân Quả vận hành vô cùng chính xác và công bằng: Gieo nhân nào gặt quả nấy, không một ai có thể trốn tránh được món nợ nghiệp lực của chính mình."""
            },
            {
                "title": "Chương 4: Thức tỉnh tâm linh - Con đường cứu rỗi",
                "content": """Thế giới hôm nay đang đứng trước những hiểm họa khôn lường về dịch bệnh, thiên tai và chiến tranh do chính lòng tham của con người gây ra. Lối thoát duy nhất cho nhân loại là sự chuyển hóa từ bên trong: phát khởi tình thương yêu đồng loại, sống hài hòa với mẹ thiên nhiên và thức tỉnh trách nhiệm của từng cá nhân."""
            }
        ]
    },
    {
        "slug": "hanh_trinh_ve_phuong_dong",
        "title": "Hành Trình Về Phương Đông",
        "author": "Baird T. Spalding (Nguyên Phong dịch)",
        "category": "Triết học & Tư tưởng",
        "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 980,
        "format": "pdf",
        "summary": "Cuộc thám hiểm kỳ vĩ của phái đoàn khoa học Hoàng gia Anh tại rặng núi Himalaya, khám phá những chân lý minh triết cổ xưa của phương Đông.",
        "narration_text": "Sách nói Hành Trình Về Phương Đông do dịch giả Nguyên Phong phóng tác. Cuối thế kỷ 19, một đoàn khoa học gồm các giáo sư hàng đầu nước Anh lên đường sang Ấn Độ để nghiên cứu về khí công và các hiện tượng siêu nhiên. Cuộc hành trình đã mở ra trước mắt họ một thế giới tâm linh sâu sắc, nơi khoa học thực nghiệm bắt tay cùng triết học cổ đại.",
        "chapters": [
            {
                "title": "Chương 1: Một người Ấn Độ kỳ lạ",
                "content": """Phái đoàn khoa học Anh đến thành phố thần thánh Benares bên bờ sông Hằng với thái độ hoài nghi và kiêu hãnh của những trí thức phương Tây. Tại đây, họ gặp gỡ những đạo sĩ yoga chân chính có khả năng làm chủ hơi thở, kiểm soát nhịp tim và kết nối với các tầng năng lượng vũ trụ."""
            },
            {
                "title": "Chương 2: Người chết sống lại và Khoa học Yoga",
                "content": """Yoga không đơn thuần là những động tác uốn dẻo thể xác, mà là một hệ thống triết học khoa học nghiêm ngặt nhằm thanh lọc tâm trí và hợp nhất tiểu vũ trụ con người với đại vũ trụ bao la."""
            },
            {
                "title": "Chương 3: Chân lý vĩnh hằng trên đỉnh tuyết sơn",
                "content": """Tiến sâu vào rặng núi tuyết Himalaya hùng vĩ, đoàn thám hiểm được diện kiến các bậc Chân sư đắc đạo. Họ nhận ra rằng hạnh phúc đích thực không nằm ở việc sở hữu vật chất bên ngoài, mà nằm ở sự thức tỉnh giác ngộ từ bên trong."""
            }
        ]
    },
    {
        "slug": "nha_gia_kim",
        "title": "Nhà Giả Kim",
        "author": "Paulo Coelho",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1512820790803-83ca734da794?q=80&w=600",
        "rating_avg": 5.0,
        "review_count": 1680,
        "format": "epub",
        "summary": "Kiệt tác ngụ ngôn thần thoại về hành trình theo đuổi vận mệnh riêng của chàng chăn cừu Santiago, khẳng định khi bạn thực sự mong muốn điều gì thì cả vũ trụ sẽ hiệp lực giúp bạn.",
        "narration_text": "Sách nói Nhà Giả Kim của nhà văn Paulo Coelho. Bản dịch tiếng Việt chuẩn. Chàng trai tên là Santiago. Trời vừa chập tối khi chàng tới một nhà thờ cổ đổ nát gần rặng núi Andalusia. Chàng ngả lưng cùng đàn cừu và chìm vào giấc mơ: một đứa trẻ dẫn chàng tới chân Kim Tự Tháp Ai Cập và bảo rằng nơi đó có kho báu vĩ đại đang chờ chàng. Hãy lắng nghe tiếng gọi của trái tim và dũng cảm đi tìm Vận Mệnh Riêng của chính mình.",
        "chapters": [
            {
                "title": "Chương 1: Giấc mơ của chàng chăn cừu Santiago",
                "content": """Chàng trai tên là Santiago. Trời vừa chập tối khi chàng đến một nhà thờ cổ đổ nát. Mái nhà thờ đã sập từ lâu, và một cây sung lớn đã mọc lên ngay tại nơi từng là phòng thánh. Chàng ngả lưng ngủ cùng đàn cừu dưới bầu trời ngàn sao rực rỡ.

Đêm đó, Santiago lại lặp lại giấc mơ kỳ lạ: một đứa trẻ nắm tay chàng dẫn tới chân Kim Tự Tháp Ai Cập hùng vĩ và bảo rằng tại đó có một kho báu bí mật đang chờ chàng khai quật. Thức giấc, chàng băn khoăn tự hỏi liệu mình nên tiếp tục cuộc sống an nhàn của một kẻ chăn cừu hay dấn thân vào một cuộc phiêu lưu vô định."""
            },
            {
                "title": "Chương 2: Cuộc gặp với Vua xứ Salem và dấu hiệu vũ trụ",
                "content": """Tại quảng trường thị trấn Tarifa, Santiago gặp gỡ ông lão Melchizedek - vua xứ Salem. Ông nói với chàng về điều dối trá lớn nhất trần gian: rằng vào một thời điểm nào đó, chúng ta không còn làm chủ được cuộc đời mình nữa và số phận sẽ quyết định tất cả.

Ông dạy chàng về Vận Mệnh Riêng: 'Bất kể bạn là ai và bạn làm gì, khi bạn thực sự mong muốn một điều gì đó, thì toàn bộ vũ trụ sẽ hiệp lực để giúp bạn đạt được điều đó'. Chàng quyết định bán đàn cừu, vượt eo biển Gibraltar tiến vào lục địa châu Phi mênh mông."""
            },
            {
                "title": "Chương 3: Băng qua sa mạc Sahara và tìm thấy tình yêu",
                "content": """Sau một năm làm việc chăm chỉ tại cửa hàng pha lê ở Tangier, Santiago cùng đoàn lữ hành tiến sâu vào sa mạc Sahara bão cát. Tại ốc đảo Al-Fayoum rợp bóng chà là, chàng tình cờ gặp nàng Fatima bên giếng nước.

Đó là tiếng sét ái tình kỳ diệu, thứ ngôn ngữ duy nhất mà cả vũ trụ đều hiểu mà không cần phiên dịch. Fatima bảo chàng: 'Em là một người phụ nữ sa mạc. Em tự hào vì sa mạc đã đưa anh đến với em, và em muốn anh tiếp tục đi tìm kho báu của đời mình. Tình yêu chân chính không bao giờ cản bước con người theo đuổi ước mơ'."""
            },
            {
                "title": "Chương 4: Bài học biến thành gió và kho báu dưới gốc cây sung",
                "content": """Đồng hành cùng Nhà Giả Kim thông thái qua những vùng chiến tranh giữa các bộ tộc sa mạc, Santiago học cách lắng nghe trái tim mình và thấu hiểu Tâm Linh Vũ Trụ. Bằng niềm tin tuyệt đối, chàng đã trò chuyện cùng sa mạc, cùng gió và mặt trời để tạo nên một cơn lốc xoáy thần kỳ.

Đến được chân Kim Tự Tháp, chàng đào đất tìm kiếm nhưng bị một nhóm cướp sa mạc bắt giữ đánh đập tàn nhẫn. Tên tướng cướp cười khẩy bảo: 'Đừng có ngu ngốc tin vào giấc mơ! Hai năm trước tao cũng mơ thấy có kho báu chôn dưới gốc cây sung trong một nhà thờ cổ ở Tây Ban Nha!'.

Santiago mỉm cười gượng dậy trong gió cát. Kho báu vĩ đại hóa ra vẫn nằm ngay tại nơi chàng đã khởi hành. Cuộc hành trình vạn dặm ấy không hề uổng phí, bởi chính nó đã tôi luyện chàng thành một con người giác ngộ trọn vẹn."""
            }
        ]
    },
    {
        "slug": "buoc_cham_lai_giua_the_gian_voi_va",
        "title": "Bước Chậm Lại Giữa Thế Gian Vội Vã",
        "author": "Đại đức Haemin",
        "category": "Tâm lý & Xã hội",
        "image_url": "https://images.unsplash.com/photo-1509021436665-8f07dbf5bf1d?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 890,
        "format": "pdf",
        "summary": "Những tản văn chữa lành nhẹ nhàng và sâu lắng của Đại đức Haemin, giúp tâm hồn tìm lại sự tĩnh lặng giữa guồng quay hối hả của đời sống hiện đại.",
        "narration_text": "Sách nói Bước Chậm Lại Giữa Thế Gian Vội Vã của Đại đức Haemin. Khi bạn thấy cả thế giới xung quanh mình đang quay cuồng hối hả, hãy tự hỏi: Là do thế giới bận rộn hay chính tâm trí bạn đang bận rộn? Hãy dừng lại một nhịp, hít thở thật sâu và nhìn ngắm bầu trời trong xanh. Bình an vốn dĩ bắt đầu từ sự buông bỏ những muộn phiền không đáng có.",
        "chapters": [
            {
                "title": "Chương 1: Nghỉ ngơi - Khi bạn thấy thế giới quá vội vàng",
                "content": """Chúng ta thường nhầm lẫn giữa sự bận rộn và hiệu quả. Nhiều người lao vào công việc như những cỗ máy không biết mệt mỏi chỉ để lấp đầy khoảng trống cô đơn trong lòng.

Nghỉ ngơi không phải là lười biếng, mà là hành động cần thiết để tái tạo năng lượng sống. Khi bạn biết dừng lại đúng lúc, tâm trí bạn sẽ lấy lại sự sáng suốt để đưa ra những quyết định đúng đắn."""
            },
            {
                "title": "Chương 2: Mối quan hệ - Khoảng cách vừa đủ cho tình yêu",
                "content": """Các mối quan hệ giống như một đống lửa sưởi ấm trong đêm đông: nếu đứng quá xa bạn sẽ bị lạnh, nhưng nếu bước lại quá gần bạn sẽ bị bỏng. Hãy giữ một khoảng cách vừa vặn đầy tôn trọng để cả hai cùng cảm thấy thoải mái và tự do."""
            },
            {
                "title": "Chương 3: Tương lai - Đừng lo lắng cho những điều chưa tới",
                "content": """Tương lai chỉ là hệ quả của những gì bạn làm trong ngày hôm nay. Thay vì lo sợ về những biến cố chưa xảy ra, hãy tập trung làm thật tốt công việc hiện tại và đối xử tử tế với những người đang ở bên cạnh bạn."""
            }
        ]
    },
    # ---------------- 5. LỊCH SỬ, THIẾU NHI & VĂN HÓA VIỆT NAM ----------------
    {
        "slug": "viet_nam_su_luoc",
        "title": "Việt Nam Sử Lược",
        "author": "Trần Trọng Kim",
        "category": "Lịch sử & Tiểu sử",
        "image_url": "https://images.unsplash.com/photo-1461360370896-922624d12aa1?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 780,
        "format": "pdf",
        "summary": "Bộ thông sử đầu tiên viết bằng chữ quốc ngữ, tái hiện hào khí bốn ngàn năm dựng nước và giữ nước oanh liệt của dân tộc Việt Nam.",
        "narration_text": "Sách nói Việt Nam Sử Lược của học giả Trần Trọng Kim. Dân tộc Việt Nam ta có truyền thống ngàn năm văn hiến, từ thời các vua Hùng dựng nước Văn Lang cho đến những chiến công hiển hách đánh đuổi giặc ngoại xâm của Hai Bà Trưng, Ngô Quyền, Lý Thường Kiệt, Trần Hưng Đạo và vua Quang Trung. Lịch sử là cội nguồn sức mạnh và niềm tự hào thiêng liêng của mỗi người con đất Việt.",
        "chapters": [
            {
                "title": "Chương 1: Thời đại Hồng Bàng và nguồn gốc Rồng Tiên",
                "content": """Tổ tiên nước ta từ thuở khai thiên lập địa đã quần cư bên bờ sông Hồng trù phú. Vua Kinh Dương Vương sinh ra Lạc Long Quân. Lạc Long Quân kết duyên cùng nàng Âu Cơ sinh ra bọc trăm trứng, nở thành trăm người con - khởi nguồn của nòi giống Tiên Rồng.

Năm mươi người con theo cha xuống biển, năm mươi người con theo mẹ lên núi, cùng nhau khai hoang mở cõi lập nên nước Văn Lang với mười tám đời vua Hùng truyền nối."""
            },
            {
                "title": "Chương 2: Chiến thắng Bạch Đằng giang năm 938",
                "content": """Mùa đông năm 938, tướng quân Ngô Quyền lãnh đạo nhân dân đánh tan quân Nam Hán xâm lược trên sông Bạch Đằng. Bằng mưu trí cắm cọc nhọn bịt sắt dưới lòng sông nhân lúc thủy triều lên rồi nhử địch vào bẫy, Ngô Quyền đã chôn vùi toàn bộ hạm đội giặc, chấm dứt hơn một ngàn năm Bắc thuộc tăm tối, mở ra kỷ nguyên độc lập tự chủ lâu dài cho dân tộc."""
            },
            {
                "title": "Chương 3: Hào khí Đông A ba lần đại thắng quân Nguyên Mông",
                "content": """Dưới triều đại nhà Trần, trước vó ngựa hung hãn của đế chế Mông Cổ từng san bằng lục địa Á - Âu, toàn thể quân dân Đại Việt đã đồng lòng sát cánh tại Hội nghị Diên Hồng thề 'Sát Thát'.

Dưới sự chỉ huy thiên tài của Quốc công Tiết chế Hưng Đạo Đại Vương Trần Quốc Tuấn, quân dân ta đã lập nên những kỳ tích Chương Dương, Hàm Tử, Tây Kết và Bạch Đằng giang bất tử."""
            },
            {
                "title": "Chương 4: Chiến dịch Ngọc Hồi - Đống Đa đại phá quân Thanh",
                "content": """Mùa xuân năm Kỷ Dậu 1789, người anh hùng áo vải cờ đào Quang Trung - Nguyễn Huệ đã thực hiện cuộc hành quân thần tốc ra Bắc. Với lời hịch đanh thép 'Đánh cho để dài tóc, đánh cho để đen răng, đánh cho nó chích luân bất phản', nghĩa quân Tây Sơn đã quét sạch 29 vạn quân Mãn Thanh chỉ trong năm ngày Tết, bảo toàn trọn vẹn bờ cõi non sông."""
            }
        ]
    },
    {
        "slug": "luc_van_tien",
        "title": "Lục Vân Tiên",
        "author": "Nguyễn Đình Chiểu",
        "category": "Thơ ca & Kịch nghệ",
        "image_url": "https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?q=80&w=600",
        "rating_avg": 4.8,
        "review_count": 450,
        "format": "pdf",
        "summary": "Truyện thơ Nôm kinh điển của văn học Nam Bộ, ngợi ca tinh thần trượng nghĩa hiệp khách, đạo lý làm người và lòng trung hiếu tiết nghĩa sáng ngời.",
        "narration_text": "Sách nói Lục Vân Tiên của cụ đồ Nguyễn Đình Chiểu. Nhớ câu kiến nghĩa bất vi, làm người thế ấy cũng phi anh hùng. Chàng thư sinh Lục Vân Tiên trên đường lai kinh ứng thí đã bẻ cây làm gậy đánh tan bầy cướp Phong Lai cứu nàng Kiều Nguyệt Nga. Tác phẩm là bài ca bất hủ về đạo nghĩa và lẽ sống cao đẹp của người dân Nam Bộ.",
        "chapters": [
            {
                "title": "Hồi 1: Lục Vân Tiên đánh cướp cứu Kiều Nguyệt Nga",
                "content": """Lục Vân Tiên là chàng trai tuấn tú, văn võ toàn tài. Trên đường lên kinh đô dự thi khoa cử, chàng bắt gặp toán cướp Phong Lai hung hãn đang cướp bóc và bắt giữ con gái quan tri phủ là Kiều Nguyệt Nga.

Vân Tiên nổi giận bẻ gãy nhánh cây bên đường xông vào giữa vòng vây quân cướp như Triệu Tử Long đại phá Đương Dương Trường Bản. Tướng cướp bị đập chết tại trận, lũ lâu la tan tác tháo chạy.

Cứu được giai nhân, Vân Tiên từ chối mọi vàng bạc tạ ơn, thể hiện khí phách hào sảng của trang quân tử: 'Làm ơn há dễ trông người trả ơn'."""
            },
            {
                "title": "Hồi 2: Gặp nạn mù mắt và tấm lòng son sắt Nguyệt Nga",
                "content": """Nghe tin mẹ mất, Vân Tiên bỏ thi về chịu tang, khóc thương đến mù lòa đôi mắt. Chàng bị kẻ gian Trịnh Hâm hãm hại đẩy xuống sông, gia đình vị hôn thê tráo trở bội ước đuổi đi.

Trong khi đó, Kiều Nguyệt Nga một lòng gìn giữ bức họa Vân Tiên, thề chết không chịu khuất phục trước lệnh ép gả sang cống nạp giặc Ô Qua, liều mình nhảy xuống biển tự vẫn để giữ tròn danh tiết."""
            },
            {
                "title": "Hồi 3: Trùng phùng đoàn viên và công lý chiến thắng",
                "content": """Trời xanh không phụ người hiền lương. Cả Vân Tiên và Nguyệt Nga đều được các bậc thần linh và dân lành cứu mạng. Vân Tiên được thuốc quý chữa sáng mắt, thi đỗ Trạng nguyên và cầm quân dẹp tan giặc ngoại xâm.

Ngày khải hoàn trở về, chàng tìm lại được Kiều Nguyệt Nga. Kẻ ác bị trừng trị thích đáng, đôi lứa nghĩa tình sum họp một nhà, rạng rỡ đạo lý chính nghĩa tất thắng gian tà."""
            }
        ]
    },
    {
        "slug": "bi_vo",
        "title": "Bỉ Vỏ",
        "author": "Nguyên Hồng",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1476275466078-4007374efbbe?q=80&w=600",
        "rating_avg": 4.8,
        "review_count": 510,
        "format": "pdf",
        "summary": "Bức tranh gai góc và dữ dội về thế giới giang hồ trộm cắp nơi đất cảng Hải Phòng thời thuộc Pháp cùng bi kịch của người phụ nữ bị tha hóa.",
        "narration_text": "Sách nói Bỉ Vỏ của nhà văn Nguyên Hồng. Tác phẩm đầu tay xuất sắc phản ánh số phận đau đớn của Bính - một cô gái quê mùa ngây thơ bị lừa gạt, ruồng bỏ rồi trôi dạt vào chốn giang hồ đất cảng Hải Phòng, trở thành một 'bỉ vỏ' tức tay trộm cắp chuyên nghiệp bên cạnh trùm giang hồ Năm Sài Gòn.",
        "chapters": [
            {
                "title": "Chương 1: Cô gái quê mùa bước vào bẫy rập thị thành",
                "content": """Bính vốn là một cô thôn nữ xinh xắn, ngoan ngoãn nơi đồng quê. Nhưng vì ngây thơ nhẹ dạ, cô bị một viên tham sự đồi bại lừa gạt có thai rồi bỏ rơi.

Gia đình bắt phạt, làng xóm sỉ vả miệt thị khiến Bính phải cắn răng bán đi đứa con đỏ hỏn rồi trôi dạt ra Hải Phòng tìm kế sinh nhai. Giữa thành phố cảng đầy cạm bẫy, cô bị lừa bán vào nhà chứa lầu xanh nhơ nhớp."""
            },
            {
                "title": "Chương 2: Thế giới giang hồ của Năm Sài Gòn",
                "content": """Tại đây, Bính gặp Năm Sài Gòn - một tay giang hồ cộm cán khét tiếng trộm cắp với ngón nghề 'chạy vỏ' điêu luyện. Cảm phục trước vẻ đẹp và sự cam chịu của Bính, Năm đã chuộc cô ra và đưa về sống chung.

Từ đó, Bính bước chân vào giới bất hảo, học cách móc túi, canh gác và sống cuộc đời bấp bênh rình rập giữa sự truy lùng ráo riết của mật thám."""
            },
            {
                "title": "Chương 3: Bi kịch định mệnh của tình mẫu tử",
                "content": """Trong một phi vụ móc túi trên chuyến tàu xuôi về Hà Nội, Năm Sài Gòn giật được chiếc vòng vàng và đứa trẻ sơ sinh của một phụ nữ khá giả.

Khi đem về nhà mở bọc tã ra xem, Bính rụng rời bàng hoàng nhận ra vết bớt đỏ trên ngực đứa bé: đó chính là đứa con ruột thịt mà cô đã dứt ruột bán đi năm xưa. Tiếng khóc thất thanh của người mẹ giang hồ xé toạc màn đêm u ám, khép lại tấn bi kịch đau đớn đến nghẹt thở."""
            }
        ]
    },
    {
        "slug": "chiec_thuyen_ngoai_xa",
        "title": "Chiếc Thuyền Ngoài Xa",
        "author": "Nguyễn Minh Châu",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1509021436665-8f07dbf5bf1d?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 630,
        "format": "pdf",
        "summary": "Chiêm nghiệm sâu sắc về mối quan hệ giữa nghệ thuật và cuộc đời, cái nhìn đa diện về số phận con người sau chiến tranh.",
        "narration_text": "Sách nói Chiếc Thuyền Ngoài Xa của Nguyễn Minh Châu. Nghệ sĩ nhiếp ảnh Phùng chụp được một bức ảnh toàn bích tuyệt đẹp về chiếc thuyền lưới vó ẩn hiện trong làn sương sớm mờ ảo. Nhưng khi chiếc thuyền cập bờ, anh bàng hoàng chứng kiến cảnh tượng bạo lực gia đình tàn nhẫn bước ra từ chính khung cảnh thơ mộng ấy.",
        "chapters": [
            {
                "title": "Chương 1: Bức ảnh nghệ thuật toàn bích",
                "content": """Để có một tấm ảnh nghệ thuật cho cuốn lịch năm mới, nghệ sĩ Phùng đã phục kích nhiều ngày bên bờ biển miền Trung. Một buổi sớm mai, anh bắt gặp một cảnh đắt trời cho: chiếc thuyền lưới vó từ từ tiến vào bờ trong làn sương mù màu hồng phớt của ánh bình minh.

Mũi thuyền in một nét mơ hồ vào bầu trời, vài bóng người ngồi im phăng phắc như một bức tranh mực tàu của danh họa cổ. Phùng bấm máy liên tục trong niềm hạnh phúc ngập tràn của sự thăng hoa nghệ thuật."""
            },
            {
                "title": "Chương 2: Hiện thực trần trụi phía sau ống kính",
                "content": """Nhưng ngay sau khoảnh khắc toàn bích ấy, chiếc thuyền cập bến cát. Một người đàn bà thô kệch, rỗ mặt bước xuống, theo sau là người đàn ông lực lưỡng với đôi mắt dữ dằn.

Không nói một lời, người chồng rút chiếc thắt lưng da quất tới tấp vào lưng vợ như trút cơn giận dữ, nghiến răng rủa: 'Mày chết đi cho ông nhờ!'. Đứa con trai nhỏ lao vào bảo vệ mẹ bị bố tát ngã dúi dụi. Phùng chết lặng trước nghịch cảnh bạo tàn diễn ra ngay sau bức tranh thơ mộng."""
            },
            {
                "title": "Chương 3: Câu chuyện ở tòa án huyện và cái nhìn đa chiều",
                "content": """Tại tòa án huyện, chánh án Đẩu khuyên người đàn bà ly hôn để giải thoát. Nhưng người đàn bà van xin quỳ lạy: 'Con lạy quý tòa, quý tòa bắt tội con cũng được nhưng đừng bắt con bỏ nó!'.

Bà giải thích rằng gia đình trên thuyền cần một người đàn ông khỏe mạnh để chèo chống qua những cơn giông bão biển khơi, và niềm vui lớn nhất của đời bà là nhìn thấy đàn con được ăn no. Bài học về sự thấu hiểu cuộc đời sâu sắc hơn mọi lý thuyết suông màu xám."""
            }
        ]
    },
    {
        "slug": "vo_chong_a_phu",
        "title": "Vợ Chồng A Phủ",
        "author": "Tô Hoài",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600",
        "rating_avg": 4.9,
        "review_count": 710,
        "format": "pdf",
        "summary": "Khúc ca ngợi ca sức sống tiềm tàng bất diệt và tinh thần vùng lên tự giải phóng của đồng bào vùng cao Tây Bắc khỏi ách áp bức phong kiến thần quyền.",
        "narration_text": "Sách nói Vợ Chồng A Phủ của nhà văn Tô Hoài. Ai ở xa về Hồng Ngài thường thấy một cô gái ngồi quay sợi gai bên tảng đá trước cửa nhà thống lý Pá Tra. Lúc nào cô cũng cúi mặt, mặt buồn rười rượi. Đó là Mị, con dâu gạt nợ nhà quan thống lý. Nhưng đằng sau sự câm lặng nhẫn nhục ấy là một ngọn lửa khát vọng tự do mãnh liệt đang âm ỉ cháy.",
        "chapters": [
            {
                "title": "Chương 1: Thân phận con dâu gạt nợ nhà Pá Tra",
                "content": """Mị là bông hoa xinh đẹp của núi rừng Tây Bắc, yêu đời và thổi sáo rất hay. Vì món nợ truyền kiếp của cha mẹ từ ngày cưới, Mị bị A Sử - con trai thống lý Pá Tra - bắt về làm dâu gạt nợ.

Ở nhà thống lý, Mị sống lùi lũi như con rùa nuôi nơi xó cửa. Mỗi ngày chỉ biết cắm cúi thái cỏ ngựa, dệt vải, gánh nước. Mị tưởng chừng đã chai sạn hết mọi cảm xúc, quên mất cả ý niệm về thời gian và sự sống."""
            },
            {
                "title": "Chương 2: Đêm tình mùa xuân và sức sống trỗi dậy",
                "content": """Mùa xuân về trên rẻo cao, hoa thuốc phiện nở trắng rực rỡ sườn đồi, tiếng khèn gọi bạn tình tha thiết vang vọng qua vách đá. Tiếng khèn ấy đã đánh thức tâm hồn Mị.

Mị lén lấy váy hoa, quấn lại tóc chuẩn bị đi chơi xuân. Dù bị A Sử trói đứng vào cột nhà bằng cả thúng sợi đay, tâm hồn Mị vẫn bay theo tiếng khèn, khát khao được sống một cuộc đời tự do như thời con gái."""
            },
            {
                "title": "Chương 3: Nhát dao cắt dây trói và con đường tự do",
                "content": """A Phủ vì để hổ vồ mất một con bò nên bị thống lý trói đứng vào cọc suốt mấy ngày đêm giữa mùa đông giá rét, kiệt sức sắp chết. Ban đầu Mị dửng dưng, nhưng khi nhìn thấy hai dòng nước mắt lấp lánh chảy dài trên gò má xám ngắt của A Phủ, lòng trắc ẩn trong Mị bùng cháy.

Mị liều mình lấy dao cắt đứt dây mây cứu A Phủ. Khi A Phủ quỵ xuống rồi gượng chạy đi, nỗi sợ cái chết bỗng biến thành sức mạnh phi thường. Mị chạy vụt theo: 'A Phủ cho tôi đi! Ở đây thì chết mất!'. Hai người cùng nhau trốn khỏi Hồng Ngài, tìm đến Phiềng Sa tham gia kháng chiến bảo vệ quê hương."""
            }
        ]
    },
    {
        "slug": "canh_dong_bat_tan",
        "title": "Cánh Đồng Bất Tận",
        "author": "Nguyễn Ngọc Tư",
        "category": "Văn học & Tiểu thuyết",
        "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=600",
        "rating_avg": 4.8,
        "review_count": 670,
        "format": "pdf",
        "summary": "Khúc bi ca da diết về những phận đời trôi dạt trên sông nước miền Tây, nỗi đau thương tổn tâm hồn và ánh sáng của sự thứ tha cứu chuộc.",
        "narration_text": "Sách nói Cánh Đồng Bất Tận của nhà văn Nguyễn Ngọc Tư. Chiếc ghe vịt lững lờ trôi dọc theo những cánh đồng bát ngát rợp bóng mây trời phương Nam. Cha con ông Út Vũ, Nương và Điền mang theo nỗi đau bị phụ bạc trôi dạt qua từng mùa gặt. Một tác phẩm chạm đến tận cùng những góc khuất xót xa của tình người và hy vọng hồi sinh.",
        "chapters": [
            {
                "title": "Chương 1: Chiếc ghe chở đàn vịt và những cuộc phiêu dạt",
                "content": """Cuộc đời của chị em Nương và Điền gắn liền với chiếc ghe chở đàn vịt chạy đồng rày đây mai đó. Sau khi mẹ bỏ đi theo một người đàn ông giàu có buôn vải, ông cha - Út Vũ - trở nên câm lặng và cay độc với cả thế giới.

Ông đốt rụi căn nhà cũ, chất hai đứa con thơ lên ghe rồi đưa chúng đi biệt xứ. Đàn vịt đi tới đâu, mùi bùn non và nỗi cô đơn lại bám riết lấy họ tới đó."""
            },
            {
                "title": "Chương 2: Sự xuất hiện của người đàn bà tên Sương",
                "content": """Một ngày nọ, hai đứa trẻ cứu vớt cô Sương - một phụ nữ làm nghề bán phấn buôn hương bị người ta đánh ghen tàn nhẫn và dìm xuống bùn. Sương bước lên ghe mang lại chút hơi ấm gia đình và sự dịu dàng của người phụ nữ mà hai đứa trẻ khao khát bấy lâu.

Nhưng ông Vũ chỉ nhìn Sương bằng con mắt khinh miệt và trả thù phụ nữ. Sự tàn nhẫn lạnh lùng của ông cuối cùng đã đẩy Sương lặng lẽ rời bỏ chiếc ghe trong một đêm mưa."""
            },
            {
                "title": "Chương 3: Nỗi đau tột cùng và mầm sống hồi sinh",
                "content": """Bi kịch ập đến khi Nương bị một nhóm thợ gặt côn đồ hãm hiếp giữa cánh đồng hoang vắng. Nhìn con gái đau đớn, tột cùng nỗi căm hờn đã làm sụp đổ bức tường băng giá trong lòng người cha. Ông ôm lấy con khóc nức nở trong sự muộn màng.

Dù phải trải qua nỗi đau đớn tột cùng, Nương vẫn chọn cách bao dung. Cô nhìn về tương lai và mong ước đứa con trong bụng mình lớn lên sẽ biết yêu thương con người, khép lại vòng xoáy hận thù trên cánh đồng bất tận."""
            }
        ]
    },
    {
        "slug": "hoang_tu_be",
        "title": "Hoàng Tử Bé",
        "author": "Antoine de Saint-Exupéry",
        "category": "Thiếu nhi & Cổ tích",
        "image_url": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?q=80&w=600",
        "rating_avg": 5.0,
        "review_count": 1400,
        "format": "epub",
        "summary": "Kiệt tác văn học thiếu nhi bất hủ của thế giới bản dịch tiếng Việt chuẩn: Người ta chỉ có thể nhìn thấy rõ ràng bằng trái tim, cái cốt lõi thì vô hình trong mắt trần.",
        "narration_text": "Sách nói Hoàng Tử Bé của nhà văn Antoine de Saint-Exupéry. Một phi công bị rơi máy bay giữa sa mạc Sahara hoang vu bất ngờ gặp một cậu bé tóc vàng kỳ lạ từ tiểu hành tinh B612 xa xôi. Câu chuyện về bông hoa hồng kiêu kỳ, chú cáo thông thái và bài học về sự gắn kết thiêng liêng sẽ mãi sưởi ấm trái tim người đọc.",
        "chapters": [
            {
                "title": "Chương 1: Cuộc gặp gỡ kỳ lạ giữa sa mạc Sahara",
                "content": """Máy bay của tôi bị hỏng động cơ rơi xuống giữa sa mạc Sahara bao la, cách xa mọi chốn có người ở hàng ngàn dặm. Trong lúc đang cặm cụi sửa máy bay với nguồn nước uống ít ỏi, tôi bỗng giật mình bởi một giọng nói nhỏ nhẹ: 'Làm ơn... vẽ cho tôi một con cừu!'.

Đó là Hoàng Tử Bé - một cậu bé với mái tóc vàng óng ả, khăn choàng bay trong gió, đến từ tiểu hành tinh B612 chỉ to bằng một ngôi nhà."""
            },
            {
                "title": "Chương 2: Bông hoa hồng kiêu kỳ trên tiểu tinh cầu",
                "content": """Trên hành tinh của mình, Hoàng Tử Bé có ba ngọn núi lửa và một bông hoa hồng duy nhất. Bông hoa xinh đẹp lộng lẫy nhưng lại kiêu kỳ và hay hờn dỗi.

Vì không hiểu được tình yêu ẩn sau những lời phàn nàn của hoa, Hoàng Tử Bé đã bỏ đi ngao du qua các hành tinh khác để tìm kiếm những người bạn mới."""
            },
            {
                "title": "Chương 3: Bài học thuần hóa của chú Cáo thông thái",
                "content": """Đến Trái Đất, Hoàng Tử Bé gặp một chú cáo hoang dã. Cáo dạy cho cậu bí mật lớn nhất của tình yêu: 'Thuần hóa' là tạo nên những mối dây ràng buộc.

'Nếu bạn thuần hóa tôi, chúng ta sẽ cần đến nhau. Bạn sẽ là duy nhất trên đời đối với tôi, và tôi sẽ là duy nhất trên đời đối với bạn. Người ta chỉ có thể nhìn thấy thật rõ ràng bằng trái tim; những gì cốt lõi thì vô hình đối với mắt trần'."""
            },
            {
                "title": "Chương 4: Sự trở về giữa ngàn sao lấp lánh",
                "content": """Nhận ra bông hồng của mình là duy nhất trên đời vì cậu đã dành trọn thời gian chăm sóc nàng, Hoàng Tử Bé quyết định để chú rắn vàng cắn mình để trút bỏ thể xác nặng nề, đưa linh hồn bay trở về tiểu hành tinh B612.

Mỗi khi ngước nhìn bầu trời đêm đầy sao lấp lánh, ta lại nghe thấy tiếng cười trong trẻo như ngàn chiếc chuông nhỏ vang vọng từ một hành tinh xa xôi."""
            }
        ]
    }
]

if __name__ == "__main__":
    print(f"Tổng số sách trong danh mục: {len(BOOKS_DATA)} cuốn.")
    for i, b in enumerate(BOOKS_DATA, 1):
        print(f"{i}. {b['title']} - {b['author']} ({b['category']}) [{len(b['chapters'])} chương]")
