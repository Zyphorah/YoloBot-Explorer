import 'package:flutter/material.dart';

import 'enfants/menu_build_list_items.dart';

class MenuBuildContent extends StatelessWidget {
  final AnimationController staggeredController;
  final List<Interval> itemSlideIntervals;
  final List<String> menuTitles;
  final VoidCallback onMenuAction;

  const MenuBuildContent({
    required this.staggeredController,
    required this.itemSlideIntervals,
    required this.menuTitles,
    required this.onMenuAction,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const SizedBox(height: 32),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                'Navigation',
                style: TextStyle(
                  fontSize: 14,
                  fontWeight: FontWeight.w600,
                  color: const Color(0xFF6C63FF).withAlpha(179),
                  letterSpacing: 1.2,
                ),
              ),
              const SizedBox(height: 8),
              Container(
                width: 40,
                height: 3,
                decoration: BoxDecoration(
                  gradient: const LinearGradient(
                    colors: [Color(0xFF6C63FF), Color(0xFF8B84FF)],
                  ),
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 24),
        MenuBuildListItems(
          staggeredController: staggeredController,
          itemSlideIntervals: itemSlideIntervals,
          menuTitles: menuTitles,
          onMenuAction: onMenuAction,
        ),
      ],
    );
  }
}
