import asyncio
import threading

# from bleak import BleakServer, BleakGATTCharacteristic
from bless import (
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions,
)

# --- Configuration des UUIDs (Identifiants uniques) ---
# Vous devrez utiliser ces mêmes UUIDs dans votre application Flutter
SERVICE_UUID = "A07498CA-AD5B-474E-940D-16F1FBE7E8CD"
CHAR_RX_UUID = "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B"  # Pour recevoir (App -> Robot)
CHAR_TX_UUID = "51FF12BB-3ED8-46E5-B4F9-D64E2FEC021C"  # Pour envoyer (Robot -> App)


class BLEService:
    def __init__(self, device_name: str = "RobotBLEDevice"):
        self.device_name = device_name
        self.server = None
        self.loop = None
        self.running = False

        # Buffer pour stocker la dernière commande reçue
        self.derniere_commande = None
        self.command_lock = threading.Lock()

        # Thread pour gérer la boucle asynchrone du BLE
        self.thread = threading.Thread(target=self._run_async_loop)
        self.thread.daemon = True  # Le thread se ferme si le programme principal quitte

    def start(self):
        """Démarre le service BLE dans un thread séparé."""
        self.running = True
        self.thread.start()

    def stop(self):
        """Arrête le service BLE."""
        self.running = False
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join()

    def obtenir_derniere_commande(self):
        """Retourne la dernière commande reçue et la réinitialise."""
        with self.command_lock:
            commande = self.derniere_commande
            self.derniere_commande = None
        return commande

    def send_status(self, message: str):
        """Envoie un statut à l'application Flutter."""
        if self.server and self.loop:
            data = message.encode("utf-8")
            asyncio.run_coroutine_threadsafe(
                self.server.write_request(CHAR_TX_UUID, data), self.loop
            )

    def _run_async_loop(self):
        """Fonction interne exécutée par le thread pour gérer la boucle asynchrone BLE."""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._init_server())
        self.loop.run_forever()

    async def _init_server(self):
        """Initialise le serveur BLE avec les services et caractéristiques."""
        self.server = BlessServer(self.device_name, loop=self.loop)

        # Ajouter le service principal
        await self.server.add_new_service(SERVICE_UUID)

        # Caractéristique pour recevoir des commandes (App -> Robot)
        await self.server.add_new_characteristic(
            service_uuid=SERVICE_UUID,
            char_uuid=CHAR_RX_UUID,
            properties=GATTCharacteristicProperties.write
            | GATTCharacteristicProperties.write_without_response,
            value=None,
            permissions=GATTAttributePermissions.writeable,
        )

        # Caractéristique pour envoyer des statuts (Robot -> App)
        await self.server.add_new_characteristic(
            service_uuid=SERVICE_UUID,
            char_uuid=CHAR_TX_UUID,
            properties=GATTCharacteristicProperties.read | GATTCharacteristicProperties.notify,
            value=b"Status: Ready",
            permissions=GATTAttributePermissions.readable,
        )

        # Définir le callback pour les écritures sur la caractéristique RX
        self.server.set_write_callback(CHAR_RX_UUID, self._on_write)

        # Démarrer le serveur
        await self.server.start()
        print(f"[BLE] Advertising démarré sur {self.device_name}...")
        print(f"[BLE] Prêt à recevoir sur {CHAR_RX_UUID}")
    
    def _on_write(self, char: BlessGATTCharacteristic, value: bytearray):
        """Callback appelé lorsqu'une commande est reçue via la l'application Flutter."""
        try:
            commande = value.decode("utf-8").strip()
            print(f"[BLE] Commande reçue: {commande}")
            with self.command_lock:
                self.derniere_commande = commande

        except Exception as e:
            print(f"[BLE] Erreur lors du décodage de la commande: {e}")
