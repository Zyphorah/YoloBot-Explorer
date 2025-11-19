import 'package:flutter/material.dart';
import '../widget/button/action_button.dart';
import '../widget/button/left_right_up_down_direction.dart';
import '../widget/button/stop.dart';

class ManualCommand extends StatefulWidget {
  const ManualCommand({super.key});

  @override
  State<ManualCommand> createState() => _ManualCommandState();
}

class _ManualCommandState extends State<ManualCommand> {
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
          Container(
            decoration: BoxDecoration(
              color: Colors.white, 
            ),
          ),
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
                      color: Colors.white, 
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
                  ),
                ),  
                
                Stop(
                  initialStopping: isStopping,
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
                          if(isAutonomous && !isDetecting) {
                            // Empêcher l'activation de la détection si en mode autonome
                            return;
                          }
                          setState(() => isDetecting = !isDetecting);
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
