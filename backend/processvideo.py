import cv2
from ultralytics import YOLO
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f'Using device: {device}')
model = YOLO('yolov8s.pt').to(device)
device = model.device
print(f"Model is using: {device}")

# Define the classes you want to detect (bus, truck, person, car, bicycle)
target_classes = [0, 1, 2, 5, 7]

# save video falg and load vid
save_video = False
video_path = "C:/Users/wwwsh/OneDrive/Documents/Projects/OptiCommute/OptiCommute Demo Clip.mp4"
cap = cv2.VideoCapture(video_path)

# only set these if save video is true
if save_video:
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    out = cv2.VideoWriter('output_video.avi', cv2.VideoWriter_fourcc(*'XVID'), fps, (frame_width, frame_height))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame, (640,380))
    # results = model(frame)
    results = model(frame, classes=target_classes)
    annotated_frame = results[0].plot()

    if save_video:
        out.write(annotated_frame)

    cv2.imshow('YOLOv8 Detection', annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if save_video:
    out.release()
cv2.destroyAllWindows()
