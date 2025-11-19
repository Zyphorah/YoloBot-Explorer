import 'package:flutter/material.dart';
import 'DirectionalButton.dart';

class LeftRightUpDownDirection extends StatelessWidget {
  bool isStopping;
  void Function(VoidCallback fn) setState;

  LeftRightUpDownDirection({
    Key? key,
    required this.isStopping,
    required this.setState,
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
                    print('Avancer');
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
                        print('Tourner à gauche');
                      },
                    ),
                    DirectionalButton(
                      icon: Icons.arrow_right,
                      label: 'DROITE',
                      onPressed: () {
                        print('Tourner à droite');
                      },
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                DirectionalButton(
                  icon: Icons.arrow_downward,
                  label: 'RECULER',
                  onPressed: () {
                    print('Reculer');
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