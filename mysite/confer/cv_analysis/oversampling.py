from sklearn.preprocessing import scale
import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from imblearn.over_sampling import RandomOverSampler

import seaborn as sn
from sklearn.metrics import precision_score, recall_score, accuracy_score, confusion_matrix, classification_report
import numpy as np
import collections
import matplotlib.pyplot as plt

df = pd.read_csv("dataset/dataset_cv.csv", header=None)

x = df.drop(0, axis=1)
y = df[0]
oversample = RandomOverSampler(sampling_strategy='minority')

X_over, y_over = oversample.fit_resample(x, y)
print(df[0].value_counts())

w = collections.Counter(y_over)
plt.bar(w.keys(), w.values())

x = scale(X_over)
x_train_over, x_test_over, y_train_over, y_test_over = train_test_split(X_over, y_over, test_size=0.20, random_state=40)

y_train_over = to_categorical(y_train_over)

model = Sequential()
model.add(Dense(15, activation='relu', input_dim=7))
model.add(Dense(7, activation='relu'))
model.add(Dense(2, activation='softmax'))

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(x_train_over, y_train_over, validation_split=0.3, epochs=10)


predictions = model.predict(x_test_over)
print(x_test_over.shape)

p = np.argmax(predictions, axis=1)
print(p)


cm = confusion_matrix(y_true=y_test_over, y_pred=p)

print(cm)
print(accuracy_score(y_test_over, p))

print(classification_report(y_test_over, p))

print(precision_score(y_test_over, p))
print(recall_score(y_test_over, p))
print(accuracy_score(y_test_over, p))
ax = plt.subplot()
sn.heatmap(cm, annot=True, fmt='g', ax=ax, cmap="Blues")
