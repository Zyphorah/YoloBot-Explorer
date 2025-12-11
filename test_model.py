from ultralytics import YOLO

model = YOLO("best.pt")

# results = model.predict(source="debug_captured_frame.jpg", save=True)

results = model(source=0, show=True, conf=0.20)