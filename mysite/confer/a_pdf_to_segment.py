import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from confer.a_pdf_to_csv import input_cv, data_manipulation, conversion_html
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import scale
from tensorflow.keras.models import load_model



def segmentation(segment):
    read_file = pd.read_excel('confer/cv_analysis/dataset/segmentation.xls', index_col=None)
    read_file.to_csv('confer/cv_analysis/dataset/segmentation.csv', index=None, header=True)
    df1 = pd.read_csv("confer/cv_analysis/dataset/segmentation.csv", header=None)
    liste = []
    for i in range(0, len(df1[segment])):
        if (str(df1[segment][i])) != 'nan':
            liste.append(df1[segment][i])
    return liste


objective = segmentation(0)
work = segmentation(1)
education = segmentation(2)
hard = segmentation(3)
soft = segmentation(4)
achievement = segmentation(5)

vectorizer = TfidfVectorizer()


def similarite(seg_cv, segment):
    res = []
    for i in range(0, len(segment)):
        X = vectorizer.fit_transform([segment[i], seg_cv])
        tfidf = (X * X.T).A[0, 1]
        res.append(tfidf)
    return max(res)


def bloc_recognition(seg_cv):
    obj = similarite(seg_cv, objective)
    w = similarite(seg_cv, work)
    ed = similarite(seg_cv, education)
    h = similarite(seg_cv, hard)
    so = similarite(seg_cv, soft)
    ach = similarite(seg_cv, achievement)
    f = (max(obj, w, ed, h, so, ach))
    if obj == f and f > 0.5:
        return 'Profil'
    if w == f and f > 0.5:
        return 'Experience professionelle'
    if ed == f and f > 0.5:
        return 'Expérience académique'
    if h == f and f > 0.5:
        return 'Hard skills et projets'
    if so == f and f > 0.5:
        return 'Soft skills'
    if ach == f and f > 0.5:
        return 'certifications et compétitions'
    else:
        return ' '


def segment(id_candidat, path):
    saved_model = load_model('confer/cv_analysis/models/cv_neural_network.h5')
    input_cv(path, id_candidat)
    df1 = pd.read_csv(f'confer/cv_analysis/dataset/{id_candidat}{id_candidat}.csv', header=None)
    x1 = df1.drop(0, axis=1)
    x_pred1 = scale(x1)
    predictions1 = saved_model.predict(x_pred1)
    p1 = np.argmax(predictions1, axis=1)

    vectorizer = TfidfVectorizer()
    dict_cv = data_manipulation(conversion_html(path), 2)
    d = dict_cv
    text = []
    for cle in d:
        text.append(cle)

    headlines = []
    for i in range(0, len(text)):
        if (p1[i] == 1):
            headlines.append(text[i])

    liste1 = []
    for i in range(0, len(headlines)):
        a = bloc_recognition(headlines[i])
        liste1.append(a)
    for cle in d:
        if (cle not in headlines):
            if ((similarite(cle, work)) > 0.5):
                headlines.append(cle)
                liste1.append('Experience professionelle')

            if ((similarite(cle, objective)) > 0.5):
                headlines.append(cle)
                liste1.append('Profil')

            if similarite(str(cle), education) > 0.5:
                headlines.append(cle)
                liste1.append('Expérience académique')

            if (similarite(cle, hard) > 0.5):
                headlines.append(cle)
                liste1.append('Hard skills et projets')

            if (similarite(cle, soft) > 0.5):
                headlines.append(cle)
                liste1.append('Soft skills')

            if (similarite(cle, achievement) > 0.5):
                headlines.append(cle)
                liste1.append('certifications et compétitions')
        segments = []
    for cle in d:
        if (cle not in headlines):
            d[cle] = ' '
        else:
            index = headlines.index(cle)
            d[cle] = liste1[index]
        seg = {}
    for cle in list(d):
        if (d[cle] == ' '):
            del d[cle]
        else:
            break
    z = list(d)
    for i in range(0, len(z)):
        if d[z[i]] != ' ':
            seg[z[i]] = d[z[i]]
            e = i + 1
            for j in range(e, len(z)):
                if d[z[j]] == ' ':
                    seg[z[j]] = d[z[i]]

    for cle in list(seg):
        if cle in headlines:
            del seg[cle]

    segment = {}
    for cle in seg:
        segment[seg[cle]] = ' '

    for cle in seg:
        segment[seg[cle]] = segment[seg[cle]] + '\n' + cle
    return segment


