import 'package:flutter/material.dart';

class SettingsScreen extends StatelessWidget {  
  const SettingsScreen({super.key});  

  @override  
  Widget build(BuildContext context) {  
    return Scaffold(  
      appBar: AppBar(  
        title: const Text('Paramètres'),  
      ),  
      body: const Center(  
        child: Text('Écran des paramètres'),  
      ),  
    );  
  }  
}

class SettingsOption extends StatelessWidget {
  final String title;
  final IconData icon;
  final VoidCallback onTap;

  const SettingsOption({
    required this.title,
    required this.icon,
    required this.onTap,
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon),
      title: Text(title),
      trailing: const Icon(Icons.arrow_forward_ios),
      onTap: onTap,
    );
  }
}