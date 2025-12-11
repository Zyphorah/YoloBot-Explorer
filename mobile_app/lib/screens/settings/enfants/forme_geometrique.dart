import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

import '../../../services/ble_service.dart';
import '../../../widget/settings/settings_option.dart';

class FormeGeometrique extends StatefulWidget {
  const FormeGeometrique({super.key});

  @override
  State<FormeGeometrique> createState() => _FormeGeometriqueState();
}

class _FormeGeometriqueState extends State<FormeGeometrique> {
  final BleService _bleService = BleService();
  final storage = FlutterSecureStorage();

  String? selectedOption;
  String? selectionColor;

  selectedOptionInit() async {
    String? shape = await storage.read(key: 'selected_shape');
    setState(() {
      if (shape == 'square') {
        selectedOption = 'Carré';
      } else if (shape == 'circle') {
        selectedOption = 'Cercle';
      } else if (shape == 'triangle') {
        selectedOption = 'Triangle';
      }
    });
  }

  selectionColorInit() async {
    String? color = await storage.read(key: 'selected_color');
    setState(() {
      if (color == 'rouge') {
        selectionColor = 'Rouge';
      } else if (color == 'vert') {
        selectionColor = 'Vert';
      } else if (color == 'bleu') {
        selectionColor = 'Bleu';
      }
    });
  }

  /// Envoie la commande set_target avec la forme et la couleur actuelles
  void _sendTargetCommand() async {
    String? shape = await storage.read(key: 'selected_shape');
    String? color = await storage.read(key: 'selected_color');

    if (shape != null && color != null) {
      // Envoie forme + couleur: set_target:shape:color
      _bleService.sendCommand('set_target', '$shape:$color');
    } else if (shape != null) {
      // Envoie seulement la forme: set_target:shape
      _bleService.sendCommand('set_target', shape);
    } else if (color != null) {
      // Seulement la couleur: set_color:color
      _bleService.sendCommand('set_color', color);
    }
  }

  @override
  void initState() {
    super.initState();
    selectedOptionInit();
    selectionColorInit();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Paramètres')),
      body: Column(
        children: [
          SettingsOption(
            title: 'Carré',
            icon: Icons.crop_square,
            isSelected: selectedOption == 'Carré',
            onTap: () {
              setState(() {
                selectedOption = selectedOption == 'Carré' ? null : 'Carré';
              });
              if (selectedOption == 'Carré') {
                storage.write(key: 'selected_shape', value: 'square');
                storage.delete(key: 'custom_object');
                _sendTargetCommand();
              } else {
                storage.delete(key: 'selected_shape');
              }
            },
          ),
          SettingsOption(
            title: 'Cercle',
            icon: Icons.sports_soccer,
            isSelected: selectedOption == 'Cercle',
            onTap: () {
              setState(() {
                selectedOption = selectedOption == 'Cercle' ? null : 'Cercle';
              });
              if (selectedOption == 'Cercle') {
                storage.write(key: 'selected_shape', value: 'circle');
                storage.delete(key: 'custom_object');
                _sendTargetCommand();
              } else {
                storage.delete(key: 'selected_shape');
              }
            },
          ),
          SettingsOption(
            title: 'Triangle',
            icon: Icons.change_history,
            isSelected: selectedOption == 'Triangle',
            onTap: () {
              setState(() {
                selectedOption = selectedOption == 'Triangle'
                    ? null
                    : 'Triangle';
              });
              if (selectedOption == 'Triangle') {
                storage.write(key: 'selected_shape', value: 'triangle');
                storage.delete(key: 'custom_object');
                _sendTargetCommand();
              } else {
                storage.delete(key: 'selected_shape');
              }
            },
          ),
          // Gestion des couleurs
          const Padding(
            padding: EdgeInsets.symmetric(vertical: 16.0),
            child: Text(
              'Selectionner une couleur',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
          ),
          SettingsOption(
            title: 'Rouge',
            icon: Icons.circle,
            isSelected: selectionColor == 'Rouge',
            onTap: () {
              setState(() {
                selectionColor = selectionColor == 'Rouge' ? null : 'Rouge';
              });
              if (selectionColor == 'Rouge') {
                storage.write(key: 'selected_color', value: 'rouge');
                storage.delete(key: 'custom_object');
                _sendTargetCommand();
              } else {
                storage.delete(key: 'selected_color');
              }
            },
          ),
          SettingsOption(
            title: 'Vert',
            icon: Icons.circle,
            isSelected: selectionColor == 'Vert',
            onTap: () {
              setState(() {
                selectionColor = selectionColor == 'Vert' ? null : 'Vert';
              });
              if (selectionColor == 'Vert') {
                storage.write(key: 'selected_color', value: 'vert');
                storage.delete(key: 'custom_object');
                _sendTargetCommand();
              } else {
                storage.delete(key: 'selected_color');
              }
            },
          ),
          SettingsOption(
            title: 'Bleu',
            icon: Icons.circle,
            isSelected: selectionColor == 'Bleu',
            onTap: () {
              setState(() {
                selectionColor = selectionColor == 'Bleu' ? null : 'Bleu';
              });
              if (selectionColor == 'Bleu') {
                storage.write(key: 'selected_color', value: 'bleu');
                storage.delete(key: 'custom_object');
                _sendTargetCommand();
              } else {
                storage.delete(key: 'selected_color');
              }
            },
          ),
        ],
      ),
    );
  }
}
