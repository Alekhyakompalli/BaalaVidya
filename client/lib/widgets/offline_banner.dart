import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';

/// Offline / Online mode indicator banner.
/// Adheres to [Arch: Offline indicator; docs/eval.md:131].
/// Shows 'Offline' when network is disconnected or 'Live' when online.
class OfflineBanner extends ConsumerWidget {
  const OfflineBanner({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isOnline = ref.watch(isOnlineProvider);
    final lang = ref.watch(languageProvider);

    if (isOnline) {
      return Container(
        width: double.infinity,
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 4),
        color: const Color(0xFFE8F5E9),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 8,
              height: 8,
              decoration: const BoxDecoration(
                color: Color(0xFF2E7D32),
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(width: 6),
            Text(
              lang == 'te' ? 'లైవ్ (Live) • ఆన్‌లైన్ మోడ్' : 'Live • Connected',
              style: const TextStyle(
                color: Color(0xFF2E7D32),
                fontSize: 12,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      );
    }

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
      color: AppColors.coralOrange,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Text('⚡', style: TextStyle(fontSize: 16)),
          const SizedBox(width: 8),
          Text(
            lang == 'te'
                ? 'ఆఫ్‌లైన్ మోడ్ • డౌన్‌లోడ్ చేసిన పాఠాలు సిద్ధంగా ఉన్నాయి'
                : 'Offline Mode • Using downloaded chapter lessons',
            style: const TextStyle(
              color: Colors.white,
              fontSize: 13,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}

/// Interactive Connection Status Badge showing 'Live' (green) or 'Offline' (orange).
/// Tapping it toggles connection state for rapid on-device testing.
class ConnectionStatusBadge extends ConsumerWidget {
  const ConnectionStatusBadge({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final isOnline = ref.watch(isOnlineProvider);

    return InkWell(
      onTap: () {
        ref.read(isOnlineProvider.notifier).state = !isOnline;
      },
      borderRadius: BorderRadius.circular(12),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        margin: const EdgeInsets.symmetric(vertical: 12, horizontal: 4),
        decoration: BoxDecoration(
          color: isOnline ? const Color(0xFFE8F5E9) : const Color(0xFFFFF3E0),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(
            color: isOnline ? const Color(0xFF81C784) : const Color(0xFFFFB74D),
            width: 1,
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              width: 7,
              height: 7,
              decoration: BoxDecoration(
                color: isOnline ? const Color(0xFF2E7D32) : const Color(0xFFE65100),
                shape: BoxShape.circle,
              ),
            ),
            const SizedBox(width: 4),
            Text(
              isOnline ? 'Live' : 'Offline',
              style: TextStyle(
                color: isOnline ? const Color(0xFF2E7D32) : const Color(0xFFE65100),
                fontSize: 11.5,
                fontWeight: FontWeight.w800,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
