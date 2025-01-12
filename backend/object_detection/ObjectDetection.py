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
        self.confidence_threshold = 0.38
        self.class_of_interests = [0, 1, 2, 5, 7]  # person, bicycle, car, bus, truck
        self.static_object_frames = {}

    def detect_objects(self, frame, frame_index):
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

        # static detection check (multiple frames)
        detections = self.detect_static_detections(detections, frame_index)

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
    
    def detect_static_detections(self, detections, frame_index):
        """
        detect static detections across multiple frames 
        """
        filtered_detections = []
        iou_threshold = 0.5  # IOU threshold for static object matching

        for detection in detections:
            x1, y1, x2, y2 = detection['bounding_box']
            current_bbox = [x1, y1, x2, y2]

            # check if the object is static
            static = False
            for static_bbox, (last_seen, count) in list(self.static_object_frames.items()):
                
                # calculate current IoU between the current bounding box and the tracked static bounding box
                iou = self.calculate_iou(current_bbox, static_bbox)
                if iou >= iou_threshold:
                    # update last seen and increment the static count
                    self.static_object_frames[tuple(static_bbox)] = (frame_index, count + 1)

                    # mark detction as static if it > static_frame_threshold
                    if count + 1 >= self.config.static_frame_threshold:
                        static = True
                    break

            if not static:
                # add the detection to filtered results as normal
                filtered_detections.append(detection)
                # track this detection for static suppression
                self.static_object_frames[tuple(current_bbox)] = (frame_index, 1)

        # remove outdated static objects
        self.static_object_frames = {
            bbox: (last_seen, count)
            for bbox, (last_seen, count) in self.static_object_frames.items()
            if frame_index - last_seen < self.config.static_frame_threshold
        }

        return filtered_detections

    def calculate_iou(self, boxA, boxB):
        """
        calculate the Intersection over Union (IoU) between two bounding boxes.
        """
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])

        # compute intersection area
        interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

        # compute union area
        boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
        boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

        # avoid division by zero
        unionArea = boxAArea + boxBArea - interArea
        if unionArea == 0:
            return 0.0

        return interArea / unionArea
