import 'package:flutter/material.dart';

import '../../../../../screens/scan_screen.dart'; // Importez l'écran de scan

class MenuBuildListItems extends StatelessWidget {
  final AnimationController staggeredController;
  final List<Interval> itemSlideIntervals;
  final List<String> menuTitles;

  const MenuBuildListItems({
    required this.staggeredController,
    required this.itemSlideIntervals,
    required this.menuTitles,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    final menuIcons = [
      Icons.bluetooth_rounded,
      Icons.mic_rounded,
      Icons.touch_app_rounded,
      Icons.info_rounded,
    ];

    return Column(
      children: List.generate(menuTitles.length, (i) {
        return AnimatedBuilder(
          animation: staggeredController,
          builder: (context, child) {
            final animationPercent = Curves.easeOutCubic.transform(
              itemSlideIntervals[i].transform(staggeredController.value),
            );
            final opacity = animationPercent;
            final slideDistance = (1.0 - animationPercent) * 150;

            return Opacity(
              opacity: opacity,
              child: Transform.translate(
                offset: Offset(slideDistance, 0),
                child: child,
              ),
            );
          },
          child: Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
            child: Material(
              color: Colors.transparent,
              child: InkWell(
                onTap: () {
                  // Navigation basée sur l'index
                  if (i == 0) {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const ScanScreen(),
                      ),
                    );
                  }
                  // Vous pourrez ajouter les autres pages ici (else if (i == 1) ...)
                },
                borderRadius: BorderRadius.circular(16),
                child: Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 20,
                    vertical: 18,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(16),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.04),
                        blurRadius: 10,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Row(
                    children: [
                      Container(
                        width: 48,
                        height: 48,
                        decoration: BoxDecoration(
                          gradient: const LinearGradient(
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                            colors: [Color(0xFF6C63FF), Color(0xFF8B84FF)],
                          ),
                          borderRadius: BorderRadius.circular(12),
                          boxShadow: [
                            BoxShadow(
                              color: const Color(0xFF6C63FF).withOpacity(0.3),
                              blurRadius: 8,
                              offset: const Offset(0, 4),
                            ),
                          ],
                        ),
                        child: Icon(
                          menuIcons[i],
                          color: Colors.white,
                          size: 24,
                        ),
                      ),
                      const SizedBox(width: 16),
                      Expanded(
                        child: Text(
                          menuTitles[i],
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w600,
                            color: Color(0xFF1A1A2E),
                            letterSpacing: 0.3,
                          ),
                        ),
                      ),
                      Icon(
                        Icons.arrow_forward_ios_rounded,
                        size: 16,
                        color: const Color(0xFF6C63FF).withOpacity(0.5),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        );
      }),
    );
  }
}
