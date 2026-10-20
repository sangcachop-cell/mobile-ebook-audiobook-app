// admin_online_books_screen.dart
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'api_config.dart';

class AdminOnlineBooksScreen extends StatefulWidget {
  final String adminUsername;
  const AdminOnlineBooksScreen({super.key, required this.adminUsername});

  @override
  State<AdminOnlineBooksScreen> createState() => _AdminOnlineBooksScreenState();
}

class _AdminOnlineBooksScreenState extends State<AdminOnlineBooksScreen> {
  final TextEditingController _searchCtrl = TextEditingController(text: "Sherlock Holmes");
  String _selectedSource = "all"; // all, gutendex, librivox, openlibrary
  bool _isLoading = false;
  List<dynamic> _onlineBooks = [];
  final Set<String> _importedExternalIds = {};
  final Set<String> _importingIds = {};

  final List<Map<String, String>> _sources = [
    {"id": "all", "label": "Tất cả các nguồn", "icon": "🌐"},
    {"id": "gutendex", "label": "Gutendex (EPUB)", "icon": "📖"},
    {"id": "librivox", "label": "LibriVox (Audio)", "icon": "🎧"},
    {"id": "openlibrary", "label": "Open Library", "icon": "📚"},
  ];

  final List<String> _suggestedTopics = [
    "Sherlock Holmes",
    "Pride and Prejudice",
    "Adventure",
    "Philosophy",
    "Science",
    "History",
    "Children",
    "Economics",
  ];

  @override
  void initState() {
    super.initState();
    _performSearch();
  }

  @override
  void dispose() {
    _searchCtrl.dispose();
    super.dispose();
  }

