import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiConfig {
  static const String _prefKey = 'custom_api_base_url';
  static String? _customBaseUrl;

  /// Nạp URL tùy chỉnh từ SharedPreferences khi khởi động
  static Future<void> init() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      _customBaseUrl = prefs.getString(_prefKey);
    } catch (_) {}
  }

  /// Cập nhật URL máy chủ mới (hoặc null để về mặc định)
  static Future<void> setCustomBaseUrl(String? newUrl) async {
    final prefs = await SharedPreferences.getInstance();
    if (newUrl == null || newUrl.trim().isEmpty) {
      _customBaseUrl = null;
      await prefs.remove(_prefKey);
    } else {
      String clean = newUrl.trim();
      if (clean.endsWith('/')) {
        clean = clean.substring(0, clean.length - 1);
      }
      if (!clean.startsWith('http://') && !clean.startsWith('https://')) {
        clean = 'http://$clean';
      }
      _customBaseUrl = clean;
      await prefs.setString(_prefKey, clean);
    }
  }

  /// Base URL đang hoạt động
  static String get baseUrl {
    if (_customBaseUrl != null && _customBaseUrl!.isNotEmpty) {
      return _customBaseUrl!;
    }
    if (kIsWeb) {
      return 'http://localhost:8000';
    }
    if (defaultTargetPlatform == TargetPlatform.android) {
      return 'http://10.0.2.2:8000';
    }
    return 'http://localhost:8000';
  }

  /// Kiểm tra kết nối tới máy chủ (Ping test)
  static Future<bool> testConnection([String? candidateUrl]) async {
    final target = (candidateUrl != null && candidateUrl.isNotEmpty) ? candidateUrl : baseUrl;
    try {
      final uri = Uri.parse('$target/api/ping');
      final res = await http.get(uri).timeout(const Duration(seconds: 3));
      return res.statusCode == 200;
    } catch (_) {
      return false;
    }
  }

  /// Chuyển đổi định dạng URL media/ảnh/audio/pdf tương thích với nền tảng và IP đang chọn
  static String formatUrl(String? url) {
    if (url == null || url.isEmpty) return '';

    String result = url.trim();

    // Chuẩn hóa domain archive.org (bỏ www. để tránh timeout kết nối)
    if (result.contains('www.archive.org')) {
      result = result.replaceAll('www.archive.org', 'archive.org');
    }

    // 1. Tự động thêm baseUrl nếu là đường dẫn tệp tương đối trên server (uploads/... hoặc /uploads/...)
    if (result.startsWith('uploads/')) {
      result = '$baseUrl/$result';
    } else if (result.startsWith('/uploads/')) {
      result = '$baseUrl$result';
    }

    // 2. Nếu chạy trên Trình duyệt Web (kIsWeb) và là URL từ server bên thứ ba ngoài hệ thống,
    // tự động điều hướng qua API proxy-file của FastAPI để bỏ qua giới hạn CORS của trình duyệt.
    if (kIsWeb && result.startsWith('http')) {
      final uri = Uri.tryParse(result);
      if (uri != null) {
        final baseUri = Uri.parse(baseUrl);
        final isOurServer = (uri.host == 'localhost' ||
            uri.host == '127.0.0.1' ||
            uri.host == '10.0.2.2' ||
            uri.host == baseUri.host);
        if (!isOurServer && !result.contains('/api/proxy-file')) {
          result = '$baseUrl/api/proxy-file?url=${Uri.encodeComponent(result)}';
        }
      }
    }

    // 3. Thay thế localhost / 10.0.2.2 theo đúng địa chỉ máy chủ đang được chọn
    try {
      final baseUri = Uri.parse(baseUrl);
      final currentHostPort = '${baseUri.host}:${baseUri.port}';

      if (result.contains('localhost:8000')) {
        result = result.replaceAll('localhost:8000', currentHostPort);
      } else if (result.contains('10.0.2.2:8000')) {
        result = result.replaceAll('10.0.2.2:8000', currentHostPort);
      } else if (result.contains('localhost')) {
        result = result.replaceAll('localhost', baseUri.host);
      } else if (result.contains('10.0.2.2')) {
        result = result.replaceAll('10.0.2.2', baseUri.host);
      }
      return result;
    } catch (_) {
      return result;
    }
  }
}
