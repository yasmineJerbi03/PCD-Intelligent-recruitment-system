import librosa as lb
import librosa.display as display

import matplotlib.pyplot as plt
import numpy as np
import os
import cv2

#liste_train = os.listdir('dataset/dataset-emotion/train')
#liste_test = os.listdir('dataset/dataset-emotion/test')

def transformation(audio):
    y, sr = lb.load(audio)
    y, f = lb.effects.trim(y)
    mel_spect = lb.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=100)
    mel_spect = lb.power_to_db(mel_spect, ref=np.max)
    return mel_spect

def data_preprocessing(liste, path, path_dest):
    for i in range(0, len(liste)):
        l = os.listdir(f'{path}/{liste[i]}')
        for j in range(0, len(l)):
            mel_spect = transformation(f'{path}/{liste[i]}/{l[j]}')
            display.specshow(mel_spect, y_axis='mel', fmax=20000, x_axis='time');
            plt.savefig(f'{path_dest}/{liste[i]}/{j}.jpg')

def cropping(path):
    y=46
    x=33
    h=393
    w=258
    image = cv2.imread(path)
    crop_image = image[x:w, y:h]
    cv2.imwrite(path,crop_image)
#data_preprocessing(liste_train, 'dataset/dataset-emotion/train', 'dataset/data_emotion_jpg/train')
#data_preprocessing(liste_train, 'dataset/dataset-emotion/test', 'dataset/data_emotion_jpg/test')