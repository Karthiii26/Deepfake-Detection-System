import numpy as np
from PIL import Image

def preprocess_resnet(image_path, target_size=(224, 224)):
    img = Image.open(image_path).convert("RGB")
    img = img.resize(target_size)
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, axis=0)

def preprocess_xception(image_path, target_size=(128, 128)):
    img = Image.open(image_path).convert("RGB")
    img = img.resize(target_size)
    arr = np.array(img) / 255.0
    return np.expand_dims(arr, axis=0)
