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

# xy′ + y = x**2 cos x => y' = (cos(x) * x**2 - y)/x 
min_val = -5
max_val = 5

# ODE solver
class ODEsolver(Sequential):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    # Mide la funcion de costo definida
    self.loss_tracker = keras.metrics.Mean(name="loss")

  @property
  def metrics(self):
    # Para que se sepa cual es la metrica a imprimir
    return [self.loss_tracker]
  
  def train_step(self, data): # Override a train_step
    batch_size = tf.shape(data)[0] # Minibatch.shape[0] es resolucion de sol
    # Puntos aleatorios del dominio de la ecuacion para "integracion montecarlo"
    x = tf.random.uniform((batch_size,1), minval=min_val, maxval=max_val)

    # Records calculations made inside "with" block to calculate gradient
    with tf.GradientTape() as tape: # For weights and biases
      # Compute loss value
      with tf.GradientTape() as tape2: # For d(output)/d(input)
        tape2.watch(x) # watch calculations made with 'x'
        y_pred = self(x, training=True) # Evaluate Network on 'x'
        # training=True to indicate saving of hidden parameters
      
      dy = tape2.gradient(y_pred, x) # get grandient of input1 with respect to input2
      x_0 = tf.zeros((batch_size, 1)) # Initial condition for 'x' is 0
      y_0 = self(x_0, training=True) # Initial condition of y i.e. y(0)
      eq = dy - (tf.math.cos(x)*x**2 - y_pred)/x # y' = (2*cos(x) * x**2 - y)/x 
      ic = y_0 - 0.0 # Condicion inicial
      # Define custom loss inside gradient tape
      loss = keras.losses.mean_squared_error(0.0, eq) + keras.losses.mean_squared_error(0.0, ic)
    
    # Apply grads
    grads = tape.gradient(loss, self.trainable_variables)
    self.optimizer.apply_gradients(zip(grads, self.trainable_variables))

    # Update metrics
    self.loss_tracker.update_state(loss)

    # Return a dict mapping metric names to current value
    return {"loss":self.loss_tracker.result()}


x = tf.linspace(min_val, max_val, 1000) # Puntos en el dominio

name_type = "ode_a"
epochs = 500
UNITS = [10, 30, 60]
loss = "loss"
learning_rate = 1e-3
OPTIMIZERS = [Adam(learning_rate=learning_rate), 
              RMSprop(learning_rate=learning_rate)]
OPT = ["Adam","RMSprop"]
activations = []
activations.append("tanh")
activations.append("relu")
activations.append("tanh")

sol_analitica = lambda x: (x**2*tf.sin(x)+2*x*tf.cos(x)-2*tf.sin(x))/x

def create_path(path, PATH = f"./logs/{name_type}"):
  return os.path.join(PATH, path)

for units in UNITS:
  for optimizer, opt in zip(OPTIMIZERS, OPT):
    NAME = f"{units}-{opt}"+name_activations(activations)
    print(NAME)
    tensorboard = TensorBoard(log_dir=create_path(f"{NAME}"))

    # Hyper parameters
    reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.9, min_delta=0.01, patience=50, min_lr=1e-4)

    model = ODEsolver()

    for i in range(len(activations)):
      if i == 0:
        model.add(Dense(units, activation=activations[i], input_shape=(1,)))
      else:
        model.add(Dense(units, activation=activations[i]))
    model.add(Dense(1, activation="linear"))

    # model.summary()

    model.compile(optimizer=optimizer, loss=loss)

    history = model.fit(x, 
                        epochs=epochs,
                        callbacks=[tensorboard, reduce_lr],
                        verbose=0)
    model.save(create_path(NAME+".h5", PATH = f"./models/{name_type}"))
    
    fig, ax = plt.subplots()
    ax.plot(x,model.predict(x),"--",color="r", label="RNA")
    ax.plot(x,sol_analitica(x),"-",color="b", label="Sol. analítica")
    ax.set_title(NAME)
    plt.legend()
    fig.savefig(create_path(NAME+".png",PATH = f"./img/{name_type}"))

