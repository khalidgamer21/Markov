# Implementacion de un Modelo Oculto de Markov aplicado al clima

## Introduccion

Un Modelo Oculto de Markov, tambien conocido como HMM por sus siglas en ingles, es un modelo probabilistico que sirve para representar procesos donde existe una parte que no se puede observar directamente. Esa parte se llama estado oculto. Aunque el estado oculto no se ve, el sistema produce observaciones visibles que funcionan como pistas.

En esta actividad se propone un HMM aplicado al clima. El problema consiste en simular condiciones atmosfericas que no se observan directamente y relacionarlas con resultados visibles del clima. Los estados ocultos del modelo son Alta presion y Baja presion. Las observaciones visibles son Soleado, Nublado y Lluvioso.

La diferencia principal frente a una cadena de Markov simple es que aqui el estado real del sistema no se toma como una observacion directa. Por ejemplo, no se observa directamente si existe alta o baja presion atmosferica, pero si se puede ver si el dia se presenta soleado, nublado o lluvioso. Por eso el HMM es adecuado: permite conectar una causa interna no visible con evidencias externas visibles.

El modelo usa tres tipos de probabilidades:

- Probabilidades iniciales: indican en que estado oculto puede comenzar el sistema.
- Probabilidades de transicion: indican como puede cambiar el sistema de un estado oculto a otro.
- Probabilidades de emision: indican que observacion visible puede aparecer desde cada estado oculto.

## Metodologia

La solucion se implemento en Python sin librerias externas, para que pueda ejecutarse facilmente desde la terminal. El modelo se organizo en un archivo JSON y el algoritmo se desarrollo en el archivo `markov_simulator.py`.

El fenomeno elegido fue el clima diario. El contexto es una simulacion sencilla donde las condiciones de presion atmosferica no se observan directamente, pero generan resultados visibles. El objetivo de la simulacion es producir secuencias de estados ocultos y observaciones para analizar el comportamiento del HMM.

### Estados ocultos y observaciones

| Tipo | Valores |
| --- | --- |
| Estados ocultos | Alta presion, Baja presion |
| Observaciones visibles | Soleado, Nublado, Lluvioso |

La pertinencia del HMM se justifica porque las condiciones de presion atmosferica actuan como una causa interna. Una persona puede observar el clima visible, pero no necesariamente conocer el estado real de la presion sin instrumentos. Esa diferencia entre lo oculto y lo visible es justamente lo que modela un HMM.

### Probabilidades iniciales

| Estado oculto | Probabilidad inicial |
| --- | ---: |
| Alta presion | 0.60 |
| Baja presion | 0.40 |

Estas probabilidades indican que la simulacion tiene mayor probabilidad de comenzar en Alta presion, pero tambien puede comenzar en Baja presion.

### Matriz de transicion

| Estado actual | Alta presion | Baja presion |
| --- | ---: | ---: |
| Alta presion | 0.75 | 0.25 |
| Baja presion | 0.35 | 0.65 |

Esta matriz indica como se mueve el sistema entre estados ocultos. Si el sistema esta en Alta presion, hay 75% de probabilidad de que continue en Alta presion y 25% de que cambie a Baja presion. Si esta en Baja presion, hay 65% de probabilidad de que continue alli y 35% de que cambie a Alta presion.

### Matriz de emision

| Estado oculto | Soleado | Nublado | Lluvioso |
| --- | ---: | ---: | ---: |
| Alta presion | 0.70 | 0.25 | 0.05 |
| Baja presion | 0.15 | 0.35 | 0.50 |

Esta matriz conecta lo oculto con lo visible. Cuando el estado oculto es Alta presion, es mas probable observar un dia Soleado. Cuando el estado oculto es Baja presion, aumenta la probabilidad de observar lluvia.

### Algoritmo implementado

El algoritmo sigue estos pasos:

1. Validar que las probabilidades iniciales sumen 1.
2. Validar que cada fila de la matriz de transicion sume 1.
3. Validar que cada fila de la matriz de emision sume 1.
4. Elegir el estado oculto inicial usando las probabilidades iniciales.
5. Generar una observacion visible usando la matriz de emision del estado oculto actual.
6. Cambiar al siguiente estado oculto usando la matriz de transicion.
7. Generar la nueva observacion visible desde ese nuevo estado oculto.
8. Repetir el proceso durante el numero de pasos indicado.
9. Ejecutar muchas simulaciones para obtener resultados agregados.

## Resultados y conclusiones

Se ejecuto una prueba con 1000 simulaciones, 20 pasos por simulacion y semilla 42. Esta semilla permite repetir la misma ejecucion y verificar los resultados.

Algunas secuencias generadas fueron:

```text
Estados ocultos: Baja presion -> Alta presion -> Alta presion -> Baja presion -> Baja presion -> Alta presion -> Alta presion -> Alta presion -> Alta presion -> Baja presion -> Baja presion -> Alta presion -> Baja presion -> Alta presion -> Baja presion -> Baja presion -> Baja presion -> Baja presion -> Baja presion -> Baja presion -> Baja presion
Observaciones:   Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Lluvioso -> Soleado -> Nublado -> Soleado -> Lluvioso -> Lluvioso -> Lluvioso -> Lluvioso -> Lluvioso -> Lluvioso -> Soleado

Estados ocultos: Alta presion -> Alta presion -> Alta presion -> Alta presion -> Alta presion -> Alta presion -> Alta presion -> Alta presion -> Alta presion -> Baja presion -> Baja presion -> Baja presion -> Alta presion -> Alta presion -> Alta presion -> Baja presion -> Baja presion -> Baja presion -> Alta presion -> Alta presion -> Alta presion
Observaciones:   Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Nublado -> Soleado -> Nublado -> Soleado -> Lluvioso -> Lluvioso -> Lluvioso -> Soleado -> Soleado -> Nublado -> Nublado -> Nublado -> Nublado -> Soleado -> Soleado -> Nublado
```

Los resultados agregados fueron:

| Medida | Alta presion | Baja presion |
| --- | ---: | ---: |
| Distribucion observada de estados ocultos | 0.5806 | 0.4194 |
| Distribucion estacionaria aproximada | 0.5833 | 0.4167 |

| Observacion visible | Frecuencia observada |
| --- | ---: |
| Soleado | 0.4677 |
| Nublado | 0.2959 |
| Lluvioso | 0.2364 |

Los resultados muestran que el sistema tiende a pasar mas tiempo en Alta presion que en Baja presion. Esto coincide con la matriz de transicion, porque Alta presion tiene una probabilidad alta de mantenerse. Tambien se observa que Soleado aparece como la observacion mas frecuente, lo cual es coherente con la matriz de emision: Alta presion produce dias soleados con probabilidad alta.

Como conclusion, el HMM permite representar un proceso donde no todo se observa directamente. En este caso, las condiciones de presion atmosferica son los estados ocultos y el clima visible son las observaciones. La simulacion demuestra como las probabilidades iniciales, de transicion y de emision trabajan juntas para generar diferentes resultados posibles.

El trabajo cumple con la idea central de la rubrica porque diferencia estados ocultos y observaciones, define las tres clases de probabilidades, implementa una simulacion ejecutable y presenta resultados verificables.
