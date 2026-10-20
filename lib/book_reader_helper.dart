import 'package:flutter/material.dart';
import 'package:flutter/foundation.dart';
import 'dart:io';
import 'pdf_viewer_screen.dart';
import 'epub_viewer_screen.dart';
import 'content_reader_screen.dart';
import 'offline_manager.dart';

class BookReaderHelper {
  /// Nhận diện định dạng EPUB dựa theo URL (hỗ trợ Gutenberg epub3.images, epub2, URL encoding, v.v.)
  static bool _isEpubUrl(String url) {
    String decoded = url;
    try {
      decoded = Uri.decodeFull(url);
    } catch (_) {}
    final lower = decoded.toLowerCase();
    if (lower.endsWith('.epub')) return true;
    if (lower.contains('.epub3') || lower.contains('.epub2') || lower.contains('.epub')) return true;
    if (lower.contains('/epub') && !lower.contains('.mp3') && !lower.contains('.mp4')) return true;
    if (lower.contains('gutenberg.org/ebooks/') && !lower.contains('.pdf')) return true;
    return false;
  }

  /// Điều hướng thông minh dựa vào định dạng tệp (PDF, EPUB hoặc Text Reader), ưu tiên tệp ngoại tuyến đã tải
  static Future<dynamic> openBook({
    required BuildContext context,
    required String fileUrl,
    required String bookTitle,
    required int bookId,
    required String username,
    String author = '',
    int initialPage = 0,
  }) {
    final lower = fileUrl.toLowerCase();
    // Nếu là file audio thuần túy
    if (lower.endsWith('.mp3') || lower.endsWith('.mp4') || lower.endsWith('.wav') || lower.endsWith('.m4a')) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Sách này chỉ có bản Audio. Hãy bấm "Nghe Sách Nói" bên dưới!'),
          backgroundColor: Colors.orangeAccent,
        ),
      );
      return Future.value();
    }

    // Nếu không có tệp PDF/EPUB đính kèm hoặc là tệp txt -> Mở ContentReaderScreen đọc trực tiếp
    if (fileUrl.trim().isEmpty || lower.endsWith('.txt')) {
      return Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => ContentReaderScreen(
            bookId: bookId,
            bookTitle: bookTitle,
            author: author,
            username: username,
          ),
        ),
      );
    }

    String effectivePath = fileUrl;
    if (!kIsWeb) {
      final offline = OfflineManager().getOfflineBook(bookId);
      if (offline != null && offline.localPdfPath.isNotEmpty && File(offline.localPdfPath).existsSync()) {
        effectivePath = offline.localPdfPath;
      }
    }

    if (_isEpubUrl(effectivePath)) {
      return Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => EpubViewerScreen(
            epubUrl: effectivePath,
            bookTitle: bookTitle,
            bookId: bookId,
            username: username,
          ),
        ),
      );
    } else {
      return Navigator.push(
        context,
        MaterialPageRoute(
          builder: (context) => PdfViewerScreen(
            pdfUrl: effectivePath,
            bookTitle: bookTitle,
            bookId: bookId,
            username: username,
            initialPage: initialPage,
          ),
        ),
      );
    }
  }
}
