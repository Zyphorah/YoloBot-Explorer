# Robot Autonome avec Interface Mobile

## Vue d'ensemble

Système robotique complet composé d'un robot Raspberry Pi capable de détecter des objets et naviguer de manière autonome, contrôlé via une application mobile Flutter. Le robot analyse son environnement, identifie les obstacles, et exécute les commandes reçues en validant les conditions de sécurité. En cas de situation critique (collision, perte de vision), le robot arrête immédiatement et signale l'anomalie.

## Architecture

Le système est divisé en deux composantes : un backend (robot_python) qui gère la vision YOLO, la navigation, les collisions et la communication Bluetooth, et un frontend (mobile_app) Flutter permettant commandes manuelles, voix et configuration de cibles. La communication se fait en Bluetooth Low Energy avec des UUID spécifiques.

## Configuration Bluetooth

Service UUID : A07498CA-AD5B-474E-940D-16F1FBE7E8CD
Commandes : 51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B
Statut : 2F8C4D2A-1D3B-4F5A-9C6E-7B8A9B0C1D2E

Ces identifiants doivent être identiques sur le robot et l'application mobile. Appairez d'abord le robot via les paramètres Bluetooth du système avant utilisation.

## Installation

### Dépendances système (Linux/Debian)

```
sudo apt update
sudo apt install -y libcap-dev
sudo apt install libcairo2-dev pkg-config python3-dev libgirepository1.0-dev -y
```

### Installation de libcamera

```
il faut installer libcamera
```

### Environnement Python

```
uv venv --system-site-packages
```

### Dépendances Python

```
uv pip uninstall numpy
uv pip install -r robot_python/requirements.txt
uv pip install bluezero
```

### Installation des dépendances Bluetooth

```
pip install bleak
```

### Dépendances Flutter

```
cd mobile_app
flutter pub get
```

## Structure du projet

**robot_python** : Backend du robot
- moteur : Drivers servos et moteurs DC
- navigation : Mouvements, trajectoires, collisions
- vision : Capture et analyse YOLO
- services : Service BLE
- comportements : Modes autonome, détection, scan
- commande : Interprétation des commandes

**mobile_app** : Application Flutter
- lib/screens : Écrans de l'interface
- lib/services : Service BLE
- lib/widgets : Composants réutilisables
- lib/utils : Constantes et utilitaires

## Lancement du systeme

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

Sélectionnez le robot dans la liste Bluetooth après démarrage.

## Utilisation

Commandes disponibles : manuelles (avancer, reculer, tourner), vocales, et autonome. L'application permet de configurer la forme et couleur cibles. En mode autonome, le robot cherche et s'approche automatiquement de la cible. Chaque mode a ses limitations : l'autonome analyse l'environnement avant de se déplacer, le manuel nécessite des inputs constants.

## Gestion des erreurs

Collision détectée : arrêt immédiat et signalement à l'application. Caméra défaillante : basculement en mode réduit sans vision. Perte Bluetooth : le robot continue de fonctionner mais notifie l'utilisateur. Avant redémarrage après arrêt d'urgence, vérifier que l'environnement est sûr.

## Notes importantes

- Vérifier l'espace disponible avant lancement
- Tester en environnement contrôlé avant utilisation
- Vérifier la batterie avant chaque session
- Le fichier best.pt (modèle YOLO) doit être présent dans robot_python
