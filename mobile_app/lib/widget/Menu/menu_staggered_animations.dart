// Code source pour lib/widget/Menu/menu.dart https://docs.flutter.dev/cookbook/effects/staggered-menu-animation
import 'package:flutter/material.dart';

import 'Enfants/menu_app_bar.dart';
import 'Enfants/menu_build_drawer.dart';
import 'Logiques/drawer_controller_helper.dart';

class StaggeredAnimations extends StatefulWidget {
  const StaggeredAnimations({super.key});

  @override
  State<StaggeredAnimations> createState() => _StaggeredAnimationsState();
}

class _StaggeredAnimationsState extends State<StaggeredAnimations>
    with SingleTickerProviderStateMixin {
  late AnimationController _drawerSlideController;
  late final DrawerControllerHelper _drawerControllerHelper =
      DrawerControllerHelper(_drawerSlideController);

  @override
  void initState() {
    super.initState();

    _drawerSlideController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 150),
    );
  }

  @override
  void dispose() {
    _drawerSlideController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),
      appBar: MenuAppBar(
        drawerSlideController: _drawerSlideController,
        toggleDrawer: _drawerControllerHelper.toggleDrawer,
        isDrawerOpen: _drawerControllerHelper.isDrawerOpen,
        isDrawerOpening: _drawerControllerHelper.isDrawerOpening,
      ),
      body: Stack(
        children: [
          const SizedBox(),
          MenuBuildDrawer(
            drawerSlideController: _drawerSlideController,
            isDrawerClosed: _drawerControllerHelper.isDrawerClosed,
          ),
        ],
      ),
    );
  }
}
