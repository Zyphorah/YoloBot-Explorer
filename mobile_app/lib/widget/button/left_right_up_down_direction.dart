import 'package:flutter/material.dart';
import 'directional_button.dart';

// ignore: must_be_immutable
class LeftRightUpDownDirection extends StatelessWidget {
  bool isStopping;
  void Function(VoidCallback fn) setState;
  final Function(String) onCommand;

  LeftRightUpDownDirection({
    Key? key,
    required this.isStopping,
    required this.setState,
    required this.onCommand,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Column(
        children: [
          // Contrôles droite (direction)
          Expanded(
            flex: 2,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Flèche haut
                const SizedBox(height: 20),
                DirectionalButton(
                  icon: Icons.arrow_upward,
                  label: 'AVANCER',
                  onPressed: () {
                    onCommand('avancer');
                  },
                ),
                const SizedBox(height: 16),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    DirectionalButton(
                      icon: Icons.arrow_left,
                      label: 'GAUCHE',
                      onPressed: () {
                        onCommand('gauche');
                      },
                    ),
                    DirectionalButton(
                      icon: Icons.arrow_right,
                      label: 'DROITE',
                      onPressed: () {
                        onCommand('droite');
                      },
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                DirectionalButton(
                  icon: Icons.arrow_downward,
                  label: 'RECULER',
                  onPressed: () {
                    onCommand('reculer');
                  },
                ),
                const SizedBox(height: 20),
              ],
            ),
          ),
        ],
      ),
    );
  }
}