import 'dart:async';
import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

class VoiceCommand extends StatefulWidget {
  const VoiceCommand({super.key});

  @override
  State<VoiceCommand> createState() => _VoiceCommandState();
}

class _VoiceCommandState extends State<VoiceCommand> {
  late stt.SpeechToText _speech;
  bool _isListening = false;
  String _text = 'Appuyer pour activer la reconnaissance vocale';
  double _confidence = 1.0;
  bool _initialized = false;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _speech = stt.SpeechToText();
    _initSpeech();
  }
  
    @override
    void dispose() {
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
            _errorMessage = 'La reconnaissance vocale n\'est pas disponible sur cet appareil.';
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

  Future<void> _listen() async {
    if (!_initialized) {
      await _initSpeech();
      if (!_initialized) return;
    }

    if (!_isListening) {
      bool available = await _speech.initialize();
      if (available) {
        setState(() {
          _isListening = true;
          _errorMessage = null;
        });
        _speech.listen(
          onResult: (val) => setState(() {
            _text = val.recognizedWords;
            if (val.hasConfidenceRating && val.confidence > 0) {
              _confidence = val.confidence;
            }
          }),
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
    return Scaffold(
      appBar: AppBar(
        title: const Text('Commandes vocales'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const SizedBox(height: 24),
            Expanded(
              child: Center(
                child: GestureDetector(
                  onTap: _errorMessage == null ? _listen : null,
                  child: Container(
                    width: 140,
                    height: 140,
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      color: _errorMessage != null 
                        ? Colors.orange 
                        : (_isListening ? Colors.red : Colors.grey),
                      boxShadow: _isListening ? [
                        BoxShadow(
                          color: Colors.red.withOpacity(0.5),
                          blurRadius: 20,
                          spreadRadius: 5,
                        )
                      ] : [],
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
            const SizedBox(height: 20),
            Text(
              _errorMessage ?? _text,
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.w500,
                color: _errorMessage != null ? Colors.red : Colors.black87,
              ),
            ),
            const SizedBox(height: 8),
            if (_errorMessage == null && _text.isNotEmpty && _text != 'Appuyer pour activer la reconnaissance vocale')
              Text(
                'Confiance: ${(_confidence * 100.0).toStringAsFixed(1)}%',
                style: const TextStyle(fontSize: 12, color: Colors.grey),
              ),
            const Spacer(),
            Text(
              _errorMessage != null 
                ? 'Erreur détectée'
                : (_initialized ? 'Module vocal prêt' : 'Initialisation...'),
              style: const TextStyle(fontSize: 12, color: Colors.blueGrey),
            ),
            const SizedBox(height: 8),
          ],
        ),
      ),
    );
  }
}

