import cv2
import numpy as np


class ImageProcessor:
    def __init__(self, image_path):
        self.image_path = image_path
        self.original = None
        self.gray = None
        self.roi = None

    def load_image(self):
        self.original = cv2.imread(self.image_path)
        if self.original is None:
            raise FileNotFoundError(f"Cannot load image {self.image_path}")
        return self.original

    def to_grayscale(self):
        self.gray = cv2.cvtColor(self.original, cv2.COLOR_BGR2GRAY)
        return self.gray

    def normalize(self):
        self.gray = cv2.equalizeHist(self.gray)
        return self.gray

    def extract_roi(self):
        # Simple contour-based ROI extraction
        edges = cv2.Canny(self.gray, 100, 200)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            self.roi = self.gray
        else:
            cnt = max(contours, key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(cnt)
            self.roi = self.original[y:y+h, x:x+w]
        return self.roi