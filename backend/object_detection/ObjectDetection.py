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
