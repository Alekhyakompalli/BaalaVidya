import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';

/// Instant bilingual language toggle button (English <-> తెలుగు).
/// Positioned at the top right of app bars across the application.
/// Changes all visible text instantly without reloading or restarting the app.
class LanguageToggle extends ConsumerWidget {
  const LanguageToggle({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final currentLang = ref.watch(languageProvider);
    final isTelugu = currentLang == 'te';

    return Container(
      constraints: const BoxConstraints(minHeight: 48, minWidth: 120),
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: AppColors.primaryBlue.withOpacity(0.4), width: 1.5),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 4,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(24),
          onTap: () {
            ref.read(languageProvider.notifier).state = isTelugu ? 'en' : 'te';
          },
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 4),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                _buildPill(
                  text: 'EN',
                  isSelected: !isTelugu,
                  color: AppColors.primaryBlue,
                ),
                const SizedBox(width: 4),
                _buildPill(
                  text: 'తెలుగు',
                  isSelected: isTelugu,
                  color: AppColors.meadowGreen,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildPill({
    required String text,
    required bool isSelected,
    required Color color,
  }) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      curve: Curves.easeInOut,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      decoration: BoxDecoration(
        color: isSelected ? color : Colors.transparent,
        borderRadius: BorderRadius.circular(18),
      ),
      child: Text(
        text,
        style: TextStyle(
          color: isSelected ? Colors.white : AppColors.textDark,
          fontWeight: FontWeight.bold,
          fontSize: 15,
        ),
      ),
    );
  }
}
