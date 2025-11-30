import 'dart:async';
import 'package:flutter/material.dart';
import '../services/ble_service.dart';

class ReturnToState extends StatefulWidget {
  final VoidCallback returnToPreviousState;

  const ReturnToState({required this.returnToPreviousState, super.key});

  @override
  State<ReturnToState> createState() => _ReturnToStateState();
}

class _ReturnToStateState extends State<ReturnToState> {
  final BleService _bleService = BleService();
  late StreamSubscription<RobotStatus> _statusSubscription;
  late StreamSubscription<RobotMessage> _messageSubscription;
  late StreamSubscription<int> _servoSubscription;

  RobotStatus _currentStatus = RobotStatus.disconnected;
  int _servoAngle = 90;
  final List<RobotMessage> _messages = [];

  @override
  void initState() {
    super.initState();
    _currentStatus = _bleService.currentRobotStatus;
    _servoAngle = _bleService.currentServoAngle;
    _messages.addAll(_bleService.messageHistory);

    _statusSubscription = _bleService.robotStatus.listen((status) {
      if (mounted) setState(() => _currentStatus = status);
    });

    _messageSubscription = _bleService.robotMessages.listen((message) {
      if (mounted) {
        setState(() {
          _messages.add(message);
          if (_messages.length > 50) _messages.removeAt(0);
        });
      }
    });

    _servoSubscription = _bleService.servoAngle.listen((angle) {
      if (mounted) setState(() => _servoAngle = angle);
    });
  }

  @override
  void dispose() {
    _statusSubscription.cancel();
    _messageSubscription.cancel();
    _servoSubscription.cancel();
    super.dispose();
  }

  String _getStatusText(RobotStatus status) {
    switch (status) {
      case RobotStatus.disconnected:
        return 'Déconnecté';
      case RobotStatus.connected:
        return 'Connecté';
      case RobotStatus.moving:
        return 'En mouvement';
      case RobotStatus.inMission:
        return 'En mission autonome';
    }
  }

  Color _getStatusColor(RobotStatus status) {
    switch (status) {
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

  IconData _getStatusIcon(RobotStatus status) {
    switch (status) {
      case RobotStatus.disconnected:
        return Icons.bluetooth_disabled;
      case RobotStatus.connected:
        return Icons.bluetooth_connected;
      case RobotStatus.moving:
        return Icons.directions_run;
      case RobotStatus.inMission:
        return Icons.auto_awesome;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Retour d\'état'),
        actions: [
          IconButton(
            icon: const Icon(Icons.delete_outline),
            onPressed: () {
              setState(() => _messages.clear());
              _bleService.clearMessageHistory();
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Statut de connexion
            Card(
              child: ListTile(
                leading: Icon(_getStatusIcon(_currentStatus), color: _getStatusColor(_currentStatus)),
                title: const Text('État du robot'),
                subtitle: Text(
                  _getStatusText(_currentStatus),
                  style: TextStyle(color: _getStatusColor(_currentStatus), fontWeight: FontWeight.bold),
                ),
                trailing: (_currentStatus == RobotStatus.moving || _currentStatus == RobotStatus.inMission)
                    ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2))
                    : null,
              ),
            ),
            const SizedBox(height: 8),

            // Angle du servo
            Card(
              child: ListTile(
                leading: const Icon(Icons.rotate_right, color: Colors.orange),
                title: const Text('Angle du Servo'),
                trailing: Text('$_servoAngle°', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              ),
            ),
            const SizedBox(height: 8),

            // Messages du robot
            const Text('Messages du robot', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w600)),
            const SizedBox(height: 8),
            Expanded(
              child: Card(
                child: _messages.isEmpty
                    ? const Center(child: Text('Aucun message', style: TextStyle(color: Colors.grey)))
                    : ListView.builder(
                        padding: const EdgeInsets.all(8),
                        itemCount: _messages.length,
                        itemBuilder: (context, index) {
                          final msg = _messages[index];
                          return Padding(
                            padding: const EdgeInsets.symmetric(vertical: 4),
                            child: Text(
                              '${_formatTime(msg.timestamp)} - ${msg.message}',
                              style: const TextStyle(fontSize: 13),
                            ),
                          );
                        },
                      ),
              ),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: widget.returnToPreviousState,
              child: const Text('Retour'),
            ),
          ],
        ),
      ),
    );
  }

  String _formatTime(DateTime time) {
    return '${time.hour.toString().padLeft(2, '0')}:${time.minute.toString().padLeft(2, '0')}:${time.second.toString().padLeft(2, '0')}';
  }
}

