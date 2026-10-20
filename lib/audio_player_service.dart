import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:audioplayers/audioplayers.dart';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'progress_service.dart';
import 'offline_manager.dart';
import 'api_config.dart';

class AudioPlayerService extends ChangeNotifier {
  static final AudioPlayerService _instance = AudioPlayerService._internal();
  factory AudioPlayerService() => _instance;
  AudioPlayerService._internal() {
    _initAudioListeners();
  }

  final AudioPlayer _player = AudioPlayer();

  // Trạng thái phát
  bool _isPlaying = false;
  bool _isLoading = false;
  Duration _position = Duration.zero;
  Duration _duration = Duration.zero;
  double _playbackSpeed = 1.0;

  // Hẹn giờ tắt (Sleep Timer)
  Timer? _sleepTimer;
  Timer? _countdownTicker;
  int _sleepTimerSecondsLeft = 0;

  // Thông tin sách hiện tại
  int? _currentBookId;
  String _currentTitle = '';
  String _currentAuthor = '';
  String _currentCoverUrl = '';
  String _currentAudioUrl = '';
  String _currentChapter = 'Chương 1: Mở đầu';
  String _currentChapterContent = '';
  List<Map<String, dynamic>> _dynamicChapters = [];

  // Getters
  bool get isPlaying => _isPlaying;
  bool get isLoading => _isLoading;
  Duration get position => _position;
  Duration get duration => _duration;
  double get playbackSpeed => _playbackSpeed;
  int? get currentBookId => _currentBookId;
  String get currentTitle => _currentTitle;
  String get currentAuthor => _currentAuthor;
  String get currentCoverUrl => _currentCoverUrl;
  String get currentAudioUrl => _currentAudioUrl;
  String get currentChapter => _currentChapter;
  String get currentChapterContent => _currentChapterContent;
  bool get hasActiveAudio => _currentAudioUrl.isNotEmpty;
  bool get isSleepTimerActive => _sleepTimer != null && _sleepTimerSecondsLeft > 0;
  int get sleepTimerSecondsLeft => _sleepTimerSecondsLeft;

  String get formattedSleepTimer {
    if (!isSleepTimerActive) return '';
    final mins = _sleepTimerSecondsLeft ~/ 60;
    final secs = _sleepTimerSecondsLeft % 60;
    return '${mins.toString().padLeft(2, '0')}:${secs.toString().padLeft(2, '0')}';
  }

  List<Map<String, dynamic>> get chapters {
    if (_dynamicChapters.isNotEmpty) {
      final totalSec = _duration.inSeconds > 0 ? _duration.inSeconds : 600;
      final step = totalSec / _dynamicChapters.length;
      return _dynamicChapters.asMap().entries.map((entry) {
        final idx = entry.key;
        final c = entry.value;
        return {
          'title': c['title'] ?? 'Chương ${idx + 1}',
          'startSec': (idx * step).toInt(),
          'content': c['content'] ?? '',
          'order': idx + 1,
        };
      }).toList();
    }

    if (_duration.inSeconds > 0) {
      final totalSec = _duration.inSeconds;
      return [
        {'title': 'Chương 1: Mở đầu & Khởi nguyên', 'startSec': 0, 'order': 1},
        {'title': 'Chương 2: Đột phá & Tăng tốc', 'startSec': (totalSec * 0.35).toInt(), 'order': 2},
        {'title': 'Chương 3: Đích đến & Thành công', 'startSec': (totalSec * 0.70).toInt(), 'order': 3},
      ];
    }
    return [
      {'title': 'Chương 1: Mở đầu & Khởi nguyên', 'startSec': 0, 'order': 1},
    ];
  }

  void _initAudioListeners() {
    _player.onPlayerStateChanged.listen((state) {
      _isPlaying = state == PlayerState.playing;
      if (state == PlayerState.playing || state == PlayerState.paused) {
        _isLoading = false;
      }
      notifyListeners();
    });

    _player.onPositionChanged.listen((pos) {
      _position = pos;
      _isLoading = false;
      notifyListeners();
      _autoSavePosition();
    });

    _player.onDurationChanged.listen((dur) {
      _duration = dur;
      notifyListeners();
    });

    _player.onPlayerComplete.listen((_) {
      _isPlaying = false;
      _isLoading = false;
      _position = Duration.zero;
      notifyListeners();
    });
  }

  // Tự động lưu vị trí nghe mỗi 5 giây
  DateTime _lastSaveTime = DateTime.now();
  void _autoSavePosition() async {
    if (_currentBookId == null) return;
    if (DateTime.now().difference(_lastSaveTime).inSeconds < 5) return;
    _lastSaveTime = DateTime.now();

    try {
      final double percent = _duration.inMilliseconds > 0
          ? (_position.inMilliseconds / _duration.inMilliseconds * 100).clamp(0.0, 100.0)
          : 0.0;
      await ProgressService.updateProgress(
        bookId: _currentBookId!,
        lastAudioPositionMs: _position.inMilliseconds,
        progressPercent: percent,
      );
    } catch (_) {}
  }

