import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import 'screens/menu_staggered_animations.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  SystemChrome.setPreferredOrientations([
    DeviceOrientation.portraitUp,
    DeviceOrientation.portraitDown,
  ]);
  runApp(
    MaterialApp(
      home: MenuStaggeredAnimations(),
      debugShowCheckedModeBanner: false,
    ),
  );
}
