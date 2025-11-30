import 'dart:async';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart';

import '../services/ble_service.dart';

class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key});

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  final BleService _ble = BleService();
  bool _isScanning = false;
  bool _isConnecting = false;
  String? _connectingDeviceId;

  Future<void> _handleScan() async {
    if (Platform.isAndroid || Platform.isIOS) {
      Map<Permission, PermissionStatus> statuses = await [
        Permission.bluetoothScan,
        Permission.bluetoothConnect,
        Permission.location,
      ].request();

      bool isGranted = statuses[Permission.bluetoothScan]!.isGranted &&
          statuses[Permission.bluetoothConnect]!.isGranted;

      if (isGranted) {
        setState(() => _isScanning = true);
        await _ble.startScan();
        Future.delayed(const Duration(seconds: 15), () {
          if (mounted) setState(() => _isScanning = false);
        });
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(content: Text("Permissions Bluetooth requises."), backgroundColor: Colors.red),
          );
          openAppSettings();
        }
      }
    } else {
      setState(() => _isScanning = true);
      await _ble.startScan();
      Future.delayed(const Duration(seconds: 15), () {
        if (mounted) setState(() => _isScanning = false);
      });
    }
  }

  Future<void> _handleStopScan() async {
    await _ble.stopScan();
    setState(() => _isScanning = false);
  }

  Future<void> _connectToDevice(BluetoothDevice device) async {
    setState(() {
      _isConnecting = true;
      _connectingDeviceId = device.remoteId.toString();
    });

    try {
      await _ble.connect(device);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Connecté à ${device.platformName}"), backgroundColor: Colors.green),
        );
        Navigator.pop(context);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text("Erreur: $e"), backgroundColor: Colors.red),
        );
      }
    } finally {
      if (mounted) {
        setState(() {
          _isConnecting = false;
          _connectingDeviceId = null;
        });
      }
    }
  }

  Future<void> _disconnectDevice() async {
    await _ble.disconnect();
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Déconnecté"), backgroundColor: Colors.orange),
      );
      setState(() {});
    }
  }

  @override
  Widget build(BuildContext context) {
    final isConnected = _ble.isConnected;
    final connectedDevice = _ble.connectedDevice;

    return Scaffold(
      appBar: AppBar(
        title: const Text("Connexion BLE"),
        actions: [
          if (isConnected)
            IconButton(
              icon: const Icon(Icons.bluetooth_disabled),
              onPressed: _disconnectDevice,
            ),
        ],
      ),
      body: Column(
        children: [
          // Appareil connecté
          if (isConnected && connectedDevice != null)
            Card(
              margin: const EdgeInsets.all(16),
              color: Colors.green[50],
              child: ListTile(
                leading: const Icon(Icons.bluetooth_connected, color: Colors.green),
                title: Text(connectedDevice.platformName.isNotEmpty ? connectedDevice.platformName : 'Robot'),
                subtitle: Text(connectedDevice.remoteId.toString()),
                trailing: TextButton(
                  onPressed: _disconnectDevice,
                  child: const Text('Déconnecter'),
                ),
              ),
            ),

          // Bouton scan
          Padding(
            padding: const EdgeInsets.all(16),
            child: ElevatedButton.icon(
              icon: _isScanning
                  ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                  : const Icon(Icons.bluetooth_searching),
              label: Text(_isScanning ? "Arrêter" : "Lancer le Scan"),
              onPressed: _isScanning ? _handleStopScan : _handleScan,
            ),
          ),

          // Liste des appareils
          Expanded(
            child: StreamBuilder<List<ScanResult>>(
              stream: _ble.scanResults,
              builder: (context, snapshot) {
                if (!snapshot.hasData || snapshot.data!.isEmpty) {
                  return Center(
                    child: Text(
                      _isScanning ? "Recherche..." : "Aucun appareil trouvé.\nAppuyez sur 'Lancer le Scan'.",
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: Colors.grey),
                    ),
                  );
                }

                final results = snapshot.data!
                    .where((r) => r.device.platformName.isNotEmpty)
                    .toList()
                  ..sort((a, b) => b.rssi.compareTo(a.rssi));

                if (results.isEmpty) {
                  return const Center(
                    child: Text("Aucun appareil nommé trouvé.", style: TextStyle(color: Colors.grey)),
                  );
                }

                return ListView.builder(
                  padding: const EdgeInsets.symmetric(horizontal: 16),
                  itemCount: results.length,
                  itemBuilder: (context, index) {
                    final result = results[index];
                    final deviceName = result.device.platformName;
                    final deviceId = result.device.remoteId.toString();
                    final isCurrentlyConnecting = _connectingDeviceId == deviceId;
                    final isThisDeviceConnected = connectedDevice?.remoteId.toString() == deviceId;

                    return Card(
                      margin: const EdgeInsets.symmetric(vertical: 4),
                      child: ListTile(
                        leading: Icon(
                          Icons.bluetooth,
                          color: isThisDeviceConnected ? Colors.green : Colors.grey,
                        ),
                        title: Text(deviceName),
                        subtitle: Text('$deviceId (${result.rssi} dBm)'),
                        trailing: isThisDeviceConnected
                            ? const Text('Connecté', style: TextStyle(color: Colors.green))
                            : ElevatedButton(
                                onPressed: _isConnecting ? null : () => _connectToDevice(result.device),
                                child: isCurrentlyConnecting
                                    ? const SizedBox(width: 16, height: 16, child: CircularProgressIndicator(strokeWidth: 2))
                                    : const Text("Connecter"),
                              ),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
