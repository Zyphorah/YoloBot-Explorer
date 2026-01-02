# Autonomous Robot with Mobile Interface

## Overview

Complete robotic system composed of a Raspberry Pi robot capable of detecting objects and navigating autonomously, controlled via a Flutter mobile application. The robot analyzes its environment, identifies obstacles, and executes received commands while validating safety conditions. In critical situations (collision, loss of vision), the robot stops immediately and reports the anomaly.

## Architecture

The system is divided into two components: a backend (robot_python) that handles YOLO vision, navigation, collisions, and Bluetooth communication, and a frontend (mobile_app) Flutter application providing manual controls, voice input, and target configuration. Communication is done over Bluetooth Low Energy with specific UUIDs.

## Bluetooth Configuration

Service UUID : A07498CA-AD5B-474E-940D-16F1FBE7E8CD
Commands : 51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B
Status : 2F8C4D2A-1D3B-4F5A-9C6E-7B8A9B0C1D2E

These identifiers must be identical on the robot and the mobile app. Pair the robot first via the system Bluetooth settings before use.

## Installation

### System dependencies (Linux/Debian)

```
sudo apt update
sudo apt install -y libcap-dev
sudo apt install libcairo2-dev pkg-config python3-dev libgirepository1.0-dev -y
```

### Installing libcamera

```
libcamera must be installed
```

### Python environment

```
uv venv --system-site-packages
```

### Python dependencies

```
uv pip uninstall numpy
uv pip install -r robot_python/requirements.txt
uv pip install bluezero
```

### Bluetooth dependencies

```
pip install bleak
```

### Flutter dependencies

```
cd mobile_app
flutter pub get
```

## Project structure

**robot_python** : Robot backend
- moteur : Servo drivers and DC motor drivers
- navigation : Movements, trajectories, collisions
- vision : Capture and YOLO analysis
- services : BLE service
- comportements : Autonomous, detection, scan modes
- commande : Command interpretation

**mobile_app** : Flutter application
- lib/screens : Interface screens
- lib/services : BLE service
- lib/widgets : Reusable components
- lib/utils : Constants and utilities

## Running the system

### Backend robot_python

```
cd robot_python
python main.py
```

### Frontend mobile_app

```
cd mobile_app
flutter run
```

Select the robot from the Bluetooth list after startup.

## Usage

Available commands: manual (forward, backward, turn), voice, and autonomous. The app allows configuring target shape and color. In autonomous mode, the robot searches for and approaches the target automatically. Each mode has limitations: autonomous analyzes the environment before moving, manual requires continuous inputs.

## Error handling

Collision detected: immediate stop and notification to the app. Camera failure: fallback to a reduced mode without vision. Bluetooth loss: the robot continues operating but notifies the user. Before restarting after an emergency stop, verify the environment is safe.

## Important notes

- Check available space before starting
- Test in a controlled environment before use
- Check battery before each session
- The file best.pt (YOLO model) must be present in robot_python
