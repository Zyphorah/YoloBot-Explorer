import 'package:flutter/material.dart';

class VoiceCommand extends StatefulWidget {
  const VoiceCommand({super.key});

  @override
  State<VoiceCommand> createState() => _VoiceCommandState();
}

class _VoiceCommandState extends State<VoiceCommand> {
  bool isActivated = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Commandes vocales'),
      ),
      body: Center(
        child: GestureDetector(
          onTap: () {
            setState(() {
              isActivated = !isActivated;
            });
          },
          child: Container(
            width: 120,
            height: 120,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: isActivated ? Colors.red : Colors.grey,
            ),
            child: Icon(
              isActivated ? Icons.mic : Icons.mic_none,
              size: 60,
              color: Colors.white,
            ),
          ),
        ),
      ),
    );
  }
}

