// main_screen.dart
import 'dart:async';
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:ui';
import 'package:shared_preferences/shared_preferences.dart';

// --- IMPORT CÁC MÀN HÌNH LIÊN QUAN ---
import 'profile_screen.dart';
import 'explore_screen.dart';
import 'book_shelf_screen.dart';
import 'api_config.dart';
import 'book_reader_helper.dart';
import 'audio_player_service.dart';
import 'audio_player_screen.dart';
import 'mini_audio_player.dart';
import 'offline_manager.dart';
import 'progress_service.dart';

// --- 1. CLASS MODEL BOOK ---
class Book {
  final int id;
  final String title;
  final String author;
  final String imageUrl;
  final String pdfUrl;
  final String audioUrl;
  final String description;
  final String category;
  final double ratingAvg;
  final int reviewCount;
  final String source;

  Book({
    required this.id,
    required this.title,
    required this.author,
    required this.imageUrl,
    required this.pdfUrl,
    required this.audioUrl,
    this.description = "",
    this.category = "Văn học & Tiểu thuyết",
    this.ratingAvg = 4.8,
    this.reviewCount = 15,
    this.source = "Project Gutenberg & LibriVox",
  });

  factory Book.fromJson(Map<String, dynamic> json) {
    return Book(
      id: json['id'] ?? 0,
      title: json['title'] ?? 'Không có tiêu đề',
      author: json['author'] ?? 'Chưa rõ tác giả',
      imageUrl: json['image_url'] ?? '',
      pdfUrl: json['pdf_url'] ?? '',
      audioUrl: json['audio_url'] ?? '',
      description: json['content'] ?? json['description'] ?? '',
      category: json['category'] ?? 'Văn học & Tiểu thuyết',
      ratingAvg: (json['rating_avg'] != null) ? (json['rating_avg'] as num).toDouble() : 4.8,
      reviewCount: json['review_count'] ?? 15,
      source: json['source'] ?? 'Project Gutenberg & LibriVox',
    );
  }
}

// --- 2. HÀM HIỂN THỊ HỒ SƠ TÁC GIẢ (AUTHOR PROFILE) ---
void showAuthorProfileModal(BuildContext context, String authorName, List<Book> allBooks) {
  final authorBooks = allBooks
      .where((b) => b.author.trim().toLowerCase() == authorName.trim().toLowerCase())
      .toList();

  showModalBottomSheet(
    context: context,
    backgroundColor: const Color(0xFF1E1E1E),
    shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
    isScrollControlled: true,
    builder: (context) {
      return DraggableScrollableSheet(
        initialChildSize: 0.65,
        minChildSize: 0.4,
        maxChildSize: 0.9,
        expand: false,
        builder: (context, scrollController) {
          return SingleChildScrollView(
            controller: scrollController,
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                Container(
                  width: 40, height: 4,
                  margin: const EdgeInsets.only(bottom: 20),
                  decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(2)),
                ),
                CircleAvatar(
                  radius: 38,
                  backgroundColor: Colors.orange,
                  child: Text(
                    authorName.isNotEmpty ? authorName[0].toUpperCase() : 'A',
                    style: const TextStyle(color: Colors.white, fontSize: 30, fontWeight: FontWeight.bold),
                  ),
                ),
                const SizedBox(height: 12),
                Text(
                  authorName,
                  style: const TextStyle(color: Colors.white, fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 4),
                const Text(
                  "Tác giả & Diễn giả truyền cảm hứng",
                  style: TextStyle(color: Colors.orangeAccent, fontSize: 13),
                ),
                const SizedBox(height: 16),
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.05),
                    borderRadius: BorderRadius.circular(14),
                  ),
                  child: Text(
                    "Tác giả $authorName là cây bút nổi tiếng với nhiều tác phẩm truyền cảm hứng, phát triển bản thân và tư duy chiến lược được đông đảo độc giả yêu thích.",
                    style: const TextStyle(color: Colors.white70, fontSize: 13, height: 1.5),
                    textAlign: TextAlign.center,
                  ),
                ),
                const SizedBox(height: 20),
                Align(
                  alignment: Alignment.centerLeft,
                  child: Text(
                    "Tác phẩm của tác giả (${authorBooks.length})",
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 15),
                  ),
                ),
                const SizedBox(height: 10),
                if (authorBooks.isEmpty)
                  const Padding(
                    padding: EdgeInsets.all(16.0),
                    child: Text("Đang cập nhật thêm tác phẩm của tác giả này...", style: TextStyle(color: Colors.white38)),
                  )
                else
                  ListView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: authorBooks.length,
                    itemBuilder: (context, index) {
                      final b = authorBooks[index];
                      return ListTile(
                        contentPadding: const EdgeInsets.symmetric(vertical: 4),
                        leading: ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: b.imageUrl.isNotEmpty
                              ? Image.network(
                                  ApiConfig.formatUrl(b.imageUrl),
                                  width: 42,
                                  height: 56,
                                  fit: BoxFit.cover,
                                  errorBuilder: (_, __, ___) => Container(width: 42, height: 56, color: Colors.grey[800]),
                                )
                              : Container(width: 42, height: 56, color: Colors.grey[800]),
                        ),
                        title: Text(b.title, style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.bold)),
                        subtitle: Text(b.description.isNotEmpty ? b.description : 'Sách đọc & Audio', style: const TextStyle(color: Colors.white54, fontSize: 11), maxLines: 1),
                        trailing: const Icon(Icons.arrow_forward_ios_rounded, color: Colors.white30, size: 14),
                        onTap: () {
                          Navigator.pop(context);
                          Navigator.push(context, MaterialPageRoute(builder: (context) => BookDetailScreen(book: b, username: 'User')));
                        },
                      );
                    },
                  ),
              ],
            ),
          );
        },
      );
    },
  );
}

// --- 3. WIDGET TRANG CHỦ HIỂN THỊ DANH SÁCH THEO BỐ CỤC CAROUSEL & TÌM KIẾM ---
class HomeScreen extends StatefulWidget {
  final String username;

  const HomeScreen({super.key, required this.username});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Book> books = [];
  bool isLoading = true;

  // Tìm kiếm với Debounce 300ms
  final TextEditingController _searchController = TextEditingController();
  Timer? _debounceTimer;
  String _searchQuery = '';

  // Carousel Banner
  final PageController _bannerController = PageController();
  int _currentBannerIndex = 0;

  // Lọc theo thể loại
  String _selectedCategory = "Tất cả";
  final List<String> _categories = [
    "Tất cả",
    "Văn học & Tiểu thuyết",
    "Phiêu lưu & Kỳ ảo",
    "Trinh thám & Bí ẩn",
    "Khoa học & Viễn tưởng",
    "Triết học & Tư tưởng",
    "Lịch sử & Tiểu sử",
    "Tâm lý & Xã hội",
    "Thiếu nhi & Cổ tích",
    "Thơ ca & Kịch nghệ",
    "Kinh doanh & Phát triển",
  ];

  // Danh sách đọc dở / nghe dở
  List<Map<String, dynamic>> _continueItems = [];