  Future<void> _performSearch() async {
    final query = _searchCtrl.text.trim();
    if (query.isEmpty) return;

    setState(() => _isLoading = true);

    final url = Uri.parse(
      '${ApiConfig.baseUrl}/api/admin/online-books/search?query=${Uri.encodeComponent(query)}&source=$_selectedSource',
    );

    try {
      final response = await http.get(url).timeout(const Duration(seconds: 25));
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(utf8.decode(response.bodyBytes));
        if (mounted) {
          setState(() {
            _onlineBooks = data;
            _isLoading = false;
          });
        }
      } else {
        if (mounted) {
          setState(() => _isLoading = false);
          _showSnackBar("Không thể tìm kiếm sách online (${response.statusCode})", Colors.redAccent);
        }
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isLoading = false);
        _showSnackBar("Lỗi kết nối khi tìm kiếm: $e", Colors.redAccent);
      }
    }
  }

  Future<void> _importBook(Map<String, dynamic> bookItem) async {
    final extId = bookItem['external_id'] ?? '';
    if (extId.isNotEmpty) {
      setState(() => _importingIds.add(extId));
    }

    final url = Uri.parse('${ApiConfig.baseUrl}/api/admin/online-books/import');
    final payload = {
      "username": widget.adminUsername,
      "title": bookItem['title'] ?? 'Sách mới',
      "author": bookItem['author'] ?? 'Nhiều tác giả',
      "category": bookItem['category'] ?? 'Văn học & Tiểu thuyết',
      "content": bookItem['description'] ?? '',
      "image_url": bookItem['image_url'] ?? '',
      "pdf_url": bookItem['pdf_url'] ?? '',
      "audio_url": bookItem['audio_url'] ?? '',
      "source": bookItem['source'] ?? 'Project Gutenberg & LibriVox',
      "external_id": extId,
      "rating_avg": (bookItem['rating_avg'] != null) ? (bookItem['rating_avg'] as num).toDouble() : 4.8,
      "review_count": bookItem['review_count'] ?? 30,
    };

    try {
      final response = await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode(payload),
      );

      if (response.statusCode == 200) {
        final res = jsonDecode(utf8.decode(response.bodyBytes));
        if (mounted) {
          setState(() {
            _importingIds.remove(extId);
            _importedExternalIds.add(extId);
            bookItem['already_in_db'] = true;
          });
          _showSnackBar(res['message'] ?? "Đã nhập sách thành công!", Colors.green);
        }
      } else {
        if (mounted) {
          setState(() => _importingIds.remove(extId));
          _showSnackBar("Nhập sách thất bại (${response.statusCode})", Colors.redAccent);
        }
      }
    } catch (e) {
      if (mounted) {
        setState(() => _importingIds.remove(extId));
        _showSnackBar("Lỗi kết nối khi nhập sách: $e", Colors.redAccent);
      }
    }
  }

  void _showSnackBar(String msg, Color bg) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(msg), backgroundColor: bg, duration: const Duration(seconds: 3)),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: Stack(
        children: [
          // Background Glow
          Positioned(
            top: -100,
            left: -50,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.orange.withOpacity(0.12),
              ),
            ),
          ),
          Positioned(
            bottom: -50,
            right: -50,
            child: Container(
              width: 250,
              height: 250,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Colors.blueAccent.withOpacity(0.08),
              ),
            ),
          ),

          SafeArea(
            child: Column(
              children: [
                // Header Bar
                _buildHeaderBar(),

                // Search Bar & Filter Chips
                _buildSearchBar(),

                // Source Tabs
                _buildSourceChips(),

                // Suggestions
                _buildSuggestedTopics(),

                const SizedBox(height: 6),

                // Content List
                Expanded(
                  child: _isLoading
                      ? const Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              CircularProgressIndicator(color: Colors.orange),
                              SizedBox(height: 16),
                              Text(
                                "Đang tìm kiếm trên Gutendex, LibriVox & Open Library...",
                                style: TextStyle(color: Colors.white70, fontSize: 13),
                              ),
                            ],
                          ),
                        )
                      : _onlineBooks.isEmpty
                          ? _buildEmptyState()
                          : _buildBookList(),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeaderBar() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Row(
        children: [
          IconButton(
            icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white, size: 20),
            onPressed: () => Navigator.pop(context),
          ),
          const SizedBox(width: 4),
          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "Khám Phá & Tải Sách Online",
                  style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                ),
                Text(
                  "Gutendex (EPUB) • LibriVox (Audio) • Open Library",
                  style: TextStyle(color: Colors.orangeAccent, fontSize: 11),
                ),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.08),
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: Colors.orange.withOpacity(0.3)),
            ),
            child: const Row(
              children: [
                Icon(Icons.cloud_download_rounded, color: Colors.orange, size: 16),
                SizedBox(width: 4),
                Text("Admin", style: TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSearchBar() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      child: Container(
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.08),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.white24),
        ),
        child: TextField(
          controller: _searchCtrl,
          style: const TextStyle(color: Colors.white, fontSize: 14),
          textInputAction: TextInputAction.search,
          onSubmitted: (_) => _performSearch(),
          decoration: InputDecoration(
            hintText: "Nhập tên sách, tác giả hoặc chủ đề...",
            hintStyle: const TextStyle(color: Colors.white38, fontSize: 13),
            prefixIcon: const Icon(Icons.search_rounded, color: Colors.orange, size: 22),
            suffixIcon: IconButton(
              icon: const Icon(Icons.send_rounded, color: Colors.orangeAccent, size: 20),
              onPressed: _performSearch,
            ),
            border: InputBorder.none,
            contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
          ),
        ),
      ),
    );
  }

  Widget _buildSourceChips() {
    return SizedBox(
      height: 42,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
        itemCount: _sources.length,
        itemBuilder: (context, index) {
          final s = _sources[index];
          final isSelected = _selectedSource == s['id'];
          return GestureDetector(
            onTap: () {
              setState(() => _selectedSource = s['id']!);
              _performSearch();
            },
            child: Container(
              margin: const EdgeInsets.only(right: 8),
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: isSelected ? Colors.orange : Colors.white.withOpacity(0.06),
                borderRadius: BorderRadius.circular(20),
                border: Border.all(color: isSelected ? Colors.orange : Colors.white24),
              ),
              child: Row(
                children: [
                  Text(s['icon']!, style: const TextStyle(fontSize: 12)),
                  const SizedBox(width: 6),
                  Text(
                    s['label']!,
                    style: TextStyle(
                      color: isSelected ? Colors.black : Colors.white,
                      fontSize: 12,
                      fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildSuggestedTopics() {
    return SizedBox(
      height: 32,
      child: ListView.builder(
        scrollDirection: Axis.horizontal,
        padding: const EdgeInsets.symmetric(horizontal: 16),
        itemCount: _suggestedTopics.length,
        itemBuilder: (context, index) {
          final topic = _suggestedTopics[index];
          return GestureDetector(
            onTap: () {
              _searchCtrl.text = topic;
              _performSearch();
            },
            child: Container(
              margin: const EdgeInsets.only(right: 6),
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.04),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Colors.white12),
              ),
              child: Text(
                "#$topic",
                style: const TextStyle(color: Colors.white60, fontSize: 11),
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildBookList() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(18, 10, 18, 6),
          child: Text(
            "Tìm thấy ${_onlineBooks.length} kết quả từ cơ sở dữ liệu mở",
            style: const TextStyle(color: Colors.white54, fontSize: 12),
          ),
        ),
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
            itemCount: _onlineBooks.length,
            itemBuilder: (context, index) {
              final b = _onlineBooks[index];
              return _buildOnlineBookCard(b);
            },
          ),
        ),
      ],
    );
  }

  Widget _buildOnlineBookCard(Map<String, dynamic> b) {
    final extId = b['external_id'] ?? '';
    final isAlreadyInDb = b['already_in_db'] == true || _importedExternalIds.contains(extId);
    final isImporting = _importingIds.contains(extId);

    final title = b['title'] ?? 'Không có tiêu đề';
    final author = b['author'] ?? 'Chưa rõ tác giả';
    final category = b['category'] ?? 'Văn học & Tiểu thuyết';
    final imageUrl = b['image_url'] ?? '';
    final source = b['source'] ?? 'Mở';
    final hasEbook = b['has_ebook'] == true || (b['pdf_url'] != null && (b['pdf_url'] as String).isNotEmpty);
    final hasAudio = b['has_audio'] == true || (b['audio_url'] != null && (b['audio_url'] as String).isNotEmpty);
    final description = b['description'] ?? '';

    return Container(
      margin: const EdgeInsets.only(bottom: 14),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.06),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: isAlreadyInDb ? Colors.green.withOpacity(0.4) : Colors.white12,
        ),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Cover
          ClipRRect(
            borderRadius: BorderRadius.circular(10),
            child: SizedBox(
              width: 80,
              height: 115,
              child: imageUrl.isNotEmpty
                  ? Image.network(
                      ApiConfig.formatUrl(imageUrl),
                      fit: BoxFit.cover,
                      errorBuilder: (_, __, ___) => Container(
                        color: Colors.grey[900],
                        child: const Icon(Icons.book_rounded, color: Colors.white24, size: 36),
                      ),
                    )
                  : Container(
                      color: Colors.grey[900],
                      child: const Icon(Icons.book_rounded, color: Colors.white24, size: 36),
                    ),
            ),
          ),
          const SizedBox(width: 14),

          // Details & Actions
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // Title
                Text(
                  title,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14),
                ),
                const SizedBox(height: 3),

                // Author
                Text(
                  author,
                  style: const TextStyle(color: Colors.orangeAccent, fontSize: 12, fontWeight: FontWeight.w500),
                ),
                const SizedBox(height: 6),

                // Badges Row
                Wrap(
                  spacing: 6,
                  runSpacing: 4,
                  children: [
                    _buildSmallBadge(category, Colors.amberAccent),
                    if (hasEbook) _buildSmallBadge("📖 EPUB", Colors.cyanAccent),
                    if (hasAudio) _buildSmallBadge("🎧 Audio MP3", Colors.lightGreenAccent),
                    _buildSmallBadge(source, Colors.white54),
                  ],
                ),
                const SizedBox(height: 8),

                if (description.isNotEmpty)
                  Text(
                    description,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(color: Colors.white60, fontSize: 11, height: 1.3),
                  ),
                const SizedBox(height: 10),

                // Action Button
                Align(
                  alignment: Alignment.centerRight,
                  child: isAlreadyInDb
                      ? Container(
                          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                          decoration: BoxDecoration(
                            color: Colors.green.withOpacity(0.15),
                            borderRadius: BorderRadius.circular(20),
                            border: Border.all(color: Colors.greenAccent.withOpacity(0.5)),
                          ),
                          child: const Row(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Icon(Icons.check_circle_rounded, color: Colors.greenAccent, size: 16),
                              SizedBox(width: 6),
                              Text(
                                "Đã có trong kho thư viện",
                                style: TextStyle(color: Colors.greenAccent, fontSize: 11, fontWeight: FontWeight.bold),
                              ),
                            ],
                          ),
                        )
                      : ElevatedButton.icon(
                          onPressed: isImporting ? null : () => _importBook(b),
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.orange,
                            foregroundColor: Colors.black,
                            padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
                            elevation: 0,
                          ),
                          icon: isImporting
                              ? const SizedBox(
                                  width: 14,
                                  height: 14,
                                  child: CircularProgressIndicator(strokeWidth: 2, color: Colors.black),
                                )
                              : const Icon(Icons.add_rounded, size: 18),
                          label: Text(
                            isImporting ? "Đang tải..." : "Tải vào Thư viện",
                            style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                          ),
                        ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSmallBadge(String text, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 2),
      decoration: BoxDecoration(
        color: color.withOpacity(0.12),
        borderRadius: BorderRadius.circular(6),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Text(
        text,
        style: TextStyle(color: color, fontSize: 9.5, fontWeight: FontWeight.bold),
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(Icons.search_off_rounded, size: 60, color: Colors.white.withOpacity(0.2)),
            const SizedBox(height: 16),
            const Text(
              "Không tìm thấy sách phù hợp",
              style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            const Text(
              "Thử tìm bằng từ khóa tiếng Anh hoặc chọn nguồn Gutendex / LibriVox khác.",
              style: TextStyle(color: Colors.white54, fontSize: 12),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
