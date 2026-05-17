# Implementacion de un Modelo Oculto de Markov

## Introduccion

Un Modelo Oculto de Markov permite representar procesos donde hay estados que no se observan directamente, pero que generan observaciones visibles.

En este caso, los estados ocultos son `Soleado`, `Nublado` y `Lluvioso`. Las observaciones visibles son `Gafas`, `Chaqueta` y `Paraguas`.

## Metodologia

Se definio una probabilidad inicial, una matriz de transicion entre estados ocultos y una matriz de emision para generar observaciones visibles.

El algoritmo elige el estado inicial, genera una observacion segun ese estado y luego cambia al siguiente estado usando la matriz de transicion. Este proceso se repite durante varios pasos y varias simulaciones.

## Resultados y conclusiones

El programa muestra las secuencias generadas y un resumen con la frecuencia de estados ocultos y observaciones visibles.

Se concluye que el HMM permite simular procesos donde no se conoce directamente el estado real, pero si se pueden observar pistas relacionadas con ese estado.
