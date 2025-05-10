import tensorflow as tf
import numpy as np

class NoteClassifier:
    def __init__(self, model_path="models/note_detector.h5"):
        self.model = tf.keras.models.load_model(model_path)

    def preprocess_for_model(self, roi):
        img = cv2.resize(roi, (224, 224))
        img = img.astype("float32") / 255.0
        return np.expand_dims(img, axis=0)

    def predict(self, roi):
        inp = self.preprocess_for_model(roi)
        prob = self.model.predict(inp)[0][0]
        return "Asli" if prob >= 0.5 else "Nakli", float(prob)