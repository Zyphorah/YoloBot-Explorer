import 'dart:async';
import 'dart:convert';

import 'package:flutter_blue_plus/flutter_blue_plus.dart';

import '../utils/constants.dart';

class BleService {
  static final BleService _instance = BleService._internal();

  factory BleService() {
    return _instance;
  }

  BleService._internal();

  BluetoothDevice? _connectedDevice;
  BluetoothCharacteristic? _commandCharacteristic;

  // Stream for scan results
  Stream<List<ScanResult>> get scanResults => FlutterBluePlus.scanResults;

  // Stream for connection state
  final _connectionStateController =
      StreamController<BluetoothConnectionState>.broadcast();
  Stream<BluetoothConnectionState> get connectionState =>
      _connectionStateController.stream;

  BluetoothDevice? get connectedDevice => _connectedDevice;

  Future<void> startScan() async {
    await FlutterBluePlus.startScan(timeout: const Duration(seconds: 15));
  }

  Future<void> stopScan() async {
    await FlutterBluePlus.stopScan();
  }

  Future<void> connect(BluetoothDevice device) async {
    print(
      "DEBUG: Attempting to connect with autoConnect: false, mtu: null on device ${device.remoteId} ${device.advName}",
    );

    await device.connect(
      timeout: const Duration(seconds: 10),
      autoConnect: false,
      //   mtu: null,
      license: License.free,
    );

    _connectedDevice = device;

    device.connectionState.listen((state) {
      _connectionStateController.add(state);
      if (state == BluetoothConnectionState.disconnected) {
        print("Device disconnected");
        _connectedDevice = null;
        _commandCharacteristic = null;
      }
    });

    // Wait for connection to stabilize
    await Future.delayed(const Duration(milliseconds: 1000));

    // await device.connectionState
    //     .where((val) => val == BluetoothConnectionState.connected)
    //     .first;

    // await device.requestMtu(512); // Replace 512 with your desired MTU size

    await _discoverServices(device);
  }

  Future<void> disconnect() async {
    if (_connectedDevice != null) {
      await _connectedDevice!.disconnect();
      _connectedDevice = null;
      _commandCharacteristic = null;
    }
  }

  Future<void> _discoverServices(BluetoothDevice device) async {
    print("Starting service discovery for ${device.remoteId}...");
    try {
      List<BluetoothService> services = await device.discoverServices();
      print("Discovered ${services.length} services");
      for (var service in services) {
        print("Service found: ${service.uuid}");
        if (service.uuid.toString().toUpperCase() ==
            AppConstants.BOT_SERVICE_UUID.toUpperCase()) {
          for (var characteristic in service.characteristics) {
            print("Characteristic found: ${characteristic.uuid}");
            if (characteristic.uuid.toString().toUpperCase() ==
                AppConstants.BOT_CHARACTERISTIC_UUID.toUpperCase()) {
              print(
                "Properties: write=${characteristic.properties.write}, writeWithoutResponse=${characteristic.properties.writeWithoutResponse}",
              );

              // Only set if it supports writing
              if (characteristic.properties.write ||
                  characteristic.properties.writeWithoutResponse) {
                _commandCharacteristic = characteristic;
                print(
                  "Target Characteristic found and set: ${characteristic.uuid}",
                );
              } else {
                print(
                  "Characteristic matches UUID but does not support write. Ignoring.",
                );
              }
            }
          }
        }
      }
    } catch (e) {
      print("Error discovering services: $e");
    }
  }

  Future<void> sendCommand(String command, [dynamic parameter]) async {
    if (_connectedDevice == null) {
      print("Cannot send command: Device not connected");
      return;
    }

    if (_commandCharacteristic == null) {
      print("Command characteristic not found. Attempting to rediscover...");
      await _discoverServices(_connectedDevice!);
      if (_commandCharacteristic == null) {
        print("Command characteristic still not found.");
        return;
      }
    }

    String fullCommand = command;
    if (parameter != null) {
      fullCommand += ':$parameter';
    }
    List<int> bytes = utf8.encode(fullCommand);

    // Check if the characteristic supports writeWithoutResponse
    bool canWriteWithoutResponse =
        _commandCharacteristic!.properties.writeWithoutResponse;

    try {
      await _commandCharacteristic!.write(
        bytes,
        withoutResponse: canWriteWithoutResponse,
      );
    } catch (e) {
      print("Error sending command: $e");
    }
  }
}
