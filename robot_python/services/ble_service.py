import asyncio
import threading
import logging
import random
from bluezero import adapter
from bluezero import peripheral

# --- Configuration des UUIDs ---
# UUIDs définis pour la nouvelle librairie bluezero
BOT_SERVICE_PRINCIPAL = 'A07498CA-AD5B-474E-940D-16F1FBE7E8CD'
BOT_CARACTERISTIQUE_COMMANDES = '51FF12BB-3ED8-46E5-B4F9-D64E2FEC021B'


class BLEService:
    def __init__(self, device_name: str = "Robot 1"):
        self.device_name = device_name
        self.running = False

        # Buffer pour stocker la dernière commande reçue
        self.derniere_commande = None
        self.command_lock = threading.Lock()

        # Configuration Bluezero
        self.logger = logging.getLogger('localGATT')
        self.logger.setLevel(logging.DEBUG)

        try:
            # Get the default adapter address
            self.adapter_address = list(adapter.Adapter.available())[0].address
            print(f'[BLE] Initialisation du périphérique BLE sur {self.adapter_address}')
        except IndexError:
            print("[BLE] Erreur: Aucun adaptateur Bluetooth trouvé.")
            self.adapter_address = None
            return

        # Création du périphérique BLE
        self.bot_monitor = peripheral.Peripheral(self.adapter_address,
                                            local_name=self.device_name,
                                            appearance=1344)
        
        # Add service
        self.bot_monitor.add_service(srv_id=1, uuid=BOT_SERVICE_PRINCIPAL, primary=True)
        
        # Add characteristic
        self.bot_monitor.add_characteristic(srv_id=1, chr_id=1, uuid=BOT_CARACTERISTIQUE_COMMANDES,
                                       value=[], notifying=False,
                                       flags=['write', 'write-without-response', 'read'],
                                       read_callback=self.read_value,
                                       write_callback=self.write_value,
                                       notify_callback=None
                                       )

        # Thread pour gérer la boucle (publish est bloquant)
        self.thread = threading.Thread(target=self._run_loop)
        self.thread.daemon = True

    def start(self):
        """Démarre le service BLE dans un thread séparé."""
        if not hasattr(self, 'bot_monitor'):
            print("[BLE] Service non initialisé correctement.")
            return
            
        self.running = True
        self.thread.start()

    def stop(self):
        """Arrête le service BLE."""
        self.running = False
        # Bluezero ne s'arrête pas facilement depuis un autre thread, 
        # mais comme c'est un daemon thread, il se fermera avec le programme principal.
        pass

    def obtenir_derniere_commande(self):
        """Retourne la dernière commande reçue et la réinitialise."""
        with self.command_lock:
            commande = self.derniere_commande
            self.derniere_commande = None
        return commande

    def send_status(self, message: str):
        """Envoie un statut."""
        # Note: La configuration fournie utilise 'read' sur demande plutôt que 'notify'.
        # Cette fonction est gardée pour compatibilité mais ne fait rien dans cette version.
        pass

    def _run_loop(self):
        """Fonction interne exécutée par le thread."""
        try:
            print(f"[BLE] Advertising démarré sur {self.device_name}...")
            self.bot_monitor.publish()
        except Exception as e:
            print(f"[BLE] Erreur dans la boucle BLE: {e}")

    def write_value(self, value, options):
        """Callback appelé lors d'une écriture BLE."""
        # print(f"Write request received: {value}")	
        try:
            # Bluezero peut passer une liste d'entiers ou des bytes selon la version/contexte
            if isinstance(value, list):
                data = bytes(value)
            else:
                data = value
                
            cmd_str = data.decode("utf-8").strip()
            print(f"[BLE] Commande reçue: {cmd_str}")
            
            with self.command_lock:
                self.derniere_commande = cmd_str
                
        except Exception as e:
            print(f"[BLE] Erreur de décodage: {e}")

    def read_value(self): 
        """Callback appelé lors d'une lecture BLE."""
        print(f"[BLE] Read request received")
        # Logique aléatoire demandée
        cpu_value = random.randrange(3200, 5310, 10) / 100
        return list(int(cpu_value * 100).to_bytes(2, byteorder='little', signed=True))
