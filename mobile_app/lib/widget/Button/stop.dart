import 'package:flutter/material.dart';

class Stop extends StatefulWidget {
  final bool initialStopping;
  const Stop({Key? key, this.initialStopping = false}) : super(key: key);

  @override
  State<Stop> createState() => _StopState();
}

class _StopState extends State<Stop> {
  late bool isStopping;

  @override
  void initState() {
    super.initState();
    isStopping = widget.initialStopping;
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: GestureDetector(
        onTapDown: (_) {
          setState(() => isStopping = true);
        },
        onTapUp: (_) {
          setState(() => isStopping = false);
        },
        child: Container(
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            gradient: LinearGradient(
              colors: isStopping
                  ? [Color(0xFFff0000), Color(0xFFcc0000)]
                  : [Color.fromARGB(255, 184, 0, 0), Color.fromARGB(255, 153, 0, 0)],
            ),
          ),
          width: 120,
          height: 120,
          child: Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: const [
                Icon(Icons.stop_circle, color: Colors.white, size: 40),
                Text(
                  'Stop',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 12,
                    letterSpacing: 1,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

