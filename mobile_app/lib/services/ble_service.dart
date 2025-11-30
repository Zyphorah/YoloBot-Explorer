import 'dart:async';
import 'dart:convert';

import 'package:flutter_blue_plus/flutter_blue_plus.dart';

import '../utils/constants.dart';

/// États du robot
enum RobotStatus {
  disconnected,
  connected,
  moving,
  inMission,
}

/// Modèle pour les messages reçus du robot
class RobotMessage {
  final String message;
  final DateTime timestamp;
  
  RobotMessage(this.message, this.timestamp);
}

class BleService {
  static final BleService _instance = BleService._internal();

  factory BleService() {
    return _instance;
  }

  BleService._internal();

  BluetoothDevice? _connectedDevice;
  BluetoothCharacteristic? _commandCharacteristic;
  BluetoothCharacteristic? _notifyCharacteristic;
  StreamSubscription? _connectionSubscription;
  StreamSubscription? _notificationSubscription;
  
  // Reconnexion automatique
  bool _autoReconnect = true;
  String? _lastDeviceId;

  // Stream for scan results
  Stream<List<ScanResult>> get scanResults => FlutterBluePlus.scanResults;

  // Stream for connection state
  final _connectionStateController =
      StreamController<BluetoothConnectionState>.broadcast();
  Stream<BluetoothConnectionState> get connectionState =>
      _connectionStateController.stream;
  
  // Stream pour le statut du robot
  final _robotStatusController = StreamController<RobotStatus>.broadcast();
  Stream<RobotStatus> get robotStatus => _robotStatusController.stream;
  RobotStatus _currentRobotStatus = RobotStatus.disconnected;
  RobotStatus get currentRobotStatus => _currentRobotStatus;
  
  // Stream pour les messages reçus du robot
  final _robotMessagesController = StreamController<RobotMessage>.broadcast();
  Stream<RobotMessage> get robotMessages => _robotMessagesController.stream;
  final List<RobotMessage> _messageHistory = [];
  List<RobotMessage> get messageHistory => List.unmodifiable(_messageHistory);
  
  // Stream pour l'angle du servo motor
  final _servoAngleController = StreamController<int>.broadcast();
  Stream<int> get servoAngle => _servoAngleController.stream;
  int _currentServoAngle = 90;
  int get currentServoAngle => _currentServoAngle;

  BluetoothDevice? get connectedDevice => _connectedDevice;
  bool get isConnected => _connectedDevice != null && _currentRobotStatus != RobotStatus.disconnected;

  Future<void> startScan() async {
    await FlutterBluePlus.startScan(timeout: const Duration(seconds: 15));
  }

  Future<void> stopScan() async {
    await FlutterBluePlus.stopScan();
  }

  Future<void> connect(BluetoothDevice device) async {
    print(
      "DEBUG: Attempting to connect with autoConnect: false, mtu: null on device ${device.remoteId} ${device.advName}",
    );

    try {
      await device.connect(
        timeout: const Duration(seconds: 10),
        autoConnect: false,
        license: License.free,
      );

      _connectedDevice = device;
      _lastDeviceId = device.remoteId.toString();

      _connectionSubscription?.cancel();
      _connectionSubscription = device.connectionState.listen((state) {
        _connectionStateController.add(state);
        if (state == BluetoothConnectionState.disconnected) {
          print("Device disconnected");
          _updateRobotStatus(RobotStatus.disconnected);
          _connectedDevice = null;
          _commandCharacteristic = null;
          _notifyCharacteristic = null;
          
          // Tentative de reconnexion automatique
          if (_autoReconnect && _lastDeviceId != null) {
            _attemptReconnection();
          }
        } else if (state == BluetoothConnectionState.connected) {
          _updateRobotStatus(RobotStatus.connected);
        }
      });

      // Wait for connection to stabilize
      await Future.delayed(const Duration(milliseconds: 1000));

      await _discoverServices(device);
      _updateRobotStatus(RobotStatus.connected);
      
      _addMessage("Connecté au robot: ${device.advName}");
    } catch (e) {
      print("Error connecting: $e");
      _addMessage("Erreur de connexion: $e");
      _updateRobotStatus(RobotStatus.disconnected);
      rethrow;
    }
  }
  
