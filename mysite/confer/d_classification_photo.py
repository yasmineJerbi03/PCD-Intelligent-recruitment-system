import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from confer.d_photo_extraction import extract_image
import keras
from tensorflow.keras.models import load_model
import numpy as np


def classification(id_candidat, path_pdf):
    extract_image(id_candidat, path_pdf)
    model = load_model('confer/photo_analysis/models/CNN_model.h5')
    img = keras.preprocessing.image.load_img(f'confer/photo_analysis/dataset/photo/candidats/{id_candidat}.png', target_size=(200, 200))
    x = keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    classes = model.predict(images)
    os.remove(f'confer/photo_analysis/dataset/photo/candidats/{id_candidat}.png')
    return (1 - classes[0][0])*100




#print(classification(10,'cv_analysis/dataset/aa.pdf'))