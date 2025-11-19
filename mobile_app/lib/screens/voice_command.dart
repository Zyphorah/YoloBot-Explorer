import 'package:flutter/material.dart';

class VoiceCommand extends StatefulWidget {
  const VoiceCommand({super.key});

  @override
  State<VoiceCommand> createState() => _VoiceCommandState();
}

class _VoiceCommandState extends State<VoiceCommand> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Commandes vocales'),
      ),
      body: const Center(
        child: Text('Interface de commandes vocales à implémenter'),
      ),
    );
  }
}

