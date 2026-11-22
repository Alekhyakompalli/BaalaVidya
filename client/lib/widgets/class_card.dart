import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';

/// Class selection card for the Home screen grid.
/// Adheres to accessibility requirements: large fonts, rounded cards (20px),
/// large tap targets (>= 48px x 48px).
class ClassCard extends ConsumerWidget {
  final ClassItem classItem;
  final VoidCallback onTap;

  const ClassCard({
    super.key,
    required this.classItem,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final lang = ref.watch(languageProvider);

    return Container(
      constraints: const BoxConstraints(minHeight: 100, minWidth: 120),
      child: Card(
        color: classItem.lightColor,
        elevation: classItem.isPilot ? 3 : 1,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
          side: BorderSide(
            color: classItem.isPilot ? classItem.color : Colors.transparent,
            width: classItem.isPilot ? 2.5 : 1,
          ),
        ),
        child: InkWell(
          borderRadius: BorderRadius.circular(20),
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                // Fun emoji icon
                Text(
                  classItem.iconEmoji,
                  style: const TextStyle(fontSize: 36),
                ),
                const SizedBox(height: 8),
                // Class Name
                Text(
                  classItem.localizedName(lang),
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: classItem.color,
                  ),
                ),
                if (classItem.isPilot) ...[
                  const SizedBox(height: 6),
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                    decoration: BoxDecoration(
                      color: classItem.color,
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: Text(
                      lang == 'te' ? 'సిలబస్ సిద్ధం! 🌟' : 'Pilot Ready! 🌟',
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                  ),
                ],
              ],
            ),
          ),
        ),
      ),
    );
  }
}
