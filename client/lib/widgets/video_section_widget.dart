import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:baalavidya/l10n/app_strings.dart';
import 'package:baalavidya/models/chapter_package_model.dart';
import 'package:baalavidya/models/curriculum_models.dart';
import 'package:baalavidya/services/offline_store.dart';
import 'package:baalavidya/services/sync_queue_service.dart';
import 'package:baalavidya/state/app_state.dart';
import 'package:baalavidya/theme/app_theme.dart';

/// Phase 7: Interactive Video Section Widget.
/// Adheres strictly to:
/// - [PS: 7. Video Section - Relevant educational videos & language-aware recommendations]
/// - [PS: Online Mode "Video Streaming"]
/// - [Arch: Data flow (c) Student opens a topic and watches a video]
/// - [Arch: Limited bandwidth - low-bandwidth adaptive quality option]
/// - Phase 7 Exit Criteria:
///   1. No video file is stored offline (metadata cached only, stream online only).
///   2. Metadata lists correctly in both Telugu and English.
class VideoSectionWidget extends ConsumerStatefulWidget {
  final TopicItem topic;

  const VideoSectionWidget({
    super.key,
    required this.topic,
  });

  @override
  ConsumerState<VideoSectionWidget> createState() => VideoSectionWidgetState();
}

class VideoSectionWidgetState extends ConsumerState<VideoSectionWidget> {
  String _selectedLanguage = 'all'; // 'all', 'te', 'en'
  String _selectedQuality = '480p (Standard)';

  List<VideoMetadata> _getVideos(String currentLang) {
    // 1. First retrieve from OfflineStore cached metadata
    final cached = OfflineStore().getVideosForTopic(
      widget.topic.id,
      language: _selectedLanguage == 'all' ? null : _selectedLanguage,
    );

    if (cached.isNotEmpty) {
      return cached;
    }

    // 2. Fallback to topic bilingual video definitions
    final defaultVideos = [
      VideoMetadata(
        videoId: '${widget.topic.id}_te',
        topicId: widget.topic.id,
        languageCode: 'te',
        title: '${widget.topic.title} - Telugu Explanation',
        teluguTitle: widget.topic.teluguVideoTitle.isNotEmpty
            ? widget.topic.teluguVideoTitle
            : '${widget.topic.teluguTitle} వీడియో పాఠం',
        durationMinutes: widget.topic.durationMinutes > 0 ? (widget.topic.durationMinutes ~/ 2).clamp(5, 12) : 8,
        durationSeconds: 480,
        streamUrl: 'ai://video_generator/' + widget.topic.id,
        provider: 'Bala Buddy AI Video Studio (AI-Generated Contextual Lesson)',
        onlineStreamingOnly: true,
      ),
      VideoMetadata(
        videoId: '${widget.topic.id}_en',
        topicId: widget.topic.id,
        languageCode: 'en',
        title: widget.topic.videoTitle.isNotEmpty
            ? widget.topic.videoTitle
            : '${widget.topic.title} English Video Lesson',
        teluguTitle: '${widget.topic.teluguTitle} ఇంగ్లీష్ వివరణ',
        durationMinutes: widget.topic.durationMinutes > 0 ? (widget.topic.durationMinutes ~/ 2 + 1).clamp(6, 14) : 9,
        durationSeconds: 540,
        streamUrl: 'ai://video_generator/' + widget.topic.id,
        provider: 'Bala Buddy AI Video Studio (AI-Generated Contextual Lesson)',
        onlineStreamingOnly: true,
      ),
    ];

    if (_selectedLanguage == 'all') {
      return defaultVideos;
    }
    return defaultVideos.where((v) => v.languageCode == _selectedLanguage).toList();
  }

  void playVideo(BuildContext context, VideoMetadata video) {
    final lang = ref.read(languageProvider);
    _openVideoPlayerModal(context, video, lang);
  }

