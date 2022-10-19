# Funciones y ecuaciones diferenciales
## Funciones
En todos los experimentos se utilizaron los valores epochs=500, loss=*mean absolute error* (*mae*), learning_rate=1e-3, optimizer=[Adam, RMSprop] y una reducción del learning rate hasta un mínimo de 1e-4.
### Inciso a)
Las imagenes resultantes de los experimentos se encuentran en *img/sin*, los modelos correspondientes en *models/sin* y los logs correspondientes para inicializar tensorboard en *logs/sin*.

![TensorBoard_viz_sin](./img/sin/TensorBoard.PNG)

Los mejores 3 modelos fueron:
- 10-Adam-tanh-tanh: 10 neuronas en cada capa, dos capas *tanh* y una *linear* de salida, optimizador Adam y error 0.004457.
- 30-Adam-tanh-tanh: 30 neuronas en cada capa, dos capas *tanh* y una *linear* de salida, optimizador Adam y error 0.0063576.
- 10-RMSprop-tanh-tanh: 10 neuronas en cada capa, dos capas *tanh* y una *linear* de salida, optimizador RMSprop y error 0.02013.

### Inciso b)
Las imagenes resultantes de los experimentos se encuentran en *img/poly*, los modelos correspondientes en *models/poly* y los logs correspondientes para inicializar tensorboard en *logs/poly*.

![TensorBoard_viz_poly](./img/poly/TensorBoard.PNG)

Los mejores 3 modelos fueron:
- 10-Adam-tanh-tanh: 10 neuronas en cada capa, dos capas *tanh* y una *linear* de salida, optimizador Adam y error 0.0027668.
- 10-RMSprop-tanh-tanh: 10 neuronas en cada capa, dos capas *tanh* y una *linear* de salida, optimizador RMSprop y error 0.01132.
- 60-Adam-tanh-tanh: 60 neuronas en cada capa, dos capas *tanh* y una *linear* de salida, optimizador Adam y error 0.06992.

### Nota
Las imagenes resultantes de los experimentos se encuentran en *img/sin_poly*, los modelos correspondientes en *models/sin_poly* y los logs correspondientes para inicializar tensorboard en *logs/sin_poly*.

![TensorBoard_viz_sin-poly](./img/sin_poly/TensorBoard.PNG)

Los mejores 3 modelos fueron:
- 10-Adam-tanh-tanh: 10 neuronas en cada capa, dos capas *tanh* y una *linear* de salida, optimizador Adam y error 0.0056924.
- 30-Adam-tanh-tanh: 30 neuronas en cada capa, dos capas *tanh* y una *linear* de salida, optimizador Adam y error 0.0067273.
- 60-Adam-tanh-tanh: 60 neuronas en cada capa, dos capas *tanh* y una *linear* de salida, optimizador Adam y error 0.0093344.

## Ecuaciones diferenciales

