# Implementacion de un modelo de Markov usando distribuciones de probabilidad

## Introduccion

Las cadenas de Markov son modelos probabilisticos que permiten representar sistemas que evolucionan entre un conjunto finito de estados. Su caracteristica principal es que el siguiente estado depende del estado actual y de una distribucion de probabilidad asociada, no de toda la historia previa del sistema. Esta propiedad se conoce como propiedad de Markov.

En esta actividad se implemento una cadena de Markov discreta para simular el comportamiento del clima. El sistema tiene tres estados posibles: Soleado, Nublado y Lluvioso. Cada estado cuenta con probabilidades de transicion hacia los demas estados, representadas mediante una matriz de transicion. Al ejecutar varias simulaciones se obtienen diferentes trayectorias posibles y se observa como las frecuencias se aproximan a una distribucion estable.

La solucion propuesta aplica el conocimiento de las distribuciones de probabilidad porque cada paso de la simulacion se decide mediante una seleccion aleatoria ponderada. Por ejemplo, si el estado actual es Soleado, el algoritmo puede permanecer en Soleado o cambiar a Nublado o Lluvioso de acuerdo con las probabilidades definidas en la matriz.

## Metodologia

La solucion se diseno como una implementacion en Python sin dependencias externas, con el fin de que pueda ejecutarse facilmente en cualquier entorno con Python instalado.

El modelo utilizado contiene:

- Un conjunto de estados: Soleado, Nublado y Lluvioso.
- Una distribucion inicial, que define la probabilidad de iniciar la simulacion en cada estado.
- Una matriz de transicion, en la que cada fila contiene una distribucion de probabilidad valida que suma 1.
- Un numero de pasos por simulacion.
- Un numero de simulaciones independientes.

La matriz de transicion usada fue:

| Estado actual | Soleado | Nublado | Lluvioso |
| --- | ---: | ---: | ---: |
| Soleado | 0.65 | 0.25 | 0.10 |
| Nublado | 0.30 | 0.45 | 0.25 |
| Lluvioso | 0.20 | 0.35 | 0.45 |

La distribucion inicial fue:

| Estado | Probabilidad inicial |
| --- | ---: |
| Soleado | 0.50 |
| Nublado | 0.30 |
| Lluvioso | 0.20 |

El algoritmo implementado sigue estos pasos:

1. Validar que la distribucion inicial y cada fila de la matriz de transicion sumen 1.
2. Seleccionar el estado inicial usando una distribucion de probabilidad ponderada.
3. Para cada paso, consultar la fila de la matriz correspondiente al estado actual.
4. Seleccionar el siguiente estado mediante una nueva eleccion ponderada.
5. Guardar la trayectoria completa de estados.
6. Repetir el proceso muchas veces para obtener resultados agregados.
7. Calcular la distribucion del estado final y la distribucion de visitas.
8. Aproximar la distribucion estacionaria multiplicando iterativamente una distribucion por la matriz de transicion.

La implementacion permite cambiar los parametros desde la terminal. Tambien permite cargar un archivo JSON con otro conjunto de estados, otra matriz de transicion y otra distribucion inicial.

## Resultados y conclusiones

Se ejecuto una prueba con 1000 simulaciones, 20 pasos por simulacion y semilla 42 para obtener resultados reproducibles. Algunas trayectorias generadas fueron:

```text
Nublado -> Soleado -> Soleado -> Soleado -> Nublado -> Nublado -> Lluvioso -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Nublado -> Soleado -> Nublado
Nublado -> Nublado -> Soleado -> Lluvioso -> Nublado -> Soleado -> Soleado -> Nublado -> Nublado -> Lluvioso -> Lluvioso -> Nublado -> Lluvioso -> Nublado -> Nublado -> Lluvioso -> Lluvioso -> Lluvioso -> Lluvioso -> Lluvioso -> Soleado
Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Soleado -> Lluvioso -> Lluvioso -> Lluvioso -> Soleado -> Nublado -> Soleado -> Soleado -> Lluvioso -> Lluvioso -> Lluvioso
```

Los resultados agregados de esa ejecucion fueron:

| Medida | Soleado | Nublado | Lluvioso |
| --- | ---: | ---: | ---: |
| Distribucion del estado final | 0.4120 | 0.3410 | 0.2470 |
| Distribucion de visitas | 0.4308 | 0.3356 | 0.2336 |
| Distribucion estacionaria aproximada | 0.4257 | 0.3416 | 0.2327 |

Los resultados muestran que, aunque cada simulacion individual puede producir una trayectoria diferente, el comportamiento agregado tiende a estabilizarse. La distribucion de visitas observada se aproxima a la distribucion estacionaria calculada, especialmente cuando se aumenta el numero de simulaciones y pasos.

Como conclusion, el modelo de Markov permite representar sistemas donde existe incertidumbre y donde las decisiones futuras dependen probabilisticamente del estado presente. La implementacion demuestra que las distribuciones de probabilidad son esenciales para definir tanto el estado inicial como las transiciones. Ademas, ejecutar muchas simulaciones permite analizar patrones generales, no solo trayectorias individuales.

El codigo fuente quedo organizado para ser incluido en un repositorio de GitHub junto con este documento y el archivo de configuracion del modelo.
