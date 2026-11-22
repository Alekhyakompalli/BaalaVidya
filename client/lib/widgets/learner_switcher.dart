import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';

/// Learner Profile Switcher widget for shared devices.
/// Adheres to [Arch: Shared devices; Sync rules 7; Plan: Phase 6 Scope].
/// Allows multiple children sharing a device to switch profiles and maintain
/// completely isolated progress records.
class LearnerSwitcher extends ConsumerWidget {
  const LearnerSwitcher({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final learnerName = ref.watch(currentLearnerNameProvider);
    final lang = ref.watch(languageProvider);

    return Container(
      constraints: const BoxConstraints(minHeight: 48),
      margin: const EdgeInsets.symmetric(horizontal: 6),
      child: Material(
        color: AppColors.lightBlue,
        borderRadius: BorderRadius.circular(20),
        child: InkWell(
          borderRadius: BorderRadius.circular(20),
          onTap: () => _showLearnerSwitchDialog(context, ref, lang),
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text('🧒', style: TextStyle(fontSize: 18)),
                const SizedBox(width: 6),
                Text(
                  learnerName,
                  style: const TextStyle(
                    fontSize: 14,
                    fontWeight: FontWeight.bold,
                    color: AppColors.darkBlue,
                  ),
                ),
                const SizedBox(width: 4),
                const Icon(
                  Icons.arrow_drop_down_rounded,
                  color: AppColors.primaryBlue,
                  size: 20,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void _showLearnerSwitchDialog(BuildContext context, WidgetRef ref, String lang) {
    final learners = [
      {'id': 'learner_alekhya', 'name': 'Alekhya', 'class': 'Class 10', 'avatar': '👧'},
      {'id': 'learner_ravi', 'name': 'Ravi', 'class': 'Class 8', 'avatar': '👦'},
      {'id': 'learner_sneha', 'name': 'Sneha', 'class': 'Class 5', 'avatar': '👧'},
    ];

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
        title: Row(
          children: [
            const Text('👥', style: TextStyle(fontSize: 24)),
            const SizedBox(width: 10),
            Text(
              lang == 'te' ? 'విద్యార్థిని మార్చండి' : 'Switch Learner Profile',
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
            ),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: learners.map((l) {
            return ListTile(
              contentPadding: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
              leading: Text(l['avatar']!, style: const TextStyle(fontSize: 28)),
              title: Text(l['name']!, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
              subtitle: Text(l['class']!, style: const TextStyle(color: AppColors.textMuted, fontSize: 13)),
              trailing: const Icon(Icons.check_circle_outline_rounded, color: AppColors.primaryBlue),
              onTap: () {
                ref.read(currentLearnerIdProvider.notifier).state = l['id']!;
                ref.read(currentLearnerNameProvider.notifier).state = l['name']!;
                Navigator.of(context).pop();
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(
                      lang == 'te' ? '${l['name']} ప్రొఫైల్‌కు మారారు' : 'Switched to ${l['name']}\'s profile',
                    ),
                    duration: const Duration(seconds: 1),
                  ),
                );
              },
            );
          }).toList(),
        ),
      ),
    );
  }
}
