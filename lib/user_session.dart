import 'package:shared_preferences/shared_preferences.dart';

class UserSession {
  static const _keyUsername = 'session_username';
  static const _keyIsAdmin = 'session_is_admin';
  static const _keyFullName = 'session_full_name';
  static const _keyAvatarUrl = 'session_avatar_url';

  /// Lưu thông tin phiên đăng nhập
  static Future<void> saveSession({
    required String username,
    required bool isAdmin,
    String? fullName,
    String? avatarUrl,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_keyUsername, username);
    await prefs.setBool(_keyIsAdmin, isAdmin);
    await prefs.setString(_keyFullName, fullName ?? username);
    await prefs.setString(_keyAvatarUrl, avatarUrl ?? '');
  }

  /// Lấy thông tin phiên đăng nhập hiện tại
  static Future<Map<String, dynamic>?> getSession() async {
    final prefs = await SharedPreferences.getInstance();
    final username = prefs.getString(_keyUsername);
    if (username == null || username.isEmpty) return null;
    return {
      'username': username,
      'is_admin': prefs.getBool(_keyIsAdmin) ?? false,
      'full_name': prefs.getString(_keyFullName) ?? username,
      'avatar_url': prefs.getString(_keyAvatarUrl) ?? '',
    };
  }

  /// Xóa phiên đăng nhập (Đăng xuất)
  static Future<void> clearSession() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_keyUsername);
    await prefs.remove(_keyIsAdmin);
    await prefs.remove(_keyFullName);
    await prefs.remove(_keyAvatarUrl);
  }
}
