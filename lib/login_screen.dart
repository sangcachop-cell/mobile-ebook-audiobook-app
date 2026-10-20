import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'dart:async';
import 'api_config.dart';
import 'main_screen.dart';
import 'explore_screen.dart';
import 'user_session.dart';

class AuthScreen extends StatefulWidget {
  final bool initialIsLogin;
  const AuthScreen({super.key, this.initialIsLogin = true});

  @override
  State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  // --- CONTROLLERS ---
  final userCtrl = TextEditingController();
  final passCtrl = TextEditingController();

  // Các trường đăng ký nâng cao ("kỹ hơn 1 tí")
  final fullNameCtrl = TextEditingController();
  final emailCtrl = TextEditingController();
  final phoneCtrl = TextEditingController();
  final confirmPassCtrl = TextEditingController();

  late bool isLogin;
  bool _isLoading = false;
  bool _obscurePassword = true;
  bool _obscureConfirmPassword = true;
  bool _agreeTerms = true;

  @override
  void initState() {
    super.initState();
    isLogin = widget.initialIsLogin;
    _checkAuthTargetAction();
    _loadSavedSession();
  }


  Future<void> _loadSavedSession() async {
    final session = await UserSession.getSession();
    if (session != null && mounted) {
      setState(() {
        userCtrl.text = session['username'] ?? '';
      });
    }
  }

  void _checkAuthTargetAction() {
    if (ExploreScreen.authTargetAction != null) {
      final action = ExploreScreen.authTargetAction;
      ExploreScreen.authTargetAction = null;
      WidgetsBinding.instance.addPostFrameCallback((_) {
        String msg = "Vui lòng đăng nhập để tiếp tục!";
        if (action == 'comment') {
          msg = "Vui lòng đăng nhập để bình luận bài viết này!";
        } else if (action == 'like') {
          msg = "Vui lòng đăng nhập để thích bài viết này!";
        } else if (action == 'post') {
          msg = "Vui lòng đăng nhập để đăng tải bài viết mới!";
        }
        _showMsg(msg);
      });
    }
  }

  // --- HÀM VALIDATION DỮ LIỆU ĐẦU VÀO CHUẨN XÁC CAO ---
  bool _isValidEmail(String email) {
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    return emailRegex.hasMatch(email);
  }

  bool _isValidPhone(String phone) {
    final phoneRegex = RegExp(r'^(0[3|5|7|8|9])[0-9]{8}$');
    return phoneRegex.hasMatch(phone);
  }

