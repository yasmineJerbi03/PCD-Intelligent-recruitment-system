import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
from sklearn.metrics import confusion_matrix
import numpy as np
from tensorflow.keras.models import load_model
from imblearn.combine import SMOTETomek

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale

from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical

df = pd.read_csv("dataset/dataset_cv.csv", header=None)
print(df)

x = df.drop(0, axis=1)
y = df[0]

model = Sequential()
model.add(Dense(12, activation='relu', input_dim=7))
model.add(Dense(6, activation='relu'))
model.add(Dense(2, activation='softmax'))

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

smt = SMOTETomek()
X_smt, y_smt = smt.fit_sample(x, y)

x = scale(X_smt)
x_train_smt, x_test_smt, y_train_smt, y_test_smt = train_test_split(X_smt, y_smt, test_size=0.30, random_state=42)

y_train_smt = to_categorical(y_train_smt)
model.fit(x_train_smt, y_train_smt, validation_split=0.35, epochs=10)
model.save('models/cv_neural_network.h5')

saved_model = load_model('models/cv_neural_network.h5')
predictions = saved_model.predict(x_test_smt, batch_size=30)
print(x_test_smt.shape)

p = np.argmax(predictions, axis=1)
print(p)

cm = confusion_matrix(y_true=y_test_smt, y_pred=p)
ax = plt.subplot()
sn.heatmap(cm, annot=True, fmt='g', ax=ax, cmap="Blues")
p2 = np.argmax(p, axis=1)
for i in range(0, len(p2)):
    print(f'{i + 2} ==> {p2[i]}')
