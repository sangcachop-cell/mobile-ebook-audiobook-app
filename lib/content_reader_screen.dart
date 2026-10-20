import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'api_config.dart';
import 'audio_player_service.dart';
import 'audio_player_screen.dart';
import 'progress_service.dart';

enum ContentTheme { light, sepia, dark }

class ContentReaderScreen extends StatefulWidget {
  final int bookId;
  final String bookTitle;
  final String author;
  final String username;
  final String? initialContent;

  const ContentReaderScreen({
    super.key,
    required this.bookId,
    required this.bookTitle,
    this.author = '',
    required this.username,
    this.initialContent,
  });

  @override
  State<ContentReaderScreen> createState() => _ContentReaderScreenState();
}

class _ContentReaderScreenState extends State<ContentReaderScreen> {
  bool _isLoading = true;
  String _errorMessage = '';
  List<Map<String, dynamic>> _chapters = [];
  int _currentChapterIndex = 0;
  double _fontSize = 17.0;
  ContentTheme _theme = ContentTheme.light;
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    _loadPreferences();
    _loadBookContent();
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _loadPreferences() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final savedTheme = prefs.getString('content_reader_theme');
      final savedSize = prefs.getDouble('content_reader_font_size');
      if (mounted) {
        setState(() {
          if (savedTheme == 'dark') _theme = ContentTheme.dark;
          if (savedTheme == 'sepia') _theme = ContentTheme.sepia;
          if (savedTheme == 'light') _theme = ContentTheme.light;
          if (savedSize != null && savedSize >= 13 && savedSize <= 28) {
            _fontSize = savedSize;
          }
        });
      }
    } catch (_) {}
  }

  Future<void> _savePreferences() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('content_reader_theme', _theme.name);
      await prefs.setDouble('content_reader_font_size', _fontSize);
    } catch (_) {}
  }

  Future<void> _loadBookContent() async {
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}/api/books/${widget.bookId}');
      final res = await http.get(url).timeout(const Duration(seconds: 10));
      if (res.statusCode == 200) {
        final data = jsonDecode(utf8.decode(res.bodyBytes));
        final rawChapters = data['chapters'] as List<dynamic>? ?? [];
        final List<Map<String, dynamic>> parsed = [];
        for (final c in rawChapters) {
          parsed.add({
            'title': c['title'] ?? 'Chương',
            'content': c['content'] ?? '',
          });
        }

        if (parsed.isEmpty && data['content'] != null) {
          parsed.add({
            'title': 'Toàn văn tác phẩm',
            'content': data['content'],
          });
        }

        if (mounted) {
          setState(() {
            _chapters = parsed;
            _isLoading = false;
          });
          _saveReadingProgress();
        }
      } else {
        _fallbackToInitialContent();
      }
    } catch (e) {
      _fallbackToInitialContent();
    }
  }

  void _fallbackToInitialContent() {
    if (widget.initialContent != null && widget.initialContent!.isNotEmpty) {
      if (mounted) {
        setState(() {
          _chapters = [
            {'title': 'Nội dung tác phẩm', 'content': widget.initialContent!}
          ];
          _isLoading = false;
        });
      }
    } else {
      if (mounted) {
        setState(() {
          _errorMessage = 'Không thể tải nội dung văn bản. Vui lòng thử lại sau.';
          _isLoading = false;
        });
      }
    }
  }

  void _saveReadingProgress() {
    if (_chapters.isEmpty) return;
    final percent = ((_currentChapterIndex + 1) / _chapters.length * 100).clamp(0.0, 100.0);
    ProgressService.updateProgress(
      bookId: widget.bookId,
      username: widget.username,
      lastPage: _currentChapterIndex,
      progressPercent: percent,
    );
  }

  Color get _bgColor {
    switch (_theme) {
      case ContentTheme.light:
        return const Color(0xFFFAFAFA);
      case ContentTheme.sepia:
        return const Color(0xFFF5EEDC);
      case ContentTheme.dark:
        return const Color(0xFF141414);
    }
  }

  Color get _textColor {
    switch (_theme) {
      case ContentTheme.light:
        return const Color(0xFF1E1E1E);
      case ContentTheme.sepia:
        return const Color(0xFF4A3525);
      case ContentTheme.dark:
        return const Color(0xFFF0F0F0);
    }
  }

  Color get _subTextColor {
    switch (_theme) {
      case ContentTheme.light:
        return const Color(0xFF666666);
      case ContentTheme.sepia:
        return const Color(0xFF7A624E);
      case ContentTheme.dark:
        return const Color(0xFFAAAAAA);
    }
  }

  void _listenAudiobook() {
    // Kích hoạt audio player cho sách này
    final audioUrl = '${ApiConfig.baseUrl}/uploads/vn_book_${widget.bookId}.mp3';
    AudioPlayerService().playBook(
      bookId: widget.bookId,
      title: widget.bookTitle,
      author: widget.author.isNotEmpty ? widget.author : 'Tác giả',
      audioUrl: audioUrl,
      coverUrl: '',
      chapterTitle: _chapters.isNotEmpty ? _chapters[_currentChapterIndex]['title'] : null,
    );
    Navigator.push(
      context,
      MaterialPageRoute(builder: (_) => const AudioPlayerScreen()),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: _bgColor,
      appBar: AppBar(
        title: Text(
          widget.bookTitle,
          style: TextStyle(color: _textColor, fontSize: 16, fontWeight: FontWeight.bold),
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        backgroundColor: _theme == ContentTheme.dark ? const Color(0xFF1E1E1E) : _bgColor,
        elevation: 1,
        iconTheme: IconThemeData(color: _textColor),
        actions: [
          // Nút nghe audio
          IconButton(
            icon: const Icon(Icons.headset_rounded, color: Colors.orangeAccent),
            tooltip: "Nghe sách nói tiếng Việt",
            onPressed: _listenAudiobook,
          ),
          // Nút tùy chỉnh giao diện (Theme & Cỡ chữ)
          IconButton(
            icon: const Icon(Icons.format_size_rounded),
            tooltip: "Cỡ chữ & Giao diện đọc",
            onPressed: _showAppearanceModal,
          ),
          // Nút Mục lục chương
          if (_chapters.length > 1)
            IconButton(
              icon: const Icon(Icons.toc_rounded),
              tooltip: "Mục lục chương",
              onPressed: _showChapterModal,
            ),
        ],
      ),
      body: _buildBody(),
      bottomNavigationBar: _chapters.length > 1 ? _buildBottomBar() : null,
    );
  }

  Widget _buildBody() {
    if (_isLoading) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const CircularProgressIndicator(color: Colors.orange),
            const SizedBox(height: 16),
            Text("Đang nạp nội dung cuốn sách...", style: TextStyle(color: _subTextColor)),
          ],
        ),
      );
    }

    if (_errorMessage.isNotEmpty || _chapters.isEmpty) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.error_outline_rounded, color: Colors.orange, size: 48),
              const SizedBox(height: 12),
              Text(
                _errorMessage.isNotEmpty ? _errorMessage : "Không có nội dung để hiển thị.",
                textAlign: TextAlign.center,
                style: TextStyle(color: _textColor, fontSize: 14),
              ),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                style: ElevatedButton.styleFrom(backgroundColor: Colors.orange),
                onPressed: () {
                  setState(() => _isLoading = true);
                  _loadBookContent();
                },
                icon: const Icon(Icons.refresh_rounded, color: Colors.black),
                label: const Text("Thử lại", style: TextStyle(color: Colors.black, fontWeight: FontWeight.bold)),
              ),
            ],
          ),
        ),
      );
    }

    final curChap = _chapters[_currentChapterIndex];
    final title = curChap['title'] as String;
    final content = curChap['content'] as String;

    return SingleChildScrollView(
      controller: _scrollController,
      padding: const EdgeInsets.symmetric(horizontal: 22, vertical: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Tiêu đề chương
          Text(
            title,
            style: TextStyle(
              color: Colors.orange[800] ?? Colors.orange,
              fontSize: _fontSize + 4,
              fontWeight: FontWeight.bold,
              height: 1.3,
            ),
          ),
          const SizedBox(height: 8),
          if (widget.author.isNotEmpty)
            Text(
              "Tác giả: ${widget.author}",
              style: TextStyle(color: _subTextColor, fontSize: _fontSize - 3, fontStyle: FontStyle.italic),
            ),
          const SizedBox(height: 12),
          Divider(color: _subTextColor.withOpacity(0.2), thickness: 1),
          const SizedBox(height: 14),

          // Nội dung văn bản từng đoạn
          ...content
              .split('\n')
              .where((line) => line.trim().isNotEmpty)
              .map((para) => Padding(
                    padding: const EdgeInsets.only(bottom: 16.0),
                    child: Text(
                      para.trim(),
                      textAlign: TextAlign.justify,
                      style: TextStyle(
                        color: _textColor,
                        fontSize: _fontSize,
                        height: 1.7,
                        letterSpacing: 0.3,
                      ),
                    ),
                  )),
          const SizedBox(height: 40),
        ],
      ),
    );
  }

  Widget _buildBottomBar() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
      decoration: BoxDecoration(
        color: _theme == ContentTheme.dark ? const Color(0xFF1E1E1E) : _bgColor,
        border: Border(top: BorderSide(color: _subTextColor.withOpacity(0.15))),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          TextButton.icon(
            onPressed: _currentChapterIndex > 0
                ? () {
                    setState(() => _currentChapterIndex--);
                    _scrollController.jumpTo(0);
                    _saveReadingProgress();
                  }
                : null,
            icon: const Icon(Icons.arrow_back_ios_rounded, size: 14),
            label: const Text("Chương trước"),
          ),
          Text(
            "${_currentChapterIndex + 1} / ${_chapters.length}",
            style: TextStyle(color: _subTextColor, fontWeight: FontWeight.bold, fontSize: 13),
          ),
          TextButton.icon(
            onPressed: _currentChapterIndex < _chapters.length - 1
                ? () {
                    setState(() => _currentChapterIndex++);
                    _scrollController.jumpTo(0);
                    _saveReadingProgress();
                  }
                : null,
            icon: const Icon(Icons.arrow_forward_ios_rounded, size: 14),
            label: const Text("Chương sau"),
          ),
        ],
      ),
    );
  }

  void _showAppearanceModal() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF222222),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (ctx) {
        return StatefulBuilder(
          builder: (context, setModalState) {
            return Padding(
              padding: const EdgeInsets.all(22),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text("Tùy Chỉnh Giao Diện Đọc", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 20),

                  // Chọn màu nền
                  const Text("Chế độ màu:", style: TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w600)),
                  const SizedBox(height: 10),
                  Row(
                    children: [
                      _buildThemeChip("Sáng", ContentTheme.light, const Color(0xFFFAFAFA), Colors.black, setModalState),
                      const SizedBox(width: 10),
                      _buildThemeChip("Sepia", ContentTheme.sepia, const Color(0xFFF5EEDC), const Color(0xFF4A3525), setModalState),
                      const SizedBox(width: 10),
                      _buildThemeChip("Tối", ContentTheme.dark, const Color(0xFF141414), Colors.white, setModalState),
                    ],
                  ),
                  const SizedBox(height: 22),

                  // Cỡ chữ
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Text("Cỡ chữ:", style: TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w600)),
                      Text("${_fontSize.toInt()} px", style: const TextStyle(color: Colors.orangeAccent, fontWeight: FontWeight.bold)),
                    ],
                  ),
                  Row(
                    children: [
                      const Text("A", style: TextStyle(color: Colors.white54, fontSize: 14)),
                      Expanded(
                        child: Slider(
                          value: _fontSize,
                          min: 14.0,
                          max: 26.0,
                          divisions: 6,
                          activeColor: Colors.orange,
                          inactiveColor: Colors.white24,
                          onChanged: (val) {
                            setModalState(() => _fontSize = val);
                            setState(() => _fontSize = val);
                            _savePreferences();
                          },
                        ),
                      ),
                      const Text("A", style: TextStyle(color: Colors.white, fontSize: 22, fontWeight: FontWeight.bold)),
                    ],
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

  Widget _buildThemeChip(String label, ContentTheme theme, Color bg, Color fg, StateSetter setModalState) {
    final isSel = _theme == theme;
    return Expanded(
      child: GestureDetector(
        onTap: () {
          setModalState(() => _theme = theme);
          setState(() => _theme = theme);
          _savePreferences();
        },
        child: Container(
          padding: const EdgeInsets.symmetric(vertical: 12),
          decoration: BoxDecoration(
            color: bg,
            borderRadius: BorderRadius.circular(10),
            border: Border.all(color: isSel ? Colors.orange : Colors.white24, width: isSel ? 2.5 : 1),
          ),
          alignment: Alignment.center,
          child: Text(label, style: TextStyle(color: fg, fontWeight: FontWeight.bold, fontSize: 14)),
        ),
      ),
    );
  }

  void _showChapterModal() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF222222),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (ctx) {
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 18),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 20),
                child: Text("Mục Lục Chương", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
              ),
              const SizedBox(height: 10),
              Flexible(
                child: ListView.builder(
                  shrinkWrap: true,
                  itemCount: _chapters.length,
                  itemBuilder: (c, idx) {
                    final ch = _chapters[idx];
                    final isCur = idx == _currentChapterIndex;
                    return ListTile(
                      title: Text(
                        ch['title'],
                        style: TextStyle(
                          color: isCur ? Colors.orangeAccent : Colors.white,
                          fontWeight: isCur ? FontWeight.bold : FontWeight.normal,
                          fontSize: 14,
                        ),
                      ),
                      trailing: isCur ? const Icon(Icons.check_circle_rounded, color: Colors.orangeAccent, size: 20) : null,
                      onTap: () {
                        setState(() => _currentChapterIndex = idx);
                        _scrollController.jumpTo(0);
                        _saveReadingProgress();
                        Navigator.pop(ctx);
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
