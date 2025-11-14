import cv2

def test_camera_with_settings(device, backend=None, width=640, height=480):
    """Test caméra avec configuration explicite."""
    print(f"\n{'='*60}")
    print(f"Test: device={device}, backend={backend}, resolution={width}x{height}")
    print('='*60)
    
    try:
        if backend is not None:
            cap = cv2.VideoCapture(device, backend)
        else:
            cap = cv2.VideoCapture(device)
        
        if not cap.isOpened():
            print("✗ Échec d'ouverture")
            return False
        
        print("✓ Caméra ouverte")
        
        # Configurer explicitement la résolution et le format
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_FPS, 30)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
        
        # Lire les propriétés actuelles
        actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        actual_fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
        fourcc_str = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
        
        print(f"  Résolution demandée: {width}x{height}")
        print(f"  Résolution obtenue: {actual_width}x{actual_height}")
        print(f"  FPS: {actual_fps}")
        print(f"  Format: {fourcc_str}")
        
        # Essayer de lire une frame
        ret, frame = cap.read()
        
        if ret and frame is not None:
            print(f"✓ Lecture réussie! Frame shape: {frame.shape}")
            cap.release()
            return True
        else:
            print(f"✗ Lecture échouée: ret={ret}, frame={'None' if frame is None else 'OK'}")
            cap.release()
            return False
            
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False

# Tests avec différentes configurations
configs = [
    (0, None, 640, 480),
    (0, cv2.CAP_V4L2, 640, 480),
    (0, cv2.CAP_V4L2, 1920, 1080),
    (0, cv2.CAP_V4L2, 1280, 720),
    (0, cv2.CAP_V4L2, 320, 240),
    ("/dev/video0", cv2.CAP_V4L2, 640, 480),
]

print("Recherche de la meilleure configuration...")
for device, backend, width, height in configs:
    if test_camera_with_settings(device, backend, width, height):
        print(f"\n{'='*60}")
        print(f"✓ SUCCÈS avec: device={device}, backend={backend}, {width}x{height}")
        print('='*60)
        break
else:
    print("\n✗ Aucune configuration n'a fonctionné")