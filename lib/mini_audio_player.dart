// mini_audio_player.dart
import 'dart:ui';
import 'package:flutter/material.dart';
import 'audio_player_service.dart';
import 'audio_player_screen.dart';

class MiniAudioPlayer extends StatelessWidget {
  const MiniAudioPlayer({super.key});

  @override
  Widget build(BuildContext context) {
    final service = AudioPlayerService();

    return AnimatedBuilder(
      animation: service,
      builder: (context, _) {
        if (!service.hasActiveAudio) {
          return const SizedBox.shrink();
        }

        final duration = service.duration.inMilliseconds;
        final position = service.position.inMilliseconds;
        final progress = (duration > 0) ? (position / duration).clamp(0.0, 1.0) : 0.0;

        return Dismissible(
          key: Key('mini_player_${service.currentBookId}'),
          direction: DismissDirection.down,
          onDismissed: (_) => service.stop(),
          child: Container(
            margin: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            height: 64,
            decoration: BoxDecoration(
              color: const Color(0xFF222222).withOpacity(0.92),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.white12),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.4),
                  blurRadius: 15,
                  offset: const Offset(0, 6),
                ),
              ],
            ),
            child: ClipRRect(
              borderRadius: BorderRadius.circular(16),
              child: BackdropFilter(
                filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
                child: Column(
                  children: [
                    // Thanh tiến trình mỏng phía trên cùng của thanh mini
                    LinearProgressIndicator(
                      value: progress,
                      minHeight: 2.5,
                      backgroundColor: Colors.white10,
                      valueColor: const AlwaysStoppedAnimation<Color>(Colors.orange),
                    ),
                    Expanded(
                      child: InkWell(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => const AudioPlayerScreen(),
                              fullscreenDialog: true,
                            ),
                          );
                        },
                        child: Padding(
                          padding: const EdgeInsets.symmetric(horizontal: 12),
                          child: Row(
                            children: [
                              // Ảnh bìa sách
                              ClipRRect(
                                borderRadius: BorderRadius.circular(8),
                                child: service.currentCoverUrl.isNotEmpty
                                    ? Image.network(
                                        service.currentCoverUrl,
                                        width: 44,
                                        height: 44,
                                        fit: BoxFit.cover,
                                        errorBuilder: (_, __, ___) => Container(
                                          width: 44,
                                          height: 44,
                                          color: Colors.grey[800],
                                          child: const Icon(Icons.headset, color: Colors.white54, size: 20),
                                        ),
                                      )
                                    : Container(
                                        width: 44,
                                        height: 44,
                                        color: Colors.grey[800],
                                        child: const Icon(Icons.headset, color: Colors.white54, size: 20),
                                      ),
                              ),
                              const SizedBox(width: 12),

                              // Tiêu đề sách & tác giả
                              Expanded(
                                child: Column(
                                  mainAxisAlignment: MainAxisAlignment.center,
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      service.currentTitle,
                                      style: const TextStyle(
                                        color: Colors.white,
                                        fontWeight: FontWeight.bold,
                                        fontSize: 13,
                                      ),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                    const SizedBox(height: 2),
                                    Text(
                                      service.currentAuthor,
                                      style: const TextStyle(
                                        color: Colors.white54,
                                        fontSize: 11,
                                      ),
                                      maxLines: 1,
                                      overflow: TextOverflow.ellipsis,
                                    ),
                                  ],
                                ),
                              ),

                              // Nút Play / Pause
                              IconButton(
                                icon: service.isLoading
                                    ? const SizedBox(
                                        width: 24,
                                        height: 24,
                                        child: CircularProgressIndicator(
                                          strokeWidth: 2.5,
                                          color: Colors.orange,
                                        ),
                                      )
                                    : Icon(
                                        service.isPlaying ? Icons.pause_circle_filled_rounded : Icons.play_circle_filled_rounded,
                                        color: Colors.orange,
                                        size: 36,
                                      ),
                                onPressed: () => service.togglePlayPause(),
                              ),

                              // Nút Đóng
                              IconButton(
                                icon: const Icon(Icons.close_rounded, color: Colors.white38, size: 20),
                                onPressed: () => service.stop(),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        );
      },
    );
  }
}