  final List<Map<String, dynamic>> _banners = [
    {
      'tag': 'XU HƯỚNG ĐỌC SÁCH NĂM 2026',
      'title': 'Không Gian Tri Thức Số',
      'subtitle': 'Hàng ngàn đầu sách PDF, EPUB & Audio\nchất lượng cao đang chờ bạn.',
      'btn': 'Khám phá ngay',
      'icon': Icons.local_fire_department,
      'gradient': [Color(0xFFFFA040), Color(0xFFFF6600), Color(0xFF903000)],
    },
    {
      'tag': 'SÁCH NÓI ĐẶC QUYỀN',
      'title': 'Thư Viện Audio Sống Động',
      'subtitle': 'Nghe mọi lúc mọi nơi với tốc độ tùy biến\nvà phát nền không gián đoạn.',
      'btn': 'Nghe ngay',
      'icon': Icons.headset_rounded,
      'gradient': [Color(0xFF2980B9), Color(0xFF6DD5FA), Color(0xFF1B4F72)],
    },
    {
      'tag': 'TUYỂN CHỌN HÀNG TUẦN',
      'title': 'Tủ Sách Tinh Hoa 2026',
      'subtitle': 'Kỹ năng lãnh đạo, tư duy đột phá\nđược biên tập công phu.',
      'btn': 'Xem tủ sách',
      'icon': Icons.star_rounded,
      'gradient': [Color(0xFF8E44AD), Color(0xFFC39BD3), Color(0xFF4A235A)],
    },
  ];

  @override
  void initState() {
    super.initState();
    fetchBooks();
  }

  @override
  void dispose() {
    _debounceTimer?.cancel();
    _searchController.dispose();
    _bannerController.dispose();
    super.dispose();
  }

  void _onSearchChanged(String query) {
    _debounceTimer?.cancel();
    _debounceTimer = Timer(const Duration(milliseconds: 300), () {
      if (mounted) {
        setState(() {
          _searchQuery = query.trim();
        });
      }
    });
  }

