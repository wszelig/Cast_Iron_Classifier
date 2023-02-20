import numpy as np
import tensorflow as tf


def predict(img):
    # Crop to avoid image stretch
    width = img.width
    height = img.height
    if width > height:
        img = img.crop((0, 0, height, height))
    else:
        img = img.crop((0, 0, width, width))
    img = img.convert('RGB').resize((100, 100))
    img = np.array(img).reshape((1, 100, 100, 3))
    # Load model
    model = tf.keras.models.load_model('saved_model/graphite_classifier')
    # Classify
    predictions = model.predict(img)
    test_labels = ['White', 'Malleable', 'Ductile', 'Gray']
    answer = f'{test_labels[np.argmax(predictions[0])]}'

    return answer
