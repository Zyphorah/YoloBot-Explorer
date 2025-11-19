import 'dart:async';
import 'dart:convert';

import 'package:flutter_blue_plus/flutter_blue_plus.dart';

class BleService {
  // --- Singleton Pattern (Instance unique) ---
  static final BleService _instance = BleService._internal();
  factory BleService() => _instance;
  BleService._internal();

  // --- UUIDs ---
  final String _serviceUuid = "A07498CA-AD5B-474E-940D-16F1FBE7E8CD";
  final String _charRxUuid = "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B"; // Envoi
  final String _charTxUuid =
      "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021C"; // Réception

  BluetoothDevice? _connectedDevice;
  BluetoothCharacteristic? _rxCharacteristic; // Pour écrire
  BluetoothCharacteristic? _txCharacteristic; // Pour écouter

  // Streams pour mettre à jour l'UI
  final _scanResultsController = StreamController<List<ScanResult>>.broadcast();
  final _statusController =
      StreamController<String>.broadcast(); // Messages du robot
  final _connectionStateController =
      StreamController<BluetoothConnectionState>.broadcast();

  // Getters pour l'UI
  Stream<List<ScanResult>> get scanResults => _scanResultsController.stream;
  Stream<String> get statusStream => _statusController.stream;
  Stream<BluetoothConnectionState> get connectionState =>
      _connectionStateController.stream;
  BluetoothDevice? get currentDevice => _connectedDevice;

  /// Initialisation (optionnel, pour log ou setup)
  void init() {
    FlutterBluePlus.adapterState.listen((state) {
      print("État adaptateur Bluetooth: $state");
    });
  }

  Future<void> startScan() async {
    print("Démarrage du scan...");

    FlutterBluePlus.scanResults.listen((results) {
      _scanResultsController.add(results);
    });

    await FlutterBluePlus.startScan(
      timeout: const Duration(seconds: 5),
      withServices: [Guid(_serviceUuid)],
    );
  }

  Future<void> stopScan() async {
    await FlutterBluePlus.stopScan();
  }

  Future<void> connect(BluetoothDevice device) async {
    await stopScan();

    try {
      await device.connect(autoConnect: true, license: License.free);
      _connectedDevice = device;

      device.connectionState.listen((state) {
        _connectionStateController.add(state);
        if (state == BluetoothConnectionState.disconnected) {
          print("Robot déconnecté");
          _cleanUp();
        }
      });

      print("Recherche des services...");
      List<BluetoothService> services = await device.discoverServices();

      for (var service in services) {
        if (service.uuid.toString().toUpperCase() == _serviceUuid) {
          print("Service robot trouvé !");

          for (var char in service.characteristics) {
            String uuid = char.uuid.toString().toUpperCase();

            // Configuration RX (Écriture)
            if (uuid == _charRxUuid) {
              _rxCharacteristic = char;
              print("Caractéristique RX liée.");
            }

            // Configuration TX (Lecture/Notification)
            if (uuid == _charTxUuid) {
              _txCharacteristic = char;
              print("Caractéristique TX liée.");

              // Activer les notifications pour recevoir les réponses du robot
              await char.setNotifyValue(true);
              char.lastValueStream.listen((value) {
                String message = utf8.decode(value);
                print("Reçu du robot: $message");
                _statusController.add(message);
              });
            }
          }
        }
      }
    } catch (e) {
      print("Erreur de connexion : $e");
      _cleanUp();
      rethrow;
    }
  }

  Future<void> disconnect() async {
    if (_connectedDevice != null) {
      await _connectedDevice!.disconnect();
      _cleanUp();
    }
  }

  Future<void> sendCommand(String command) async {
    if (_rxCharacteristic == null) {
      print("Erreur: Non connecté ou caractéristique RX introuvable.");
      return;
    }

    try {
      List<int> bytes = utf8.encode(command);
      // Écriture sans réponse (plus rapide pour le contrôle temps réel)
      await _rxCharacteristic!.write(bytes, withoutResponse: true);
      print("Commande envoyée: $command");
    } catch (e) {
      print("Erreur d'envoi: $e");
    }
  }

  void _cleanUp() {
    _connectedDevice = null;
    _rxCharacteristic = null;
    _txCharacteristic = null;
  }
}