  Future<void> fetchBooks() async {
    final url = Uri.parse('${ApiConfig.baseUrl}/api/books');
    try {
      final response = await http.get(url);
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
        if (mounted) {
          final list = data.map((json) => Book.fromJson(json)).toList();
          setState(() {
            books = list;
            isLoading = false;
          });
          _loadContinueReading(list);
        }
      } else {
        if (mounted) setState(() => isLoading = false);
      }
    } catch (e) {
      if (mounted) setState(() => isLoading = false);
      debugPrint("Lỗi kết nối API: $e");
    }
  }

  Future<void> _loadContinueReading(List<Book> bookList) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final Map<int, Map<String, dynamic>> progressMap = {};

      // 1. Quét tiến độ cục bộ từ SharedPreferences
      for (final b in bookList) {
        final page = prefs.getInt('pdf_page_${widget.username.trim()}_${b.id}');
        final audioPos = prefs.getInt('audio_pos_${b.id}');
        if ((page != null && page > 0) || (audioPos != null && audioPos > 0)) {
          progressMap[b.id] = {
            'book': b,
            'page': page ?? 0,
            'audioPos': audioPos ?? 0,
          };
        }
      }

      // 2. Đồng bộ tiến độ từ Backend nếu người dùng đã đăng nhập
      final remoteList = await ProgressService.getUserProgress(widget.username);
      for (final rp in remoteList) {
        final int bId = rp['book_id'] ?? 0;
        final b = bookList.firstWhere(
          (item) => item.id == bId,
          orElse: () => Book(
            id: bId,
            title: rp['title'] ?? '',
            author: rp['author'] ?? '',
            imageUrl: rp['image_url'] ?? '',
            pdfUrl: rp['pdf_url'] ?? '',
            audioUrl: rp['audio_url'] ?? '',
          ),
        );
        final int rPage = rp['last_page'] ?? 0;
        final int rAudio = rp['last_audio_position_ms'] ?? 0;

        if (rPage > 0 || rAudio > 0) {
          final existing = progressMap[bId];
          final finalPage = (existing != null && (existing['page'] as int) > rPage) ? existing['page'] : rPage;
          final finalAudio = (existing != null && (existing['audioPos'] as int) > rAudio) ? existing['audioPos'] : rAudio;
          progressMap[bId] = {
            'book': b,
            'page': finalPage,
            'audioPos': finalAudio,
          };
        }
      }

      if (mounted) {
        setState(() {
          _continueItems = progressMap.values.toList();
        });
      }
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Center(child: CircularProgressIndicator(color: Colors.orange));
    }

    // Lọc theo tìm kiếm và thể loại
    final filtered = books.where((b) {
      if (_searchQuery.isNotEmpty) {
        final q = _searchQuery.toLowerCase();
        final matchTitle = b.title.toLowerCase().contains(q);
        final matchAuthor = b.author.toLowerCase().contains(q);
        if (!matchTitle && !matchAuthor) return false;
      }
      if (_selectedCategory != "Tất cả") {
        final catLower = _selectedCategory.toLowerCase();
        final bCatLower = b.category.toLowerCase();
        final descLower = b.description.toLowerCase();
        final titleLower = b.title.toLowerCase();
        if (!bCatLower.contains(catLower) && !catLower.contains(bCatLower) && !descLower.contains(catLower) && !titleLower.contains(catLower)) {
          return false;
        }
      }
      return true;
    }).toList();

    final readingBooks = filtered.where((b) => b.pdfUrl.isNotEmpty).toList();
    final audioBooks = filtered.where((b) => b.audioUrl.isNotEmpty).toList();

    return RefreshIndicator(
      color: Colors.orange,
      onRefresh: fetchBooks,
      child: Stack(
        children: [
          // Lớp nền thư viện
          Positioned.fill(
            child: Image.network(
              'https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1000&auto=format&fit=crop',
              fit: BoxFit.cover,
            ),
          ),
          Positioned.fill(
            child: BackdropFilter(
              filter: ImageFilter.blur(sigmaX: 10.0, sigmaY: 10.0),
              child: Container(color: Colors.black.withOpacity(0.4)),
            ),
          ),

          // Nội dung chính
          Positioned.fill(
            child: SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.only(bottom: 40),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // ==================== THANH TÌM KIẾM DEBOUNCE 300MS ====================
                  Container(
                    margin: const EdgeInsets.fromLTRB(16, 12, 16, 8),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.12),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(color: Colors.white24),
                    ),
                    child: TextField(
                      controller: _searchController,
                      onChanged: _onSearchChanged,
                      style: const TextStyle(color: Colors.white, fontSize: 14),
                      decoration: InputDecoration(
                        hintText: "Tìm kiếm sách, tác giả...",
                        hintStyle: TextStyle(color: Colors.white.withOpacity(0.5), fontSize: 14),
                        prefixIcon: const Icon(Icons.search_rounded, color: Colors.orangeAccent),
                        suffixIcon: _searchController.text.isNotEmpty
                            ? IconButton(
                                icon: const Icon(Icons.clear, color: Colors.white54, size: 18),
                                onPressed: () {
                                  _searchController.clear();
                                  _onSearchChanged('');
                                },
                              )
                            : null,
                        border: InputBorder.none,
                        contentPadding: const EdgeInsets.symmetric(vertical: 14),
                      ),
                    ),
                  ),

                  // ==================== 1. BANNER CAROUSEL CÓ CHUYỂN SLIDE ====================
                  SizedBox(
                    height: 185,
                    child: PageView.builder(
                      controller: _bannerController,
                      itemCount: _banners.length,
                      onPageChanged: (idx) {
                        setState(() => _currentBannerIndex = idx);
                      },
                      itemBuilder: (context, index) {
                        final b = _banners[index];
                        return Container(
                          margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(20),
                            gradient: LinearGradient(
                              colors: b['gradient'] as List<Color>,
                              begin: Alignment.topLeft,
                              end: Alignment.bottomRight,
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: (b['gradient'][1] as Color).withOpacity(0.35),
                                blurRadius: 16,
                                offset: const Offset(0, 8),
                              )
                            ],
                          ),
                          child: Stack(
                            children: [
                              Positioned(
                                right: 15,
                                top: 15,
                                bottom: 15,
                                child: Opacity(
                                  opacity: 0.25,
                                  child: Icon(b['icon'] as IconData, size: 130, color: Colors.white),
                                ),
                              ),
                              Padding(
                                padding: const EdgeInsets.all(20.0),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                  children: [
                                    Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      children: [
                                        Row(
                                          children: [
                                            Icon(b['icon'] as IconData, color: Colors.white, size: 14),
                                            const SizedBox(width: 4),
                                            Text(
                                              b['tag'],
                                              style: TextStyle(color: Colors.white.withOpacity(0.85), fontSize: 10, fontWeight: FontWeight.w600, letterSpacing: 0.5),
                                            ),
                                          ],
                                        ),
                                        const SizedBox(height: 6),
                                        Text(
                                          b['title'],
                                          style: const TextStyle(color: Colors.white, fontSize: 21, fontWeight: FontWeight.bold, letterSpacing: 0.5),
                                        ),
                                        const SizedBox(height: 4),
                                        Text(
                                          b['subtitle'],
                                          style: TextStyle(color: Colors.white.withOpacity(0.9), fontSize: 11, height: 1.3),
                                        ),
                                      ],
                                    ),
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                                      decoration: BoxDecoration(
                                        color: Colors.white,
                                        borderRadius: BorderRadius.circular(20),
                                      ),
                                      child: Row(
                                        mainAxisSize: MainAxisSize.min,
                                        children: [
                                          Text(b['btn'], style: const TextStyle(color: Colors.orange, fontSize: 11, fontWeight: FontWeight.bold)),
                                          const SizedBox(width: 4),
                                          const Icon(Icons.arrow_forward_ios_rounded, color: Colors.orangeAccent, size: 10),
                                        ],
                                      ),
                                    )
                                  ],
                                ),
                              ),
                            ],
                          ),
                        );
                      },
                    ),
                  ),

                  // Indicator dots của Carousel
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: List.generate(_banners.length, (idx) {
                      final isSel = idx == _currentBannerIndex;
                      return AnimatedContainer(
                        duration: const Duration(milliseconds: 250),
                        margin: const EdgeInsets.symmetric(horizontal: 3),
                        width: isSel ? 16 : 6,
                        height: 5,
                        decoration: BoxDecoration(
                          color: isSel ? Colors.orange : Colors.white38,
                          borderRadius: BorderRadius.circular(3),
                        ),
                      );
                    }),
                  ),
                  const SizedBox(height: 10),

                  // ==================== TIẾP TỤC ĐỌC & NGHE (CONTINUE READING) ====================
                  if (_continueItems.isNotEmpty) ...[
                    _buildSectionTitle("TIẾP TỤC ĐỌC & NGHE", Icons.history_rounded),
                    SizedBox(
                      height: 110,
                      child: ListView.builder(
                        scrollDirection: Axis.horizontal,
                        padding: const EdgeInsets.symmetric(horizontal: 16),
                        itemCount: _continueItems.length,
                        itemBuilder: (context, index) {
                          final item = _continueItems[index];
                          final Book b = item['book'];
                          final int page = item['page'];
                          final int audioMs = item['audioPos'];

                          return GestureDetector(
                            onTap: () {
                              if (page > 0) {
                                BookReaderHelper.openBook(
                                  context: context,
                                  fileUrl: ApiConfig.formatUrl(b.pdfUrl),
                                  bookTitle: b.title,
                                  bookId: b.id,
                                  username: widget.username,
                                  initialPage: page,
                                );
                              } else {
                                AudioPlayerService().playBook(
                                  bookId: b.id,
                                  title: b.title,
                                  author: b.author,
                                  audioUrl: ApiConfig.formatUrl(b.audioUrl),
                                  coverUrl: ApiConfig.formatUrl(b.imageUrl),
                                );
                                Navigator.push(context, MaterialPageRoute(builder: (_) => const AudioPlayerScreen()));
                              }
                            },
                            child: Container(
                              width: 220,
                              margin: const EdgeInsets.only(right: 12),
                              padding: const EdgeInsets.all(10),
                              decoration: BoxDecoration(
                                color: Colors.white.withOpacity(0.08),
                                borderRadius: BorderRadius.circular(14),
                                border: Border.all(color: Colors.orange.withOpacity(0.3)),
                              ),
                              child: Row(
                                children: [
                                  ClipRRect(
                                    borderRadius: BorderRadius.circular(8),
                                    child: b.imageUrl.isNotEmpty
                                        ? Image.network(ApiConfig.formatUrl(b.imageUrl), width: 50, height: 75, fit: BoxFit.cover)
                                        : Container(width: 50, height: 75, color: Colors.grey[800]),
                                  ),
                                  const SizedBox(width: 10),
                                  Expanded(
                                    child: Column(
                                      crossAxisAlignment: CrossAxisAlignment.start,
                                      mainAxisAlignment: MainAxisAlignment.center,
                                      children: [
                                        Text(b.title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13), maxLines: 1, overflow: TextOverflow.ellipsis),
                                        const SizedBox(height: 4),
                                        Text(b.author, style: const TextStyle(color: Colors.white54, fontSize: 11), maxLines: 1),
                                        const SizedBox(height: 8),
                                        Container(
                                          padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                                          decoration: BoxDecoration(color: Colors.orange.withOpacity(0.2), borderRadius: BorderRadius.circular(6)),
                                          child: Text(
                                            page > 0 ? "Trang ${page + 1}" : "Đã nghe ${(audioMs / 60000).toInt()}p",
                                            style: const TextStyle(color: Colors.orange, fontSize: 10, fontWeight: FontWeight.bold),
                                          ),
                                        ),
                                      ],
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
                    ),
                    const SizedBox(height: 12),
                  ],

                  // ==================== BỘ LỌC THỂ LOẠI (CATEGORY CHIPS) ====================
                  SizedBox(
                    height: 38,
                    child: ListView.builder(
                      scrollDirection: Axis.horizontal,
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      itemCount: _categories.length,
                      itemBuilder: (context, index) {
                        final cat = _categories[index];
                        final isSel = _selectedCategory == cat;
                        return GestureDetector(
                          onTap: () {
                            setState(() => _selectedCategory = cat);
                          },
                          child: Container(
                            margin: const EdgeInsets.only(right: 8),
                            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                            decoration: BoxDecoration(
                              color: isSel ? Colors.orange : Colors.white.withOpacity(0.08),
                              borderRadius: BorderRadius.circular(20),
                              border: Border.all(color: isSel ? Colors.orange : Colors.white24),
                            ),
                            child: Text(
                              cat,
                              style: TextStyle(
                                color: isSel ? Colors.black : Colors.white,
                                fontWeight: isSel ? FontWeight.bold : FontWeight.normal,
                                fontSize: 12,
                              ),
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                  const SizedBox(height: 10),

                  // ==================== 2. DANH MỤC: SÁCH ĐỌC ĐƯỢC YÊU THÍCH ====================
                  if (readingBooks.isNotEmpty) ...[
                    _buildSectionTitle(
                      "SÁCH ĐỌC ĐƯỢC YÊU THÍCH",
                      Icons.star_rounded,
                      onSeeAll: () => _showAllBooksModal("Sách Đọc Được Yêu Thích", readingBooks, false),
                    ),
                    ListView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      itemCount: readingBooks.length > 3 ? 3 : readingBooks.length,
                      itemBuilder: (context, index) {
                        return _buildVerticalBookRow(context, readingBooks[index], isAudio: false);
                      },
                    ),
                    const SizedBox(height: 14),
                  ],

                  // ==================== 3. DANH MỤC: AUDIO SÁCH NỔI BẬT ====================
                  if (audioBooks.isNotEmpty) ...[
                    _buildSectionTitle(
                      "AUDIO SÁCH NỔI BẬT",
                      Icons.headset_rounded,
                      onSeeAll: () => _showAllBooksModal("Audio Sách Nổi Bật", audioBooks, true),
                    ),
                    ListView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      itemCount: audioBooks.length > 3 ? 3 : audioBooks.length,
                      itemBuilder: (context, index) {
                        return _buildVerticalBookRow(context, audioBooks[index], isAudio: true);
                      },
                    ),
                    const SizedBox(height: 14),
                  ],

                  // ==================== 4. DANH MỤC: SÁCH MỚI PHÁT HÀNH ====================
                  if (filtered.isNotEmpty) ...[
                    _buildSectionTitle(
                      "SÁCH MỚI PHÁT HÀNH",
                      Icons.new_releases_rounded,
                      onSeeAll: () => _showAllBooksModal("Sách Mới Phát Hành", filtered.reversed.toList(), false),
                    ),
                    ListView.builder(
                      shrinkWrap: true,
                      physics: const NeverScrollableScrollPhysics(),
                      padding: const EdgeInsets.symmetric(horizontal: 16),
                      itemCount: filtered.length > 3 ? 3 : filtered.length,
                      itemBuilder: (context, index) {
                        final reversedList = filtered.reversed.toList();
                        return _buildVerticalBookRow(context, reversedList[index], isAudio: reversedList[index].pdfUrl.isEmpty);
                      },
                    ),
                    const SizedBox(height: 20),
                  ],
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showAllBooksModal(String title, List<Book> books, bool isAudio) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: const Color(0xFF1E1E1E),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (ctx) {
        return DraggableScrollableSheet(
          initialChildSize: 0.85,
          minChildSize: 0.5,
          maxChildSize: 0.95,
          expand: false,
          builder: (context, scrollController) {
            return Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Row(
                        children: [
                          Icon(isAudio ? Icons.headset_rounded : Icons.menu_book_rounded, color: Colors.orange, size: 22),
                          const SizedBox(width: 8),
                          Text(title, style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                        ],
                      ),
                      IconButton(icon: const Icon(Icons.close, color: Colors.white70), onPressed: () => Navigator.pop(ctx)),
                    ],
                  ),
                  const SizedBox(height: 12),
                  Expanded(
                    child: ListView.builder(
                      controller: scrollController,
                      itemCount: books.length,
                      itemBuilder: (context, index) {
                        return _buildVerticalBookRow(context, books[index], isAudio: isAudio);
                      },
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  Widget _buildSectionTitle(String title, IconData? icon, {VoidCallback? onSeeAll}) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              if (icon != null) Icon(icon, color: Colors.orangeAccent, size: 18),
              if (icon != null) const SizedBox(width: 8),
              Text(
                title,
                style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13, letterSpacing: 0.5),
              ),
            ],
          ),
          InkWell(
            onTap: onSeeAll,
            borderRadius: BorderRadius.circular(6),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 3),
              child: Text(
                "Xem tất cả >",
                style: TextStyle(color: Colors.white.withValues(alpha: 0.6), fontSize: 11),
              ),
            ),
          ),
        ],
      ),
    );
  }

  // THẺ HIỂN THỊ SÁCH HÀNG DỌC ĐÃ ĐƯỢC SỬA LỖI ĐÚNG THAM SỐ CỦA COLUMN
  Widget _buildVerticalBookRow(BuildContext context, Book book, {required bool isAudio}) {
    return GestureDetector(
      onTap: () {
        Navigator.push(
          context,
          MaterialPageRoute(
            builder: (context) => BookDetailScreen(book: book, username: widget.username),
          ),
        );
      },
      child: Container(
        margin: const EdgeInsets.only(bottom: 14),
        height: 140,
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.05),
          borderRadius: BorderRadius.circular(12),
        ),
        padding: const EdgeInsets.all(10),
        child: Row(
          children: [
            Stack(
              children: [
                Container(
                  width: 95,
                  height: 120,
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.white24),
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(11),
                    child: book.imageUrl.isNotEmpty
                        ? Image.network(
                      ApiConfig.formatUrl(book.imageUrl),
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) => Container(color: Colors.grey[900], child: const Icon(Icons.broken_image, color: Colors.white30)),
                    )
                        : Container(color: Colors.grey[900], child: const Icon(Icons.image, color: Colors.white30)),
                  ),
                ),
                Positioned(
                  right: 6,
                  bottom: 6,
                  child: CircleAvatar(
                    radius: 15,
                    backgroundColor: Colors.white.withOpacity(0.8),
                    child: Icon(
                      isAudio ? Icons.play_arrow_rounded : Icons.bookmark_border_rounded,
                      color: Colors.orange,
                      size: 18,
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Column(
                // ✨ ĐÃ SỬA LỖI TẠI ĐÂY: Sử dụng đúng tham số crossAxisAlignment của Column
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    book.title,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    book.author,
                    style: const TextStyle(color: Colors.orangeAccent, fontSize: 11, fontWeight: FontWeight.w500),
                  ),
                  const SizedBox(height: 6),
                  if (book.description.isNotEmpty)
                    Text(
                      book.description,
                      maxLines: 3,
                      overflow: TextOverflow.ellipsis,
                      style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 11, height: 1.4),
                    ),
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      if (book.pdfUrl.contains('vn_book') || book.audioUrl.contains('vn_book') || book.id <= 4 || book.source.contains('Việt Nam')) ...[
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 5, vertical: 2),
                          decoration: BoxDecoration(
                            color: Colors.red.withOpacity(0.18),
                            borderRadius: BorderRadius.circular(4),
                            border: Border.all(color: Colors.redAccent.withOpacity(0.4)),
                          ),
                          child: const Text(
                            "🇻🇳 Việt Nam",
                            style: TextStyle(color: Colors.redAccent, fontSize: 9.5, fontWeight: FontWeight.bold),
                          ),
                        ),
                        const SizedBox(width: 6),
                      ],
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.08),
                          borderRadius: BorderRadius.circular(4),
                          border: Border.all(color: Colors.amberAccent.withOpacity(0.3)),
                        ),
                        child: Text(
                          book.category,
                          style: const TextStyle(color: Colors.amberAccent, fontSize: 9.5, fontWeight: FontWeight.bold),
                        ),
                      ),
                      const SizedBox(width: 6),
                      const Icon(Icons.star_rounded, color: Colors.amber, size: 13),
                      const SizedBox(width: 2),
                      Text(
                        "${book.ratingAvg}",
                        style: const TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.bold),
                      ),
                      const Spacer(),
                      Icon(isAudio ? Icons.headset_rounded : Icons.menu_book_rounded, color: Colors.orangeAccent, size: 12),
                      const SizedBox(width: 3),
                      Text(
                        isAudio ? "Audio" : "EPUB",
                        style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 11),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// --- 3. MÀN HÌNH CHI TIẾT SÁCH (HỖ TRỢ ĐỌC, NGHE, TẢI OFFLINE & ĐÁNH GIÁ SAO) ---
class BookDetailScreen extends StatefulWidget {
  final Book book;
  final String username;

  const BookDetailScreen({
    super.key,
    required this.book,
    required this.username,
  });

  @override
  State<BookDetailScreen> createState() => _BookDetailScreenState();
}

class _BookDetailScreenState extends State<BookDetailScreen> {
  List<dynamic> _reviews = [];
  double _avgRating = 0.0;
  int _totalReviews = 0;
  bool _isLoadingReviews = true;

  @override
  void initState() {
    super.initState();
    _fetchReviews();
    OfflineManager().addListener(_onOfflineChanged);
  }

  @override
  void dispose() {
    OfflineManager().removeListener(_onOfflineChanged);
    super.dispose();
  }

  void _onOfflineChanged() {
    if (mounted) setState(() {});
  }

  bool get _isGuest {
    final u = widget.username.trim().toLowerCase();
    return u.isEmpty || u == 'guest' || u == 'null' || u.contains('khach');
  }

  bool get _isAdmin {
    return widget.username.trim().toLowerCase() == 'admin';
  }

  Future<void> _fetchReviews() async {
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}/api/books/${widget.book.id}/reviews');
      final res = await http.get(url).timeout(const Duration(seconds: 4));
      if (res.statusCode == 200) {
        final data = jsonDecode(utf8.decode(res.bodyBytes));
        if (mounted) {
          setState(() {
            _reviews = data['reviews'] ?? [];
            _avgRating = (data['average_rating'] as num?)?.toDouble() ?? 0.0;
            _totalReviews = data['total_reviews'] ?? 0;
            _isLoadingReviews = false;
          });
        }
      } else {
        if (mounted) setState(() => _isLoadingReviews = false);
      }
    } catch (_) {
      if (mounted) setState(() => _isLoadingReviews = false);
    }
  }

  Future<void> _deleteReview(int reviewId) async {
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}/api/reviews/$reviewId?username=${widget.username.trim()}');
      final res = await http.delete(url);
      if (!mounted) return;
      if (res.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Đã xóa đánh giá thành công!"), backgroundColor: Colors.green),
        );
        _fetchReviews();
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("Không thể xóa đánh giá!"), backgroundColor: Colors.redAccent),
        );
      }
    } catch (_) {}
  }

  void _showAddReviewModal() {
    if (_isGuest) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Vui lòng đăng nhập tài khoản để đánh giá sách!"),
          backgroundColor: Colors.orangeAccent,
        ),
      );
      return;
    }

    int selectedStars = 5;
    final commentCtrl = TextEditingController();
    bool isSubmitting = false;

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: const Color(0xFF1E1E1E),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (modalCtx) {
        return StatefulBuilder(
          builder: (sheetCtx, setModalState) {
            final starLabels = ["Rất tệ", "Tệ", "Bình thường", "Hay", "Tuyệt vời!"];

            return Padding(
              padding: EdgeInsets.only(
                left: 20,
                right: 20,
                top: 20,
                bottom: MediaQuery.of(sheetCtx).viewInsets.bottom + 20,
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  Container(
                    width: 40, height: 4,
                    decoration: BoxDecoration(color: Colors.white24, borderRadius: BorderRadius.circular(2)),
                  ),
                  const SizedBox(height: 16),
                  const Text(
                    "Đánh giá & Cảm nhận",
                    style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    widget.book.title,
                    style: const TextStyle(color: Colors.white70, fontSize: 14),
                    textAlign: TextAlign.center,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                  const SizedBox(height: 16),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: List.generate(5, (index) {
                      final starValue = index + 1;
                      return IconButton(
                        icon: Icon(
                          starValue <= selectedStars ? Icons.star_rounded : Icons.star_border_rounded,
                          color: Colors.amber,
                          size: 38,
                        ),
                        onPressed: () {
                          setModalState(() => selectedStars = starValue);
                        },
                      );
                    }),
                  ),
                  Text(
                    starLabels[selectedStars - 1],
                    style: const TextStyle(color: Colors.amber, fontWeight: FontWeight.bold, fontSize: 14),
                  ),
                  const SizedBox(height: 16),
                  TextField(
                    controller: commentCtrl,
                    maxLines: 3,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: "Hãy chia sẻ cảm nghĩ của bạn về tác phẩm này...",
                      hintStyle: const TextStyle(color: Colors.white38, fontSize: 13),
                      filled: true,
                      fillColor: Colors.black38,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                    ),
                  ),
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    height: 48,
                    child: ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.orange,
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                      onPressed: isSubmitting
                          ? null
                          : () async {
                              setModalState(() => isSubmitting = true);
                              try {
                                final url = Uri.parse('${ApiConfig.baseUrl}/api/books/${widget.book.id}/reviews');
                                final res = await http.post(
                                  url,
                                  headers: {'Content-Type': 'application/json'},
                                  body: jsonEncode({
                                    'book_id': widget.book.id,
                                    'username': widget.username.trim(),
                                    'rating': selectedStars,
                                    'comment': commentCtrl.text.trim(),
                                  }),
                                );
                                if (res.statusCode == 200) {
                                  if (modalCtx.mounted) Navigator.pop(modalCtx);
                                  if (mounted) {
                                    ScaffoldMessenger.of(context).showSnackBar(
                                      const SnackBar(
                                        content: Text("Gửi đánh giá thành công!"),
                                        backgroundColor: Colors.green,
                                      ),
                                    );
                                    _fetchReviews();
                                  }
                                } else {
                                  setModalState(() => isSubmitting = false);
                                  if (mounted) {
                                    ScaffoldMessenger.of(context).showSnackBar(
                                      const SnackBar(
                                        content: Text("Không thể gửi đánh giá, vui lòng thử lại!"),
                                        backgroundColor: Colors.redAccent,
                                      ),
                                    );
                                  }
                                }
                              } catch (e) {
                                setModalState(() => isSubmitting = false);
                                if (mounted) {
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    SnackBar(content: Text("Lỗi: $e"), backgroundColor: Colors.redAccent),
                                  );
                                }
                              }
                            },
                      child: isSubmitting
                          ? const SizedBox(width: 22, height: 22, child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2))
                          : const Text("Gửi Đánh Giá", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold, fontSize: 15)),
                    ),
                  ),
                ],
              ),
            );
          },
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final book = widget.book;
    final offlineMgr = OfflineManager();
    final isDownloaded = offlineMgr.isDownloaded(book.id);
    final isDownloading = offlineMgr.isDownloading(book.id);
    final downloadProgress = offlineMgr.getProgress(book.id);

    return Scaffold(
      backgroundColor: Colors.black,
      appBar: AppBar(
        title: Text(book.title),
        backgroundColor: Colors.black,
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Center(
              child: Container(
                height: 300,
                width: 200,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: const [
                    BoxShadow(color: Colors.black54, blurRadius: 10, offset: Offset(0, 5))
                  ],
                ),
                child: ClipRRect(
                  borderRadius: BorderRadius.circular(16),
                  child: book.imageUrl.isNotEmpty
                      ? Image.network(ApiConfig.formatUrl(book.imageUrl), fit: BoxFit.cover)
                      : Container(color: Colors.grey[800], child: const Icon(Icons.image, size: 80, color: Colors.white24)),
                ),
              ),
            ),
            const SizedBox(height: 24),
            Text(
              book.title,
              style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 8),
            GestureDetector(
              onTap: () {
                showAuthorProfileModal(context, book.author, [book]);
              },
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Icon(Icons.person_pin_rounded, color: Colors.orangeAccent, size: 18),
                  const SizedBox(width: 6),
                  Text(
                    "Tác giả: ${book.author}",
                    style: const TextStyle(
                      color: Colors.orangeAccent,
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                      decoration: TextDecoration.underline,
                    ),
                  ),
                ],
              ),
            ),

            // Category & Source Badges
            const SizedBox(height: 10),
            Wrap(
              alignment: WrapAlignment.center,
              spacing: 8,
              runSpacing: 6,
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.amber.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.amber.withOpacity(0.4)),
                  ),
                  child: Text(
                    book.category,
                    style: const TextStyle(color: Colors.amberAccent, fontSize: 12, fontWeight: FontWeight.bold),
                  ),
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                  decoration: BoxDecoration(
                    color: Colors.blueAccent.withOpacity(0.15),
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.blueAccent.withOpacity(0.4)),
                  ),
                  child: Text(
                    book.source,
                    style: const TextStyle(color: Colors.lightBlueAccent, fontSize: 12),
                  ),
                ),
              ],
            ),

            // Rating Stars Summary
            const SizedBox(height: 12),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ...List.generate(5, (index) {
                  return Icon(
                    index < _avgRating.round() ? Icons.star_rounded : Icons.star_border_rounded,
                    color: Colors.amber,
                    size: 20,
                  );
                }),
                const SizedBox(width: 8),
                Text(
                  _avgRating > 0 ? _avgRating.toStringAsFixed(1) : "Chưa có sao",
                  style: const TextStyle(color: Colors.amber, fontWeight: FontWeight.bold, fontSize: 14),
                ),
                const SizedBox(width: 4),
                Text(
                  "($_totalReviews)",
                  style: const TextStyle(color: Colors.white54, fontSize: 13),
                ),
              ],
            ),

            const SizedBox(height: 16),
            if (book.description.isNotEmpty)
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 10),
                child: Text(
                  book.description,
                  style: TextStyle(color: Colors.white.withOpacity(0.8), fontSize: 14, height: 1.5),
                  textAlign: TextAlign.center,
                ),
              ),
            const SizedBox(height: 24),

            // --- NÚT ĐỌC SÁCH ---
            if (book.pdfUrl.isNotEmpty) ...[
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.orangeAccent,
                  foregroundColor: Colors.white,
                  minimumSize: const Size(double.infinity, 50),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                icon: Icon(
                  book.pdfUrl.toLowerCase().endsWith('.epub') ? Icons.chrome_reader_mode_rounded : Icons.picture_as_pdf_rounded,
                  color: Colors.white,
                ),
                label: Text(
                  book.pdfUrl.toLowerCase().endsWith('.epub') ? "Đọc Sách EPUB (Chia chương chuẩn)" : "Đọc Sách PDF (Bản in ấn)",
                  style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
                onPressed: () {
                  final correctedPdfUrl = ApiConfig.formatUrl(book.pdfUrl);
                  BookReaderHelper.openBook(
                    context: context,
                    fileUrl: correctedPdfUrl,
                    bookTitle: book.title,
                    author: book.author,
                    bookId: book.id,
                    username: widget.username,
                  );
                },
              ),
              const SizedBox(height: 10),
              if (book.pdfUrl.toLowerCase().endsWith('.pdf')) ...[
                OutlinedButton.icon(
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Colors.orangeAccent,
                    side: const BorderSide(color: Colors.orangeAccent, width: 1.2),
                    minimumSize: const Size(double.infinity, 44),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  icon: const Icon(Icons.chrome_reader_mode_rounded, color: Colors.orangeAccent, size: 18),
                  label: const Text(
                    "Đọc Bản EPUB (Chia chương điện tử)",
                    style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                  ),
                  onPressed: () {
                    final epubUrl = ApiConfig.formatUrl(book.pdfUrl.replaceAll('.pdf', '.epub'));
                    BookReaderHelper.openBook(
                      context: context,
                      fileUrl: epubUrl,
                      bookTitle: book.title,
                      author: book.author,
                      bookId: book.id,
                      username: widget.username,
                    );
                  },
                ),
                const SizedBox(height: 10),
              ] else if (book.pdfUrl.toLowerCase().endsWith('.epub')) ...[
                OutlinedButton.icon(
                  style: OutlinedButton.styleFrom(
                    foregroundColor: Colors.orangeAccent,
                    side: const BorderSide(color: Colors.orangeAccent, width: 1.2),
                    minimumSize: const Size(double.infinity, 44),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  ),
                  icon: const Icon(Icons.picture_as_pdf_rounded, color: Colors.orangeAccent, size: 18),
                  label: const Text(
                    "Đọc Bản PDF (Định dạng in ấn)",
                    style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                  ),
                  onPressed: () {
                    final pdfUrl = ApiConfig.formatUrl(book.pdfUrl.replaceAll('.epub', '.pdf'));
                    BookReaderHelper.openBook(
                      context: context,
                      fileUrl: pdfUrl,
                      bookTitle: book.title,
                      author: book.author,
                      bookId: book.id,
                      username: widget.username,
                    );
                  },
                ),
                const SizedBox(height: 10),
              ],
            ] else ...[
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.orangeAccent,
                  foregroundColor: Colors.white,
                  minimumSize: const Size(double.infinity, 50),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                icon: const Icon(Icons.chrome_reader_mode_rounded, color: Colors.white),
                label: const Text(
                  "Đọc Bản Văn Bản Thuần",
                  style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                ),
                onPressed: () {
                  BookReaderHelper.openBook(
                    context: context,
                    fileUrl: '',
                    bookTitle: book.title,
                    author: book.author,
                    bookId: book.id,
                    username: widget.username,
                  );
                },
              ),
              const SizedBox(height: 12),
            ],

            // --- NÚT NGHE SÁCH NÓI ---
            if (book.audioUrl.isNotEmpty) ...[
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.grey[900],
                  foregroundColor: Colors.orangeAccent,
                  side: const BorderSide(color: Colors.orangeAccent, width: 1.5),
                  minimumSize: const Size(double.infinity, 50),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                icon: const Icon(Icons.audiotrack, color: Colors.orangeAccent),
                label: const Text("Nghe Sách Nói (Audiobook)", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                onPressed: () {
                  final correctedAudioUrl = ApiConfig.formatUrl(book.audioUrl);
                  AudioPlayerService().playBook(
                    bookId: book.id,
                    title: book.title,
                    author: book.author,
                    audioUrl: correctedAudioUrl,
                    coverUrl: ApiConfig.formatUrl(book.imageUrl),
                  );
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => const AudioPlayerScreen(),
                    ),
                  );
                },
              ),
              const SizedBox(height: 12),
            ],

            // --- NÚT TẢI NGOẠI TUYẾN (OFFLINE DOWNLOAD MANAGER) ---
            Container(
              width: double.infinity,
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.05),
                borderRadius: BorderRadius.circular(14),
                border: Border.all(
                  color: isDownloaded ? Colors.greenAccent.withOpacity(0.3) : Colors.white12,
                ),
              ),
              child: isDownloading
                  ? Column(
                      children: [
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            const Text(
                              "Đang tải về máy...",
                              style: TextStyle(color: Colors.orangeAccent, fontSize: 13, fontWeight: FontWeight.bold),
                            ),
                            Text(
                              "${(downloadProgress * 100).toInt()}%",
                              style: const TextStyle(color: Colors.orangeAccent, fontSize: 13, fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                        const SizedBox(height: 8),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(4),
                          child: LinearProgressIndicator(
                            value: downloadProgress,
                            backgroundColor: Colors.white12,
                            valueColor: const AlwaysStoppedAnimation<Color>(Colors.orangeAccent),
                          ),
                        ),
                      ],
                    )
                  : isDownloaded
                      ? Row(
                          children: [
                            const Icon(Icons.check_circle_rounded, color: Colors.greenAccent, size: 22),
                            const SizedBox(width: 8),
                            const Expanded(
                              child: Text(
                                "Đã lưu ngoại tuyến",
                                style: TextStyle(color: Colors.greenAccent, fontWeight: FontWeight.bold, fontSize: 13),
                              ),
                            ),
                            TextButton.icon(
                              onPressed: () async {
                                await offlineMgr.deleteOfflineBook(book.id);
                                if (!context.mounted) return;
                                ScaffoldMessenger.of(context).showSnackBar(
                                  const SnackBar(content: Text("Đã xóa sách ngoại tuyến khỏi máy")),
                                );
                              },
                              icon: const Icon(Icons.delete_outline, color: Colors.redAccent, size: 18),
                              label: const Text("Xóa tải về", style: TextStyle(color: Colors.redAccent, fontSize: 12)),
                            ),
                          ],
                        )
                      : OutlinedButton.icon(
                          style: OutlinedButton.styleFrom(
                            side: const BorderSide(color: Colors.white24),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                            padding: const EdgeInsets.symmetric(vertical: 12),
                          ),
                          onPressed: () async {
                            if (kIsWeb) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                const SnackBar(
                                  content: Text("Tính năng tải về ngoại tuyến được tối ưu cho Android/iOS. Trên Web bạn có thể đọc và nghe trực tiếp mượt mà!"),
                                  backgroundColor: Colors.blueGrey,
                                ),
                              );
                              return;
                            }
                            final success = await offlineMgr.downloadBook(
                              bookId: book.id,
                              title: book.title,
                              author: book.author,
                              imageUrl: book.imageUrl,
                              pdfUrl: book.pdfUrl,
                              audioUrl: book.audioUrl,
                              description: book.description,
                              isAudioOnly: book.pdfUrl.isEmpty && book.audioUrl.isNotEmpty,
                            );
                            if (!context.mounted) return;
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text(success ? "Đã tải về thành công! Giờ bạn có thể đọc offline." : "Tải sách thất bại, vui lòng thử lại."),
                                backgroundColor: success ? Colors.green : Colors.redAccent,
                              ),
                            );
                          },
                          icon: const Icon(Icons.download_for_offline_rounded, color: Colors.white70),
                          label: const Text(
                            "Tải về đọc Ngoại Tuyến (Offline)",
                            style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                          ),
                        ),
            ),

            const SizedBox(height: 30),
            const Divider(color: Colors.white12),
            const SizedBox(height: 16),

            // --- KHU VỰC ĐÁNH GIÁ & BÌNH LUẬN (MODULE 7) ---
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      "Đánh giá & Nhận xét",
                      style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                    ),
                    Text(
                      "$_totalReviews lượt đánh giá từ độc giả",
                      style: const TextStyle(color: Colors.white54, fontSize: 12),
                    ),
                  ],
                ),
                ElevatedButton.icon(
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.orange.withOpacity(0.15),
                    foregroundColor: Colors.orangeAccent,
                    side: const BorderSide(color: Colors.orangeAccent),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                  ),
                  onPressed: _showAddReviewModal,
                  icon: const Icon(Icons.rate_review_rounded, size: 16),
                  label: const Text("Viết đánh giá", style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                ),
              ],
            ),
            const SizedBox(height: 16),

            if (_isLoadingReviews)
              const Center(child: Padding(padding: EdgeInsets.all(20), child: CircularProgressIndicator(color: Colors.orange)))
            else if (_reviews.isEmpty)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.03),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  children: const [
                    Icon(Icons.star_border_rounded, color: Colors.white24, size: 40),
                    SizedBox(height: 8),
                    Text(
                      "Chưa có đánh giá nào cho cuốn sách này.\nHãy là người đầu tiên chia sẻ cảm nhận!",
                      style: TextStyle(color: Colors.white54, fontSize: 13),
                      textAlign: TextAlign.center,
                    ),
                  ],
                ),
              )
            else
              ListView.separated(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                itemCount: _reviews.length,
                separatorBuilder: (context, index) => const SizedBox(height: 10),
                itemBuilder: (context, index) {
                  final r = _reviews[index];
                  final isOwn = r['username'] == widget.username.trim() || _isAdmin;
                  return Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.04),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(color: Colors.white.withOpacity(0.05)),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          children: [
                            CircleAvatar(
                              radius: 16,
                              backgroundColor: Colors.orangeAccent.withOpacity(0.2),
                              backgroundImage: (r['avatar_url'] != null && (r['avatar_url'] as String).isNotEmpty)
                                  ? NetworkImage(ApiConfig.formatUrl(r['avatar_url']))
                                  : null,
                              child: (r['avatar_url'] == null || (r['avatar_url'] as String).isEmpty)
                                  ? Text(
                                      (r['username'] != null && (r['username'] as String).isNotEmpty)
                                          ? r['username'][0].toUpperCase()
                                          : 'U',
                                      style: const TextStyle(color: Colors.orangeAccent, fontSize: 12, fontWeight: FontWeight.bold),
                                    )
                                  : null,
                            ),
                            const SizedBox(width: 10),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    r['full_name'] != null && (r['full_name'] as String).isNotEmpty
                                        ? r['full_name']
                                        : r['username'],
                                    style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13),
                                  ),
                                  Row(
                                    children: [
                                      ...List.generate(5, (starIdx) {
                                        return Icon(
                                          starIdx < (r['rating'] ?? 0) ? Icons.star_rounded : Icons.star_border_rounded,
                                          color: Colors.amber,
                                          size: 14,
                                        );
                                      }),
                                      const SizedBox(width: 6),
                                      Text(
                                        r['created_at'] != null ? r['created_at'].toString().split(' ')[0] : '',
                                        style: const TextStyle(color: Colors.white38, fontSize: 11),
                                      ),
                                    ],
                                  ),
                                ],
                              ),
                            ),
                            if (isOwn)
                              IconButton(
                                icon: const Icon(Icons.delete_outline, color: Colors.white38, size: 18),
                                onPressed: () => _deleteReview(r['id']),
                              ),
                          ],
                        ),
                        if (r['comment'] != null && (r['comment'] as String).isNotEmpty) ...[
                          const SizedBox(height: 8),
                          Text(
                            r['comment'],
                            style: const TextStyle(color: Colors.white70, fontSize: 13, height: 1.4),
                          ),
                        ],
                      ],
                    ),
                  );
                },
              ),
            const SizedBox(height: 30),
          ],
        ),
      ),
    );
  }
}

