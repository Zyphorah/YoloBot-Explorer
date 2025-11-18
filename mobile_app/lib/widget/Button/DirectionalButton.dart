import 'package:flutter/material.dart';

class DirectionalButton extends StatefulWidget {
  final IconData icon;
  final String label;
  final VoidCallback onPressed;

  const DirectionalButton({
    required this.icon,
    required this.label,
    required this.onPressed,
  });

  @override
  State<DirectionalButton> createState() => _DirectionalButtonState();
}

class _DirectionalButtonState extends State<DirectionalButton> {
  bool isPressed = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: (_) {
        setState(() => isPressed = true);
        widget.onPressed();
      },
      onTapUp: (_) {
        setState(() => isPressed = false);
      },
      child: AnimatedContainer(
        duration: Duration(milliseconds: 100),
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          gradient: LinearGradient(
            colors: isPressed
                ? [Color.fromARGB(255, 182, 182, 182), Color.fromARGB(255, 172, 172, 172)]
                : [Color.fromARGB(255, 143, 143, 143), Color.fromARGB(255, 105, 105, 105)],
          ),
        ),
        width: 90,
        height: 90,
        child: Center(
          child: Icon(widget.icon, color: Colors.white, size: 35),
        ),
      ),
    );
  }
}