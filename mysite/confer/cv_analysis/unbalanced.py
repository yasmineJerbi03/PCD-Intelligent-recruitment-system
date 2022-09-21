from sklearn.preprocessing import scale
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import seaborn as sn
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, precision_score, recall_score

df = pd.read_csv("dataset/dataset_cv.csv", header=None)
print(df)

x = df.drop(0, axis=1)
y = df[0]

x = scale(x)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=40)

y_train = to_categorical(y_train)

target_count = df[0].value_counts()
print('Class 0:', target_count[0])
print('Class 1:', target_count[1])
print('Proportion:', round(target_count[0] / target_count[1], 2), ': 1')

target_count.plot(kind='bar', title='Classes distribution');

model = Sequential()
model.add(Dense(15, activation='relu', input_dim=7))
model.add(Dense(7, activation='relu'))
model.add(Dense(9, activation='relu'))
model.add(Dense(2, activation='softmax'))

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.summary()

model.fit(x_train, y_train, validation_split=0.3, epochs=20)

predictions = model.predict(x_test)
print(x_test.shape)

p = np.argmax(predictions, axis=1)
print(p)

cm = confusion_matrix(y_true=y_test, y_pred=p)

print(cm)

print(accuracy_score(y_test, p))

print(classification_report(y_test, p))

print(precision_score(y_test, p))
print(recall_score(y_test, p))
print(accuracy_score(y_test, p))

ax = plt.subplot()
sn.heatmap(cm, annot=True, fmt='g', ax=ax, cmap="Blues")
