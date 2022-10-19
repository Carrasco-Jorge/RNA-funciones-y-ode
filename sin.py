# Import DL framework
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import RMSprop, Adam
from keras.callbacks import TensorBoard, ReduceLROnPlateau

# Import modules
import matplotlib.pyplot as plt 
import numpy as np
import os

# Workaround
os.environ['KMP_DUPLICATE_LIB_OK']='True'

def name_activations(activations):
  s = ""
  for a in activations:
    s += f"-{a}"
  return s

x = tf.linspace(-1, 1, 1000) # Puntos en el dominio
y = 3*tf.sin(np.pi*x)
plt.plot(x,y)
plt.show()

name_type = "sin"
epochs = 500
UNITS = [10, 30, 60]
loss = "mae"
learning_rate = 1e-3
OPTIMIZERS = [Adam(learning_rate=learning_rate), 
              RMSprop(learning_rate=learning_rate)]
OPT = ["Adam","RMSprop"]
activations = []
activations.append("tanh")
# activations.append("tanh")

def create_path(path, PATH = f"./logs/{name_type}"):
  return os.path.join(PATH, path)

for units in UNITS:
  for optimizer, opt in zip(OPTIMIZERS, OPT):
    NAME = f"{units}-{opt}"+name_activations(activations)
    print(NAME)
    tensorboard = TensorBoard(log_dir=create_path(f"{NAME}"))

    # Hyper parameters
    reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.9, min_delta=0.01, patience=50, min_lr=1e-4)

    model = Sequential()

    for i in range(len(activations)):
      if i == 0:
        model.add(Dense(units, activation=activations[i], input_shape=(1,)))
      else:
        model.add(Dense(units, activation=activations[i]))
    model.add(Dense(1, activation="linear"))

    # model.summary()

    model.compile(optimizer=optimizer, loss=loss)

    history = model.fit(x,y, epochs=epochs,
                        callbacks=[tensorboard, reduce_lr],
                        verbose=0)
    model.save(create_path(NAME+".h5", PATH = f"./models/{name_type}"))
    
    fig, ax = plt.subplots()
    ax.plot(x,y)
    ax.plot(x,model.predict(x))
    ax.set_title(NAME)
    fig.savefig(create_path(NAME+".png",PATH = f"./img/{name_type}"))