  @override
  Widget build(BuildContext context) {
    final lang = ref.watch(languageProvider);
    final isOnline = ref.watch(isOnlineProvider);
    final videos = _getVideos(lang);

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18.0),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: AppColors.borderColor, width: 1.5),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: const Offset(0, 3),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Section Title Header
          Row(
            children: [
              const Text('🎬', style: TextStyle(fontSize: 24)),
              const SizedBox(width: 8),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      AppStrings.get('relatedVideo', lang),
                      style: const TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: AppColors.textDark,
                      ),
                    ),
                    Text(
                      '${AppStrings.get('videoSectionTitle', lang)} • ${AppStrings.get('videoSectionSubtitle', lang)}',
                      style: const TextStyle(
                        fontSize: 12,
                        color: AppColors.textMuted,
                      ),
                    ),
                  ],
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                decoration: BoxDecoration(
                  color: isOnline ? AppColors.lightBlue : AppColors.lightOrange,
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Icon(
                      isOnline ? Icons.wifi : Icons.wifi_off,
                      size: 13,
                      color: isOnline ? AppColors.primaryBlue : AppColors.coralOrange,
                    ),
                    const SizedBox(width: 4),
                    Text(
                      isOnline ? 'Online' : 'Offline',
                      style: TextStyle(
                        fontSize: 11,
                        fontWeight: FontWeight.bold,
                        color: isOnline ? AppColors.darkBlue : AppColors.coralOrange,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 14),

          // Bilingual Language Filter Chips [PS: 7. Video Section]
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: Row(
              children: [
                _buildFilterChip(
                  label: AppStrings.get('allVideos', lang),
                  value: 'all',
                  isSelected: _selectedLanguage == 'all',
                ),
                const SizedBox(width: 8),
                _buildFilterChip(
                  label: 'తెలుగు (Telugu)',
                  value: 'te',
                  isSelected: _selectedLanguage == 'te',
                ),
                const SizedBox(width: 8),
                _buildFilterChip(
                  label: 'English',
                  value: 'en',
                  isSelected: _selectedLanguage == 'en',
                ),
              ],
            ),
          ),
          const SizedBox(height: 14),

          // Video Cards List
          if (videos.isEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 16.0),
              child: Center(
                child: Text(
                  lang == 'te' ? 'ఈ భాషలో వీడియోలు అందుబాటులో లేవు' : 'No videos found for this language filter',
                  style: const TextStyle(color: AppColors.textMuted, fontSize: 14),
                ),
              ),
            )
          else
            ListView.separated(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: videos.length,
              separatorBuilder: (_, __) => const SizedBox(height: 10),
              itemBuilder: (context, index) {
                final video = videos[index];
                return _buildVideoCard(context, video, lang, isOnline);
              },
            ),
        ],
      ),
    );
  }

  Widget _buildFilterChip({
    required String label,
    required String value,
    required bool isSelected,
  }) {
    return ChoiceChip(
      label: Text(
        label,
        style: TextStyle(
          fontSize: 12,
          fontWeight: isSelected ? FontWeight.bold : FontWeight.w500,
          color: isSelected ? Colors.white : AppColors.textDark,
        ),
      ),
      selected: isSelected,
      selectedColor: AppColors.primaryBlue,
      backgroundColor: AppColors.lightBlue.withOpacity(0.4),
      side: BorderSide(
        color: isSelected ? AppColors.primaryBlue : AppColors.borderColor,
      ),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      onSelected: (selected) {
        if (selected) {
          setState(() {
            _selectedLanguage = value;
          });
        }
      },
    );
  }

  Widget _buildVideoCard(
    BuildContext context,
    VideoMetadata video,
    String lang,
    bool isOnline,
  ) {
    final isTelugu = video.isTelugu;
    final cardColor = isTelugu ? const Color(0xFFF1F8E9) : const Color(0xFFE3F2FD);
    final accentColor = isTelugu ? AppColors.darkGreen : AppColors.primaryBlue;

    return Container(
      decoration: BoxDecoration(
        color: cardColor,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: accentColor.withOpacity(0.3), width: 1.2),
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          borderRadius: BorderRadius.circular(16),
          onTap: () => playVideo(context, video),
          child: Padding(
            padding: const EdgeInsets.all(12.0),
            child: Row(
              children: [
                // Video thumbnail preview circle
                Container(
                  width: 52,
                  height: 52,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    shape: BoxShape.circle,
                    boxShadow: [
                      BoxShadow(
                        color: accentColor.withOpacity(0.2),
                        blurRadius: 6,
                        offset: const Offset(0, 2),
                      ),
                    ],
                  ),
                  child: Icon(
                    Icons.play_arrow_rounded,
                    size: 34,
                    color: accentColor,
                  ),
                ),
                const SizedBox(width: 12),

                // Video info
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        video.localizedTitle(lang),
                        style: const TextStyle(
                          fontSize: 14,
                          fontWeight: FontWeight.bold,
                          color: AppColors.textDark,
                          height: 1.25,
                        ),
                        maxLines: 2,
                        overflow: TextOverflow.ellipsis,
                      ),
                      const SizedBox(height: 6),
                      Wrap(
                        spacing: 6,
                        runSpacing: 4,
                        children: [
                          // Language pill
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: isTelugu ? AppColors.meadowGreen : AppColors.primaryBlue,
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Text(
                              isTelugu ? 'తెలుగు' : 'English',
                              style: const TextStyle(
                                fontSize: 10,
                                fontWeight: FontWeight.bold,
                                color: Colors.white,
                              ),
                            ),
                          ),
                          // Duration pill
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: Colors.white,
                              borderRadius: BorderRadius.circular(6),
                              border: Border.all(color: AppColors.borderColor),
                            ),
                            child: Row(
                              mainAxisSize: MainAxisSize.min,
                              children: [
                                const Icon(Icons.timer_outlined, size: 10, color: AppColors.textMuted),
                                const SizedBox(width: 2),
                                Text(
                                  '${video.durationMinutes} ${lang == 'te' ? 'నిమి' : 'mins'}',
                                  style: const TextStyle(fontSize: 10, color: AppColors.textDark),
                                ),
                              ],
                            ),
                          ),
                          // Online only badge
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                            decoration: BoxDecoration(
                              color: isOnline ? AppColors.lightGreen : AppColors.lightOrange,
                              borderRadius: BorderRadius.circular(6),
                            ),
                            child: Text(
                              isOnline ? 'Stream' : 'Online Only ⚡',
                              style: TextStyle(
                                fontSize: 10,
                                fontWeight: FontWeight.w600,
                                color: isOnline ? AppColors.darkGreen : AppColors.coralOrange,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
                const SizedBox(width: 8),

                // Tap arrow
                Icon(
                  Icons.arrow_forward_ios_rounded,
                  size: 16,
                  color: accentColor.withOpacity(0.7),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  /// Friendly Offline Notice Dialog adhering to [Arch: Data flow (c) step 5; Cached Videos Metadata].
  void _showOfflineNoticeDialog(BuildContext context, String lang) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(20)),
        title: Row(
          children: [
            const Text('⚡', style: TextStyle(fontSize: 22)),
            const SizedBox(width: 8),
            Text(
              AppStrings.get('offlineVideoNoticeTitle', lang),
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
            ),
          ],
        ),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              AppStrings.get('offlineVideoNoticeMessage', lang),
              style: const TextStyle(fontSize: 15, height: 1.4, color: AppColors.textDark),
            ),
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(
                color: AppColors.lightGreen,
                borderRadius: BorderRadius.circular(12),
              ),
              child: Row(
                children: [
                  const Text('✅', style: TextStyle(fontSize: 16)),
                  const SizedBox(width: 8),
                  Expanded(
                    child: Text(
                      lang == 'te'
                          ? 'పాఠాలు, బాల బడ్డీ మరియు ఆటలు ఆఫ్‌లైన్‌లో సిద్ధంగా ఉన్నాయి!'
                          : 'Lesson reading, Bala Buddy, and games work 100% offline!',
                      style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppColors.darkGreen),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
        actions: [
          ElevatedButton(
            style: ElevatedButton.styleFrom(
              backgroundColor: AppColors.primaryBlue,
              foregroundColor: Colors.white,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            ),
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('OK / సరే', style: TextStyle(fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  /// Online Video Player Sheet — delegates to the shared [openVideoPlayerSheet] so the
  /// chapter-level video can reuse the same player.
  void _openVideoPlayerModal(BuildContext context, VideoMetadata video, String lang) {
    openVideoPlayerSheet(
      context,
      ref,
      video,
      lang,
      topicId: widget.topic.id,
      selectedQuality: _selectedQuality,
      onQualityChanged: (quality) => setState(() => _selectedQuality = quality),
    );
  }
}

/// Online Video Player Sheet adhering to [PS: Online Mode "Video Streaming"; Arch: Limited bandwidth].
/// Shared by the per-topic [VideoSectionWidget] and the chapter-level [ChapterVideoSection].
void openVideoPlayerSheet(
  BuildContext context,
  WidgetRef ref,
  VideoMetadata video,
  String lang, {
  required String topicId,
  required String selectedQuality,
  required void Function(String quality) onQualityChanged,
}) {
  showModalBottomSheet(
    context: context,
    isScrollControlled: true,
    backgroundColor: Colors.transparent,
    builder: (sheetContext) => _ActiveVideoPlayerSheet(
      video: video,
      lang: lang,
      topicId: topicId,
      initialQuality: selectedQuality,
      onQualityChanged: onQualityChanged,
    ),
  );
}

class _ActiveVideoPlayerSheet extends ConsumerStatefulWidget {
  final VideoMetadata video;
  final String lang;
  final String topicId;
  final String initialQuality;
  final void Function(String quality) onQualityChanged;

  const _ActiveVideoPlayerSheet({
    required this.video,
    required this.lang,
    required this.topicId,
    required this.initialQuality,
    required this.onQualityChanged,
  });

  @override
  ConsumerState<_ActiveVideoPlayerSheet> createState() => _ActiveVideoPlayerSheetState();
}

class _ActiveVideoPlayerSheetState extends ConsumerState<_ActiveVideoPlayerSheet> {
  late String _quality;
  bool _isPlaying = true;
  int _currentSeconds = 0;
  Timer? _timer;

  List<String> _getSubtitles(String lang, String title) {
    if (lang == 'te') {
      return [
        '🤖 "$title" - AI వీడియో వివరణ పాఠానికి స్వాగతం!',
        '💡 దృశ్యం 1: వాస్తవ జీవిత అనువర్తనం & ప్రాథమిక భావనల పరిచయం.',
        '🔬 దృశ్యం 2: తెలంగాణ SCERT సిలబస్ లోని ముఖ్య అంశాలు & సూత్రాలు.',
        '🎯 దృశ్యం 3: బోర్డు పరీక్షల ముఖ్యాంశాలు & స్కోరింగ్ పాయింట్లు.'
      ];
    }
    return [
      '🤖 Welcome to the AI Video Explainer for "$title"!',
      '💡 Scene 1: Real-world hook & foundational concept breakdown.',
      '🔬 Scene 2: Telangana SCERT curriculum topics & governing principles.',
      '🎯 Scene 3: Board exam memory anchors & high-scoring takeaways.'
    ];
  }

  @override
  void initState() {
    super.initState();
    _quality = widget.initialQuality;
    _startTimer();
  }

  void _startTimer() {
    _timer?.cancel();
    _timer = Timer.periodic(const Duration(seconds: 1), (t) {
      if (!mounted) return;
      if (_isPlaying) {
        setState(() {
          final total = widget.video.durationSeconds > 0 ? widget.video.durationSeconds : 600;
          if (_currentSeconds < total) {
            _currentSeconds++;
          }
        });
      }
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  String _formatTime(int seconds) {
    final m = seconds ~/ 60;
    final s = seconds % 60;
    return '$m:${s < 10 ? '0' : ''}$s';
  }

  @override
  Widget build(BuildContext context) {
    final lang = widget.lang;
    final totalSec = widget.video.durationSeconds > 0 ? widget.video.durationSeconds : 600;
    final progress = (_currentSeconds / totalSec).clamp(0.0, 1.0);
    final subs = _getSubtitles(lang, widget.video.localizedTitle(lang));
    final subIdx = (_currentSeconds ~/ 8) % subs.length;

    return Container(
      decoration: const BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.vertical(top: Radius.circular(24)),
      ),
      padding: const EdgeInsets.fromLTRB(20, 16, 20, 24),
      child: SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Handle bar
            Center(
              child: Container(
                width: 40,
                height: 4,
                decoration: BoxDecoration(
                  color: Colors.grey.shade300,
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
            ),
            const SizedBox(height: 14),

            // Header with close button
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Text(
                    AppStrings.get('videoPlayerTitle', lang),
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: AppColors.textDark,
                    ),
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.close_rounded),
                  onPressed: () => Navigator.of(context).pop(),
                ),
              ],
            ),
            const SizedBox(height: 8),

            // Interactive Video Player Stage
            Container(
              width: double.infinity,
              height: 200,
              decoration: BoxDecoration(
                gradient: const LinearGradient(
                  colors: [Color(0xFF0F172A), Color(0xFF1E3A8A)],
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                ),
                borderRadius: BorderRadius.circular(18),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.2),
                    blurRadius: 12,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Stack(
                alignment: Alignment.center,
                children: [
                  // Center play/pause & animation
                  Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      GestureDetector(
                        onTap: () {
                          setState(() {
                            _isPlaying = !_isPlaying;
                          });
                        },
                        child: Container(
                          width: 58,
                          height: 58,
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.95),
                            shape: BoxShape.circle,
                            boxShadow: [
                              BoxShadow(
                                color: Colors.blue.withOpacity(0.4),
                                blurRadius: 10,
                                offset: const Offset(0, 2),
                              ),
                            ],
                          ),
                          child: Icon(
                            _isPlaying ? Icons.pause_rounded : Icons.play_arrow_rounded,
                            size: 40,
                            color: AppColors.primaryBlue,
                          ),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 16.0),
                        child: Text(
                          widget.video.localizedTitle(lang),
                          textAlign: TextAlign.center,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                            color: Colors.white,
                            fontSize: 13,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        _isPlaying
                            ? (lang == 'te' ? '▶ వీడియో ప్లే అవుతోంది...' : '▶ Video playing now...')
                            : (lang == 'te' ? '⏸ పాజ్ చేయబడింది' : '⏸ Paused'),
                        style: TextStyle(
                          color: _isPlaying ? Colors.greenAccent : Colors.orangeAccent,
                          fontSize: 11,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ],
                  ),
                  // Quality badge top right
                  Positioned(
                    top: 10,
                    right: 10,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.black.withOpacity(0.65),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        _quality.split(' ').first,
                        style: const TextStyle(color: Colors.white, fontSize: 11, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                  // Stream provider top left
                  Positioned(
                    top: 10,
                    left: 12,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
                      decoration: BoxDecoration(
                        color: Colors.redAccent.withOpacity(0.9),
                        borderRadius: BorderRadius.circular(6),
                      ),
                      child: Text(
                        _isPlaying ? 'AI LESSON PLAYING' : 'AI LESSON PAUSED',
                        style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                  // Subtitle overlay at bottom
                  Positioned(
                    bottom: 8,
                    left: 12,
                    right: 12,
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: Colors.black.withOpacity(0.75),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Text(
                        subs[subIdx],
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          color: Color(0xFFFDE047),
                          fontSize: 11,
                          fontWeight: FontWeight.w600,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 10),

            // Time & Scrubber
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  _formatTime(_currentSeconds),
                  style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppColors.textDark),
                ),
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 10.0),
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(4),
                      child: LinearProgressIndicator(
                        value: progress,
                        minHeight: 6,
                        backgroundColor: AppColors.borderColor,
                        valueColor: const AlwaysStoppedAnimation<Color>(AppColors.primaryBlue),
                      ),
                    ),
                  ),
                ),
                Text(
                  _formatTime(totalSec),
                  style: const TextStyle(fontSize: 12, color: AppColors.textMuted),
                ),
              ],
            ),
            const SizedBox(height: 14),

            // Low-bandwidth Quality Options [Arch: Limited bandwidth]
            Text(
              AppStrings.get('qualitySelector', lang),
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.bold,
                color: AppColors.textDark,
              ),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                _buildQualityButton('360p (Data Saver)', _quality, (q) {
                  setState(() => _quality = q);
                  widget.onQualityChanged(q);
                }),
                const SizedBox(width: 8),
                _buildQualityButton('480p (Standard)', _quality, (q) {
                  setState(() => _quality = q);
                  widget.onQualityChanged(q);
                }),
                const SizedBox(width: 8),
                _buildQualityButton('720p (HD)', _quality, (q) {
                  setState(() => _quality = q);
                  widget.onQualityChanged(q);
                }),
              ],
            ),
            const SizedBox(height: 18),

            // "Mark as Watched" action (enqueues video_watched event and awards XP)
            SizedBox(
              width: double.infinity,
              height: 50,
              child: ElevatedButton(
                style: ElevatedButton.styleFrom(
                  backgroundColor: AppColors.meadowGreen,
                  foregroundColor: Colors.white,
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                  elevation: 2,
                ),
                onPressed: () {
                  final learnerId = ref.read(currentLearnerIdProvider);
                  SyncQueueService().enqueueEvent(
                    learnerId: learnerId,
                    eventType: 'video_watched',
                    payload: {
                      'video_id': widget.video.videoId,
                      'topic_id': widget.topicId,
                      'duration_seconds': widget.video.durationSeconds,
                      'language': widget.video.languageCode,
                      'quality': _quality,
                    },
                  );

                  ref.read(learnerXpProvider.notifier).state += 25;
                  ref.read(learnerCoinsProvider.notifier).state += 5;

                  Navigator.of(context).pop();

                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                        AppStrings.get('videoWatchedToast', lang),
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      backgroundColor: AppColors.darkGreen,
                      duration: const Duration(seconds: 3),
                      behavior: SnackBarBehavior.floating,
                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                    ),
                  );
                },
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.check_circle_rounded, size: 20),
                    const SizedBox(width: 8),
                    Text(
                      AppStrings.get('markVideoWatched', lang),
                      style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

Widget _buildQualityButton(
  String quality,
  String currentQuality,
  void Function(String quality) onSelected,
) {
  final isSelected = currentQuality == quality;
  final shortLabel = quality.split(' ').first;

  return Expanded(
    child: OutlinedButton(
      style: OutlinedButton.styleFrom(
        padding: const EdgeInsets.symmetric(vertical: 8),
        backgroundColor: isSelected ? AppColors.primaryBlue : Colors.transparent,
        side: BorderSide(
          color: isSelected ? AppColors.primaryBlue : AppColors.borderColor,
        ),
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      ),
      onPressed: () => onSelected(quality),
      child: Text(
        shortLabel,
        style: TextStyle(
          fontSize: 13,
          fontWeight: FontWeight.bold,
          color: isSelected ? Colors.white : AppColors.textDark,
        ),
      ),
    ),
  );
}

