import 'package:flutter/material.dart';

/// Child-friendly color palette adhering to BAALAVIDYA Functional Requirements:
/// - Primary: Fun Sky Blue & Sunshine Yellow
/// - Secondary: Meadow Green & Coral Orange
/// - High contrast, warm, and playful for primary & secondary school students.
class AppColors {
  // Figma Design System Palette (from file 8SILxKv7h9nH8VoKvHDikX)
  static const Color primaryBlue = Color(0xFF2461D6);
  static const Color darkBlue = Color(0xFF192C50);
  static const Color lightBlue = Color(0xFFE8F0FF);
  static const Color activeTabBlue = Color(0xFFEAF1FF);
  static const Color progressBlue = Color(0xFF4F8CFF);

  static const Color sunshineYellow = Color(0xFFFFB300);
  static const Color mathTileYellow = Color(0xFFFFF1C8);
  static const Color mathTileText = Color(0xFF996100);

  // Secondary & Status Palette
  static const Color meadowGreen = Color(0xFF198348);
  static const Color offlineGreenBg = Color(0xFFEAF7EF);
  static const Color offlineGreenText = Color(0xFF198348);

  static const Color coralOrange = Color(0xFFFF7043);
  static const Color darkOrange = Color(0xFFE64A19);
  static const Color lightOrange = Color(0xFFFBE9E7);

  // Background & Surface
  static const Color softBackground = Color(0xFFF6F9FF);
  static const Color cardBackground = Colors.white;
  static const Color textDark = Color(0xFF192C50);
  static const Color textMuted = Color(0xFF62728C);
  static const Color borderColor = Color(0xFFE3EAF5);
}

/// BAALAVIDYA Theme definition:
/// Large fonts, rounded cards (20px), large buttons (min 48px), responsive layout.
class AppTheme {
  static ThemeData get lightTheme {
    return ThemeData(
      useMaterial3: true,
      colorScheme: ColorScheme.fromSeed(
        seedColor: AppColors.primaryBlue,
        primary: AppColors.primaryBlue,
        secondary: AppColors.sunshineYellow,
        tertiary: AppColors.meadowGreen,
        surface: AppColors.softBackground,
      ),
      scaffoldBackgroundColor: AppColors.softBackground,
      textTheme: const TextTheme(
        headlineLarge: TextStyle(
          fontSize: 26,
          fontWeight: FontWeight.bold,
          color: AppColors.textDark,
          height: 1.25,
        ),
        headlineMedium: TextStyle(
          fontSize: 22,
          fontWeight: FontWeight.bold,
          color: AppColors.textDark,
          height: 1.3,
        ),
        titleLarge: TextStyle(
          fontSize: 20,
          fontWeight: FontWeight.bold,
          color: AppColors.textDark,
          height: 1.3,
        ),
        titleMedium: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.w600,
          color: AppColors.textDark,
        ),
        bodyLarge: TextStyle(
          fontSize: 18,
          color: AppColors.textDark,
          height: 1.4,
        ),
        bodyMedium: TextStyle(
          fontSize: 16,
          color: AppColors.textMuted,
          height: 1.4,
        ),
        labelLarge: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.bold,
          color: Colors.white,
        ),
      ),
      cardTheme: CardTheme(
        color: AppColors.cardBackground,
        elevation: 2,
        shadowColor: Colors.black.withOpacity(0.06),
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          minimumSize: const Size(48, 52),
          elevation: 2,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 14),
          textStyle: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}
