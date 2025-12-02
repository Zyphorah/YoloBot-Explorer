from robot_python import BLEService, FacadeNavigation, Servo, Camera, ControleurRobot

def main():    
    camera = Camera("yolov8n.pt")
    ble = BLEService()
    nav = FacadeNavigation()
    servo = Servo()
    
    ble.start()
    
    controleur = ControleurRobot(nav, servo, camera, ble)
    controleur.initialiser()
    
    try:
        while True:
            controleur.executer_cycle()
    except KeyboardInterrupt:
        print("Main: arret du programme")
    except Exception as e:
        print(f"Main: erreur inattendue: {e}")
    finally:
        controleur.nettoyer()

if __name__ == "__main__":
    main()

