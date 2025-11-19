import 'dart:async';
import 'dart:convert';

import 'package:flutter_blue_plus/flutter_blue_plus.dart';

class BleService {
  // --- Singleton Pattern (Instance unique) ---
  static final BleService _instance = BleService._internal();
  factory BleService() => _instance;
  BleService._internal();

  // --- UUIDs (DOIVENT MATCHER CEUX DU PYTHON) ---
  final String _serviceUuid = "A07498CA-AD5B-474E-940D-16F1FBE7E8CD";
  final String _charRxUuid = "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B"; // Envoi
  final String _charTxUuid =
      "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021C"; // Réception

  // --- Variables d'état ---
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
    // Écouteur global de l'état du Bluetooth (On/Off)
    FlutterBluePlus.adapterState.listen((state) {
      print("État adaptateur Bluetooth: $state");
    });
  }

  /// Lance le scan pour trouver le robot
  Future<void> startScan() async {
    print("Démarrage du scan...");

    // On écoute les résultats du scan
    FlutterBluePlus.scanResults.listen((results) {
      _scanResultsController.add(results);
    });

    // On lance le scan en filtrant par UUID pour ne trouver que NOTRE robot
    // Cela évite de lister les télés et écouteurs des voisins.
    await FlutterBluePlus.startScan(
      timeout: const Duration(seconds: 5),
      withServices: [Guid(_serviceUuid)],
    );
  }

  /// Arrête le scan
  Future<void> stopScan() async {
    await FlutterBluePlus.stopScan();
  }

  /// Connexion au robot
  Future<void> connect(BluetoothDevice device) async {
    await stopScan(); // Toujours arrêter le scan avant de connecter

    try {
      await device.connect(autoConnect: false, license: null);
      _connectedDevice = device;

      // Écouter l'état de connexion (connecté/déconnecté)
      device.connectionState.listen((state) {
        _connectionStateController.add(state);
        if (state == BluetoothConnectionState.disconnected) {
          print("Robot déconnecté");
          _cleanUp();
        }
      });

      // Découverte des services
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

  /// Déconnexion manuelle
  Future<void> disconnect() async {
    if (_connectedDevice != null) {
      await _connectedDevice!.disconnect();
      _cleanUp();
    }
  }

  /// Envoie une commande texte au robot
  Future<void> sendCommand(String command) async {
    if (_rxCharacteristic == null) {
      print("Erreur: Non connecté ou caractéristique RX introuvable.");
      return;
    }

    try {
      // Encodage en UTF-8
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