  Future<void> _attemptReconnection() async {
    if (_lastDeviceId == null || !_autoReconnect) return;
    
    _addMessage("Tentative de reconnexion...");
    
    await Future.delayed(const Duration(seconds: 2));
    
    try {
      // Chercher l'appareil précédemment connecté
      await FlutterBluePlus.startScan(timeout: const Duration(seconds: 5));
      
      await for (var results in FlutterBluePlus.scanResults) {
        for (var result in results) {
          if (result.device.remoteId.toString() == _lastDeviceId) {
            await FlutterBluePlus.stopScan();
            await connect(result.device);
            return;
          }
        }
      }
    } catch (e) {
      print("Reconnection failed: $e");
      _addMessage("Reconnexion échouée: $e");
    }
  }
  
  void setAutoReconnect(bool value) {
    _autoReconnect = value;
  }

  Future<void> disconnect() async {
    _autoReconnect = false; // Désactiver la reconnexion auto lors d'une déconnexion manuelle
    if (_connectedDevice != null) {
      await _connectedDevice!.disconnect();
      _connectedDevice = null;
      _commandCharacteristic = null;
      _notifyCharacteristic = null;
      _updateRobotStatus(RobotStatus.disconnected);
      _addMessage("Déconnecté du robot");
    }
  }
  
  void _updateRobotStatus(RobotStatus status) {
    _currentRobotStatus = status;
    _robotStatusController.add(status);
  }
  
  void _addMessage(String message) {
    final robotMessage = RobotMessage(message, DateTime.now());
    _messageHistory.add(robotMessage);
    _robotMessagesController.add(robotMessage);
    
    // Limiter l'historique à 50 messages
    if (_messageHistory.length > 50) {
      _messageHistory.removeAt(0);
    }
  }

  Future<void> _discoverServices(BluetoothDevice device) async {
    print("Starting service discovery for ${device.remoteId}...");
    try {
      List<BluetoothService> services = await device.discoverServices();
      print("Discovered ${services.length} services");
      for (var service in services) {
        print("Service found: ${service.uuid}");
        if (service.uuid.toString().toUpperCase() ==
            AppConstants.BOT_SERVICE_UUID.toUpperCase()) {
          for (var characteristic in service.characteristics) {
            print("Characteristic found: ${characteristic.uuid}");
            if (characteristic.uuid.toString().toUpperCase() ==
                AppConstants.BOT_CHARACTERISTIC_UUID.toUpperCase()) {
              print(
                "Properties: write=${characteristic.properties.write}, writeWithoutResponse=${characteristic.properties.writeWithoutResponse}",
              );

              // Only set if it supports writing
              if (characteristic.properties.write ||
                  characteristic.properties.writeWithoutResponse) {
                _commandCharacteristic = characteristic;
                print(
                  "Target Characteristic found and set: ${characteristic.uuid}",
                );
              } else {
                print(
                  "Characteristic matches UUID but does not support write. Ignoring.",
                );
              }
              
              // Configuration des notifications si supportées
              if (characteristic.properties.notify || characteristic.properties.indicate) {
                _notifyCharacteristic = characteristic;
                await _setupNotifications(characteristic);
              }
            }
          }
        }
      }
    } catch (e) {
      print("Error discovering services: $e");
      _addMessage("Erreur lors de la découverte des services: $e");
    }
  }
  
  Future<void> _setupNotifications(BluetoothCharacteristic characteristic) async {
    try {
      await characteristic.setNotifyValue(true);
      _notificationSubscription?.cancel();
      _notificationSubscription = characteristic.lastValueStream.listen((value) {
        if (value.isNotEmpty) {
          _handleNotification(value);
        }
      });
      print("Notifications enabled for ${characteristic.uuid}");
      _addMessage("Notifications activées");
    } catch (e) {
      print("Error setting up notifications: $e");
    }
  }
  
