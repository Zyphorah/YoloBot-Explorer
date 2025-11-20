import 'dart:io'; // Add this import

import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import 'package:permission_handler/permission_handler.dart'; // Nécessaire pour les permissions

import '../services/ble_service.dart';
import 'manual_command.dart';

class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key});

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  final BleService _ble = BleService();

  Future<void> _handleScan() async {
    // Seulement sur Android et iOS
    if (Platform.isAndroid || Platform.isIOS) {
      Map<Permission, PermissionStatus> statuses = await [
        Permission.bluetoothScan,
        Permission.bluetoothConnect,
        Permission.location,
      ].request();

      bool isGranted =
          statuses[Permission.bluetoothScan]!.isGranted &&
          statuses[Permission.bluetoothConnect]!.isGranted;

      if (isGranted) {
        _ble.startScan();
      } else {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("Permissions Bluetooth requises pour scanner."),
              backgroundColor: Colors.red,
            ),
          );
          openAppSettings();
        }
      }
    } else {
      _ble.startScan();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Recherche du Robot")),
      body: Column(
        children: [
          const SizedBox(height: 20),
          ElevatedButton.icon(
            icon: const Icon(Icons.bluetooth_searching),
            label: const Text("Lancer le Scan"),
            onPressed: _handleScan,
          ),
          const SizedBox(height: 10),
          Expanded(
            child: StreamBuilder<List<ScanResult>>(
              stream: _ble.scanResults,
              builder: (context, snapshot) {
                if (!snapshot.hasData) {
                  return const Center(
                    child: Text(
                      "Aucun appareil trouvé.\nAssurez-vous que le robot est allumé.",
                    ),
                  );
                }

                // Filtrer pour ne garder que les appareils avec un nom
                final results = snapshot.data!
                    .where((r) => r.device.platformName.isNotEmpty)
                    .toList();

                if (results.isEmpty) {
                  return const Center(
                    child: Text(
                      "Aucun appareil nommé trouvé.\n(Les appareils inconnus sont masqués)",
                      textAlign: TextAlign.center,
                    ),
                  );
                }

                return ListView.builder(
                  itemCount: results.length,
                  itemBuilder: (context, index) {
                    final result = results[index];
                    final deviceName = result.device.platformName;

                    return Card(
                      margin: const EdgeInsets.symmetric(
                        horizontal: 10,
                        vertical: 5,
                      ),
                      child: ListTile(
                        leading: const Icon(Icons.bluetooth),
                        title: Text(deviceName),
                        subtitle: Text(result.device.remoteId.toString()),
                        trailing: ElevatedButton(
                          child: const Text("Connecter"),
                          onPressed: () async {
                            await _ble.connect(result.device);
                            if (mounted) {
                              ScaffoldMessenger.of(context).showSnackBar(
                                SnackBar(
                                  content: Text("Connecté à $deviceName (v3)"),
                                ),
                              );
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => const ManualCommand(),
                                ),
                              );
                            }
                          },
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
