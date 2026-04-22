from imageai.Detection import ObjectDetection  # Install imageai
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
import os

def load_keras_model(model_path='./cv_models/keras_Model.h5', labels_path='./cv_models/labels.txt'):
    model = load_model(model_path, compile=False)
    with open(labels_path, 'r', encoding='utf-8') as file:
        class_names = file.readlines()
    return model, class_names

def classificate_image(model, class_names, image_path):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name.split()[1], round(confidence_score*100)

def detect_object(image_path, model_path='./cv_models/yolov3.pt'):
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath("yolov3.pt")
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=image_path,
                                                 output_image_path='./images/' + image_path.split('.')[0] + '_result.jpg',
                                                 minimum_percentage_probability=30)
    return detections