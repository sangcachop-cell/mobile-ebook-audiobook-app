import 'dart:io';
import 'package:flutter_test/flutter_test.dart';
import 'package:epub_view/epub_view.dart';
import 'package:epub_view/src/data/epub_parser.dart';

void main() {
  test('Verify so_do.epub contains full chapters and paragraphs', () async {
    final file = File('backend/uploads/so_do.epub');
    expect(await file.exists(), isTrue);

    final bytes = await file.readAsBytes();
    final document = await EpubDocument.openData(bytes);

    expect(document, isNotNull);
    final chapters = parseChapters(document);
    expect(chapters.length, equals(4));

    final parseResult = parseParagraphs(chapters, document.Content);
    // Elements should include all paragraphs
    expect(parseResult.flatParagraphs.isNotEmpty, isTrue);

    final allText = parseResult.flatParagraphs.map((p) => p.element.text).join(' ');
    print('Total parsed paragraphs in so_do.epub: ${parseResult.flatParagraphs.length}');
    print('Sample text from so_do.epub: ${allText.substring(0, 180)}...');

    expect(allText, contains('Xuân Tóc Đỏ vốn là một đứa trẻ mồ côi'));
    expect(allText, contains('Bà Phó Đoan quyết định ra tay cứu vớt Xuân Tóc Đỏ'));
    expect(allText, contains('Hạnh phúc của một tang gia'));
  });
}