// --- 4. TRÌNH PHÁT SÁCH AUDIO PLAYER ---
class SimpleAudioPlayerScreen extends StatefulWidget {
  final Book book;
  const SimpleAudioPlayerScreen({super.key, required this.book});

  @override
  State<SimpleAudioPlayerScreen> createState() => _SimpleAudioPlayerScreenState();
}

class _SimpleAudioPlayerScreenState extends State<SimpleAudioPlayerScreen> {
  late AudioPlayer _audioPlayer;
  bool isPlaying = false;
  Duration _duration = Duration.zero;
  Duration _position = Duration.zero;
  bool _isLoading = true;
  String _errorMessage = "";

  @override
  void initState() {
    super.initState();
    _initAudioPlayer();
  }

  Future<void> _initAudioPlayer() async {
    _audioPlayer = AudioPlayer();
    _audioPlayer.onPlayerStateChanged.listen((state) { if (mounted) setState(() => isPlaying = state == PlayerState.playing); });
    _audioPlayer.onDurationChanged.listen((newDuration) { if (mounted) setState(() => _duration = newDuration); });
    _audioPlayer.onPositionChanged.listen((newPosition) { if (mounted) setState(() => _position = newPosition); });
    try {
      await _audioPlayer.setSource(UrlSource(ApiConfig.formatUrl(widget.book.audioUrl)));
      if (mounted) setState(() => _isLoading = false);
    } catch (e) {
      if (mounted) setState(() { _isLoading = false; _errorMessage = e.toString(); });
    }
  }

