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
    // 1. Demander les permissions nécessaires (Android 12+ et Location pour les anciens)
    Map<Permission, PermissionStatus> statuses = await [
      Permission.bluetoothScan,
      Permission.bluetoothConnect,
      Permission.location,
    ].request();

    // 2. Vérifier si tout est accordé
    bool isGranted =
        statuses[Permission.bluetoothScan]!.isGranted &&
        statuses[Permission.bluetoothConnect]!.isGranted;

    if (isGranted) {
      // 3. Lancer le scan si autorisé
      _ble.startScan();
    } else {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Permissions Bluetooth requises pour scanner."),
            backgroundColor: Colors.red,
          ),
        );
        // Optionnel : Ouvrir les paramètres si l'utilisateur a refusé définitivement
        openAppSettings();
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Recherche du Robot (v4)")),
      body: Column(
        children: [
          const SizedBox(height: 20),
          ElevatedButton.icon(
            icon: const Icon(Icons.bluetooth_searching),
            label: const Text("Lancer le Scan"),
            onPressed: _handleScan, // Appel de la nouvelle fonction sécurisée
          ),
          const SizedBox(height: 10),
          Expanded(
            child: StreamBuilder<List<ScanResult>>(
              stream: _ble.scanResults,
              builder: (context, snapshot) {
                if (!snapshot.hasData || snapshot.data!.isEmpty) {
                  return const Center(
                    child: Text(
                      "Aucun appareil trouvé.\nAssurez-vous que le robot est allumé.",
                    ),
                    // textAlign: TextAlign.center,
                  );
                }

                final results = snapshot.data!;

                return ListView.builder(
                  itemCount: results.length,
                  itemBuilder: (context, index) {
                    final result = results[index];
                    final deviceName = result.device.platformName.isNotEmpty
                        ? result.device.platformName
                        : "Appareil inconnu (${result.device.remoteId})";

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
                              // Navigate to ManualCommand screen
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
