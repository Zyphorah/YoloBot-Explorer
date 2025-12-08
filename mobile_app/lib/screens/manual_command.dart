import 'dart:async';
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
  StreamSubscription<RobotStatus>? _statusSubscription;
  RobotStatus _currentStatus = RobotStatus.disconnected;

  @override
  void initState() {
    super.initState();
    _currentStatus = _bleService.currentRobotStatus;
    _statusSubscription = _bleService.robotStatus.listen((status) {
      if (mounted) {
        setState(() {
          _currentStatus = status;
          if (status == RobotStatus.inMission) {
            isAutonomous = true;
          } else if (status == RobotStatus.connected || status == RobotStatus.disconnected) {
            isAutonomous = false;
          }
        });
      }
    });
  }

  @override
  void dispose() {
    _statusSubscription?.cancel();
    super.dispose();
  }

  void _sendCommand(String command) {
    if (!_bleService.isConnected) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Robot non connecté'), backgroundColor: Colors.orange),
      );
      return;
    }
    _bleService.sendCommand(command);
  }

  Color _getStatusColor() {
    switch (_currentStatus) {
      case RobotStatus.disconnected:
        return Colors.red;
      case RobotStatus.connected:
        return Colors.green;
      case RobotStatus.moving:
        return Colors.blue;
      case RobotStatus.inMission:
        return Colors.purple;
    }
  }

  String _getStatusText() {
    switch (_currentStatus) {
      case RobotStatus.disconnected:
        return 'Déconnecté';
      case RobotStatus.connected:
        return 'Connecté';
      case RobotStatus.moving:
        return 'En mouvement';
      case RobotStatus.inMission:
        return 'Mode autonome';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          children: [
            // Header
            Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                children: [
                  const Text(
                    'COMMANDE MANUELLE',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, letterSpacing: 2),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Container(
                        width: 10,
                        height: 10,
                        decoration: BoxDecoration(color: _getStatusColor(), shape: BoxShape.circle),
                      ),
                      const SizedBox(width: 8),
                      Text(_getStatusText(), style: TextStyle(color: _getStatusColor())),
                    ],
                  ),
                ],
              ),
            ),
            
            // Directions
            Expanded(
              child: LeftRightUpDownDirection(
                isStopping: isStopping,
                setState: setState,
                onCommand: (cmd) => _sendCommand(cmd),
              ),
            ),

            // Stop
            Stop(
              initialStopping: isStopping,
              onStop: () => _sendCommand('stop'),
            ),
            
            // Boutons d'action
            Padding(
              padding: const EdgeInsets.all(20),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ActionButton(
                    icon: Icons.radar,
                    label: 'DÉTECTER',
                    isActive: isDetecting,
                    onPressed: () {
                      if (isAutonomous && !isDetecting) return;
                      setState(() => isDetecting = !isDetecting);
                      _sendCommand(isDetecting ? 'detect_on' : 'detect_off');
                    },
                    color: Colors.orange,
                  ),
                  ActionButton(
                    icon: Icons.auto_awesome,
                    label: 'AUTONOME',
                    isActive: isAutonomous,
                    onPressed: () {
                      if (isDetecting && !isAutonomous) return;
                      setState(() => isAutonomous = !isAutonomous);
                      _sendCommand(isAutonomous ? 'auto_on' : 'auto_off');
                    },
                    color: Colors.purple,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
