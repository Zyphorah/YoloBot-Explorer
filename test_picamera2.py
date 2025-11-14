try:
    from picamera2 import Picamera2
    import numpy as np
    
    print("Test avec picamera2")
    picam2 = Picamera2()
    
    # Configuration
    config = picam2.create_preview_configuration(
        main={"size": (640, 480), "format": "RGB888"}
    )
    picam2.configure(config)
    
    print("✓ Configuration OK")
    print("  Démarrage de la caméra...")
    
    picam2.start()
    print("✓ Caméra démarrée")
    
    # Capturer une frame
    frame = picam2.capture_array()
    print(f"✓ Capture réussie! Shape: {frame.shape}, dtype: {frame.dtype}")
    
    # Test de 10 captures
    print("\nTest de 10 captures...")
    for i in range(10):
        frame = picam2.capture_array()
        print(f"  Frame {i+1}: {frame.shape}")
    
    picam2.stop()
    print("✓ Test réussi!")
    
except ImportError as e:
    print(f"✗ picamera2 n'est pas installé: {e}")
    print("  Installez avec: sudo apt install -y python3-picamera2")
except Exception as e:
    print(f"✗ Erreur: {e}")
    import traceback
    traceback.print_exc()