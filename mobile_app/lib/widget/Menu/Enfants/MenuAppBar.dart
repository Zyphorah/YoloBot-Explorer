import 'package:flutter/material.dart';

class MenuAppBar extends StatelessWidget implements PreferredSizeWidget {
  final AnimationController drawerSlideController;
  final VoidCallback toggleDrawer;
  final bool Function() isDrawerOpen;
  final bool Function() isDrawerOpening;

  const MenuAppBar({
    required this.drawerSlideController,
    required this.toggleDrawer,
    required this.isDrawerOpen,
    required this.isDrawerOpening,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: const Text(
        'Menu',
        style: TextStyle(
          color: Color(0xFF1A1A2E),
          fontSize: 22,
          fontWeight: FontWeight.w600,
          letterSpacing: 0.5,
        ),
      ),
      backgroundColor: Colors.white,
      elevation: 0.0,
      automaticallyImplyLeading: false,
      shadowColor: Colors.black.withOpacity(0.1),
      actions: [
        AnimatedBuilder(
          animation: drawerSlideController,
          builder: (context, child) {
            return Container(
              margin: const EdgeInsets.only(right: 8),
              decoration: BoxDecoration(
                color: isDrawerOpen() || isDrawerOpening()
                    ? const Color(0xFF6C63FF).withOpacity(0.1)
                    : Colors.transparent,
                borderRadius: BorderRadius.circular(12),
              ),
              child: IconButton(
                onPressed: toggleDrawer,
                icon: isDrawerOpen() || isDrawerOpening()
                    ? const Icon(Icons.close_rounded, color: Color(0xFF6C63FF), size: 28)
                    : const Icon(Icons.menu_rounded, color: Color(0xFF1A1A2E), size: 28),
              ),
            );
          },
        ),
      ],
    );
  }

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);
}