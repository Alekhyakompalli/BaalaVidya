import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:baalavidya/main.dart';
import 'package:baalavidya/screens/home_screen.dart';
import 'package:baalavidya/screens/splash_screen.dart';
import 'package:baalavidya/widgets/class_card.dart';
import 'package:baalavidya/widgets/language_toggle.dart';

void main() {
  testWidgets('Splash Screen renders brand, logo, and friendly tagline', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: BaalavidyaApp(autoNavigateSplash: false),
      ),
    );

    // Verify BAALAVIDYA logo, title, and tagline
    expect(find.byType(SplashScreen), findsOneWidget);
    expect(find.text('BAALAVIDYA'), findsOneWidget);
    expect(find.text('Bilingual Learning with Bala Buddy 🌟'), findsOneWidget);
    expect(find.text('Opening your lessons...'), findsOneWidget);
  });

  testWidgets('Tapping Splash Screen navigates immediately to HomeScreen', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: BaalavidyaApp(autoNavigateSplash: false),
      ),
    );

    // Tap anywhere on splash to continue
    await tester.tap(find.byType(SplashScreen));
    await tester.pumpAndSettle();

    // Verify HomeScreen is reached
    expect(find.byType(HomeScreen), findsOneWidget);
    expect(find.text('Hello Learner! 🌟'), findsOneWidget);
    expect(find.byType(LanguageToggle), findsOneWidget);
  });

  testWidgets('HomeScreen displays search bar and all 10 class cards', (WidgetTester tester) async {
    await tester.pumpWidget(
      const ProviderScope(
        child: MaterialApp(home: HomeScreen()),
      ),
    );

    // Verify greeting and search
    expect(find.text('Hello Learner! 🌟'), findsOneWidget);
    expect(find.text('Search topics, lessons, concepts...'), findsOneWidget);
    expect(find.text('Select Your Class:'), findsOneWidget);

    // Verify 10 class cards are generated in grid
    expect(find.byType(ClassCard), findsNWidgets(10));
    expect(find.text('Class 1'), findsOneWidget);
    expect(find.text('Class 5'), findsOneWidget);
    expect(find.text('Class 10'), findsOneWidget);
  });
}
