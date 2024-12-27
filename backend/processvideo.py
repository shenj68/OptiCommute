import cv2
from ultralytics import YOLO
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')

# Load the YOLO model
#model = YOLO('yolov8s.pt').to(device)  # Use a pretrained YOLOv8 model
model = YOLO('yolov5s.pt').to(device) # try optimized model
device = model.device  # Returns 'cuda' for GPU or 'cpu'
print(f"Model is using: {device}")

# Define the classes you want to detect (bus, truck, person, car, bicycle)
target_classes = [0, 1, 2, 5, 7]  # COCO indices for target classes
TARGET_CLASS_NAMES = ["person", "bicycle", "car", "bus", "truck"]  # Names for target classes

# save video falg and load vid
save_video = False
video_path = "C:/Users/wwwsh/OneDrive/Documents/Projects/OptiCommute/OptiCommute Demo Clip.mp4"
cap = cv2.VideoCapture(video_path)

if save_video:
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 380))
    results = model(frame, classes=target_classes)
    annotated_frame = results[0].plot()

    # Extract and log detection details
    detections = results[0].boxes.data.cpu().numpy()  
    for detection in detections:
        x1, y1, x2, y2, confidence, class_id = detection
        # Map class index to target class name
        if int(class_id) in target_classes:
            class_name = TARGET_CLASS_NAMES[target_classes.index(int(class_id))]
            print(f"Detected: {class_name} with confidence: {confidence:.2f} at [{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]")

    if save_video:
        out.write(annotated_frame)

    cv2.imshow('YOLOv8 Detection', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if save_video:
    out.release()
cv2.destroyAllWindows()
