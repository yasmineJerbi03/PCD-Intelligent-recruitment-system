import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from sklearn.metrics import confusion_matrix
from tensorflow.keras.models import load_model
import os
import numpy as np
from keras.preprocessing import image
import seaborn as sn

from sklearn.metrics import precision_score, recall_score, accuracy_score

data_dir = 'dataset/photo/train'
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(200, 200))

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    data_dir,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(200, 200))

model = Sequential()

model.add(layers.experimental.preprocessing.RandomFlip("horizontal", input_shape=(200, 200, 3)))
model.add(layers.experimental.preprocessing.Rescaling(1. / 255))
model.add(layers.Conv2D(32, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(32, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(layers.MaxPooling2D(pool_size=(2, 2)))
model.add(layers.Flatten())
model.add(layers.Dense(160, activation='relu'))
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dense(50, activation='relu'))
model.add(layers.Dense(30, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.compile(optimizer=keras.optimizers.Adam(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=10,
)

model = load_model('models/cnn_model.h5')
list_test = []
for i in range(0, 50):
    list_test.append(0)
for j in range(0, 45):
    list_test.append(1)
print(list_test)


list_test_0 = os.listdir('dataset/photo/Test/bonne')
list_test_1 = os.listdir('dataset/photo/Test/mauvaise')
list_test_pred = []
for i in range(0, 50):
    img = image.load_img(f'dataset/photo/Test/bonne/{list_test_0[i]}', target_size=(200, 200))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    prediction = model.predict(images)
    if prediction[0][0] < 0.5:
        list_test_pred.append(0)
    else:
        list_test_pred.append(1)

for i in range(0, 45):
    img = image.load_img(f'dataset/photo/Test/mauvaise/{list_test_1[i]}', target_size=(200, 200))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    prediction = model.predict(images)
    if prediction[0][0] < 0.5:
        list_test_pred.append(0)
    else:
        list_test_pred.append(1)

cm = confusion_matrix(y_true=list_test, y_pred=list_test_pred)
ax = plt.subplot()
sn.heatmap(cm, annot=True, fmt='g', ax=ax, cmap="Blues");

print(precision_score(list_test, list_test_pred))
print(recall_score(list_test, list_test_pred))
print(accuracy_score(list_test, list_test_pred))

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(10)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
