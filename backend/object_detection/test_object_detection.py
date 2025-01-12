import sys
import os
import cv2 as cv
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from preprocessing.config import Config
from preprocessing.preprocess import Preprocess
from object_detection.ObjectDetection import ObjectDetection

# VISUALIZE FLAG
VISUALIZE = True

config = Config()
preprocessor = Preprocess(config)
model_path = "C:/Users/wwwsh/OneDrive/Documents/Projects/OptiCommute/backend/yolov5su.pt" 
object_detector = ObjectDetection(model_path, config)

print("Preprocessing the video...")
processed_frames = preprocessor.preprocess()

print("Performing object detection...")
for idx, frame in enumerate(processed_frames):
    # run detection on the current frame
    detections = object_detector.detect_objects(frame, idx)

    # print the detection results for the current frame of the vid
    print(f"Frame {idx + 1}: {len(detections)} detections")
    for detection in detections:
        print(f" - Class ID: {detection['class_id']}, Confidence: {detection['confidence']:.2f}, "
              f"BBox: {detection['bounding_box']}, AOI: {detection.get('aoi', 'N/A')}")

    # if visualization is enabled
    if VISUALIZE:
        visualized_frame = frame.copy()

        # draw AOIs on the frame
        for mask_name, mask_coords in config.area_of_interest_coords.items():
            cv.polylines(visualized_frame, [np.array(mask_coords, dtype=np.int32)], isClosed=True, color=(255, 0, 0), thickness=2)
            cv.putText(visualized_frame, mask_name, mask_coords[0], cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

        # draw the detections
        for detection in detections:
            x1, y1, x2, y2 = detection['bounding_box']
            class_id = detection['class_id']
            confidence = detection['confidence']

            # draw the bounding box
            cv.rectangle(visualized_frame, (x1, y1), (x2, y2), color=(0, 255, 0), thickness=2)

            # add the label and its confidence
            label = f"Class {class_id}: {confidence:.2f}"
            cv.putText(visualized_frame, label, (x1, y1 - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        cv.imshow("Detection Results", visualized_frame)

        if cv.waitKey(30) & 0xFF == ord('q'):
            break

if VISUALIZE:
    cv.destroyAllWindows()
