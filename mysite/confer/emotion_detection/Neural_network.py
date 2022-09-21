import numpy as np
import os
import tensorflow as tf
from sklearn.metrics import confusion_matrix , accuracy_score , recall_score , precision_score
from tensorflow import keras
from tensorflow.keras import layers
from keras.preprocessing import image
from tensorflow.keras.models import Sequential
from tensorflow.keras.applications.vgg16 import VGG16

data_dir = '/dataset/data_emotion_jpg/Train'
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(327,225))


val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(327,225))


model = Sequential()
model.add(layers.experimental.preprocessing.RandomFlip("horizontal",input_shape=(327,225,3)))
model.add(layers.experimental.preprocessing.Rescaling(1./255))
model.add( VGG16(include_top = False, weights = 'imagenet'))
for layer in model.layers:
    layer.trainable = False
model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dense(500, activation='relu'))
model.add(layers.Dense(3, activation='softmax'))

model.compile(optimizer=keras.optimizers.Adam(),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=10,
)

list_test = []
for j in range(0, 39):
    list_test.append(0)
for j in range(0, 19):
    list_test.append(2)
for j in range(0, 39):
    list_test.append(1)

list_predict = []
test_dir = '/dataset/data_emotion_jpg/Test'
list_test_dir = os.listdir(test_dir)
print(list_test_dir)
for i in range (0,len(list_test_dir)):
    l = os.listdir(f'dataset/data_emotion_jpg/Test/{list_test_dir[i]}')
    for j in range(0,len(l)):
        img = image.load_img(f'dataset/data_emotion_jpg/Test/{list_test_dir[i]}/{l[j]}', target_size=(327,225))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])
        prediction = model.predict(images)
        score = tf.nn.softmax(prediction[0])
        res = np.max(score)
        for m in range(0,len(score)):
            if(score[m]==res):
                list_predict.append(m)
print(list_predict)


cm = confusion_matrix(y_true = list_test, y_pred=list_predict)
print(cm)

print(precision_score(list_test,list_predict, average='weighted'))
print(recall_score(list_test,list_predict,average='weighted'))
print(accuracy_score(list_test,list_predict))

model.save('models/emotion_model.h5')