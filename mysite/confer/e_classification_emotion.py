from confer.e_video_preprocessing import transformation
from tensorflow.keras.models import load_model
import librosa.display as display
from keras.preprocessing import image
import numpy as np
import tensorflow as tf

import matplotlib.pyplot as plt


def classification_video(audio, id_candidat):
    #mel_spect = transformation(audio)
    #display.specshow(mel_spect, y_axis='mel', fmax=20000, x_axis='time')
    #plt.axis('off')
    #plt.savefig(f'static/images/hire/_emotion_jpg/candidats/{id_candidat}.jpg')
    model = load_model('confer/emotion_detection/models/emotion_model.h5')
    print('.........................................................................ok')
    img = image.load_img(f'confer/emotion_detection/dataset/data_emotion_jpg/candidats/{id_candidat}.jpg', target_size=(327, 225))
    print('.........................................................................ok')
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    prediction = model.predict(images)
    score = tf.nn.softmax(prediction[0])
    res = np.max(score)
    label = 0
    for m in range(0, len(score)):
        if (score[m] == res):
            label = m
    #if (label == 0):
     #   return ('calm')
    #if (label == 1):
     #   return ('fearful')
    #if (label == 2):
     #   return ('neutral')
    return label


#print(classification('emotion_detection/0.wav', 5))
#print(classification('emotion_detection/1.wav', 1))

# cropping('dataset/data_emotion_jpg/candidats/0.jpg')
