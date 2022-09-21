import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pandas as pd

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
import seaborn as sn
import matplotlib.pyplot as plt
from google_trans_new import google_translator

test = pd.read_csv("confer/Sentiment_analysis/dataset/Classeur2.csv", sep=';', encoding='latin-1', engine='python')

train = pd.read_csv("confer/Sentiment_analysis/dataset/final.csv", sep=';', encoding='latin-1', engine='python')

train['y'] = np.vectorize(lambda x: 1 if x == 1 else -1)(train.sentiment)

translator = google_translator()


def translate(mot):
    mot = translator.translate(mot, lang_src='fr', lang_tgt='en')
    return mot


c = len(test)
for i in range(c):
    test.loc[i, "text"] = translate(test.loc[i, "text"])

pipe = make_pipeline(

    CountVectorizer(stop_words='english'),
    LinearRegression(), )

pipe.fit(train.content, train.y)
vectorizer = pipe.named_steps['countvectorizer']
model = pipe.named_steps['linearregression']
vectorizer.transform(train.content)
coef = pd.DataFrame([model.coef_], columns=sorted(vectorizer.vocabulary_.keys()), index=['coef']).T
coef = coef.sort_values(by='coef', ascending=False)
test['model2_pos'] = (pipe.predict(test.text) > 0).astype(bool)
test['scores'] = pipe.predict(test.text)

cm = confusion_matrix(y_true=test.real_positive, y_pred=test.model2_pos)
ax = plt.subplot()
sn.heatmap(cm, annot=True, fmt='g', ax=ax, cmap="Blues")


def analyser(text):
    text = [text]
    score = pipe.predict(text)

    return score[0]

