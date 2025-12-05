from ultralytics import YOLO

model = YOLO("yolov8n.pt")

model.predict("img3.jpeg", show=True, conf=0.90, save=True)