// Code source pour lib/widget/Menu/menu.dart https://docs.flutter.dev/cookbook/effects/staggered-menu-animation
import 'package:flutter/material.dart';
import '../widget/Menu/menu_app_bar.dart';
import '../widget/Menu/menu_build_drawer.dart';
import '../widget/Menu/Logiques/drawer_controller_helper.dart';
import 'manual_command.dart';

class MenuStaggeredAnimations extends StatefulWidget {
  const MenuStaggeredAnimations({super.key});

  @override
  State<MenuStaggeredAnimations> createState() => _MenuStaggeredAnimationsState();
}

class _MenuStaggeredAnimationsState extends State<MenuStaggeredAnimations>
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
          ManualCommand(),
          MenuBuildDrawer(
            drawerSlideController: _drawerSlideController,
            isDrawerClosed: _drawerControllerHelper.isDrawerClosed,
          ),
         
        ],
      ),
    );
  }
}
