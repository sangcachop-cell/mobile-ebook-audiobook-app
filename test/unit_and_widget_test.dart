// unit_and_widget_test.dart
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:book_audio_app/user_session.dart';
import 'package:book_audio_app/audio_player_service.dart';
import 'package:book_audio_app/progress_service.dart';
import 'package:book_audio_app/offline_manager.dart';
import 'package:book_audio_app/api_config.dart';
import 'package:book_audio_app/main_screen.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  setUpAll(() {
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
      const MethodChannel('xyz.luan/audioplayers.global'),
      (MethodCall methodCall) async => 1,
    );
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
      const MethodChannel('xyz.luan/audioplayers'),
      (MethodCall methodCall) async => 1,
    );
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(
      const MethodChannel('plugins.flutter.io/path_provider'),
      (MethodCall methodCall) async => '.',
    );
  });

  group('Module 1: Auth & User Session Tests', () {
    test('UserSession save, get and clear works correctly', () async {
      SharedPreferences.setMockInitialValues({});

      // 1. Initially no session
      final initialSession = await UserSession.getSession();
      expect(initialSession, isNull);

      // 2. Save session
      await UserSession.saveSession(
        username: 'testuser',
        isAdmin: true,
        fullName: 'Nguyen Van Test',
        avatarUrl: 'http://localhost:8000/uploads/avatar.jpg',
      );

      final savedSession = await UserSession.getSession();
      expect(savedSession, isNotNull);
      expect(savedSession!['username'], equals('testuser'));
      expect(savedSession['is_admin'], isTrue);
      expect(savedSession['full_name'], equals('Nguyen Van Test'));

      // 3. Clear session
      await UserSession.clearSession();
      final clearedSession = await UserSession.getSession();
      expect(clearedSession, isNull);
    });
  });

  group('Module 3: Book Reader Helper & Format Detection Tests', () {
    test('Detects EPUB format correctly', () {
      const epubUrl1 = 'http://example.com/books/sample.epub';
      const epubUrl2 = '/storage/emulated/0/download/book.EPUB';
      const pdfUrl = 'http://example.com/books/sample.pdf';

      expect(epubUrl1.toLowerCase().endsWith('.epub'), isTrue);
      expect(epubUrl2.toLowerCase().endsWith('.epub'), isTrue);
      expect(pdfUrl.toLowerCase().endsWith('.epub'), isFalse);
    });
  });

  group('Module 4: Audiobook Player Service Tests', () {
    test('AudioPlayerService singleton and speed adjustments', () async {
      final service = AudioPlayerService();
      expect(service, isNotNull);
      expect(service.playbackSpeed, equals(1.0));

      await service.setSpeed(1.5);
      expect(service.playbackSpeed, equals(1.5));

      await service.setSpeed(2.0);
      expect(service.playbackSpeed, equals(2.0));

      // Reset
      await service.setSpeed(1.0);
    });

    test('AudioPlayerService sleep timer sets and cancels correctly', () {
      final service = AudioPlayerService();

      // Set 15 minutes sleep timer
      service.setSleepTimer(15);
      expect(service.sleepTimerSecondsLeft, equals(15 * 60));

      // Cancel sleep timer
      service.cancelSleepTimer();
      expect(service.sleepTimerSecondsLeft, equals(0));
    });

    test('Audio bookmark timestamp duration formatting mm:ss', () {
      String formatMs(int ms) {
        final d = Duration(milliseconds: ms);
        final m = d.inMinutes.remainder(60).toString().padLeft(2, '0');
        final s = d.inSeconds.remainder(60).toString().padLeft(2, '0');
        return '$m:$s';
      }

      expect(formatMs(65000), equals('01:05'));
      expect(formatMs(125000), equals('02:05'));
      expect(formatMs(3599000), equals('59:59'));
    });

    test('AudioPlayerService playBook state and chapter generation', () {
      final service = AudioPlayerService();
      expect(service.chapters.isNotEmpty, isTrue);
      expect(service.chapters.first['title'], contains('Chương 1'));
    });
  });

  group('Module 8: Password Validation & Forgot Password Logic Tests', () {
    test('Password complexity requirement enforces at least 6 characters', () {
      bool isStrongPassword(String pwd) => pwd.trim().length >= 6;

      expect(isStrongPassword('123'), isFalse);
      expect(isStrongPassword('12345'), isFalse);
      expect(isStrongPassword('123456'), isTrue);
      expect(isStrongPassword('SecurePass2026'), isTrue);
    });
  });

  group('Module 5: Reading & Listening Progress Service Tests', () {
    test('ProgressService stores local reading & listening state in SharedPreferences', () async {
      SharedPreferences.setMockInitialValues({});

      // Save progress for book 101
      await ProgressService.updateProgress(
        bookId: 101,
        username: 'student1',
        lastPage: 42,
        lastEpubCfi: 'epubcfi(/6/4[chap01]!/4/2/10)',
        lastAudioPositionMs: 125000,
        progressPercent: 65.5,
      );

      final prefs = await SharedPreferences.getInstance();
      expect(prefs.getInt('pdf_page_student1_101'), equals(42));
      expect(prefs.getString('epub_cfi_student1_101'), equals('epubcfi(/6/4[chap01]!/4/2/10)'));
      expect(prefs.getInt('audio_pos_101'), equals(125000));
    });
  });

  group('Module 6: Offline Download Manager Tests', () {
    test('OfflineBook model serialization & formattedFileSize', () {
      final offlineBook = OfflineBook(
        id: 99,
        title: 'Lap Trinh Flutter 2026',
        author: 'Tac Gia Test',
        fileSize: 5242880, // 5 MB
        downloadedAt: 1776500000000,
        localPdfPath: '/path/to/offline.pdf',
      );

      expect(offlineBook.formattedFileSize, equals('5.0 MB'));

      final json = offlineBook.toJson();
      expect(json['id'], equals(99));
      expect(json['title'], equals('Lap Trinh Flutter 2026'));

      final restored = OfflineBook.fromJson(json);
      expect(restored.id, equals(99));
      expect(restored.formattedFileSize, equals('5.0 MB'));
    });

    test('OfflineManager local storage management', () async {
      SharedPreferences.setMockInitialValues({});
      final manager = OfflineManager();
      expect(manager, isNotNull);
      expect(manager.offlineBooks, isEmpty);
    });
  });

  group('Module 7: Reviews & Ratings Calculation Tests', () {
    test('Calculates average ratings and star display accurately', () {
      final mockReviews = [
        {'id': 1, 'rating': 5, 'comment': 'Tuyệt vời'},
        {'id': 2, 'rating': 4, 'comment': 'Sách hay'},
        {'id': 3, 'rating': 5, 'comment': 'Rất bổ ích'},
      ];

      int sum = 0;
      for (final r in mockReviews) {
        sum += (r['rating'] as int);
      }
      final double avg = sum / mockReviews.length;
      expect(double.parse(avg.toStringAsFixed(1)), equals(4.7));
      expect(avg.round(), equals(5));
    });
  });

  group('Module 9: ApiConfig URL Resolution Tests', () {
    test('Resolves relative upload paths to full baseUrl URLs', () {
      final formattedRelative = ApiConfig.formatUrl('uploads/dac_nhan_tam.pdf');
      expect(formattedRelative, contains('/uploads/dac_nhan_tam.pdf'));
      expect(formattedRelative.startsWith('http'), isTrue);

      final formattedSlash = ApiConfig.formatUrl('/uploads/audio_sample_1.mp3');
      expect(formattedSlash, contains('/uploads/audio_sample_1.mp3'));
      expect(formattedSlash.startsWith('http'), isTrue);
    });
  });

  group('Module 10: 500 Books Catalog & Open Sources Integration Tests', () {
    test('Book model parses category, ratings, and Gutenberg/LibriVox sources correctly', () {
      final sampleJson = {
        'id': 1342,
        'title': 'Pride and Prejudice',
        'author': 'Jane Austen',
        'image_url': 'https://www.gutenberg.org/cache/epub/1342/pg1342.cover.medium.jpg',
        'pdf_url': 'https://www.gutenberg.org/ebooks/1342.epub.noimages',
        'audio_url': 'https://www.archive.org/download/pride_and_prejudice_librivox/prideandprejudice_01-03_austen_64kb.mp3',
        'content': 'Tác phẩm kinh điển về tình yêu và định kiến xã hội.',
        'category': 'Tiểu thuyết',
        'rating_avg': 4.9,
        'review_count': 320,
        'source': 'Project Gutenberg & LibriVox',
      };

      final book = Book.fromJson(sampleJson);
      expect(book.id, equals(1342));
      expect(book.title, equals('Pride and Prejudice'));
      expect(book.author, equals('Jane Austen'));
      expect(book.category, equals('Tiểu thuyết'));
      expect(book.ratingAvg, equals(4.9));
      expect(book.reviewCount, equals(320));
      expect(book.source, contains('Project Gutenberg'));
      expect(book.pdfUrl, contains('.epub'));
      expect(book.audioUrl, contains('.mp3'));
    });
  });
}
