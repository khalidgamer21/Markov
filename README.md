# Modelo Oculto de Markov

Este proyecto es una simulacion sencilla de un Modelo Oculto de Markov usando Python.

La idea fue representar una situacion donde el clima real no se observa directamente, pero si se pueden ver algunas pistas. Por ejemplo, si una persona lleva gafas, chaqueta o paraguas, eso puede dar una idea de si el clima oculto es soleado, nublado o lluvioso.

## Que contiene

El archivo principal es:

- `markov_simulator.py`

En ese archivo esta todo el codigo de la simulacion.

## Como funciona

El modelo trabaja con:

- Estados ocultos: `Soleado`, `Nublado` y `Lluvioso`.
- Observaciones visibles: `Gafas`, `Chaqueta` y `Paraguas`.

Primero el programa elige un estado inicial del clima. Luego, segun ese estado, genera una observacion visible. Despues cambia al siguiente estado usando las probabilidades de transicion y repite el proceso varias veces.

## Como ejecutarlo

Desde la carpeta del proyecto, ejecuta:

```bash
python markov_simulator.py
```

El programa muestra varias simulaciones y al final presenta un resumen con la frecuencia de los estados ocultos y de las observaciones visibles.

## Como cambiar los valores

Si quiero modificar la cantidad de pasos, simulaciones o la semilla, puedo cambiar estas lineas al final del archivo:

```python
pasos = 10
cantidad_simulaciones = 5
semilla = 42
```

Tambien puedo cambiar las probabilidades directamente en el codigo, en la probabilidad inicial, la matriz de transicion o la matriz de emision.

## Conclusion

Este modelo me permite ver como se pueden simular situaciones donde no se conoce directamente el estado real, pero si se observan pistas relacionadas con ese estado.