  @override
  void dispose() { _audioPlayer.dispose(); super.dispose(); }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[950],
      appBar: AppBar(title: const Text("Trình Phát Sách Nói", style: TextStyle(color: Colors.white)), backgroundColor: Colors.transparent, elevation: 0),
      body: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(20),
              child: widget.book.imageUrl.isNotEmpty ? Image.network(ApiConfig.formatUrl(widget.book.imageUrl), height: 240, width: 240, fit: BoxFit.cover) : Container(height: 240, width: 240, color: Colors.grey[800], child: const Icon(Icons.music_note, size: 80, color: Colors.orange)),
            ),
            const SizedBox(height: 30),
            Text(widget.book.title, style: const TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
            Text(widget.book.author, style: const TextStyle(color: Colors.white70, fontSize: 16)),
            const SizedBox(height: 40),
            if (_isLoading) const CircularProgressIndicator(color: Colors.orangeAccent)
            else if (_errorMessage.isNotEmpty) Text("Lỗi: $_errorMessage", style: const TextStyle(color: Colors.redAccent)),
            Slider(
              min: 0, max: _duration.inMilliseconds.toDouble() > 0 ? _duration.inMilliseconds.toDouble() : 1.0,
              value: _position.inMilliseconds.toDouble().clamp(0.0, _duration.inMilliseconds.toDouble() > 0 ? _duration.inMilliseconds.toDouble() : 1.0),
              activeColor: Colors.orangeAccent, inactiveColor: Colors.white24,
              onChanged: (value) async { await _audioPlayer.seek(Duration(milliseconds: value.toInt())); },
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton(icon: const Icon(Icons.replay_10, size: 36, color: Colors.white), onPressed: () async { final p = _position - const Duration(seconds: 10); await _audioPlayer.seek(p < Duration.zero ? Duration.zero : p); }),
                const SizedBox(width: 20),
                CircleAvatar(radius: 35, backgroundColor: Colors.orangeAccent, child: IconButton(icon: Icon(isPlaying ? Icons.pause : Icons.play_arrow, size: 36, color: Colors.white), onPressed: () async { if (isPlaying) { await _audioPlayer.pause(); } else { await _audioPlayer.resume(); } })),
                const SizedBox(width: 20),
                IconButton(icon: const Icon(Icons.forward_10, size: 36, color: Colors.white), onPressed: () async { final p = _position + const Duration(seconds: 10); await _audioPlayer.seek(p > _duration ? _duration : p); }),
              ],
            )
          ],
        ),
      ),
    );
  }
}

