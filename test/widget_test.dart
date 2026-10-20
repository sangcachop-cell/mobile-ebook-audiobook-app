import 'package:flutter/foundation.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:book_audio_app/main.dart';

void main() {
  testWidgets('BookApp welcome screen smoke test', (WidgetTester tester) async {
    final originalOnError = FlutterError.onError;
    FlutterError.onError = (FlutterErrorDetails details) {
      final msg = details.exception.toString();
      if (msg.contains('NetworkImage') || msg.contains('HTTP request failed') || msg.contains('statusCode: 400')) {
        return;
      }
      originalOnError?.call(details);
    };
    addTearDown(() => FlutterError.onError = originalOnError);

    await tester.pumpWidget(const BookApp());
    await tester.pump();

    // Verify WelcomeScreen text exists
    expect(find.text('Chào Mừng Đến Với'), findsOneWidget);
    expect(find.text('Sách & AudioBook'), findsOneWidget);
    expect(find.text('Đăng Nhập'), findsOneWidget);
  });
}


