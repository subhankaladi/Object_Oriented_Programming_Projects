import cv2
import numpy as np

class FeatureExtractor:
    def __init__(self, roi):
        self.roi = roi
        self.gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    def watermark_detect(self, template_path, threshold=0.7):
        tpl = cv2.imread(template_path, 0)
        res = cv2.matchTemplate(self.gray_roi, tpl, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        return len(zip(*loc[::-1])) > 0

    def thread_detect(self):
        # Example: Hough line transform to detect thin vertical line
        edges = cv2.Canny(self.gray_roi, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)
        return lines is not None