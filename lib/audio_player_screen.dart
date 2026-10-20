// audio_player_screen.dart
import 'dart:convert';
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'audio_player_service.dart';
import 'api_config.dart';
import 'user_session.dart';
import 'book_reader_helper.dart';

class AudioPlayerScreen extends StatefulWidget {
  const AudioPlayerScreen({super.key});

  @override
  State<AudioPlayerScreen> createState() => _AudioPlayerScreenState();
}

class _AudioPlayerScreenState extends State<AudioPlayerScreen> with SingleTickerProviderStateMixin {
  final AudioPlayerService _service = AudioPlayerService();
  final List<double> _speeds = [0.75, 1.0, 1.25, 1.5, 2.0];
  final List<int> _sleepTimerMinutes = [5, 15, 30, 45, 60];
  int _selectedTab = 0; // 0: Máy phát audio & Bìa sách, 1: Đọc nội dung sách
  double _transcriptFontSize = 15.0;
  late AnimationController _rotationController;

  @override
  void initState() {
    super.initState();
    _rotationController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 20),
    );
    if (_service.isPlaying) {
      _rotationController.repeat();
    }
    _service.addListener(_handleAudioState);
  }

  void _handleAudioState() {
    if (_service.isPlaying && !_rotationController.isAnimating) {
      _rotationController.repeat();
    } else if (!_service.isPlaying && _rotationController.isAnimating) {
      _rotationController.stop();
    }
  }

  @override
  void dispose() {
    _service.removeListener(_handleAudioState);
    _rotationController.dispose();
    super.dispose();
  }

  String _formatDuration(Duration d) {
    final minutes = d.inMinutes.remainder(60).toString().padLeft(2, '0');
    final seconds = d.inSeconds.remainder(60).toString().padLeft(2, '0');
    return d.inHours > 0 ? "${d.inHours}:$minutes:$seconds" : "$minutes:$seconds";
  }

  void _showSpeedPicker() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF202020),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text("Chọn tốc độ đọc", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              Wrap(
                spacing: 12,
                runSpacing: 12,
                children: _speeds.map((s) {
                  final isCurrent = _service.playbackSpeed == s;
                  return ChoiceChip(
                    label: Text("${s}x", style: TextStyle(color: isCurrent ? Colors.black : Colors.white, fontWeight: FontWeight.bold)),
                    selected: isCurrent,
                    selectedColor: Colors.orange,
                    backgroundColor: Colors.white12,
                    onSelected: (_) {
                      _service.setSpeed(s);
                      Navigator.pop(context);
                    },
                  );
                }).toList(),
              ),
              const SizedBox(height: 12),
            ],
          ),
        );
      },
    );
  }

  void _showSleepTimerPicker() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF202020),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) {
        return Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Row(
                    children: [
                      Icon(Icons.bedtime_rounded, color: Colors.orange, size: 22),
                      SizedBox(width: 8),
                      Text("Hẹn giờ tắt sách nói", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                    ],
                  ),
                  if (_service.isSleepTimerActive)
                    TextButton(
                      onPressed: () {
                        _service.cancelSleepTimer();
                        Navigator.pop(context);
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text("Đã tắt hẹn giờ!"), duration: Duration(seconds: 2)),
                        );
                      },
                      child: const Text("Hủy hẹn giờ", style: TextStyle(color: Colors.redAccent)),
                    ),
                ],
              ),
              if (_service.isSleepTimerActive)
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  child: Text(
                    "Đang đếm ngược: ${_service.formattedSleepTimer} sẽ tự động tạm dừng.",
                    style: const TextStyle(color: Colors.orangeAccent, fontSize: 13),
                  ),
                ),
              const SizedBox(height: 12),
              Wrap(
                spacing: 12,
                runSpacing: 12,
                children: _sleepTimerMinutes.map((m) {
                  return ActionChip(
                    avatar: const Icon(Icons.timer_outlined, size: 16, color: Colors.orange),
                    label: Text("$m phút", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                    backgroundColor: Colors.white12,
                    onPressed: () {
                      _service.setSleepTimer(m);
                      Navigator.pop(context);
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text("Đã hẹn giờ tắt sau $m phút."),
                          backgroundColor: Colors.green,
                          duration: const Duration(seconds: 2),
                        ),
                      );
                    },
                  );
                }).toList(),
              ),
              const SizedBox(height: 12),
            ],
          ),
        );
      },
    );
  }

  void _showChapterList() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1E1E1E),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) {
        final chapters = _service.chapters;
        return Padding(
          padding: const EdgeInsets.symmetric(vertical: 20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Padding(
                padding: EdgeInsets.symmetric(horizontal: 20),
                child: Row(
                  children: [
                    Icon(Icons.playlist_play_rounded, color: Colors.orange, size: 24),
                    SizedBox(width: 8),
                    Text("Danh sách chương sách nói", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                  ],
                ),
              ),
              const SizedBox(height: 12),
              Flexible(
                child: ListView.builder(
                  shrinkWrap: true,
                  itemCount: chapters.length,
                  itemBuilder: (ctx, idx) {
                    final chap = chapters[idx];
                    final isCurrent = _service.currentChapter == chap['title'];
                    final startSec = chap['startSec'] as int;
                    return ListTile(
                      leading: Icon(
                        Icons.record_voice_over_rounded,
                        color: isCurrent ? Colors.orange : Colors.white38,
                      ),
                      title: Text(
                        chap['title'],
                        style: TextStyle(
                          color: isCurrent ? Colors.orange : Colors.white,
                          fontWeight: isCurrent ? FontWeight.bold : FontWeight.normal,
                          fontSize: 14,
                        ),
                      ),
                      subtitle: Text(
                        "Thời điểm: ${_formatDuration(Duration(seconds: startSec))}",
                        style: const TextStyle(color: Colors.white54, fontSize: 12),
                      ),
                      trailing: isCurrent ? const Icon(Icons.check_circle_rounded, color: Colors.orange, size: 20) : null,
                      onTap: () {
                        _service.seekToChapter(
                          startSec,
                          chap['title'],
                          chapterContent: chap['content'] as String?,
                        );
                        Navigator.pop(context);
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

  void _showBookmarksModal() async {
    final bookId = _service.currentBookId;
    if (bookId == null) return;

    final session = await UserSession.getSession();
    final username = session?['username'] ?? 'guest';
    final isGuest = username == 'guest' || username.isEmpty;

    List<dynamic> bookmarks = [];
    if (!isGuest) {
      try {
        final url = Uri.parse('${ApiConfig.baseUrl}/api/bookmarks/$username/$bookId');
        final res = await http.get(url);
        if (res.statusCode == 200) {
          bookmarks = jsonDecode(utf8.decode(res.bodyBytes));
        }
      } catch (_) {}
    }

    if (!mounted) return;

    final noteCtrl = TextEditingController();

    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      backgroundColor: const Color(0xFF1E1E1E),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (ctx) {
        return StatefulBuilder(
          builder: (modalCtx, setModalState) {
            final currentPosMs = _service.position.inMilliseconds;
            final currentPosFormatted = _formatDuration(_service.position);

            return Padding(
              padding: EdgeInsets.only(
                left: 20,
                right: 20,
                top: 20,
                bottom: MediaQuery.of(modalCtx).viewInsets.bottom + 20,
              ),
              child: SingleChildScrollView(
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.bookmark_added_rounded, color: Colors.orange, size: 22),
                            SizedBox(width: 8),
                            Text("Đánh dấu mốc âm thanh", style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
                          ],
                        ),
                        IconButton(
                          icon: const Icon(Icons.close, color: Colors.white54),
                          onPressed: () => Navigator.pop(modalCtx),
                        )
                      ],
                    ),
                    const SizedBox(height: 12),
                    // Hộp thêm bookmark mới
                    Container(
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.06),
                        borderRadius: BorderRadius.circular(14),
                        border: Border.all(color: Colors.orange.withOpacity(0.3)),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              const Icon(Icons.access_time_filled_rounded, color: Colors.orangeAccent, size: 18),
                              const SizedBox(width: 8),
                              Text("Thời điểm hiện tại: $currentPosFormatted", style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
                            ],
                          ),
                          const SizedBox(height: 10),
                          TextField(
                            controller: noteCtrl,
                            style: const TextStyle(color: Colors.white, fontSize: 13),
                            decoration: InputDecoration(
                              hintText: "Ghi chú cho đoạn này (tùy chọn)...",
                              hintStyle: const TextStyle(color: Colors.white38),
                              filled: true,
                              fillColor: Colors.black26,
                              contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
                              border: OutlineInputBorder(borderRadius: BorderRadius.circular(10), borderSide: BorderSide.none),
                            ),
                          ),
                          const SizedBox(height: 10),
                          SizedBox(
                            width: double.infinity,
                            child: ElevatedButton.icon(
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.orange,
                                foregroundColor: Colors.black,
                                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                              ),
                              onPressed: isGuest
                                  ? () {
                                      ScaffoldMessenger.of(context).showSnackBar(
                                        const SnackBar(content: Text("Vui lòng đăng nhập để lưu đánh dấu mốc nghe!"), backgroundColor: Colors.orangeAccent),
                                      );
                                    }
                                  : () async {
                                      final note = noteCtrl.text.trim();
                                      try {
                                        final url = Uri.parse('${ApiConfig.baseUrl}/api/bookmarks/toggle');
                                        final res = await http.post(
                                          url,
                                          headers: {'Content-Type': 'application/json'},
                                          body: jsonEncode({
                                            'username': username,
                                            'book_id': bookId,
                                            'page_number': 0,
                                            'audio_position_ms': currentPosMs,
                                            'note': note.isNotEmpty ? note : "Đánh dấu tại $currentPosFormatted",
                                          }),
                                        );
                                        if (res.statusCode == 200) {
                                          noteCtrl.clear();
                                          final fetchUrl = Uri.parse('${ApiConfig.baseUrl}/api/bookmarks/$username/$bookId');
                                          final reloadRes = await http.get(fetchUrl);
                                          if (reloadRes.statusCode == 200) {
                                            setModalState(() {
                                              bookmarks = jsonDecode(utf8.decode(reloadRes.bodyBytes));
                                            });
                                          }
                                          if (mounted) {
                                            ScaffoldMessenger.of(context).showSnackBar(
                                              const SnackBar(content: Text("Đã lưu mốc âm thanh thành công!"), backgroundColor: Colors.green),
                                            );
                                          }
                                        }
                                      } catch (_) {}
                                    },
                              icon: const Icon(Icons.bookmark_add, size: 18),
                              label: const Text("Lưu mốc thời gian này", style: TextStyle(fontWeight: FontWeight.bold)),
                            ),
                          ),
                        ],
                      ),
                    ),
                    const SizedBox(height: 18),
                    const Text("Các mốc đã đánh dấu trong sách:", style: TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    if (bookmarks.isEmpty)
                      const Padding(
                        padding: EdgeInsets.symmetric(vertical: 16),
                        child: Center(
                          child: Text("Chưa có mốc thời gian nào được lưu.", style: TextStyle(color: Colors.white38, fontSize: 13)),
                        ),
                      )
                    else
                      ListView.builder(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemCount: bookmarks.length,
                        itemBuilder: (c, idx) {
                          final item = bookmarks[idx];
                          final int posMs = item['audio_position_ms'] ?? 0;
                          final String note = item['note'] ?? '';
                          final formattedPos = _formatDuration(Duration(milliseconds: posMs));

                          return ListTile(
                            contentPadding: EdgeInsets.zero,
                            leading: Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              decoration: BoxDecoration(
                                color: Colors.orange.withOpacity(0.2),
                                borderRadius: BorderRadius.circular(8),
                              ),
                              child: Text(formattedPos, style: const TextStyle(color: Colors.orange, fontWeight: FontWeight.bold, fontSize: 12)),
                            ),
                            title: Text(
                              note.isNotEmpty ? note : "Mốc nghe $formattedPos",
                              style: const TextStyle(color: Colors.white, fontSize: 13),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                            ),
                            trailing: const Icon(Icons.play_arrow_rounded, color: Colors.orangeAccent),
                            onTap: () {
                              _service.seek(Duration(milliseconds: posMs));
                              Navigator.pop(modalCtx);
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(content: Text("Đã nhảy đến mốc $formattedPos"), duration: const Duration(seconds: 1)),
                              );
                            },
                          );
                        },
                      ),
                  ],
                ),
              ),
            );
          },
        );
      },
    );
  }

  void _openBookInReader() async {
    final bookId = _service.currentBookId;
    if (bookId == null) return;

    final session = await UserSession.getSession();
    final username = session?['username'] ?? 'User';

    try {
      final url = Uri.parse('${ApiConfig.baseUrl}/api/books/$bookId');
      final res = await http.get(url);
      if (res.statusCode == 200) {
        final b = jsonDecode(utf8.decode(res.bodyBytes));
        final pdfUrl = ApiConfig.formatUrl(b['pdf_url'] ?? '');
        if (mounted) {
          BookReaderHelper.openBook(
            context: context,
            fileUrl: pdfUrl,
            bookTitle: _service.currentTitle,
            bookId: bookId,
            username: username,
            author: _service.currentAuthor,
          );
        }
      }
    } catch (_) {}
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _service,
      builder: (context, _) {
        final position = _service.position;
        final duration = _service.duration;
        final maxSeconds = duration.inSeconds > 0 ? duration.inSeconds.toDouble() : 1.0;
        final currentSeconds = position.inSeconds.toDouble().clamp(0.0, maxSeconds);

        return Scaffold(
          body: Stack(
            children: [
              // 1. Ảnh nền làm mờ theo bìa sách nghệ thuật
              Positioned.fill(
                child: _service.currentCoverUrl.isNotEmpty
                    ? Image.network(
                        _service.currentCoverUrl,
                        fit: BoxFit.cover,
                        errorBuilder: (_, __, ___) => Container(color: const Color(0xFF141414)),
                      )
                    : Container(color: const Color(0xFF141414)),
              ),
              Positioned.fill(
                child: BackdropFilter(
                  filter: ImageFilter.blur(sigmaX: 35, sigmaY: 35),
                  child: Container(
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [
                          Colors.black.withOpacity(0.75),
                          Colors.black.withOpacity(0.95),
                        ],
                        begin: Alignment.topCenter,
                        end: Alignment.bottomCenter,
                      ),
                    ),
                  ),
                ),
              ),

              // 2. Nội dung chính của Player
              SafeArea(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
                  child: Column(
                    children: [
                      // Thanh công cụ trên cùng
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          IconButton(
                            icon: const Icon(Icons.keyboard_arrow_down_rounded, color: Colors.white, size: 36),
                            onPressed: () => Navigator.pop(context),
                          ),
                          const Column(
                            children: [
                              Text(
                                "SÁCH NÓI TIẾNG VIỆT",
                                style: TextStyle(color: Colors.orangeAccent, fontSize: 11, fontWeight: FontWeight.bold, letterSpacing: 1.5),
                              ),
                              SizedBox(height: 2),
                              Text(
                                "Thuyết minh nội dung chân thực",
                                style: TextStyle(color: Colors.white54, fontSize: 10),
                              ),
                            ],
                          ),
                          Row(
                            children: [
                              // Nút Hẹn giờ tắt
                              IconButton(
                                icon: Icon(
                                  _service.isSleepTimerActive ? Icons.bedtime_rounded : Icons.bedtime_outlined,
                                  color: _service.isSleepTimerActive ? Colors.orange : Colors.white70,
                                  size: 22,
                                ),
                                tooltip: "Hẹn giờ tắt",
                                onPressed: _showSleepTimerPicker,
                              ),
                              // Nút Đánh dấu mốc
                              IconButton(
                                icon: const Icon(Icons.bookmark_add_outlined, color: Colors.white70, size: 22),
                                tooltip: "Đánh dấu thời điểm",
                                onPressed: _showBookmarksModal,
                              ),
                              // Nút Danh sách chương
                              IconButton(
                                icon: const Icon(Icons.playlist_play_rounded, color: Colors.white70, size: 26),
                                tooltip: "Danh sách chương",
                                onPressed: _showChapterList,
                              ),
                            ],
                          ),
                        ],
                      ),

                      if (_service.isSleepTimerActive)
                        Container(
                          margin: const EdgeInsets.only(top: 4, bottom: 4),
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                          decoration: BoxDecoration(
                            color: Colors.orange.withOpacity(0.15),
                            borderRadius: BorderRadius.circular(10),
                            border: Border.all(color: Colors.orange.withOpacity(0.3)),
                          ),
                          child: Text(
                            "Hẹn giờ tắt: ${_service.formattedSleepTimer}",
                            style: const TextStyle(color: Colors.orangeAccent, fontSize: 11, fontWeight: FontWeight.w600),
                          ),
                        ),

                      // BỘ CHUYỂN TAB: [ 🎵 Máy phát ] và [ 📖 Đọc nội dung sách ]
                      Container(
                        margin: const EdgeInsets.symmetric(vertical: 8),
                        padding: const EdgeInsets.all(4),
                        decoration: BoxDecoration(
                          color: Colors.white.withOpacity(0.08),
                          borderRadius: BorderRadius.circular(25),
                          border: Border.all(color: Colors.white12),
                        ),
                        child: Row(
                          children: [
                            Expanded(
                              child: GestureDetector(
                                onTap: () => setState(() => _selectedTab = 0),
                                child: Container(
                                  padding: const EdgeInsets.symmetric(vertical: 8),
                                  decoration: BoxDecoration(
                                    color: _selectedTab == 0 ? Colors.orange : Colors.transparent,
                                    borderRadius: BorderRadius.circular(20),
                                  ),
                                  alignment: Alignment.center,
                                  child: Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(Icons.graphic_eq_rounded, size: 16, color: _selectedTab == 0 ? Colors.black : Colors.white70),
                                      const SizedBox(width: 6),
                                      Text(
                                        "Trình phát Audio",
                                        style: TextStyle(
                                          color: _selectedTab == 0 ? Colors.black : Colors.white70,
                                          fontWeight: FontWeight.bold,
                                          fontSize: 12,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                            Expanded(
                              child: GestureDetector(
                                onTap: () => setState(() => _selectedTab = 1),
                                child: Container(
                                  padding: const EdgeInsets.symmetric(vertical: 8),
                                  decoration: BoxDecoration(
                                    color: _selectedTab == 1 ? Colors.orange : Colors.transparent,
                                    borderRadius: BorderRadius.circular(20),
                                  ),
                                  alignment: Alignment.center,
                                  child: Row(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(Icons.menu_book_rounded, size: 16, color: _selectedTab == 1 ? Colors.black : Colors.white70),
                                      const SizedBox(width: 6),
                                      Text(
                                        "Đọc nội dung sách",
                                        style: TextStyle(
                                          color: _selectedTab == 1 ? Colors.black : Colors.white70,
                                          fontWeight: FontWeight.bold,
                                          fontSize: 12,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),

                      // NỘI DUNG CHÍNH THEO TAB
                      Expanded(
                        child: _selectedTab == 0 ? _buildPlayerTab() : _buildTranscriptTab(),
                      ),

                      // Cụm điều khiển thời gian và Slider Seek
                      SliderTheme(
                        data: SliderTheme.of(context).copyWith(
                          activeTrackColor: Colors.orange,
                          inactiveTrackColor: Colors.white24,
                          thumbColor: Colors.orangeAccent,
                          trackHeight: 4,
                          thumbShape: const RoundSliderThumbShape(enabledThumbRadius: 7),
                          overlayShape: const RoundSliderOverlayShape(overlayRadius: 16),
                        ),
                        child: Slider(
                          value: currentSeconds,
                          min: 0.0,
                          max: maxSeconds,
                          onChanged: (val) {
                            _service.seek(Duration(seconds: val.toInt()));
                          },
                        ),
                      ),
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 16),
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(_formatDuration(position), style: const TextStyle(color: Colors.white54, fontSize: 12)),
                            Text(_formatDuration(duration), style: const TextStyle(color: Colors.white54, fontSize: 12)),
                          ],
                        ),
                      ),
                      const SizedBox(height: 10),

                      // Cụm nút bấm phát/dừng và tua
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          // Nút tốc độ
                          GestureDetector(
                            onTap: _showSpeedPicker,
                            child: Container(
                              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                              decoration: BoxDecoration(
                                color: Colors.white12,
                                borderRadius: BorderRadius.circular(12),
                              ),
                              child: Text(
                                "${_service.playbackSpeed}x",
                                style: const TextStyle(color: Colors.orange, fontWeight: FontWeight.bold, fontSize: 13),
                              ),
                            ),
                          ),

                          // Tua lùi 15s
                          IconButton(
                            icon: const Icon(Icons.replay_10_rounded, color: Colors.white, size: 36),
                            tooltip: "Lùi 15 giây",
                            onPressed: () => _service.skipBackward15(),
                          ),

                          // Nút Play / Pause tròn to
                          GestureDetector(
                            onTap: () => _service.togglePlayPause(),
                            child: Container(
                              width: 66,
                              height: 66,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                color: Colors.orange,
                                boxShadow: [
                                  BoxShadow(
                                    color: Colors.orange.withOpacity(0.4),
                                    blurRadius: 20,
                                    spreadRadius: 2,
                                  ),
                                ],
                              ),
                              child: _service.isLoading
                                  ? const Center(
                                      child: SizedBox(
                                        width: 26,
                                        height: 26,
                                        child: CircularProgressIndicator(
                                          strokeWidth: 3,
                                          color: Colors.black,
                                        ),
                                      ),
                                    )
                                  : Icon(
                                      _service.isPlaying ? Icons.pause_rounded : Icons.play_arrow_rounded,
                                      color: Colors.black,
                                      size: 40,
                                    ),
                            ),
                          ),

                          // Tua tới 15s
                          IconButton(
                            icon: const Icon(Icons.forward_10_rounded, color: Colors.white, size: 36),
                            tooltip: "Tới 15 giây",
                            onPressed: () => _service.skipForward15(),
                          ),

                          // Nút dừng
                          IconButton(
                            icon: const Icon(Icons.stop_circle_outlined, color: Colors.white54, size: 28),
                            tooltip: "Dừng phát",
                            onPressed: () {
                              _service.stop();
                              Navigator.pop(context);
                            },
                          ),
                        ],
                      ),
                      const SizedBox(height: 12),
                    ],
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  // TAB 1: BÌA SÁCH VÀ MÁY PHÁT NGHỆ THUẬT
  Widget _buildPlayerTab() {
    return Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Spacer(),
        // Đĩa quay hoặc Bìa sách nghệ thuật
        Center(
          child: RotationTransition(
            turns: _rotationController,
            child: Container(
              width: 210,
              height: 210,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.7),
                    blurRadius: 25,
                    offset: const Offset(0, 10),
                  ),
                  BoxShadow(
                    color: Colors.orange.withOpacity(0.25),
                    blurRadius: 35,
                  ),
                ],
                border: Border.all(color: Colors.orange.withOpacity(0.4), width: 3),
              ),
              child: ClipOval(
                child: _service.currentCoverUrl.isNotEmpty
                    ? Image.network(
                        _service.currentCoverUrl,
                        fit: BoxFit.cover,
                        errorBuilder: (_, __, ___) => Container(
                          color: Colors.grey[900],
                          child: const Icon(Icons.record_voice_over_rounded, color: Colors.orangeAccent, size: 60),
                        ),
                      )
                    : Container(
                        color: Colors.grey[900],
                        child: const Icon(Icons.record_voice_over_rounded, color: Colors.orangeAccent, size: 60),
                      ),
              ),
            ),
          ),
        ),
        const SizedBox(height: 20),

        // Tiêu đề sách và tác giả
        Text(
          _service.currentTitle.isNotEmpty ? _service.currentTitle : "Audiobook",
          style: const TextStyle(color: Colors.white, fontSize: 19, fontWeight: FontWeight.bold),
          textAlign: TextAlign.center,
          maxLines: 1,
          overflow: TextOverflow.ellipsis,
        ),
        const SizedBox(height: 4),
        Text(
          "Tác giả: ${_service.currentAuthor.isNotEmpty ? _service.currentAuthor : 'Đang cập nhật'}",
          style: const TextStyle(color: Colors.orangeAccent, fontSize: 13, fontWeight: FontWeight.w500),
          textAlign: TextAlign.center,
        ),
        const SizedBox(height: 6),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.08),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                _service.isPlaying ? Icons.volume_up_rounded : Icons.volume_mute_rounded,
                size: 14,
                color: Colors.orangeAccent,
              ),
              const SizedBox(width: 6),
              Flexible(
                child: Text(
                  _service.isLoading ? "Đang kết nối âm thanh..." : _service.currentChapter,
                  style: const TextStyle(color: Colors.white70, fontSize: 12),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 12),

        // Nút mở bản sách đọc
        TextButton.icon(
          onPressed: _openBookInReader,
          icon: const Icon(Icons.chrome_reader_mode_rounded, color: Colors.orangeAccent, size: 16),
          label: const Text(
            "Mở bản đọc sách (PDF/EPUB)",
            style: TextStyle(color: Colors.orangeAccent, fontSize: 13, fontWeight: FontWeight.bold),
          ),
          style: TextButton.styleFrom(
            backgroundColor: Colors.orange.withOpacity(0.12),
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
          ),
        ),
        const Spacer(),
      ],
    );
  }

  // TAB 2: ĐỌC NỘI DUNG SÁCH / LỜI ĐỌC THỰC TẾ
  Widget _buildTranscriptTab() {
    final chapters = _service.chapters;
    final content = _service.currentChapterContent;
    final bookId = _service.currentBookId;
    
    // Tìm index của chương hiện tại (0-indexed)
    int currentIdx = chapters.indexWhere((c) => c['title'] == _service.currentChapter);
    if (currentIdx < 0) currentIdx = 0;
    final bool isChapterAudioPlaying = _service.isPlaying && _service.currentAudioUrl.contains('/chapters/');

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 4),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.4),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: Colors.white12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // 1. Tiêu đề chương và công cụ chỉnh cỡ chữ
          Row(
            children: [
              const Icon(Icons.menu_book_rounded, color: Colors.orangeAccent, size: 20),
              const SizedBox(width: 8),
              Expanded(
                child: Text(
                  _service.currentChapter,
                  style: const TextStyle(color: Colors.orangeAccent, fontSize: 14, fontWeight: FontWeight.bold),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              // Nút giảm cỡ chữ
              InkWell(
                onTap: () {
                  if (_transcriptFontSize > 12.0) {
                    setState(() => _transcriptFontSize -= 1.5);
                  }
                },
                borderRadius: BorderRadius.circular(6),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 3),
                  decoration: BoxDecoration(color: Colors.white12, borderRadius: BorderRadius.circular(6)),
                  child: const Text("A-", style: TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.bold)),
                ),
              ),
              const SizedBox(width: 6),
              // Nút tăng cỡ chữ
              InkWell(
                onTap: () {
                  if (_transcriptFontSize < 24.0) {
                    setState(() => _transcriptFontSize += 1.5);
                  }
                },
                borderRadius: BorderRadius.circular(6),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 7, vertical: 3),
                  decoration: BoxDecoration(color: Colors.white12, borderRadius: BorderRadius.circular(6)),
                  child: const Text("A+", style: TextStyle(color: Colors.white70, fontSize: 11, fontWeight: FontWeight.bold)),
                ),
              ),
            ],
          ),
          const SizedBox(height: 10),

          // 2. Danh sách chọn chương nhanh dạng chips
          if (chapters.length > 1)
            SizedBox(
              height: 32,
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                itemCount: chapters.length,
                itemBuilder: (ctx, i) {
                  final ch = chapters[i];
                  final isCur = ch['title'] == _service.currentChapter;
                  return Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: ChoiceChip(
                      label: Text("Chương ${i + 1}", style: TextStyle(color: isCur ? Colors.black : Colors.white70, fontSize: 11, fontWeight: FontWeight.bold)),
                      selected: isCur,
                      selectedColor: Colors.orange,
                      backgroundColor: Colors.white10,
                      onSelected: (_) {
                        _service.seekToChapter(
                          ch['startSec'] as int,
                          ch['title'] as String,
                          chapterContent: ch['content'] as String?,
                        );
                      },
                    ),
                  );
                },
              ),
            ),
          const SizedBox(height: 10),

          // 3. NÚT PHÁT ĐỌC NỘI DUNG CHƯƠNG BẰNG GIỌNG NÓI AI
          if (bookId != null && content.isNotEmpty)
            Container(
              margin: const EdgeInsets.only(bottom: 10),
              width: double.infinity,
              child: ElevatedButton.icon(
                style: ElevatedButton.styleFrom(
                  backgroundColor: isChapterAudioPlaying ? Colors.orange : Colors.white.withOpacity(0.08),
                  foregroundColor: isChapterAudioPlaying ? Colors.black : Colors.orangeAccent,
                  side: BorderSide(color: Colors.orange.withOpacity(0.6), width: 1),
                  padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 14),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                icon: Icon(
                  isChapterAudioPlaying ? Icons.pause_circle_filled_rounded : Icons.play_circle_fill_rounded,
                  size: 20,
                  color: isChapterAudioPlaying ? Colors.black : Colors.orangeAccent,
                ),
                label: Text(
                  isChapterAudioPlaying
                      ? "Đang phát giọng đọc chương này (Bấm để tạm dừng)"
                      : "Nghe đọc nội dung chương này (Giọng AI chuẩn)",
                  style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.bold),
                  maxLines: 1,
                  overflow: TextOverflow.ellipsis,
                ),
                onPressed: () {
                  if (isChapterAudioPlaying) {
                    _service.togglePlayPause();
                  } else {
                    _service.playChapterAudio(
                      bookId: bookId,
                      chapterIndex: currentIdx + 1,
                      chapterTitle: _service.currentChapter,
                      chapterContent: content,
                    );
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text("Đang kết nối giọng đọc thuyết minh cho '${_service.currentChapter}'..."),
                        backgroundColor: Colors.orange,
                        duration: const Duration(seconds: 2),
                      ),
                    );
                  }
                },
              ),
            ),

          // 4. Nội dung văn bản đọc thực tế của chương
          Expanded(
            child: content.isNotEmpty
                ? SingleChildScrollView(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: content
                          .split('\n')
                          .where((l) => l.trim().isNotEmpty)
                          .map((para) => Padding(
                                padding: const EdgeInsets.only(bottom: 12.0),
                                child: Text(
                                  para.trim(),
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: _transcriptFontSize,
                                    height: 1.68,
                                    letterSpacing: 0.2,
                                  ),
                                  textAlign: TextAlign.justify,
                                ),
                              ))
                          .toList(),
                    ),
                  )
                : Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.menu_book_rounded, color: Colors.white38, size: 40),
                        const SizedBox(height: 10),
                        const Text(
                          "Đang tải nội dung văn bản hoàn chỉnh của tác phẩm...",
                          textAlign: TextAlign.center,
                          style: TextStyle(color: Colors.white60, fontSize: 13),
                        ),
                        const SizedBox(height: 12),
                        OutlinedButton.icon(
                          onPressed: () {
                            if (_service.currentBookId != null) {
                              _service.playBook(
                                bookId: _service.currentBookId!,
                                title: _service.currentTitle,
                                author: _service.currentAuthor,
                                audioUrl: _service.currentAudioUrl,
                                coverUrl: _service.currentCoverUrl,
                              );
                            }
                          },
                          icon: const Icon(Icons.refresh_rounded, color: Colors.orangeAccent, size: 16),
                          label: const Text("Tải lại nội dung", style: TextStyle(color: Colors.orangeAccent, fontSize: 12)),
                          style: OutlinedButton.styleFrom(side: const BorderSide(color: Colors.orangeAccent)),
                        ),
                      ],
                    ),
                  ),
          ),

          // 5. Thanh điều hướng chương trước / sau & Mở sách đọc
          if (chapters.length > 1)
            Padding(
              padding: const EdgeInsets.only(top: 8.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  TextButton.icon(
                    onPressed: currentIdx > 0
                        ? () {
                            final prev = chapters[currentIdx - 1];
                            _service.seekToChapter(
                              prev['startSec'] as int,
                              prev['title'] as String,
                              chapterContent: prev['content'] as String?,
                            );
                          }
                        : null,
                    icon: const Icon(Icons.arrow_back_ios_rounded, size: 13, color: Colors.orangeAccent),
                    label: const Text("Chương trước", style: TextStyle(color: Colors.orangeAccent, fontSize: 12)),
                  ),
                  TextButton.icon(
                    onPressed: _openBookInReader,
                    icon: const Icon(Icons.chrome_reader_mode_rounded, size: 13, color: Colors.white70),
                    label: const Text("Bản đọc sách", style: TextStyle(color: Colors.white70, fontSize: 12)),
                  ),
                  TextButton.icon(
                    onPressed: currentIdx < chapters.length - 1
                        ? () {
                            final next = chapters[currentIdx + 1];
                            _service.seekToChapter(
                              next['startSec'] as int,
                              next['title'] as String,
                              chapterContent: next['content'] as String?,
                            );
                          }
                        : null,
                    icon: const Icon(Icons.arrow_forward_ios_rounded, size: 13, color: Colors.orangeAccent),
                    label: const Text("Chương sau", style: TextStyle(color: Colors.orangeAccent, fontSize: 12)),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
