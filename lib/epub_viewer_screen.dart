// epub_viewer_screen.dart
import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:epub_view/epub_view.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'api_config.dart';
import 'progress_service.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'audio_player_service.dart';
import 'audio_player_screen.dart';
import 'content_reader_screen.dart';

// Fallback EPUB từ Gutenberg (luôn hoạt động - Pride and Prejudice)
const String _kFallbackEpubUrl =
    'https://www.gutenberg.org/ebooks/1342.epub3.images';

enum ReaderThemeMode { light, sepia, dark }

class EpubViewerScreen extends StatefulWidget {
  final String epubUrl;
  final String bookTitle;
  final int bookId;
  final String username;

  const EpubViewerScreen({
    super.key,
    required this.epubUrl,
    required this.bookTitle,
    required this.bookId,
    required this.username,
  });

  @override
  State<EpubViewerScreen> createState() => _EpubViewerScreenState();
}

class _EpubViewerScreenState extends State<EpubViewerScreen> {
  EpubController? _epubController;
  bool _isLoading = true;
  String _errorMessage = '';
  ReaderThemeMode _currentTheme = ReaderThemeMode.light;
  double _fontSize = 16.0;
  Timer? _autoSaveTimer;

  bool get _isGuest {
    final u = widget.username.trim().toLowerCase();
    return u.isEmpty || u == 'guest' || u == 'null' || u.contains('khach');
  }

  @override
  void initState() {
    super.initState();
    _loadReaderPreferences();
    _loadEpub();
    // Tự động lưu tiến độ định kỳ mỗi 10 giây theo tài liệu đặc tả
    _autoSaveTimer = Timer.periodic(const Duration(seconds: 10), (_) => _saveProgress());
  }

