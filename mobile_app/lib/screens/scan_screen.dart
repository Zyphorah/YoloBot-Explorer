import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';
import '../services/ble_service.dart';

class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key});

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  final BleService _ble = BleService();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Recherche du Robot")),
      body: Column(
        children: [
          ElevatedButton(
            onPressed: _ble.startScan,
            child: const Text("Scanner"),
          ),
          Expanded(
            child: StreamBuilder<List<ScanResult>>(
              stream: _ble.scanResults,
              builder: (context, snapshot) {
                if (!snapshot.hasData) return const Center(child: Text("Aucun robot trouvé"));
                
                final results = snapshot.data!;
                
                return ListView.builder(
                  itemCount: results.length,
                  itemBuilder: (context, index) {
                    final result = results[index];
                    return ListTile(
                      title: Text(result.device.platformName.isNotEmpty 
                          ? result.device.platformName 
                          : "Appareil inconnu"),
                      subtitle: Text(result.device.remoteId.toString()),
                      trailing: ElevatedButton(
                        child: const Text("Connecter"),
                        onPressed: () async {
                          await _ble.connect(result.device);
                          // Naviguer vers l'écran de contrôle après connexion
                          // Navigator.push(...);
                        },
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
