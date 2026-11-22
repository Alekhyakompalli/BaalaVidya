import 'dart:async';
import 'package:flutter/foundation.dart';

/// Progress Event model for sync queue
class SyncEvent {
  final String eventId;
  final String clientId;
  final String learnerId;
  final String eventType; // 'topic_read', 'workbook_completed', 'game_played', 'question_asked'
  final Map<String, dynamic> payload;
  final DateTime timestamp;
  int retryCount;
  bool isSynced;

  SyncEvent({
    required this.eventId,
    required this.clientId,
    required this.learnerId,
    required this.eventType,
    required this.payload,
    required this.timestamp,
    this.retryCount = 0,
    this.isSynced = false,
  });

  Map<String, dynamic> toJson() => {
        'event_id': eventId,
        'client_id': clientId,
        'learner_id': learnerId,
        'event_type': eventType,
        'payload': payload,
        'timestamp': timestamp.toIso8601String(),
        'retry_count': retryCount,
        'is_synced': isSynced,
      };
}

/// Sync Queue Service adhering strictly to [Arch: Sync rules 1, 2, 3, 6].
/// 1. Progress events are written locally first, always. The UI never waits for the network.
/// 2. Events are sent in the order they occurred.
/// 3. Unique client ID / event ID prevents double counting.
/// 6. Queue is kept after a failed send and retried with exponential back-off.
class SyncQueueService {
  static final SyncQueueService _instance = SyncQueueService._internal();
  factory SyncQueueService() => _instance;
  SyncQueueService._internal();

  final List<SyncEvent> _queue = [];
  bool _isSyncing = false;

  List<SyncEvent> get pendingEvents => _queue.where((e) => !e.isSynced).toList();
  List<SyncEvent> get allEvents => List.unmodifiable(_queue);

  /// 1. Write event locally first (never blocks UI)
  void enqueueEvent({
    required String learnerId,
    required String eventType,
    required Map<String, dynamic> payload,
  }) {
    final now = DateTime.now();
    final event = SyncEvent(
      eventId: 'evt_${now.millisecondsSinceEpoch}_${_queue.length}',
      clientId: 'client_device_pilot_01',
      learnerId: learnerId,
      eventType: eventType,
      payload: payload,
      timestamp: now,
    );

    _queue.add(event);
    debugPrint('[SyncQueue] Enqueued local event: ${event.eventType} (Pending: ${pendingEvents.length})');
  }

  /// Process queue with ordered retry and exponential backoff
  Future<int> processQueue({bool isOnline = true}) async {
    if (!isOnline || _isSyncing) return 0;
    _isSyncing = true;
    int syncedCount = 0;

    try {
      // Send events in the exact chronological order they occurred
      for (final event in _queue.where((e) => !e.isSynced)) {
        if (!isOnline) break;

        try {
          // Simulate network send
          await Future.delayed(const Duration(milliseconds: 100));
          event.isSynced = true;
          syncedCount++;
        } catch (_) {
          // Rule 6: keep on failure, increment retry count with exponential back-off
          event.retryCount++;
          final backoffMs = (500 * (1 << event.retryCount)).clamp(500, 10000);
          await Future.delayed(Duration(milliseconds: backoffMs));
          break; // Stop batch on failure to preserve strict order
        }
      }
    } finally {
      _isSyncing = false;
    }

    return syncedCount;
  }
}
