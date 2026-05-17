# Simulacion de Modelo Oculto de Markov

Este repositorio contiene una implementacion en Python de un Modelo Oculto de Markov (HMM) aplicado al clima.

El ejemplo parte de una idea sencilla: no siempre conocemos directamente el estado real del clima, pero si podemos observar pistas visibles, como si una persona usa gafas, chaqueta o paraguas.

## Problema

Se quiere simular el comportamiento del clima como un proceso oculto:

- Estados ocultos: `Soleado`, `Nublado` y `Lluvioso`.
- Observaciones visibles: `Gafas`, `Chaqueta` y `Paraguas`.

El modelo usa:

- Probabilidades iniciales: indican con que estado oculto empieza la simulacion.
- Matriz de transicion: indica como cambia el sistema entre estados ocultos.
- Matriz de emision: indica que observacion visible puede aparecer desde cada estado oculto.

## Archivos

- `markov_simulator.py`: algoritmo principal del HMM.
- `hmm_colab_interactivo.py`: version interactiva para Google Colab con widgets, tablas y graficas.
- `modelo_clima.json`: configuracion del modelo con estados, observaciones y matrices.
- `requirements.txt`: librerias necesarias para graficas e interfaz interactiva.
- `informe_markov.md`: informe de la actividad.
- `informe_hmm.docx`: version en Word del informe.
- `guion_video.md`: guion sugerido para la sustentacion.

## Requisitos

- Python 3.10 o superior.
- Para la ejecucion basica en terminal no requiere librerias externas.
- Para guardar graficas PNG desde terminal se necesita `matplotlib`.
- Para la version interactiva de Colab se usan `numpy`, `pandas`, `matplotlib`, `networkx` e `ipywidgets`, que normalmente ya estan disponibles en Google Colab.

Para instalar las librerias opcionales en tu computador:

```bash
pip install -r requirements.txt
```

## Ejecucion

### Opcion 1: terminal

```bash
python markov_simulator.py --steps 20 --simulations 1000 --seed 42
```

Tambien se puede ejecutar cargando el archivo JSON:

```bash
python markov_simulator.py --model modelo_clima.json --steps 20 --simulations 1000 --seed 42
```

Para guardar graficas reales en imagen:

```bash
python markov_simulator.py --model modelo_clima.json --steps 20 --simulations 1000 --seed 42 --save-plots
```

Esto crea la carpeta `graficos_resultados` con archivos PNG.

### Opcion 2: Google Colab

1. Abre Google Colab.
2. Crea un notebook nuevo.
3. Copia el contenido de `hmm_colab_interactivo.py` en una celda.
4. Ejecuta la celda.
5. Modifica los valores desde la interfaz y pulsa `Ejecutar simulacion`.

La version de Colab muestra:

- Tablas de estados ocultos, observaciones, matriz de transicion y matriz de emision.
- Diagrama de transiciones entre estados ocultos.
- Grafica de probabilidades de emision.
- Secuencias simuladas.
- Evolucion teorica de estados ocultos y observaciones visibles.
- Comparacion entre resultados teoricos y empiricos.

## Parametros

- `--steps`: numero de transiciones por simulacion.
- `--simulations`: cantidad de simulaciones independientes.
- `--seed`: semilla opcional para repetir los mismos resultados.
- `--show-paths`: cantidad de secuencias de ejemplo que se muestran.
- `--model`: ruta a un archivo JSON con el HMM.
- `--save-plots`: guarda graficas PNG con los resultados principales.
- `--plots-dir`: permite elegir la carpeta donde se guardan las graficas.

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
- Si se usa `--save-plots`, tambien guarda graficas en PNG.

## Subir a GitHub

Desde esta carpeta se puede subir el proyecto a un repositorio remoto:

```bash
git remote add origin https://github.com/USUARIO/NOMBRE_REPOSITORIO.git
git push -u origin main
```