  Future<void> _loadReaderPreferences() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedTheme = prefs.getString('reader_theme_mode');
      final savedSize = prefs.getDouble('reader_font_size');
      if (mounted) {
        setState(() {
          if (savedTheme == 'dark') {
            _currentTheme = ReaderThemeMode.dark;
          } else if (savedTheme == 'sepia') {
            _currentTheme = ReaderThemeMode.sepia;
          } else if (savedTheme == 'light') {
            _currentTheme = ReaderThemeMode.light;
          }
          if (savedSize != null && savedSize >= 12 && savedSize <= 26) {
            _fontSize = savedSize;
          }
        });
      }
    } catch (_) {}
  }

  Future<void> _saveReaderPreferences() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('reader_theme_mode', _currentTheme.name);
      await prefs.setDouble('reader_font_size', _fontSize);
    } catch (_) {}
  }

  // Tải bytes từ URL với retry và User-Agent header để tránh bị Gutenberg block
  Future<Uint8List?> _fetchEpubBytes(String url) async {
    if (url.isEmpty) return null;
    final headers = {
      'User-Agent':
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) BookHub/2026 Flutter/EPUB-Reader',
      'Accept': 'application/epub+zip, application/octet-stream, */*',
    };
    for (int attempt = 1; attempt <= 2; attempt++) {
      try {
        final response = await http
            .get(Uri.parse(url), headers: headers)
            .timeout(const Duration(seconds: 25));
        if (response.statusCode == 200 && response.bodyBytes.isNotEmpty) {
          return response.bodyBytes;
        }
        // Nếu server trả về lỗi 4xx/5xx thì không ném exception mà trả về null để thử nguồn kế tiếp
        if (response.statusCode >= 400) {
          debugPrint('>>> Không tải được từ $url: HTTP ${response.statusCode}');
          return null;
        }
      } catch (e) {
        debugPrint('>>> Thử $attempt tải $url gặp lỗi: $e');
        if (attempt < 2) {
          await Future.delayed(const Duration(milliseconds: 1000));
        }
      }
    }
    return null;
  }

  Future<void> _loadEpub() async {
    try {
      Uint8List? bytes;
      String targetUrl = widget.epubUrl;
      EpubController? controller;

      // 1. Thử tải từ cache cục bộ trước (nếu mobile/desktop)
      if (!kIsWeb) {
        try {
          final dir = await getTemporaryDirectory();
          final cached = File('${dir.path}/book_${widget.bookId}_temp.epub');
          if (await cached.exists()) {
            final cachedBytes = await cached.readAsBytes();
            if (cachedBytes.isNotEmpty) {
              try {
                controller = EpubController(document: EpubDocument.openData(cachedBytes));
                bytes = cachedBytes;
              } catch (_) {
                // Cache bị hỏng, xóa đi để tải lại
                await cached.delete();
              }
            }
          }
        } catch (_) {}
      }

      // 2. Nếu là đường dẫn file cục bộ (offline)
      if (controller == null && !targetUrl.startsWith('http') && !kIsWeb) {
        final file = File(targetUrl);
        if (await file.exists()) {
          final localBytes = await file.readAsBytes();
          try {
            controller = EpubController(document: EpubDocument.openData(localBytes));
            bytes = localBytes;
          } catch (e) {
            debugPrint("Lỗi đọc file epub local: $e");
          }
        }
      }

      // 3. Nếu chưa có controller, xây dựng danh sách các URL tiềm năng để thử tuần tự
      if (controller == null) {
        final List<String> candidateUrls = [];
        final formattedUrl = ApiConfig.formatUrl(targetUrl);
        if (formattedUrl.isNotEmpty) candidateUrls.add(formattedUrl);
        if (targetUrl.isNotEmpty && targetUrl != formattedUrl) candidateUrls.add(targetUrl);

        // Nếu là sách từ Project Gutenberg, thêm các mirror direct cache CDN
        final gMatch = RegExp(r'gutenberg\.org/(?:ebooks/|cache/epub/)?(\d+)').firstMatch(targetUrl);
        if (gMatch != null) {
          final gId = gMatch.group(1);
          final directCacheUrl = 'https://www.gutenberg.org/cache/epub/$gId/pg$gId.epub';
          final epub3Url = 'https://www.gutenberg.org/ebooks/$gId.epub3.images';
          candidateUrls.add(ApiConfig.formatUrl(directCacheUrl));
          candidateUrls.add(directCacheUrl);
          candidateUrls.add(ApiConfig.formatUrl(epub3Url));
          candidateUrls.add(epub3Url);
        }

        // Thêm fallback local backend và Gutenberg Pride & Prejudice
        candidateUrls.add(ApiConfig.formatUrl('${ApiConfig.baseUrl}/uploads/nha_gia_kim.epub'));
        candidateUrls.add(ApiConfig.formatUrl(_kFallbackEpubUrl));
        candidateUrls.add(_kFallbackEpubUrl);

        // Loại bỏ trùng lặp giữ nguyên thứ tự
        final uniqueCandidates = <String>[];
        for (final u in candidateUrls) {
          if (u.isNotEmpty && !uniqueCandidates.contains(u)) {
            uniqueCandidates.add(u);
          }
        }

        // Duyệt qua từng URL cho đến khi nạp được tệp EPUB hợp lệ
        for (final url in uniqueCandidates) {
          final fetchedBytes = await _fetchEpubBytes(url);
          if (fetchedBytes != null && fetchedBytes.length > 500) {
            // Kiểm tra magic header tệp ZIP/EPUB: PK\x03\x04 (0x50, 0x4B)
            if (fetchedBytes[0] == 0x50 && fetchedBytes[1] == 0x4B) {
              try {
                controller = EpubController(document: EpubDocument.openData(fetchedBytes));
                bytes = fetchedBytes;
                break;
              } catch (parseErr) {
                debugPrint('>>> Không parse được EPUB từ $url: $parseErr');
              }
            } else {
              debugPrint('>>> Bỏ qua tệp không phải định dạng EPUB (HTML/lỗi) từ $url');
            }
          }
        }

        if (controller == null || bytes == null || bytes.isEmpty) {
          throw Exception('Không thể tải hoặc mở tệp sách EPUB. Vui lòng thử lại sau.');
        }

        // Lưu cache cục bộ nếu không phải Web
        if (!kIsWeb) {
          try {
            final dir = await getTemporaryDirectory();
            final file = File('${dir.path}/book_${widget.bookId}_temp.epub');
            await file.writeAsBytes(bytes, flush: true);
          } catch (_) {}
        }
      }

      if (mounted) {
        setState(() {
          _epubController = controller;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        String msg = e.toString().replaceFirst("Exception: ", "").trim();
        if (msg.isEmpty) {
          msg = "Không thể tải nội dung sách. Vui lòng bấm Thử lại.";
        }
        setState(() {
          _errorMessage = msg;
          _isLoading = false;
        });
      }
    }
  }

  // Tự động lưu tiến độ đọc khi đóng màn hình hoặc định kỳ
  Future<void> _saveProgress() async {
    if (_epubController == null) return;
    try {
      final cfi = _epubController!.generateEpubCfi();
      if (cfi != null && cfi.isNotEmpty) {
        await ProgressService.updateProgress(
          bookId: widget.bookId,
          username: widget.username,
          lastEpubCfi: cfi,
        );
      }
    } catch (_) {}
  }

  void _showBookmarkDialog() {
    if (_isGuest) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text("Vui lòng đăng nhập để sử dụng tính năng đánh dấu trang!"),
          backgroundColor: Colors.orangeAccent,
        ),
      );
      return;
    }

    final noteCtrl = TextEditingController();
    showDialog(
      context: context,
      builder: (dialogCtx) => AlertDialog(
        backgroundColor: const Color(0xFF222222),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
        title: const Row(
          children: [
            Icon(Icons.bookmark_add_rounded, color: Colors.orange),
            SizedBox(width: 8),
            Text("Đánh dấu trang EPUB", style: TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.bold)),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              "Lưu vị trí đọc hiện tại để tiếp tục mở lại bất cứ lúc nào:",
              style: TextStyle(color: Colors.white70, fontSize: 13),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: noteCtrl,
              style: const TextStyle(color: Colors.white, fontSize: 14),
              decoration: InputDecoration(
                hintText: "Ghi chú cho trang này...",
                hintStyle: const TextStyle(color: Colors.white38),
                filled: true,
                fillColor: Colors.black26,
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide.none),
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(dialogCtx),
            child: const Text("Hủy", style: TextStyle(color: Colors.white54)),
          ),
          ElevatedButton(
            style: ElevatedButton.styleFrom(backgroundColor: Colors.orange, foregroundColor: Colors.black),
            onPressed: () async {
              final note = noteCtrl.text.trim();
              final cfi = _epubController?.generateEpubCfi() ?? '';
              try {
                final url = Uri.parse('${ApiConfig.baseUrl}/api/bookmarks/toggle');
                final res = await http.post(
                  url,
                  headers: {'Content-Type': 'application/json'},
                  body: jsonEncode({
                    'username': widget.username,
                    'book_id': widget.bookId,
                    'page_number': 1,
                    'note': note.isNotEmpty ? note : "Đánh dấu tại: $cfi",
                  }),
                );
                if (dialogCtx.mounted) Navigator.pop(dialogCtx);
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(res.statusCode == 200 ? "Đã lưu đánh dấu trang thành công!" : "Lỗi lưu đánh dấu"),
                      backgroundColor: res.statusCode == 200 ? Colors.green : Colors.redAccent,
                    ),
                  );
                }
              } catch (_) {}
            },
            child: const Text("Lưu Bookmark"),
          ),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _autoSaveTimer?.cancel();
    _saveProgress();
    _epubController?.dispose();
    super.dispose();
  }

  Color get _backgroundColor {
    switch (_currentTheme) {
      case ReaderThemeMode.light:
        return const Color(0xFFFAFAFA);
      case ReaderThemeMode.sepia:
        return const Color(0xFFF4ECD8);
      case ReaderThemeMode.dark:
        return const Color(0xFF141414);
    }
  }

  Color get _textColor {
    switch (_currentTheme) {
      case ReaderThemeMode.light:
        return const Color(0xFF1E1E1E);
      case ReaderThemeMode.sepia:
        return const Color(0xFF4A3525);
      case ReaderThemeMode.dark:
        return const Color(0xFFF5F5F5);
    }
  }

  Color get _dividerColor {
    switch (_currentTheme) {
      case ReaderThemeMode.light:
        return const Color(0xFFEEEEEE);
      case ReaderThemeMode.sepia:
        return const Color(0xFFE8DCBE);
      case ReaderThemeMode.dark:
        return const Color(0xFF262626);
    }
  }

  void _showAppearanceBottomSheet() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF252525),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return StatefulBuilder(
          builder: (context, setSheetState) {
            return Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Tùy chỉnh giao diện đọc",
                    style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 20),
                  const Text("Chế độ màu", style: TextStyle(color: Colors.white70, fontSize: 14)),
                  const SizedBox(height: 10),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      _buildThemeBtn(ReaderThemeMode.light, "Sáng", const Color(0xFFFAFAFA), Colors.black, setSheetState),
                      _buildThemeBtn(ReaderThemeMode.sepia, "Sepia", const Color(0xFFF4ECD8), const Color(0xFF5B4636), setSheetState),
                      _buildThemeBtn(ReaderThemeMode.dark, "Tối", const Color(0xFF1E1E1E), Colors.white, setSheetState),
                    ],
                  ),
                  const SizedBox(height: 20),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text("Cỡ chữ", style: TextStyle(color: Colors.white70, fontSize: 14)),
                      Text("${_fontSize.toInt()} px", style: const TextStyle(color: Colors.orange, fontWeight: FontWeight.bold)),
                    ],
                  ),
                  Slider(
                    value: _fontSize,
                    min: 12,
                    max: 26,
                    divisions: 7,
                    activeColor: Colors.orange,
                    inactiveColor: Colors.white24,
                    onChanged: (val) {
                      setSheetState(() => _fontSize = val);
                      setState(() => _fontSize = val);
                      _saveReaderPreferences();
                    },
                  ),
                  const SizedBox(height: 10),
                ],
              ),
            );
          },
        );
      },
    );
  }

  Widget _buildThemeBtn(ReaderThemeMode mode, String label, Color bg, Color textCol, StateSetter setSheetState) {
    final isSelected = _currentTheme == mode;
    return GestureDetector(
      onTap: () {
        setSheetState(() => _currentTheme = mode);
        setState(() => _currentTheme = mode);
        _saveReaderPreferences();
      },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
        decoration: BoxDecoration(
          color: bg,
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: isSelected ? Colors.orange : Colors.white24, width: isSelected ? 2 : 1),
        ),
        child: Text(
          label,
          style: TextStyle(color: textCol, fontWeight: isSelected ? FontWeight.bold : FontWeight.normal),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _backgroundColor,
      appBar: AppBar(
        backgroundColor: _backgroundColor,
        elevation: 0,
        iconTheme: IconThemeData(color: _textColor),
        title: _epubController == null
            ? Text(
                widget.bookTitle,
                style: TextStyle(color: _textColor, fontSize: 16, fontWeight: FontWeight.bold),
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              )
            : EpubViewActualChapter(
                controller: _epubController!,
                builder: (chapterValue) => Text(
                  chapterValue?.chapter?.Title?.trim() ?? widget.bookTitle,
                  style: TextStyle(color: _textColor, fontSize: 16, fontWeight: FontWeight.bold),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
        actions: [
          IconButton(
            icon: const Icon(Icons.headset_rounded, color: Colors.orangeAccent),
            tooltip: "Nghe sách nói",
            onPressed: () {
              final audioUrl = ApiConfig.formatUrl('uploads/vn_book_${widget.bookId}.mp3');
              AudioPlayerService().playBook(
                bookId: widget.bookId,
                title: widget.bookTitle,
                author: 'Tác giả',
                audioUrl: audioUrl,
                coverUrl: '',
              );
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => const AudioPlayerScreen()),
              );
            },
          ),
          IconButton(
            icon: const Icon(Icons.bookmark_add_outlined),
            tooltip: "Đánh dấu trang",
            onPressed: _showBookmarkDialog,
          ),
          IconButton(
            icon: const Icon(Icons.text_format),
            tooltip: "Tùy chỉnh giao diện",
            onPressed: _showAppearanceBottomSheet,
          ),
        ],
      ),
      drawer: Drawer(
        backgroundColor: const Color(0xFF222222),
        child: _epubController == null
            ? const SizedBox()
            : EpubViewTableOfContents(
                controller: _epubController!,
                itemBuilder: (context, index, chapter, itemCount) {
                  return ListTile(
                    tileColor: Colors.transparent,
                    title: Text(
                      chapter.title?.trim() ?? '',
                      style: const TextStyle(color: Colors.white, fontSize: 14),
                    ),
                    onTap: () {
                      _epubController!.scrollTo(index: chapter.startIndex);
                      Navigator.pop(context);
                    },
                  );
                },
              ),
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator(color: Colors.orange))
          : _errorMessage.isNotEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.error_outline, color: Colors.redAccent, size: 48),
                        const SizedBox(height: 12),
                        Text(
                          "Lỗi tải sách EPUB",
                          style: TextStyle(color: _textColor, fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          _errorMessage,
                          textAlign: TextAlign.center,
                          style: const TextStyle(color: Colors.white54, fontSize: 13),
                        ),
                        const SizedBox(height: 20),
                        ElevatedButton.icon(
                          onPressed: () {
                            setState(() {
                              _isLoading = true;
                              _errorMessage = '';
                            });
                            _loadEpub();
                          },
                          icon: const Icon(Icons.refresh),
                          label: const Text("Thử lại"),
                          style: ElevatedButton.styleFrom(backgroundColor: Colors.orange, foregroundColor: Colors.black),
                        ),
                        const SizedBox(height: 12),
                        OutlinedButton.icon(
                          onPressed: () {
                            Navigator.pushReplacement(
                              context,
                              MaterialPageRoute(
                                builder: (_) => ContentReaderScreen(
                                  bookId: widget.bookId,
                                  bookTitle: widget.bookTitle,
                                  username: widget.username,
                                ),
                              ),
                            );
                          },
                          icon: const Icon(Icons.menu_book_rounded, color: Colors.orangeAccent),
                          label: const Text("Chuyển sang chế độ đọc văn bản", style: TextStyle(color: Colors.white)),
                          style: OutlinedButton.styleFrom(side: const BorderSide(color: Colors.orangeAccent)),
                        ),
                      ],
                    ),
                  ),
                )
              : Theme(
                  data: ThemeData(
                    brightness: _currentTheme == ReaderThemeMode.dark
                        ? Brightness.dark
                        : Brightness.light,
                    scaffoldBackgroundColor: _backgroundColor,
                  ),
                  child: DefaultTextStyle(
                    style: TextStyle(
                      color: _textColor,
                      fontSize: _fontSize,
                      height: 1.6,
                      letterSpacing: 0.2,
                    ),
                    child: EpubView(
                      controller: _epubController!,
                      builders: EpubViewBuilders<DefaultBuilderOptions>(
                        options: DefaultBuilderOptions(
                          textStyle: TextStyle(
                            color: _textColor,
                            fontSize: _fontSize,
                            height: 1.6,
                            letterSpacing: 0.2,
                          ),
                          paragraphPadding: const EdgeInsets.symmetric(
                            horizontal: 22,
                            vertical: 8,
                          ),
                        ),
                        chapterDividerBuilder: (chapter) => Container(
                          width: double.infinity,
                          padding: const EdgeInsets.symmetric(
                            horizontal: 20,
                            vertical: 14,
                          ),
                          margin: const EdgeInsets.symmetric(vertical: 14),
                          decoration: BoxDecoration(
                            color: _dividerColor,
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(
                              color: _currentTheme == ReaderThemeMode.dark
                                  ? const Color(0xFF333333)
                                  : (_currentTheme == ReaderThemeMode.sepia
                                      ? const Color(0xFFD6C8A6)
                                      : const Color(0xFFDDDDDD)),
                            ),
                          ),
                          child: Text(
                            chapter.Title?.trim() ?? '',
                            style: TextStyle(
                              fontSize: _fontSize + 4,
                              fontWeight: FontWeight.bold,
                              color: _textColor,
                            ),
                          ),
                        ),
                      ),
                    ),
                  ),
                ),
    );
  }
}