  Future<bool> _tryPlaySource(String url, int initialPosMs) async {
    try {
      Source source;
      if (url.startsWith('http://') || url.startsWith('https://') || url.startsWith('blob:') || kIsWeb) {
        source = UrlSource(url);
      } else {
        source = DeviceFileSource(url);
      }

      await _player.play(
        source,
        position: initialPosMs > 0 ? Duration(milliseconds: initialPosMs) : null,
      );

      try {
        if (_playbackSpeed != 1.0) {
          await _player.setPlaybackRate(_playbackSpeed);
        }
      } catch (_) {}

      return true;
    } catch (e) {
      debugPrint("Lỗi khi phát nguồn âm thanh ($url): $e");
      return false;
    }
  }

  /// Nạp danh sách chương và nội dung văn bản thực từ máy chủ
  Future<void> _fetchBookDetailsAndChapters(int bookId) async {
    try {
      final url = Uri.parse('${ApiConfig.baseUrl}/api/books/$bookId');
      final res = await http.get(url).timeout(const Duration(seconds: 6));
      if (res.statusCode == 200) {
        final data = jsonDecode(utf8.decode(res.bodyBytes));
        final rawChapters = data['chapters'] as List<dynamic>? ?? [];
        if (rawChapters.isNotEmpty) {
          _dynamicChapters = rawChapters.map((e) => Map<String, dynamic>.from(e)).toList();
          _currentChapter = _dynamicChapters[0]['title'] ?? _currentChapter;
          _currentChapterContent = _dynamicChapters[0]['content'] ?? '';
        } else if (data['content'] != null && (data['content'] as String).isNotEmpty) {
          _currentChapterContent = data['content'];
        }
        notifyListeners();
      }
    } catch (e) {
      debugPrint("Lỗi nạp chương chi tiết sách ID $bookId: $e");
    }
  }

