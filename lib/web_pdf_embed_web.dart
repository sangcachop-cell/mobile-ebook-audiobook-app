import 'dart:ui_web' as ui_web;
import 'package:web/web.dart' as web;
import 'package:flutter/material.dart';

final Map<String, String> _iframeUrls = {};
final Set<String> _registeredViews = {};

Widget buildWebPdfEmbed(String url, {required int bookId}) {
  final viewType = 'pdf-web-iframe-$bookId';
  _iframeUrls[viewType] = url;

  if (!_registeredViews.contains(viewType)) {
    ui_web.platformViewRegistry.registerViewFactory(
      viewType,
      (int viewId) {
        final iframe = web.document.createElement('iframe') as web.HTMLIFrameElement;
        iframe.src = _iframeUrls[viewType] ?? url;
        iframe.style.border = 'none';
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        return iframe;
      },
    );
    _registeredViews.add(viewType);
  }
  return HtmlElementView(viewType: viewType);
}

void openPdfInNewTab(String url) {
  web.window.open(url, '_blank');
}
