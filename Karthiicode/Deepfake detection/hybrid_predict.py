import tensorflow as tf
import numpy as np
from PIL import Image

resnet_model = tf.keras.models.load_model("deepfake_resnet50.h5", compile=False)
xception_model = tf.keras.models.load_model("deepfake_model.h5", compile=False)

def preprocess_image(image_path, target_size):
    img = Image.open(image_path).convert("RGB")
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict_resnet(image_path):
    img_array = preprocess_image(image_path, (224, 224))
    pred = resnet_model.predict(img_array)[0][0]
    print("[DEBUG] ResNet raw output:", pred)

    THRESHOLD = 0.85
    if pred > THRESHOLD:
        return "REAL", pred * 100
    else:
        return "FAKE", (1 - pred) * 100

def predict_xception(image_path):
    img_array = preprocess_image(image_path, (128, 128))
    pred = xception_model.predict(img_array)[0][0]
    print("[DEBUG] Xception raw output:", pred)

    THRESHOLD = 0.75
    if pred > THRESHOLD:
        return "REAL", pred * 100
    else:
        return "FAKE", (1 - pred) * 100
def predict_hybrid(image_path):
    
    resnet_label, resnet_conf = predict_resnet(image_path)
    xception_label, xception_conf = predict_xception(image_path)
    if resnet_conf > xception_conf:
        chosen_label, chosen_conf, chosen_model = resnet_label, resnet_conf, "ResNet"
    else:
        chosen_label, chosen_conf, chosen_model = xception_label, xception_conf, "Xception"
    if chosen_model == "Xception" and chosen_label == "REAL" and resnet_label == "FAKE":
        return "FAKE", resnet_conf

    return chosen_label,chosen_conf
