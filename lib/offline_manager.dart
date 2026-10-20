// offline_manager.dart
import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'api_config.dart';

class OfflineBook {
  final int id;
  final String title;
  final String author;
  final String imageUrl;
  final String localImagePath;
  final String pdfUrl;
  final String localPdfPath;
  final String audioUrl;
  final String localAudioPath;
  final String description;
  final int fileSize; // bytes
  final int downloadedAt; // timestamp ms

  OfflineBook({
    required this.id,
    required this.title,
    required this.author,
    this.imageUrl = '',
    this.localImagePath = '',
    this.pdfUrl = '',
    this.localPdfPath = '',
    this.audioUrl = '',
    this.localAudioPath = '',
    this.description = '',
    this.fileSize = 0,
    required this.downloadedAt,
  });

  Map<String, dynamic> toJson() => {
    'id': id,
    'title': title,
    'author': author,
    'image_url': imageUrl,
    'local_image_path': localImagePath,
    'pdf_url': pdfUrl,
    'local_pdf_path': localPdfPath,
    'audio_url': audioUrl,
    'local_audio_path': localAudioPath,
    'description': description,
    'file_size': fileSize,
    'downloaded_at': downloadedAt,
  };

  factory OfflineBook.fromJson(Map<String, dynamic> json) => OfflineBook(
    id: json['id'] ?? 0,
    title: json['title'] ?? '',
    author: json['author'] ?? '',
    imageUrl: json['image_url'] ?? '',
    localImagePath: json['local_image_path'] ?? '',
    pdfUrl: json['pdf_url'] ?? '',
    localPdfPath: json['local_pdf_path'] ?? '',
    audioUrl: json['audio_url'] ?? '',
    localAudioPath: json['local_audio_path'] ?? '',
    description: json['description'] ?? '',
    fileSize: json['file_size'] ?? 0,
    downloadedAt: json['downloaded_at'] ?? 0,
  );

  String get formattedFileSize {
    if (fileSize <= 0) return '0 KB';
    if (fileSize < 1024 * 1024) {
      return '${(fileSize / 1024).toStringAsFixed(1)} KB';
    }
    return '${(fileSize / (1024 * 1024)).toStringAsFixed(1)} MB';
  }
}

class OfflineManager extends ChangeNotifier {
  static final OfflineManager _instance = OfflineManager._internal();
  factory OfflineManager() => _instance;
  OfflineManager._internal() {
    loadOfflineBooks();
  }

  static const _storageKey = 'offline_saved_books_v1';
  final List<OfflineBook> _books = [];
  final Map<int, double> _downloadProgress = {};
  final Set<int> _downloadingIds = {};

  List<OfflineBook> get offlineBooks => List.unmodifiable(_books);

  bool isDownloading(int bookId) => _downloadingIds.contains(bookId);

  double getProgress(int bookId) => _downloadProgress[bookId] ?? 0.0;

  bool isDownloaded(int bookId) {
    if (kIsWeb) return false;
    final b = getOfflineBook(bookId);
    if (b == null) return false;
    if (b.localPdfPath.isNotEmpty && File(b.localPdfPath).existsSync()) return true;
    if (b.localAudioPath.isNotEmpty && File(b.localAudioPath).existsSync()) return true;
    return false;
  }

  OfflineBook? getOfflineBook(int bookId) {
    final idx = _books.indexWhere((b) => b.id == bookId);
    return idx != -1 ? _books[idx] : null;
  }

