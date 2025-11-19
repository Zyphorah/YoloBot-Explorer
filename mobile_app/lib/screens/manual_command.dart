import 'package:flutter/material.dart';
import '../widget/Button/DirectionalButton.dart';

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
                  child: Column(
                    children: [
                      // Contrôles droite (direction)
                      Expanded(
                        flex: 2,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            // Flèche haut
                            SizedBox(height: 20),
                            DirectionalButton(
                              icon: Icons.arrow_upward,
                              label: 'AVANCER',
                              onPressed: () {
                                print('Avancer');
                              },
                            ),
                            SizedBox(height: 16),
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
                            SizedBox(height: 16),
                            DirectionalButton(
                              icon: Icons.arrow_downward,
                              label: 'RECULER',
                              onPressed: () {
                                print('Reculer');
                              },
                            ),
                            SizedBox(height: 20),
                          ],
                        ),
                      ),
                      // Contrôles gauche (retirer accélération, garder arrêt)
                      Expanded(
                        flex: 1,
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            // Bouton STOP (frein)
                            GestureDetector(
                              onTapDown: (_) {
                                setState(() => isStopping = true);
                              },
                              onTapUp: (_) {
                                setState(() => isStopping = false);
                              },
                              child: Container(
                                decoration: BoxDecoration(
                                  shape: BoxShape.circle,
                                  gradient: LinearGradient(
                                    colors: 
                                    isStopping ? [Color(0xFFff0000), Color(0xFFcc0000)]
                                            : [Color.fromARGB(255, 184, 0, 0), Color.fromARGB(255, 153, 0, 0)],
                                  ),
                                ),
                                width: 120,
                                height: 120,
                                child: Center(
                                  child: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(Icons.stop_circle,
                                          color: Colors.white, size: 40),
                                      Text('Stop',
                                          style: TextStyle(
                                              color: Colors.white,
                                              fontWeight: FontWeight.bold,
                                              fontSize: 12,
                                              letterSpacing: 1))
                                    ],
                                  ),
                                ),
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
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

class ActionButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final bool isActive;
  final VoidCallback onPressed;
  final Color color;

  const ActionButton({
    required this.icon,
    required this.label,
    required this.isActive,
    required this.onPressed,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onPressed,
      child: AnimatedContainer(
        duration: Duration(milliseconds: 200),
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(12),
          gradient: LinearGradient(
            colors: isActive
                ? [color, color.withOpacity(0.7)]
                : [color.withOpacity(0.4), color.withOpacity(0.2)],
          ),
          border: Border.all(
            color: color,
            width: isActive ? 2 : 1,
          ),
        ),
        padding: EdgeInsets.symmetric(horizontal: 20, vertical: 15),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, color: Colors.white, size: 28),
            SizedBox(height: 8),
            Text(
              label,
              style: TextStyle(
                color: Colors.white,
                fontWeight: FontWeight.bold,
                fontSize: 10,
                letterSpacing: 1,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
