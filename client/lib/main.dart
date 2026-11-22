import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/screens/splash_screen.dart';
import 'package:baalavidya/theme/app_theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const ProviderScope(child: BaalavidyaApp()));
}

/// BAALAVIDYA Client App Shell
class BaalavidyaApp extends StatelessWidget {
  final bool autoNavigateSplash;

  const BaalavidyaApp({
    super.key,
    this.autoNavigateSplash = true,
  });

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'BAALAVIDYA',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.lightTheme,
      home: SplashScreen(autoNavigate: autoNavigateSplash),
    );
  }
}
