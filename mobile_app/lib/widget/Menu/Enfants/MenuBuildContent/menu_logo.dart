import 'package:flutter/material.dart';

class MenuLogo extends StatelessWidget {
  const MenuLogo({super.key});

  @override
  Widget build(BuildContext context) {
    return Positioned(
      right: -100,
      bottom: -50,
      child: Opacity(
        opacity: 0.05,
        child: Image.asset(
          'assets/images/electronique_circuit.png',
          width: 400,
          height: 400,
          fit: BoxFit.contain,
        ),
      ),
    );
  }
}