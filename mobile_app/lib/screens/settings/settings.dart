import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:mobile_app/services/ble_service.dart';

import '../../widget/settings/settings_option.dart';
import 'enfants/forme_geometrique.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final storage = FlutterSecureStorage();
  String? selectedOption;
  final BleService _bleService = BleService();
  final TextEditingController _objectController = TextEditingController();

  selectedOptionInit() async {
    String? customObject = await storage.read(key: 'custom_object');
    setState(() {
      selectedOption = customObject;
    });
  }

  @override
  void initState() {
    super.initState();
    selectedOptionInit();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Paramètres')),
      body: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Text(
            'Options de détection d\'objets',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),

          Padding(
            padding: const EdgeInsets.symmetric(
              horizontal: 16.0,
              vertical: 8.0,
            ),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _objectController,
                    decoration: InputDecoration(
                      labelText: 'Objet personnalisé',
                      prefixIcon: Icon(Icons.local_drink),
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                IconButton(
                  icon: Icon(Icons.send),
                  tooltip: 'Envoyer',
                  onPressed: () async {
                    String value = _objectController.text.trim();
                    if (value.isNotEmpty) {
                      // Supprimer les éléments du storage
                      await storage.delete(key: 'selected_color');
                      await storage.delete(key: 'selected_shape');

                      setState(() {
                        selectedOption = value;
                      });
                      // Envoie set_target avec seulement la forme (pas de couleur pour objet personnalisé)
                      _bleService.sendCommand('set_target', value);
                      await storage.write(key: 'custom_object', value: value);
                      _objectController.clear();
                    }
                  },
                ),
              ],
            ),
          ),

          // Affichage de l'élément personnalisé
          if (selectedOption != null)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 16.0),
              child: Container(
                padding: const EdgeInsets.all(12.0),
                decoration: BoxDecoration(
                  color: Colors.blue.withOpacity(0.1),
                  border: Border.all(color: Colors.blue),
                  borderRadius: BorderRadius.circular(8.0),
                ),
                child: Text(
                  'Objet actuel : $selectedOption',
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w500,
                    color: Colors.blue,
                  ),
                ),
              ),
            ),

          const Text(
            'Forme géométrique',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),

          SettingsOption(
            title: 'Forme géométrique',
            icon: Icons.category,
            isSelected: selectedOption == 'Forme géométrique',
            onTap: () {
              setState(() {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const FormeGeometrique(),
                  ),
                );
              });
            },
          ),
        ],
      ),
    );
  }
}
