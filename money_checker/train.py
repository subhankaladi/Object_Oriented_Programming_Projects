import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model

DATA_DIR = "data/"  # data/asli/ and data/nakli/
BATCH_SIZE = 32
IMG_SIZE = (224, 224)

if __name__ == "__main__":
    # Data generators
    train_gen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=10,
        width_shift_range=0.1,
        height_shift_range=0.1,
        validation_split=0.2
    )
    train_flow = train_gen.flow_from_directory(
        DATA_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
        class_mode="binary", subset="training"
    )
    val_flow = train_gen.flow_from_directory(
        DATA_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE,
        class_mode="binary", subset="validation"
    )

    base = MobileNetV2(input_shape=IMG_SIZE+(3,), include_top=False, weights='imagenet')
    x = GlobalAveragePooling2D()(base.output)
    out = Dense(1, activation='sigmoid')(x)
    model = Model(base.input, out)
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    model.fit(train_flow, validation_data=val_flow, epochs=10)
    os.makedirs("models", exist_ok=True)
    model.save("models/note_detector.h5")
    print("Model saved to models/note_detector.h5")