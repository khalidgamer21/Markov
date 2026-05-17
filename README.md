# Simulacion de Modelo Oculto de Markov

Este repositorio contiene una implementacion en Python de un Modelo Oculto de Markov (HMM) aplicado al clima.

El ejemplo parte de una idea sencilla: no siempre podemos observar directamente la condicion atmosferica que causa el clima, pero si podemos observar pistas visibles como si el dia esta soleado, nublado o lluvioso.

## Problema

Se quiere simular el comportamiento del clima a partir de estados atmosfericos que no se observan directamente:

- Estados ocultos: `Alta presion` y `Baja presion`.
- Observaciones visibles: `Soleado`, `Nublado` y `Lluvioso`.

El modelo usa:

- Probabilidades iniciales: indican con que estado oculto empieza la simulacion.
- Matriz de transicion: indica como cambia el sistema entre estados ocultos.
- Matriz de emision: indica que observacion visible puede aparecer desde cada estado oculto.

## Archivos

- `markov_simulator.py`: algoritmo principal del HMM.
- `modelo_clima.json`: configuracion del modelo con estados, observaciones y matrices.
- `informe_markov.md`: informe de la actividad.
- `informe_hmm.docx`: version en Word del informe.
- `guion_video.md`: guion sugerido para la sustentacion.

## Requisitos

- Python 3.10 o superior.
- No requiere librerias externas.

## Ejecucion

```bash
python markov_simulator.py --steps 20 --simulations 1000 --seed 42
```

Tambien se puede ejecutar cargando el archivo JSON:

```bash
python markov_simulator.py --model modelo_clima.json --steps 20 --simulations 1000 --seed 42
```

## Parametros

- `--steps`: numero de transiciones por simulacion.
- `--simulations`: cantidad de simulaciones independientes.
- `--seed`: semilla opcional para repetir los mismos resultados.
- `--show-paths`: cantidad de secuencias de ejemplo que se muestran.
- `--model`: ruta a un archivo JSON con el HMM.

## Salida esperada

El programa muestra:

- Estados ocultos y observaciones visibles.
- Probabilidades iniciales.
- Matriz de transicion.
- Matriz de emision.
- Secuencias simuladas de estados ocultos y observaciones.
- Distribucion observada de estados ocultos.
- Distribucion observada de observaciones visibles.
- Distribucion estacionaria aproximada de los estados ocultos.

## Subir a GitHub

Desde esta carpeta se puede subir el proyecto a un repositorio remoto:

```bash
git remote add origin https://github.com/USUARIO/NOMBRE_REPOSITORIO.git
git push -u origin main
```
