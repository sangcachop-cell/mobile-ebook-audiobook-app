import 'package:flutter/material.dart';
import 'main_screen.dart';
import 'user_session.dart';

class WelcomeScreen extends StatefulWidget {
  const WelcomeScreen({super.key});

  @override
  State<WelcomeScreen> createState() => _WelcomeScreenState();
}

class _WelcomeScreenState extends State<WelcomeScreen> {
  Map<String, dynamic>? _savedSession;

  @override
  void initState() {
    super.initState();
    _checkSavedSession();
  }

  Future<void> _checkSavedSession() async {
    final session = await UserSession.getSession();
    if (session != null && mounted) {
      setState(() {
        _savedSession = session;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Container(
            decoration: const BoxDecoration(
              image: DecorationImage(
                image: NetworkImage('https://picsum.photos/id/1010/800/1200'),
                fit: BoxFit.cover,
              ),
            ),
          ),
          Container(color: Colors.black.withValues(alpha: 0.4)),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 30),
              child: Column(
                children: [
                  const SizedBox(height: 60),
                  const Text("Chào Mừng Đến Với", style: TextStyle(color: Colors.white, fontSize: 18)),
                  const Text(
                    "Sách & AudioBook",
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 32,
                      fontWeight: FontWeight.bold,
                      shadows: [Shadow(color: Colors.black45, blurRadius: 10)],
                    ),
                  ),
                  const Spacer(),
                  if (_savedSession != null) ...[
                    _buildWelcomeBtn(
                      context,
                      title: "Tiếp tục với ${_savedSession!['full_name'] ?? _savedSession!['username']}",
                      subtitle: "Đã lưu đăng nhập trước đó",
                      color: Colors.green.shade700,
                      icon: Icons.verified_user_rounded,
                      onTap: () {
                        Navigator.pushReplacement(
                          context,
                          MaterialPageRoute(
                            builder: (context) => MainScreen(
                              username: _savedSession!['username'],
                              isAdmin: _savedSession!['is_admin'] ?? false,
                            ),
                          ),
                        );
                      },
                    ),
                    const SizedBox(height: 14),
                  ],
                  _buildWelcomeBtn(
                    context,
                    title: _savedSession != null ? "Đổi Tài Khoản Khác" : "Đăng Nhập",
                    subtitle: _savedSession != null ? "Đăng nhập với tài khoản khác" : "Đăng nhập để tiếp tục",
                    color: Colors.orange.shade800,
                    icon: Icons.person,
                    onTap: () => Navigator.pushNamed(context, '/login'),
                  ),
                  const SizedBox(height: 30),
                  TextButton(
                    onPressed: () => Navigator.pushReplacement(
                      context,
                      MaterialPageRoute(builder: (context) => const MainScreen(username: "Khách")),
                    ),
                    child: const Text("Tiếp tục với tư cách Khách >", style: TextStyle(color: Colors.white, fontSize: 15)),
                  ),
                  const SizedBox(height: 20),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildWelcomeBtn(
    BuildContext context, {
    required String title,
    required String subtitle,
    required Color color,
    IconData icon = Icons.person,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 20),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(15),
        ),
        child: Row(
          children: [
            Icon(icon, color: Colors.white, size: 30),
            const SizedBox(width: 15),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 17), maxLines: 1, overflow: TextOverflow.ellipsis),
                  Text(subtitle, style: const TextStyle(color: Colors.white70, fontSize: 12)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}