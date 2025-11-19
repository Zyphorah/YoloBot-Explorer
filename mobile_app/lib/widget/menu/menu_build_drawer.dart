import 'package:flutter/material.dart';
import 'menu.dart';

class MenuBuildDrawer extends StatelessWidget {
  final AnimationController drawerSlideController;
  final bool Function() isDrawerClosed;

  const MenuBuildDrawer({
    required this.drawerSlideController,
    required this.isDrawerClosed,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: drawerSlideController,
      builder: (context, child) {
        return FractionalTranslation(
          translation: Offset(1.0 - drawerSlideController.value, 0.0),
          child: isDrawerClosed() ? const SizedBox() : const Menu(),
        );
      },
    );
  }
}