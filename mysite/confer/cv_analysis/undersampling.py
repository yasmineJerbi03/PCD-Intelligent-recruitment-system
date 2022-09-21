from sklearn.preprocessing import scale
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from imblearn.under_sampling import RandomUnderSampler

from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import seaborn as sn
from sklearn.metrics import precision_score, recall_score, accuracy_score, confusion_matrix, classification_report

df = pd.read_csv("dataset/dataset_cv.csv", header=None)
print(df)

x = df.drop(0, axis=1)
y = df[0]

undersample = RandomUnderSampler(sampling_strategy='majority')

X_under, y_under = undersample.fit_resample(x, y)

x = scale(X_under)
x_train_under, x_test_under, y_train_under, y_test_under = train_test_split(X_under, y_under, test_size=0.20,
                                                                            random_state=42)

y_train_under = to_categorical(y_train_under)

model = Sequential()
model.add(Dense(15, activation='relu', input_dim=7))
model.add(Dense(7, activation='relu'))
model.add(Dense(9, activation='relu'))
model.add(Dense(2, activation='softmax'))

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(x_train_under, y_train_under, validation_split=0.35, epochs=20)

predictions = model.predict(x_test_under)

p = np.argmax(predictions, axis=1)
print(p)

cm = confusion_matrix(y_true=y_test_under, y_pred=p)

print(cm)

print(classification_report(y_test_under, p))

print(precision_score(y_test_under, p))
print(recall_score(y_test_under, p))
print(accuracy_score(y_test_under, p))

ax = plt.subplot()
sn.heatmap(cm, annot=True, fmt='g', ax=ax, cmap="Blues")
