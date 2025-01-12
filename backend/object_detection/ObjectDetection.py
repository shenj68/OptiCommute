import cv2 as cv
import numpy as np
from ultralytics import YOLO
import torch


class ObjectDetection:
    def __init__(self, model_path, config):
        # use gpu if availbale
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f'Using device: {self.device}')

        # Load the YOLO model
        try:
            self.model = YOLO(model_path).to(self.device)
            print(f"Model loaded and using device: {self.device}")
        except Exception as e:
            raise RuntimeError(f"Error loading YOLO model: {e}")

        self.config = config
        self.confidence_threshold = 0.45
        self.class_of_interests = [0, 1, 2, 5, 7]  # person, bicycle, car, bus, truck

    def detect_objects(self, frame):
        """
        perform object detection on a single frame.
        """
        # perform object detection
        results = self.model(frame)

        # extract detections from the results
        if isinstance(results, list):
            detections = results[0].boxes.data.cpu().numpy()  # YOLOv8 format
        else:
            detections = results.boxes.data.cpu().numpy()

        # filter detections by confidence and class
        detections = self.filter_detections_by_confidence_and_class(detections)

        # filter detections by AOI
        detections = self.filter_detections_by_aoi(detections, self.config.area_of_interest_coords)

        return detections

    def filter_detections_by_confidence_and_class(self, detections):
        """
        filter detections by confidence and class of interest.
        """
        filtered_detections = [
            d for d in detections if d[4] >= self.confidence_threshold \
                and int(d[5]) in self.class_of_interests
        ]
        return filtered_detections

    def filter_detections_by_aoi(self, detections, masks):
        """
        filter detected objects to include aoi

        """
        filtered_detections = []

        # create a combined AOI mask
        combined_mask = np.zeros((self.config.resize_dimension[1], self.config.resize_dimension[0]), dtype=np.uint8)
        for mask_name, mask_coords in masks.items():
            cv.fillPoly(combined_mask, [np.array(mask_coords, dtype=np.int32)], 255)

        for detection in detections:
            x1, y1, x2, y2, conf, class_id = detection

            # calculate the center of the bounding box
            cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)

            # check if the center of the bounding box is within the AOI
            if combined_mask[cy, cx] == 255:  # White area in AOI mask
                filtered_detections.append({
                    "class_id": int(class_id),
                    "confidence": float(conf),
                    "bounding_box": [int(x1), int(y1), int(x2), int(y2)],
                    "aoi": self.get_aoi_name(cx, cy, masks)  # add AOI name for metadata
                })

        return filtered_detections

    def get_aoi_name(self, cx, cy, masks):
        """
        get the name of the AOI where the detected object is located.
        """
        for mask_name, mask_coords in masks.items():
            polygon = np.array(mask_coords, dtype=np.int32)
            if cv.pointPolygonTest(polygon, (cx, cy), False) >= 0:
                return mask_name
        return None