  Future<void> loadOfflineBooks() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final str = prefs.getString(_storageKey);
      if (str != null && str.isNotEmpty) {
        final List<dynamic> list = jsonDecode(str);
        _books.clear();
        for (final item in list) {
          _books.add(OfflineBook.fromJson(item));
        }
        notifyListeners();
      }
    } catch (e) {
      debugPrint("Lỗi tải danh sách sách offline: $e");
    }
  }

  Future<void> _saveToPrefs() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final data = jsonEncode(_books.map((b) => b.toJson()).toList());
      await prefs.setString(_storageKey, data);
    } catch (e) {
      debugPrint("Lỗi lưu SharedPreferences offline: $e");
    }
  }

  Future<String> _getOfflineDirectory() async {
    final appDir = await getApplicationDocumentsDirectory();
    final dir = Directory('${appDir.path}/offline_books');
    if (!await dir.exists()) {
      await dir.create(recursive: true);
    }
    return dir.path;
  }

  /// Tải sách điện tử (PDF/EPUB) hoặc Sách nói (Audio) về thiết bị để đọc offline
  Future<bool> downloadBook({
    required int bookId,
    required String title,
    required String author,
    String? imageUrl,
    String? pdfUrl,
    String? audioUrl,
    String? description,
    bool isAudioOnly = false,
  }) async {
    if (kIsWeb) {
      debugPrint("Tính năng tải về ngoại tuyến chưa hỗ trợ trên nền tảng Web");
      return false;
    }
    if (_downloadingIds.contains(bookId)) return false;

    _downloadingIds.add(bookId);
    _downloadProgress[bookId] = 0.05;
    notifyListeners();

    try {
      final offlineDir = await _getOfflineDirectory();
      String localPdf = '';
      String localAudio = '';
      String localImg = '';
      int totalBytes = 0;

      // 1. Tải ảnh bìa offline nếu có
      if (imageUrl != null && imageUrl.isNotEmpty) {
        try {
          final imgUrl = ApiConfig.formatUrl(imageUrl);
          final imgRes = await http.get(Uri.parse(imgUrl)).timeout(const Duration(seconds: 10));
          if (imgRes.statusCode == 200) {
            final imgFile = File('$offlineDir/cover_$bookId.jpg');
            await imgFile.writeAsBytes(imgRes.bodyBytes, flush: true);
            localImg = imgFile.path;
            totalBytes += imgRes.bodyBytes.length;
          }
        } catch (_) {}
      }

      _downloadProgress[bookId] = 0.2;
      notifyListeners();

      // 2. Tải nội dung sách (PDF / EPUB hoặc Audio)
      if (!isAudioOnly && pdfUrl != null && pdfUrl.isNotEmpty) {
        final formattedUrl = ApiConfig.formatUrl(pdfUrl);
        final ext = formattedUrl.toLowerCase().endsWith('.epub') ? 'epub' : 'pdf';
        final file = File('$offlineDir/book_${bookId}_content.$ext');

        final req = http.Request('GET', Uri.parse(formattedUrl));
        final response = await http.Client().send(req);

        if (response.statusCode == 200) {
          final contentLength = response.contentLength ?? 0;
          int downloaded = 0;
          final List<int> bytes = [];

          await for (var chunk in response.stream) {
            bytes.addAll(chunk);
            downloaded += chunk.length;
            if (contentLength > 0) {
              final progress = 0.2 + (downloaded / contentLength) * 0.75;
              _downloadProgress[bookId] = progress.clamp(0.2, 0.95);
              notifyListeners();
            }
          }
          await file.writeAsBytes(bytes, flush: true);
          localPdf = file.path;
          totalBytes += bytes.length;
        }
      }

      if (isAudioOnly && audioUrl != null && audioUrl.isNotEmpty) {
        final formattedUrl = ApiConfig.formatUrl(audioUrl);
        final file = File('$offlineDir/audio_${bookId}_content.mp3');

        final req = http.Request('GET', Uri.parse(formattedUrl));
        final response = await http.Client().send(req);

        if (response.statusCode == 200) {
          final contentLength = response.contentLength ?? 0;
          int downloaded = 0;
          final List<int> bytes = [];

          await for (var chunk in response.stream) {
            bytes.addAll(chunk);
            downloaded += chunk.length;
            if (contentLength > 0) {
              final progress = 0.2 + (downloaded / contentLength) * 0.75;
              _downloadProgress[bookId] = progress.clamp(0.2, 0.95);
              notifyListeners();
            }
          }
          await file.writeAsBytes(bytes, flush: true);
          localAudio = file.path;
          totalBytes += bytes.length;
        }
      }

      // Xóa sách cũ nếu đã tải trước đó rồi cập nhật bản mới
      _books.removeWhere((b) => b.id == bookId);
      final offlineBook = OfflineBook(
        id: bookId,
        title: title,
        author: author,
        imageUrl: imageUrl ?? '',
        localImagePath: localImg,
        pdfUrl: pdfUrl ?? '',
        localPdfPath: localPdf,
        audioUrl: audioUrl ?? '',
        localAudioPath: localAudio,
        description: description ?? '',
        fileSize: totalBytes,
        downloadedAt: DateTime.now().millisecondsSinceEpoch,
      );
      _books.insert(0, offlineBook);
      await _saveToPrefs();

      _downloadProgress[bookId] = 1.0;
      _downloadingIds.remove(bookId);
      notifyListeners();
      return true;
    } catch (e) {
      debugPrint("Lỗi tải sách offline: $e");
      _downloadingIds.remove(bookId);
      _downloadProgress.remove(bookId);
      notifyListeners();
      return false;
    }
  }

  /// Xóa sách offline khỏi bộ nhớ máy
  Future<void> deleteOfflineBook(int bookId) async {
    if (kIsWeb) return;
    try {
      final b = getOfflineBook(bookId);
      if (b != null) {
        if (b.localPdfPath.isNotEmpty) {
          final f = File(b.localPdfPath);
          if (await f.exists()) await f.delete();
        }
        if (b.localAudioPath.isNotEmpty) {
          final f = File(b.localAudioPath);
          if (await f.exists()) await f.delete();
        }
        if (b.localImagePath.isNotEmpty) {
          final f = File(b.localImagePath);
          if (await f.exists()) await f.delete();
        }
        _books.removeWhere((item) => item.id == bookId);
        await _saveToPrefs();
        notifyListeners();
      }
    } catch (e) {
      debugPrint("Lỗi xóa sách offline: $e");
    }
  }
}
