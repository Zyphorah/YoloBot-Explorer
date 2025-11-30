import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../../../widget/settings/settings_option.dart';
import '../../../../services/ble_service.dart';

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
      if (color == 'red') {
        selectionColor = 'Rouge';
      } else if (color == 'green') {
        selectionColor = 'Vert';
      } else if (color == 'blue') {
        selectionColor = 'Bleu';
      }
    });
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
                _bleService.sendCommand('set_object', 'square');
                storage.write(key: 'selected_shape', value: 'square');
                storage.delete(key: 'custom_object');
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
                _bleService.sendCommand('set_object', 'circle');
                storage.write(key: 'selected_shape', value: 'circle');
                storage.delete(key: 'custom_object');
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
                selectedOption = selectedOption == 'Triangle' ? null : 'Triangle';
              });
              if (selectedOption == 'Triangle') {
                _bleService.sendCommand('set_object', 'triangle');
                storage.write(key: 'selected_shape', value: 'triangle');
                storage.delete(key: 'custom_object');
              } else {
                storage.delete(key: 'selected_shape');
              }
            },
          ),
 
          // Gestion des couleurs
          Text(
            'Selectionner une couleur',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
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
                storage.write(key: 'selected_color', value: 'red');
                storage.delete(key: 'custom_object');
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
                storage.write(key: 'selected_color', value: 'green');
                storage.delete(key: 'custom_object');
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
                storage.write(key: 'selected_color', value: 'blue');
                storage.delete(key: 'custom_object');
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