// --- 5. CLASS CHÍNH MAIN SCREEN ĐIỀU HƯỚNG ---
class MainScreen extends StatefulWidget {
  final String username;
  final bool isAdmin;

  const MainScreen({super.key, required this.username, this.isAdmin = false});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0;

  @override
  Widget build(BuildContext context) {
    final List<Widget> tabs = [
      HomeScreen(username: widget.username),
      BookShelfScreen(username: widget.username, isAdmin: widget.isAdmin),
      ExploreScreen(username: widget.username, isAdmin: widget.isAdmin),
      ProfileScreen(username: widget.username, isAdmin: widget.isAdmin),
    ];

    return AnnotatedRegion<SystemUiOverlayStyle>(
      value: const SystemUiOverlayStyle(
        statusBarColor: Colors.transparent,
        statusBarIconBrightness: Brightness.dark,
        statusBarBrightness: Brightness.light,
        systemNavigationBarColor: Colors.black,
        systemNavigationBarIconBrightness: Brightness.light,
        systemNavigationBarDividerColor: Colors.transparent,
      ),
      child: Scaffold(
        backgroundColor: Colors.black,
        appBar: _currentIndex == 0
            ? AppBar(
          title: const Text(
              "Thư Viện Sách & Audio",
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16, letterSpacing: 0.5, fontFamily: 'serif')
          ),
          backgroundColor: Colors.black,
          foregroundColor: Colors.white,
          elevation: 0,
          centerTitle: true,
          actions: [
            IconButton(
              icon: const Icon(Icons.notifications_none_rounded, color: Colors.white, size: 22),
              onPressed: () {},
            ),
          ],
          systemOverlayStyle: const SystemUiOverlayStyle(
            statusBarColor: Colors.black,
            statusBarIconBrightness: Brightness.light,
            statusBarBrightness: Brightness.dark,
          ),
        )
            : null,
        body: IndexedStack(
          index: _currentIndex,
          children: tabs,
        ),
        bottomNavigationBar: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const MiniAudioPlayer(),
            BottomNavigationBar(
              backgroundColor: Colors.black,
              selectedItemColor: Colors.orangeAccent,
              unselectedItemColor: Colors.white60,
              currentIndex: _currentIndex,
              onTap: (index) {
                setState(() {
                  _currentIndex = index;
                });
              },
              type: BottomNavigationBarType.fixed,
              selectedLabelStyle: const TextStyle(fontWeight: FontWeight.bold, fontSize: 11),
              unselectedLabelStyle: const TextStyle(fontSize: 11),
              items: const [
                BottomNavigationBarItem(icon: Icon(Icons.home_rounded), label: "Trang chủ"),
                BottomNavigationBarItem(icon: Icon(Icons.library_books_rounded), label: "Kệ sách"),
                BottomNavigationBarItem(icon: Icon(Icons.explore_rounded), label: "Khám phá"),
                BottomNavigationBarItem(icon: Icon(Icons.person_rounded), label: "Cá nhân"),
              ],
            ),
          ],
        ),
      ),
    );
  }
}