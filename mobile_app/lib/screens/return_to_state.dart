import 'package:flutter/material.dart';

class ReturnToState extends StatelessWidget {
  final VoidCallback returnToPreviousState;

  const ReturnToState({required this.returnToPreviousState, super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Retour à l\'état précédent'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: returnToPreviousState,
          child: const Text('Retourner'),
        ),
      ),
    );
  }
}