  /// Phát một sách nói hoặc tiếp tục nếu đã đang phát
  Future<void> playBook({
    required int bookId,
    required String title,
    required String author,
    required String audioUrl,
    required String coverUrl,
    String? chapterTitle,
  }) async {
    // Chuẩn hóa URL: bỏ www.archive.org nếu có để tránh timeout mạng
    String cleanedAudioUrl = audioUrl.trim();
    if (cleanedAudioUrl.contains('www.archive.org')) {
      cleanedAudioUrl = cleanedAudioUrl.replaceAll('www.archive.org', 'archive.org');
    }
    if (cleanedAudioUrl.isEmpty) {
      cleanedAudioUrl = 'uploads/audio_sample_1.mp3';
    }

    final formattedAudio = ApiConfig.formatUrl(cleanedAudioUrl);
    final formattedCover = ApiConfig.formatUrl(coverUrl);

    // Nếu bấm đúng sách đang phát, chỉ toggle
    if (_currentBookId == bookId && _currentAudioUrl == formattedAudio) {
      if (!_isPlaying) {
        await resume();
      }
      return;
    }

    _currentBookId = bookId;
    _currentTitle = title;
    _currentAuthor = author;
    _currentAudioUrl = formattedAudio;
    _currentCoverUrl = formattedCover;
    _currentChapter = chapterTitle ?? 'Chương 1: Mở đầu';
    _currentChapterContent = '';
    _dynamicChapters = [];
    _position = Duration.zero;
    _duration = Duration.zero;
    _isLoading = true;
    notifyListeners();

    // Nạp chi tiết chương và nội dung văn bản từ máy chủ
    _fetchBookDetailsAndChapters(bookId);

    try {
      await _player.stop();

      // Kiểm tra vị trí đã lưu trước đó để tiếp tục nghe
      final prefs = await SharedPreferences.getInstance();
      final savedMs = prefs.getInt('audio_pos_$bookId') ?? 0;

      // Ưu tiên tệp audio offline nếu đã tải về máy (trên thiết bị di động/desktop)
      String effectiveAudioUrl = formattedAudio;
      if (!kIsWeb) {
        final offline = OfflineManager().getOfflineBook(bookId);
        if (offline != null && offline.localAudioPath.isNotEmpty && File(offline.localAudioPath).existsSync()) {
          effectiveAudioUrl = offline.localAudioPath;
        }
      }

      bool success = await _tryPlaySource(effectiveAudioUrl, savedMs);

      // Nếu nguồn chính không thể tải hoặc timeout, tự động chuyển sang file audio mẫu nội bộ
      if (!success) {
        final fallbackUrl = ApiConfig.formatUrl('uploads/audio_sample_1.mp3');
        if (effectiveAudioUrl != fallbackUrl) {
          debugPrint("Phát dự phòng nguồn âm thanh cục bộ: $fallbackUrl");
          success = await _tryPlaySource(fallbackUrl, savedMs);
        }
      }

      if (!success) {
        _isLoading = false;
        notifyListeners();
      }
    } catch (e) {
      debugPrint("Lỗi phát audiobook: $e");
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> resume() async {
    try {
      await _player.resume();
    } catch (e) {
      debugPrint("Lỗi resume audio: $e");
    }
  }

  Future<void> pause() async {
    try {
      await _player.pause();
    } catch (e) {
      debugPrint("Lỗi pause audio: $e");
    }
  }

  Future<void> togglePlayPause() async {
    if (_isPlaying) {
      await pause();
    } else {
      await resume();
    }
  }

  Future<void> seek(Duration pos) async {
    try {
      await _player.seek(pos);
    } catch (e) {
      debugPrint("Lỗi seek audio: $e");
    }
  }

  Future<void> skipForward15() async {
    final newPos = _position + const Duration(seconds: 15);
    if (newPos > _duration) {
      await seek(_duration);
    } else {
      await seek(newPos);
    }
  }

  Future<void> skipBackward15() async {
    final newPos = _position - const Duration(seconds: 15);
    if (newPos < Duration.zero) {
      await seek(Duration.zero);
    } else {
      await seek(newPos);
    }
  }

  Future<void> setSpeed(double speed) async {
    _playbackSpeed = speed;
    await _player.setPlaybackRate(speed);
    notifyListeners();
  }

  /// Cài đặt hẹn giờ tắt tự động (phút)
  void setSleepTimer(int minutes) {
    cancelSleepTimer();
    if (minutes <= 0) return;

    _sleepTimerSecondsLeft = minutes * 60;
    notifyListeners();

    _countdownTicker = Timer.periodic(const Duration(seconds: 1), (timer) {
      if (_sleepTimerSecondsLeft > 1) {
        _sleepTimerSecondsLeft--;
        notifyListeners();
      } else {
        _sleepTimerSecondsLeft = 0;
        timer.cancel();
      }
    });

    _sleepTimer = Timer(Duration(minutes: minutes), () async {
      await pause();
      cancelSleepTimer();
    });
    notifyListeners();
  }

  /// Hủy chế độ hẹn giờ tắt
  void cancelSleepTimer() {
    _sleepTimer?.cancel();
    _sleepTimer = null;
    _countdownTicker?.cancel();
    _countdownTicker = null;
    _sleepTimerSecondsLeft = 0;
    notifyListeners();
  }

  /// Nhảy tới chương cụ thể
  Future<void> seekToChapter(int startSec, String chapterTitle, {String? chapterContent}) async {
    _currentChapter = chapterTitle;
    if (chapterContent != null && chapterContent.isNotEmpty) {
      _currentChapterContent = chapterContent;
    } else {
      final found = _dynamicChapters.firstWhere(
        (c) => c['title'] == chapterTitle,
        orElse: () => {},
      );
      if (found.isNotEmpty && found['content'] != null) {
        _currentChapterContent = found['content'];
      }
    }
    await seek(Duration(seconds: startSec));
    notifyListeners();
  }

  int _currentChapterIndex = 1;
  int get currentChapterIndex => _currentChapterIndex;

  /// Phát âm thanh thuyết minh đọc trực tiếp nội dung từng chương từ Backend AI Speech
  Future<void> playChapterAudio({
    required int bookId,
    required int chapterIndex,
    required String chapterTitle,
    required String chapterContent,
  }) async {
    _currentBookId = bookId;
    _currentChapterIndex = chapterIndex;
    _currentChapter = chapterTitle;
    _currentChapterContent = chapterContent;
    _isLoading = true;
    notifyListeners();

    final chapterAudioUrl = ApiConfig.formatUrl('api/books/$bookId/chapters/$chapterIndex/audio');
    _currentAudioUrl = chapterAudioUrl;
    _position = Duration.zero;
    _duration = Duration.zero;

    try {
      await _player.stop();
      final success = await _tryPlaySource(chapterAudioUrl, 0);
      if (!success) {
        final fallback = ApiConfig.formatUrl('uploads/audio_sample_1.mp3');
        await _tryPlaySource(fallback, 0);
      }
    } catch (e) {
      debugPrint("Lỗi phát audio chương: $e");
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> stop() async {
    cancelSleepTimer();
    await _player.stop();
    _isPlaying = false;
    _currentAudioUrl = '';
    _currentBookId = null;
    _dynamicChapters = [];
    _currentChapterContent = '';
    notifyListeners();
  }

  @override
  void dispose() {
    cancelSleepTimer();
    _player.dispose();
    super.dispose();
  }
}
