// Source du code https://pub.dev/packages/speech_to_text
import 'dart:async';
import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import '../services/ble_service.dart';

class VoiceCommand extends StatefulWidget {
  const VoiceCommand({super.key});

  @override
  State<VoiceCommand> createState() => _VoiceCommandState();
}

class _VoiceCommandState extends State<VoiceCommand> {
  final BleService _bleService = BleService();
  late stt.SpeechToText _speech;
  bool _isListening = false;
  String _text = 'Appuyer pour activer la reconnaissance vocale';
  double _confidence = 1.0;
  bool _initialized = false;
  String? _errorMessage;
  String? _lastCommand;
  Timer? _debounceTimer;

  static const List<Map<String, dynamic>> _availableCommands = [
    {'keywords': ['avancer', 'avance', 'en avant'], 'action': 'avancer'},
    {'keywords': ['reculer', 'recule', 'en arrière'], 'action': 'reculer'},
    {'keywords': ['gauche', 'à gauche'], 'action': 'gauche'},
    {'keywords': ['droite', 'à droite'], 'action': 'droite'},
    {'keywords': ['stop', 'arrête', 'arrete'], 'action': 'stop'},
    {'keywords': ['détecter', 'détection', 'scanner'], 'action': 'detect_on'},
    {'keywords': ['autonome', 'automatique', 'mission'], 'action': 'auto_on'},
    {'keywords': ['manuel', 'manuelle'], 'action': 'auto_off'},
  ];

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
    _initSpeech();
  }

  @override
  void dispose() {
    _debounceTimer?.cancel();
    _speech.stop();
    super.dispose();
  }

  Future<void> _initSpeech() async {
    try {
      bool available = await _speech.initialize(
        onStatus: (status) {
          if (status == 'done' || status == 'notListening') {
            if (mounted) setState(() => _isListening = false);
          }
        },
        onError: (errorNotification) {
          if (mounted) {
            setState(() {
              _errorMessage = 'Erreur: ${errorNotification.errorMsg}';
              _isListening = false;
            });
          }
        },
      );
      if (mounted) {
        setState(() {
          _initialized = available;
          if (!available) {
            _errorMessage = 'Reconnaissance vocale non disponible.';
          }
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _errorMessage = 'Erreur d\'initialisation: $e';
          _initialized = false;
        });
      }
    }
  }

  String? _processCommand(String text) {
    String command = text.toLowerCase();
    for (var cmdInfo in _availableCommands) {
      for (var keyword in cmdInfo['keywords'] as List<String>) {
        if (command.contains(keyword)) {
          return cmdInfo['action'] as String;
        }
      }
    }
    return null;
  }

  void _sendCommand(String action) {
    _debounceTimer?.cancel();
    _debounceTimer = Timer(const Duration(milliseconds: 500), () {
      if (_lastCommand != action) {
        _lastCommand = action;
        _bleService.sendCommand(action);
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Commande envoyée: $action'), backgroundColor: Colors.green),
          );
        }
        Future.delayed(const Duration(seconds: 2), () => _lastCommand = null);
      }
    });
  }

  Future<void> _listen() async {
    if (!_initialized) {
      await _initSpeech();
      if (!_initialized) return;
    }

    if (!_bleService.isConnected) {
      setState(() => _errorMessage = 'Robot non connecté.');
      return;
    }

    if (!_isListening) {
      bool available = await _speech.initialize();
      if (available) {
        setState(() {
          _isListening = true;
          _errorMessage = null;
          _text = 'Écoute en cours...';
        });
        _speech.listen(
          onResult: (val) {
            setState(() {
              _text = val.recognizedWords;
              if (val.hasConfidenceRating && val.confidence > 0) {
                _confidence = val.confidence;
              }
            });
            if (val.finalResult || val.confidence > 0.7) {
              final action = _processCommand(val.recognizedWords);
              if (action != null) {
                _sendCommand(action);
              } else if (val.finalResult && val.recognizedWords.isNotEmpty) {
                if (mounted) {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Non reconnue: "${val.recognizedWords}"'), backgroundColor: Colors.orange),
                  );
                }
              }
            }
          },
          localeId: 'fr_FR',
        );
      }
    } else {
      setState(() => _isListening = false);
      _speech.stop();
    }
  }

  @override
  Widget build(BuildContext context) {
    final isConnected = _bleService.isConnected;

    return Scaffold(
      appBar: AppBar(title: const Text('Commandes vocales')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Indicateur de connexion
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  isConnected ? Icons.bluetooth_connected : Icons.bluetooth_disabled,
                  color: isConnected ? Colors.green : Colors.red,
                ),
                const SizedBox(width: 8),
                Text(
                  isConnected ? 'Robot connecté' : 'Robot non connecté',
                  style: TextStyle(color: isConnected ? Colors.green : Colors.red),
                ),
              ],
            ),
            const SizedBox(height: 24),
            
            // Bouton micro
            Expanded(
              child: Center(
                child: GestureDetector(
                  onTap: isConnected ? _listen : null,
                  child: Container(
                    width: 140,
                    height: 140,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: !isConnected
                          ? Colors.grey
                          : (_isListening ? Colors.red : const Color(0xFF6C63FF)),
                    ),
                    child: Icon(
                      _isListening ? Icons.mic : Icons.mic_none,
                      size: 72,
                      color: Colors.white,
                    ),
                  ),
                ),
              ),
            ),
            
            // Texte reconnu
            const SizedBox(height: 20),
            Text(
              _errorMessage ?? _text,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 18,
                color: _errorMessage != null ? Colors.red : Colors.black87,
              ),
            ),
            if (_errorMessage == null && _text != 'Appuyer pour activer la reconnaissance vocale' && _text != 'Écoute en cours...')
              Text(
                'Confiance: ${(_confidence * 100.0).toStringAsFixed(1)}%',
                style: const TextStyle(fontSize: 12, color: Colors.grey),
              ),
            
            const SizedBox(height: 24),
            
            // Boutons rapides
            if (isConnected)
              Wrap(
                spacing: 8,
                runSpacing: 8,
                alignment: WrapAlignment.center,
                children: [
                  ElevatedButton(onPressed: () => _sendCommand('stop'), child: const Text('Stop')),
                  ElevatedButton(onPressed: () => _sendCommand('detect_on'), child: const Text('Détecter')),
                  ElevatedButton(onPressed: () => _sendCommand('auto_on'), child: const Text('Autonome')),
                ],
              ),
            
            const Spacer(),
            Text(
              _initialized ? 'Appuyez sur le micro pour parler' : 'Initialisation...',
              style: const TextStyle(fontSize: 12, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }
}
