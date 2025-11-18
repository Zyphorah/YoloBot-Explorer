import 'package:flutter/material.dart';

class DrawerControllerHelper {
  final AnimationController drawerSlideController;

  DrawerControllerHelper(this.drawerSlideController);

  bool isDrawerOpen() => drawerSlideController.value == 1.0;

  bool isDrawerOpening() => drawerSlideController.status == AnimationStatus.forward;

  bool isDrawerClosed() => drawerSlideController.value == 0.0;

  void toggleDrawer() {
    if (isDrawerOpen() || isDrawerOpening()) {
      drawerSlideController.reverse();
    } else {
      drawerSlideController.forward();
    }
  }
}