  Future<void> authAction() async {
    final username = userCtrl.text.trim();
    final password = passCtrl.text.trim();

    if (isLogin) {
      // ==================== XỬ LÝ ĐĂNG NHẬP ====================
      if (username.isEmpty || password.isEmpty) {
        _showMsg("Vui lòng điền đầy đủ tên đăng nhập và mật khẩu!", isError: true);
        return;
      }

      setState(() => _isLoading = true);
      final url = Uri.parse('${ApiConfig.baseUrl}/api/login');

      try {
        final res = await http.post(
          url,
          headers: {"Content-Type": "application/json"},
          body: jsonEncode({"username": username, "password": password}),
        ).timeout(const Duration(seconds: 8));

        if (res.statusCode == 200) {
          final data = jsonDecode(utf8.decode(res.bodyBytes));
          bool isAdmin = data['is_admin'] ?? false;
          String fullName = data['full_name'] ?? username;
          String avatarUrl = data['avatar_url'] ?? '';

          await UserSession.saveSession(
            username: username,
            isAdmin: isAdmin,
            fullName: fullName,
            avatarUrl: avatarUrl,
          );

          if (mounted) {
            _showMsg("Đăng nhập thành công! Chào mừng $fullName.", isError: false);
            Navigator.pushReplacement(
              context,
              MaterialPageRoute(
                builder: (context) => MainScreen(
                  username: username,
                  isAdmin: isAdmin,
                ),
              ),
            );
          }
        } else {
          try {
            final errorData = jsonDecode(utf8.decode(res.bodyBytes));
            final errorMsg = errorData['detail'] ?? "Sai tài khoản hoặc mật khẩu!";
            _showMsg(errorMsg, isError: true);
          } catch (_) {
            _showMsg("Lỗi phản hồi từ máy chủ (${res.statusCode})", isError: true);
          }
        }
      } catch (e) {
        _showConnectionError();
      } finally {
        if (mounted) setState(() => _isLoading = false);
      }
    } else {
      // ==================== XỬ LÝ ĐĂNG KÝ KỸ LƯỠNG ("KỸ HƠN 1 TÍ") ====================
      final fullName = fullNameCtrl.text.trim();
      final email = emailCtrl.text.trim();
      final phone = phoneCtrl.text.trim();
      final confirmPass = confirmPassCtrl.text.trim();

      // 1. Kiểm tra Họ và tên
      if (fullName.isEmpty) {
        _showMsg("Vui lòng nhập Họ và tên của bạn!", isError: true);
        return;
      }
      if (fullName.length < 2) {
        _showMsg("Họ và tên quá ngắn! Vui lòng nhập họ tên đầy đủ.", isError: true);
        return;
      }

      // 2. Kiểm tra Tên tài khoản
      if (username.isEmpty) {
        _showMsg("Vui lòng nhập Tên tài khoản!", isError: true);
        return;
      }
      if (username.length < 3) {
        _showMsg("Tên tài khoản phải chứa ít nhất 3 ký tự!", isError: true);
        return;
      }
      if (username.contains(' ')) {
        _showMsg("Tên tài khoản không được chứa khoảng trắng!", isError: true);
        return;
      }

      // 3. Kiểm tra Email
      if (email.isEmpty) {
        _showMsg("Vui lòng nhập Địa chỉ Email!", isError: true);
        return;
      }
      if (!_isValidEmail(email)) {
        _showMsg("Địa chỉ Email không đúng định dạng hợp lệ (vd: ten@gmail.com)!", isError: true);
        return;
      }

      // 4. Kiểm tra Số điện thoại
      if (phone.isEmpty) {
        _showMsg("Vui lòng nhập Số điện thoại!", isError: true);
        return;
      }
      if (!_isValidPhone(phone)) {
        _showMsg("Số điện thoại không hợp lệ (cần 10 chữ số, vd: 0901234567)!", isError: true);
        return;
      }

      // 5. Kiểm tra Mật khẩu
      if (password.isEmpty) {
        _showMsg("Vui lòng nhập Mật khẩu bảo vệ tài khoản!", isError: true);
        return;
      }
      if (password.length < 6) {
        _showMsg("Mật khẩu phải chứa ít nhất 6 ký tự để bảo mật!", isError: true);
        return;
      }

      // 6. Kiểm tra Xác nhận Mật khẩu
      if (confirmPass.isEmpty) {
        _showMsg("Vui lòng nhập lại mật khẩu để xác nhận!", isError: true);
        return;
      }
      if (password != confirmPass) {
        _showMsg("Mật khẩu xác nhận không khớp! Vui lòng kiểm tra lại.", isError: true);
        return;
      }

      // 7. Kiểm tra Điều khoản dịch vụ
      if (!_agreeTerms) {
        _showMsg("Vui lòng đồng ý với Điều khoản dịch vụ BookHub để tiếp tục!", isError: true);
        return;
      }

      setState(() => _isLoading = true);
      final url = Uri.parse('${ApiConfig.baseUrl}/api/register');

      try {
        final res = await http.post(
          url,
          headers: {"Content-Type": "application/json"},
          body: jsonEncode({
            "username": username,
            "password": password,
            "full_name": fullName,
            "email": email,
            "phone": phone,
          }),
        ).timeout(const Duration(seconds: 8));

        if (res.statusCode == 200) {
          final data = jsonDecode(utf8.decode(res.bodyBytes));
          final successMsg = data['message'] ?? "Đăng ký thành công!";
          _showMsg(successMsg, isError: false);

          if (mounted) {
            setState(() {
              isLogin = true;
            });
            passCtrl.clear();
            confirmPassCtrl.clear();
          }
        } else {
          try {
            final errorData = jsonDecode(utf8.decode(res.bodyBytes));
            final errorMsg = errorData['detail'] ?? "Đăng ký không thành công!";
            _showMsg(errorMsg, isError: true);
          } catch (_) {
            _showMsg("Lỗi phản hồi từ máy chủ (${res.statusCode})", isError: true);
          }
        }
      } catch (e) {
        _showConnectionError();
      } finally {
        if (mounted) setState(() => _isLoading = false);
      }
    }
  }

