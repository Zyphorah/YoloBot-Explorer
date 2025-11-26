import 'package:flutter/material.dart';
import '../../../widget/settings/settings_option.dart';
import '../../../../services/ble_service.dart';

class FormeGeometrique extends StatefulWidget {
  const FormeGeometrique({super.key});

  @override
  State<FormeGeometrique> createState() => _FormeGeometriqueState();
}

class _FormeGeometriqueState extends State<FormeGeometrique> {
  final BleService _bleService = BleService();
  String? selectedOption;
  String? selectionColor;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Paramètres')),
      body: Column(
        children: [
          SettingsOption(
            title: 'Personne',
            icon: Icons.person,
            isSelected: selectedOption == 'Personne',
            onTap: () {
              setState(() {
                selectedOption = 'Personne';
              });
              _bleService.sendCommand('set_object', 'person');
            },
          ),
          SettingsOption(
            title: 'Balle',
            icon: Icons.sports_soccer,
            isSelected: selectedOption == 'Balle',
            onTap: () {
              setState(() {
                selectedOption = 'Balle';
              });
              _bleService.sendCommand('set_object', 'sports ball');
            },
          ),
          SettingsOption(
            title: 'Bouteille',
            icon: Icons.local_drink,
            isSelected: selectedOption == 'Bouteille',
            onTap: () {
              setState(() {
                selectedOption = 'Bouteille';
              });
              _bleService.sendCommand('set_object', 'bottle');
            },
          ),

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
                selectionColor = 'Rouge';
              });
            },
          ),

          SettingsOption(
            title: 'Vert',
            icon: Icons.circle,
            isSelected: selectionColor == 'Vert',
            onTap: () {
              setState(() {
                selectionColor = 'Vert';
              });
            },
          ),

          SettingsOption(
            title: 'Bleu',
            icon: Icons.circle,
            isSelected: selectionColor == 'Bleu',
            onTap: () {
              setState(() {
                selectionColor = 'Bleu';
              });
            },
          ),
        ],
      ),
    );
  }
}
