/// Constantes de l'application pour la configuration Bluetooth.
class AppConstants {
  /// UUID du service Bluetooth du robot.
  /// Doit correspondre à la valeur configurée sur votre robot.
  static const String BOT_SERVICE_UUID = 'A07498CA-AD5B-474E-940D-16F1FBE7E8CD';

  /// UUID de la caractéristique Bluetooth pour envoyer des commandes.
  /// Doit correspondre à la valeur configurée sur votre robot.
  static const String BOT_CHARACTERISTIC_UUID =
      '51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B';
}