  void _showConnectionError() {
    if (!mounted) return;
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.wifi_off_rounded, color: Colors.white, size: 20),
            const SizedBox(width: 10),
            Expanded(
              child: Text("Không thể kết nối đến máy chủ (${ApiConfig.baseUrl})!"),
            ),
          ],
        ),
        backgroundColor: Colors.redAccent,
        behavior: SnackBarBehavior.floating,
        duration: const Duration(seconds: 6),
        action: SnackBarAction(
          label: "ĐỔI IP MÁY CHỦ",
          textColor: Colors.amberAccent,
          onPressed: _showServerConfigDialog,
        ),
      ),
    );
  }

  // --- HỘP THOẠI CẤU HÌNH IP MÁY CHỦ LINH HOẠT ---
  void _showServerConfigDialog() {
    final customUrlCtrl = TextEditingController(text: ApiConfig.baseUrl);
    bool isTesting = false;
    String? testResult;
    bool? testSuccess;

    showDialog(
      context: context,
      builder: (dialogCtx) => StatefulBuilder(
        builder: (ctx, setDialogState) => AlertDialog(
          backgroundColor: const Color(0xFF1E1E1E),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
          title: const Row(
            children: [
              Icon(Icons.dns_rounded, color: Colors.orange, size: 26),
              SizedBox(width: 10),
              Text(
                "Cấu hình Máy chủ (Backend)",
                style: TextStyle(color: Colors.white, fontSize: 17, fontWeight: FontWeight.bold),
              ),
            ],
          ),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  "Chọn nhanh địa chỉ phù hợp với thiết bị bạn đang dùng để kết nối với Backend FastAPI:",
                  style: TextStyle(color: Colors.white70, fontSize: 12),
                ),
                const SizedBox(height: 12),

                // Danh sách preset
                _buildPresetButton("🌐 Máy tính / Web / Windows", "http://localhost:8000", customUrlCtrl, setDialogState),
                const SizedBox(height: 6),
                _buildPresetButton("📱 Máy ảo Android Emulator", "http://10.0.2.2:8000", customUrlCtrl, setDialogState),
                const SizedBox(height: 6),
                _buildPresetButton("📶 Điện thoại thật (Wi-Fi LAN)", "http://192.168.1.10:8000", customUrlCtrl, setDialogState),
                const SizedBox(height: 14),

                const Text("Địa chỉ URL máy chủ tùy chỉnh:", style: TextStyle(color: Colors.white60, fontSize: 12)),
                const SizedBox(height: 6),
                TextField(
                  controller: customUrlCtrl,
                  style: const TextStyle(color: Colors.white, fontSize: 13),
                  decoration: InputDecoration(
                    prefixIcon: const Icon(Icons.link_rounded, color: Colors.orange, size: 20),
                    filled: true,
                    fillColor: Colors.black38,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 12),
                  ),
                ),
                const SizedBox(height: 12),

                // Nút test kết nối
                SizedBox(
                  width: double.infinity,
                  child: OutlinedButton.icon(
                    style: OutlinedButton.styleFrom(
                      foregroundColor: Colors.orange,
                      side: const BorderSide(color: Colors.orangeAccent),
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
                    ),
                    onPressed: isTesting
                        ? null
                        : () async {
                            setDialogState(() {
                              isTesting = true;
                              testResult = null;
                            });
                            final ok = await ApiConfig.testConnection(customUrlCtrl.text.trim());
                            setDialogState(() {
                              isTesting = false;
                              testSuccess = ok;
                              testResult = ok
                                  ? "✅ Kết nối thành công tới Backend (200 OK)!"
                                  : "❌ Không thể kết nối! Hãy chắc chắn FastAPI đang chạy.";
                            });
                          },
                    icon: isTesting
                        ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(color: Colors.orange, strokeWidth: 2))
                        : const Icon(Icons.network_check_rounded, size: 18),
                    label: Text(isTesting ? "Đang kiểm tra..." : "Kiểm tra kết nối (Ping Test)"),
                  ),
                ),

                if (testResult != null) ...[
                  const SizedBox(height: 10),
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: (testSuccess == true) ? Colors.green.withValues(alpha: 0.15) : Colors.red.withValues(alpha: 0.15),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: (testSuccess == true) ? Colors.green : Colors.redAccent),
                    ),
                    child: Text(
                      testResult!,
                      style: TextStyle(
                        color: (testSuccess == true) ? Colors.greenAccent : Colors.redAccent,
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(dialogCtx),
              child: const Text("Đóng", style: TextStyle(color: Colors.white54)),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: Colors.orange, foregroundColor: Colors.black),
              onPressed: () async {
                await ApiConfig.setCustomBaseUrl(customUrlCtrl.text.trim());
                if (dialogCtx.mounted) Navigator.pop(dialogCtx);
                _showMsg("Đã cập nhật máy chủ: ${ApiConfig.baseUrl}", isError: false);
              },
              child: const Text("Lưu & Áp dụng", style: TextStyle(fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildPresetButton(
    String label,
    String url,
    TextEditingController controller,
    StateSetter setDialogState,
  ) {
    final isSelected = controller.text.trim() == url;
    return InkWell(
      onTap: () {
        setDialogState(() {
          controller.text = url;
        });
      },
      borderRadius: BorderRadius.circular(8),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 8),
        decoration: BoxDecoration(
          color: isSelected ? Colors.orange.withValues(alpha: 0.2) : Colors.white.withValues(alpha: 0.05),
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: isSelected ? Colors.orange : Colors.white12),
        ),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Expanded(
              child: Text(label, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w500)),
            ),
            Text(url, style: const TextStyle(color: Colors.white54, fontSize: 11)),
          ],
        ),
      ),
    );
  }

  void _showForgotPasswordDialog() {
    final resetUserCtrl = TextEditingController(text: userCtrl.text.trim());
    final resetPassCtrl = TextEditingController();
    bool isResetting = false;

    showDialog(
      context: context,
      builder: (dialogCtx) => StatefulBuilder(
        builder: (ctx, setDialogState) => AlertDialog(
          backgroundColor: const Color(0xFF222222),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
          title: const Row(
            children: [
              Icon(Icons.lock_reset_rounded, color: Colors.orange, size: 26),
              SizedBox(width: 10),
              Text("Quên mật khẩu", style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18)),
            ],
          ),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text(
                "Nhập tên tài khoản và mật khẩu mới để khôi phục quyền truy cập vào BookHub:",
                style: TextStyle(color: Colors.white70, fontSize: 13),
              ),
              const SizedBox(height: 16),
              TextField(
                controller: resetUserCtrl,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: "Tên đăng nhập",
                  labelStyle: const TextStyle(color: Colors.white60),
                  prefixIcon: const Icon(Icons.person_outline, color: Colors.orange),
                  filled: true,
                  fillColor: Colors.black26,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: resetPassCtrl,
                obscureText: true,
                style: const TextStyle(color: Colors.white),
                decoration: InputDecoration(
                  labelText: "Mật khẩu mới",
                  labelStyle: const TextStyle(color: Colors.white60),
                  prefixIcon: const Icon(Icons.lock_outline, color: Colors.orange),
                  filled: true,
                  fillColor: Colors.black26,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
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
              onPressed: isResetting
                  ? null
                  : () async {
                      final u = resetUserCtrl.text.trim();
                      final p = resetPassCtrl.text.trim();
                      if (u.isEmpty || p.isEmpty) {
                        _showMsg("Vui lòng điền đầy đủ thông tin!", isError: true);
                        return;
                      }
                      if (p.length < 6) {
                        _showMsg("Mật khẩu mới phải có ít nhất 6 ký tự!", isError: true);
                        return;
                      }

                      setDialogState(() => isResetting = true);
                      try {
                        final url = Uri.parse('${ApiConfig.baseUrl}/api/auth/forgot-password');
                        final res = await http.post(
                          url,
                          headers: {'Content-Type': 'application/json'},
                          body: jsonEncode({'username': u, 'new_password': p}),
                        );
                        if (dialogCtx.mounted) Navigator.pop(dialogCtx);
                        if (res.statusCode == 200) {
                          _showMsg("Đặt lại mật khẩu thành công! Hãy đăng nhập bằng mật khẩu mới.", isError: false);
                          userCtrl.text = u;
                          passCtrl.text = p;
                        } else {
                          try {
                            final err = jsonDecode(utf8.decode(res.bodyBytes))['detail'];
                            _showMsg(err ?? "Không thể đặt lại mật khẩu!", isError: true);
                          } catch (_) {
                            _showMsg("Lỗi phản hồi từ máy chủ (${res.statusCode})", isError: true);
                          }
                        }
                      } catch (e) {
                        if (dialogCtx.mounted) Navigator.pop(dialogCtx);
                        _showMsg("Lỗi kết nối máy chủ: $e", isError: true);
                      }
                    },
              child: isResetting
                  ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(color: Colors.black, strokeWidth: 2))
                  : const Text("Xác nhận", style: TextStyle(fontWeight: FontWeight.bold)),
            ),
          ],
        ),
      ),
    );
  }

  void _showMsg(String m, {bool isError = false}) {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(m),
          backgroundColor: isError ? Colors.redAccent : Colors.green,
          behavior: SnackBarBehavior.floating,
          duration: const Duration(seconds: 4),
        ),
      );
    }
  }

  @override
  void dispose() {
    userCtrl.dispose();
    passCtrl.dispose();
    fullNameCtrl.dispose();
    emailCtrl.dispose();
    phoneCtrl.dispose();
    confirmPassCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    // Màu chủ đạo: Xanh hoàng gia cho Đăng nhập, Cam đất ấm áp cho Đăng ký
    final Color mainColor = isLogin ? const Color(0xFF2C3E50) : const Color(0xFFD35400);

    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          image: DecorationImage(
            image: NetworkImage('https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1000&auto=format&fit=crop'),
            fit: BoxFit.cover,
          ),
        ),
        child: Container(
          color: Colors.black.withValues(alpha: 0.65),
          child: SafeArea(
            child: Center(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    // Thẻ Auth chính
                    Container(
                      padding: const EdgeInsets.all(24),
                      decoration: BoxDecoration(
                        color: mainColor.withValues(alpha: 0.92),
                        borderRadius: BorderRadius.circular(28),
                        boxShadow: [
                          BoxShadow(
                            color: Colors.black.withValues(alpha: 0.4),
                            blurRadius: 20,
                            offset: const Offset(0, 10),
                          ),
                        ],
                      ),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          // Tiêu đề & Logo
                          Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(isLogin ? Icons.auto_stories_rounded : Icons.person_add_alt_1_rounded, color: Colors.orangeAccent, size: 28),
                              const SizedBox(width: 8),
                              Text(
                                isLogin ? "Đăng Nhập" : "Đăng Ký Tài Khoản",
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 24,
                                  fontWeight: FontWeight.bold,
                                  letterSpacing: 0.5,
                                ),
                              ),
                            ],
                          ),
                          const SizedBox(height: 6),
                          Text(
                            isLogin
                                ? "Chào mừng trở lại với tủ sách BookHub"
                                : "Tạo tài khoản để lưu trữ & đồng bộ đọc sách",
                            style: const TextStyle(color: Colors.white70, fontSize: 12),
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 22),

                          if (!isLogin) ...[
                            // ==================== CÁC TRƯỜNG ĐĂNG KÝ CHI TIẾT ("KỸ HƠN 1 TÍ") ====================
                            _buildField(
                              fullNameCtrl,
                              "Họ và tên",
                              Icons.badge_outlined,
                              enabled: !_isLoading,
                            ),
                            const SizedBox(height: 12),

                            _buildField(
                              userCtrl,
                              "Tên đăng nhập",
                              Icons.person_outline,
                              enabled: !_isLoading,
                            ),
                            const SizedBox(height: 12),

                            _buildField(
                              emailCtrl,
                              "Email",
                              Icons.email_outlined,
                              keyboardType: TextInputType.emailAddress,
                              enabled: !_isLoading,
                            ),
                            const SizedBox(height: 12),

                            _buildField(
                              phoneCtrl,
                              "Số điện thoại",
                              Icons.phone_android_rounded,
                              keyboardType: TextInputType.phone,
                              enabled: !_isLoading,
                            ),
                            const SizedBox(height: 12),

                            _buildField(
                              passCtrl,
                              "Mật khẩu",
                              Icons.lock_outline,
                              isPass: true,
                              obscureState: _obscurePassword,
                              onToggleObscure: () => setState(() => _obscurePassword = !_obscurePassword),
                              enabled: !_isLoading,
                            ),
                            const SizedBox(height: 12),

                            _buildField(
                              confirmPassCtrl,
                              "Xác nhận mật khẩu",
                              Icons.lock_reset_rounded,
                              isPass: true,
                              obscureState: _obscureConfirmPassword,
                              onToggleObscure: () => setState(() => _obscureConfirmPassword = !_obscureConfirmPassword),
                              enabled: !_isLoading,
                            ),
                            const SizedBox(height: 12),

                            // Checkbox Điều khoản sử dụng
                            Row(
                              children: [
                                Checkbox(
                                  value: _agreeTerms,
                                  activeColor: Colors.orange,
                                  onChanged: _isLoading ? null : (v) => setState(() => _agreeTerms = v ?? false),
                                ),
                                const Expanded(
                                  child: Text(
                                    "Tôi đồng ý với Điều khoản sử dụng & Chính sách bảo mật của BookHub",
                                    style: TextStyle(color: Colors.white70, fontSize: 11),
                                  ),
                                ),
                              ],
                            ),
                            const SizedBox(height: 8),
                          ] else ...[
                            // ==================== CÁC TRƯỜNG ĐĂNG NHẬP ====================
                            _buildField(
                              userCtrl,
                              "Tên đăng nhập",
                              Icons.person_outline,
                              enabled: !_isLoading,
                            ),
                            const SizedBox(height: 14),

                            _buildField(
                              passCtrl,
                              "Mật khẩu",
                              Icons.lock_outline,
                              isPass: true,
                              obscureState: _obscurePassword,
                              onToggleObscure: () => setState(() => _obscurePassword = !_obscurePassword),
                              enabled: !_isLoading,
                            ),

                            Align(
                              alignment: Alignment.centerRight,
                              child: TextButton(
                                onPressed: _isLoading ? null : _showForgotPasswordDialog,
                                child: const Text(
                                  "Quên mật khẩu?",
                                  style: TextStyle(color: Colors.orangeAccent, fontSize: 13, fontWeight: FontWeight.w600),
                                ),
                              ),
                            ),
                          ],

                          const SizedBox(height: 10),

                          // Nút Hành Động Chính
                          SizedBox(
                            width: double.infinity,
                            height: 50,
                            child: ElevatedButton(
                              onPressed: _isLoading ? null : authAction,
                              style: ElevatedButton.styleFrom(
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(16),
                                ),
                                backgroundColor: Colors.orangeAccent,
                                elevation: 3,
                              ),
                              child: _isLoading
                                  ? const SizedBox(
                                      height: 24,
                                      width: 24,
                                      child: CircularProgressIndicator(
                                        strokeWidth: 2.5,
                                        color: Colors.black,
                                      ),
                                    )
                                  : Text(
                                      isLogin ? "ĐĂNG NHẬP" : "HOÀN TẤT ĐĂNG KÝ",
                                      style: const TextStyle(
                                        color: Colors.black,
                                        fontWeight: FontWeight.bold,
                                        fontSize: 16,
                                        letterSpacing: 0.5,
                                      ),
                                    ),
                            ),
                          ),

                          const SizedBox(height: 14),

                          // Chuyển đổi giữa Đăng nhập / Đăng ký
                          TextButton(
                            onPressed: _isLoading
                                ? null
                                : () {
                                    setState(() {
                                      isLogin = !isLogin;
                                    });
                                  },
                            child: Text(
                              isLogin
                                  ? "Chưa có tài khoản? Đăng ký ngay"
                                  : "Đã có tài khoản? Quay lại Đăng nhập",
                              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w600),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildField(
    TextEditingController controller,
    String hint,
    IconData icon, {
    bool isPass = false,
    bool obscureState = true,
    VoidCallback? onToggleObscure,
    bool enabled = true,
    TextInputType keyboardType = TextInputType.text,
  }) {
    return TextField(
      controller: controller,
      enabled: enabled,
      obscureText: isPass ? obscureState : false,
      keyboardType: keyboardType,
      style: const TextStyle(color: Colors.black87, fontSize: 14),
      decoration: InputDecoration(
        hintText: hint,
        hintStyle: const TextStyle(color: Colors.black38, fontSize: 13),
        prefixIcon: Icon(icon, color: Colors.grey[700], size: 20),
        suffixIcon: isPass
            ? IconButton(
                icon: Icon(
                  obscureState ? Icons.visibility_off : Icons.visibility,
                  color: Colors.grey[700],
                  size: 20,
                ),
                onPressed: onToggleObscure,
              )
            : null,
        filled: true,
        fillColor: Colors.white,
        contentPadding: const EdgeInsets.symmetric(vertical: 14, horizontal: 16),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: BorderSide.none,
        ),
      ),
    );
  }
}