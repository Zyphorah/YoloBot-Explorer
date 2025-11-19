import 'package:flutter/material.dart'; 
import '../../../widget/settings/settings_option.dart';  

class FormeGeometrique extends StatefulWidget
{
  const FormeGeometrique({super.key});

  @override
  State<FormeGeometrique> createState() => _FormeGeometriqueState();
}

class _FormeGeometriqueState extends State<FormeGeometrique>
{
  String? selectedOption;
  String? selectionColor;


  @override
  Widget build(BuildContext context) {
    return  
    Scaffold(  
      appBar: AppBar(  
        title: const Text('Paramètres'),  
      ),  
      body: Column(
        children: [
          SettingsOption(
              title: 'carré',
              icon: Icons.crop_square,
              isSelected: selectedOption == 'carré',
              onTap: () {
                setState(() {
                  selectedOption = 'carré';
                });
              },
            ),
            SettingsOption(
              title: 'cercle',
              icon: Icons.circle,
              isSelected: selectedOption == 'cercle',
              onTap: () {
                setState(() {
                  selectedOption = 'cercle';
                });
              },
            ),
            SettingsOption(
              title: 'Triangle',
              icon: Icons.change_history,
              isSelected: selectedOption == 'Triangle',
              onTap: () {
                setState(() {
                  selectedOption = 'Triangle';
                });
              },
            ),

            Text('Selectionner une couleur',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
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