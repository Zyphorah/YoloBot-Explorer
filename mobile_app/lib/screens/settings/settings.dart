import 'package:flutter/material.dart';
import '../../widget/Settings/settings_option.dart';
import 'enfants/forme_geometrique.dart';

class SettingsScreen extends StatefulWidget {  
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  String? selectedOption;

  @override  
  Widget build(BuildContext context) {  
    return Scaffold(  
      appBar: AppBar(  
        title: const Text('Paramètres'),  
      ),  
      body: 
        Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'Options de détection d\'objets', 
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            SettingsOption(
              title: 'Personne',
              icon: Icons.face,
              isSelected: selectedOption == 'Personne',
              onTap: () {
                setState(() {
                  selectedOption = 'Personne';
                });
              },
            ),
            const Text('Forme géométrique',
              style: TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
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