  void _handleNotification(List<int> value) {
    try {
      String message = utf8.decode(value);
      print("Received notification: $message");
      _addMessage("Robot: $message");
      
      // Parser le message pour mettre à jour l'état
      _parseRobotMessage(message);
    } catch (e) {
      print("Error decoding notification: $e");
    }
  }
  
  void _parseRobotMessage(String message) {
    final lowerMessage = message.toLowerCase();
    
    // Mise à jour du statut selon le message
    if (lowerMessage.contains('moving') || lowerMessage.contains('mouvement')) {
      _updateRobotStatus(RobotStatus.moving);
    } else if (lowerMessage.contains('mission') || lowerMessage.contains('autonome')) {
      _updateRobotStatus(RobotStatus.inMission);
    } else if (lowerMessage.contains('stop') || lowerMessage.contains('arrêt') || lowerMessage.contains('idle')) {
      _updateRobotStatus(RobotStatus.connected);
    }
    
    // Parser l'angle du servo si présent (format: "servo:90" ou "angle:90")
    final servoMatch = RegExp(r'(?:servo|angle)[:\s]*(\d+)').firstMatch(lowerMessage);
    if (servoMatch != null) {
      final angle = int.tryParse(servoMatch.group(1) ?? '');
      if (angle != null) {
        _currentServoAngle = angle;
        _servoAngleController.add(angle);
      }
    }
  }

  Future<void> sendCommand(String command, [dynamic parameter]) async {
    if (_connectedDevice == null) {
      print("Cannot send command: Device not connected");
      _addMessage("Erreur: Appareil non connecté");
      return;
    }

    if (_commandCharacteristic == null) {
      print("Command characteristic not found. Attempting to rediscover...");
      await _discoverServices(_connectedDevice!);
      if (_commandCharacteristic == null) {
        print("Command characteristic still not found.");
        _addMessage("Erreur: Caractéristique de commande introuvable");
        return;
      }
    }

    String fullCommand = command;
    if (parameter != null) {
      fullCommand += ':$parameter';
    }
    List<int> bytes = utf8.encode(fullCommand);

    // Check if the characteristic supports writeWithoutResponse
    bool canWriteWithoutResponse =
        _commandCharacteristic!.properties.writeWithoutResponse;

    try {
      await _commandCharacteristic!.write(
        bytes,
        withoutResponse: canWriteWithoutResponse,
      );
      _addMessage("Commande envoyée: $fullCommand");
      
      // Mise à jour du statut selon la commande
      if (command == 'stop') {
        _updateRobotStatus(RobotStatus.connected);
      } else if (command == 'auto_on') {
        _updateRobotStatus(RobotStatus.inMission);
      } else if (['avancer', 'reculer', 'gauche', 'droite'].contains(command)) {
        _updateRobotStatus(RobotStatus.moving);
      }
    } catch (e) {
      print("Error sending command: $e");
      _addMessage("Erreur d'envoi: $e");
    }
  }
  
  /// Envoyer une commande pour l'angle du servo
  Future<void> setServoAngle(int angle) async {
    if (angle < 0 || angle > 180) {
      _addMessage("Erreur: Angle invalide (0-180)");
      return;
    }
    await sendCommand('servo', angle);
    _currentServoAngle = angle;
    _servoAngleController.add(angle);
  }
  
  /// Nettoyer les ressources
  void dispose() {
    _connectionSubscription?.cancel();
    _notificationSubscription?.cancel();
    _connectionStateController.close();
    _robotStatusController.close();
    _robotMessagesController.close();
    _servoAngleController.close();
  }
  
  /// Effacer l'historique des messages
  void clearMessageHistory() {
    _messageHistory.clear();
  }
}
