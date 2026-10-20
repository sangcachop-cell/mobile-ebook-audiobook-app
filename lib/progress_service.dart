// progress_service.dart
import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import 'api_config.dart';
import 'user_session.dart';

class ProgressService {
  static final ProgressService _instance = ProgressService._internal();
  factory ProgressService() => _instance;
  ProgressService._internal();

  /// Lưu tiến độ đọc/nghe cục bộ và đồng bộ lên server nếu người dùng đã đăng nhập
  static Future<void> updateProgress({
    required int bookId,
    String? username,
    int? lastPage,
    String? lastEpubCfi,
    int? lastAudioPositionMs,
    double? progressPercent,
  }) async {
    // 1. Lưu cục bộ qua SharedPreferences
    try {
      final prefs = await SharedPreferences.getInstance();
      String effectiveUser = username ?? '';
      if (effectiveUser.isEmpty) {
        final session = await UserSession.getSession();
        effectiveUser = session?['username'] ?? 'guest';
      }

      if (lastPage != null) {
        await prefs.setInt('pdf_page_${effectiveUser}_$bookId', lastPage);
      }
      if (lastEpubCfi != null && lastEpubCfi.isNotEmpty) {
        await prefs.setString('epub_cfi_${effectiveUser}_$bookId', lastEpubCfi);
      }
      if (lastAudioPositionMs != null) {
        await prefs.setInt('audio_pos_$bookId', lastAudioPositionMs);
      }

      // 2. Đồng bộ lên Backend Server nếu không phải khách
      final userLower = effectiveUser.trim().toLowerCase();
      if (userLower.isNotEmpty &&
          userLower != 'guest' &&
          userLower != 'null' &&
          !userLower.contains('khach')) {
        final url = Uri.parse('${ApiConfig.baseUrl}/api/progress/update');
        http.post(
          url,
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode({
            'username': effectiveUser.trim(),
            'book_id': bookId,
            'last_page': lastPage ?? 0,
            'last_epub_cfi': lastEpubCfi ?? '',
            'last_audio_position_ms': lastAudioPositionMs ?? 0,
            'progress_percent': progressPercent ?? 0.0,
          }),
        ).catchError((e) {
          debugPrint("Lỗi đồng bộ tiến độ lên server: $e");
          return http.Response('', 500);
        });
      }
    } catch (e) {
      debugPrint("Lỗi lưu tiến độ: $e");
    }
  }

  /// Lấy danh sách tiến độ đọc/nghe của người dùng từ backend
  static Future<List<Map<String, dynamic>>> getUserProgress(String username) async {
    final userLower = username.trim().toLowerCase();
    if (userLower.isEmpty || userLower == 'guest' || userLower.contains('khach')) {
      return [];
    }

    try {
      final url = Uri.parse('${ApiConfig.baseUrl}/api/progress/${username.trim()}');
      final response = await http.get(url).timeout(const Duration(seconds: 4));
      if (response.statusCode == 200) {
        final List<dynamic> list = jsonDecode(utf8.decode(response.bodyBytes));
        return list.map((e) => Map<String, dynamic>.from(e)).toList();
      }
    } catch (e) {
      debugPrint("Lỗi lấy tiến độ từ server: $e");
    }
    return [];
  }
}
