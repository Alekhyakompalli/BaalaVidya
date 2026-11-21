import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:baalavidya/main.dart';

void main() {
  testWidgets('hello screen shows BAALAVIDYA', (WidgetTester tester) async {
    await tester.pumpWidget(const ProviderScope(child: BaalavidyaApp()));
    expect(find.text('BAALAVIDYA'), findsOneWidget);
  });
}
