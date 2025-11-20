import 'package:flutter/material.dart';
import '../widget/button/action_button.dart';
import '../widget/button/left_right_up_down_direction.dart';
import '../widget/button/stop.dart';
import '../services/ble_service.dart';

class ManualCommand extends StatefulWidget {
  const ManualCommand({super.key});

  @override
  State<ManualCommand> createState() => _ManualCommandState();
}

class _ManualCommandState extends State<ManualCommand> {
  final BleService _bleService = BleService();
  bool isDetecting = false;
  bool isAutonomous = false;
  bool isStopping = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Stack(
        children: [
          // Fond avec grille gaming
          Container(decoration: BoxDecoration(color: Colors.white)),
          // Contenu principal
          SafeArea(
            child: Column(
              children: [
                // Header
                Padding(
                  padding: EdgeInsets.all(16),
                  child: Text(
                    'COMMANDE MANUELLE',
                    style: TextStyle(
                      color: Colors
                          .black, // Changed to black for visibility on white
                      fontSize: 24,
                      fontWeight: FontWeight.bold,
                      letterSpacing: 2,
                    ),
                  ),
                ),
                Expanded(
                  child: LeftRightUpDownDirection(
                    isStopping: isStopping,
                    setState: setState,
                    onCommand: (cmd) => _bleService.sendCommand(cmd),
                  ),
                ),

                Stop(
                  initialStopping: isStopping,
                  onStop: () => _bleService.sendCommand('stop'),
                ),
                // Boutons du bas
                Padding(
                  padding: EdgeInsets.all(20),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      // Détection d'objets
                      ActionButton(
                        icon: Icons.radar,
                        label: 'DÉTECTER',
                        isActive: isDetecting,
                        onPressed: () {
                          if (isAutonomous && !isDetecting) {
                            // Empêcher l'activation de la détection si en mode autonome
                            return;
                          }
                          setState(() => isDetecting = !isDetecting);
                          // Send command to toggle detection
                          _bleService.sendCommand(
                            isDetecting ? 'detect_on' : 'detect_off',
                          );
                        },
                        color: Colors.orange,
                      ),
                      // Mode autonome
                      ActionButton(
                        icon: Icons.auto_awesome,
                        label: 'AUTONOME',
                        isActive: isAutonomous,
                        onPressed: () {
                          if (isDetecting && !isAutonomous) {
                            // Empêcher l'activation du mode autonome si la détection est active
                            return;
                          }
                          setState(() => isAutonomous = !isAutonomous);
                          // Send command to toggle autonomous mode
                          _bleService.sendCommand(
                            isAutonomous ? 'auto_on' : 'auto_off',
                          );
                        },
                        color: Colors.purple,
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
