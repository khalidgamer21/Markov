# Simulacion de cadena de Markov

Este repositorio contiene una implementacion en Python de una cadena de Markov discreta aplicada a un ejemplo de clima. El modelo usa distribuciones de probabilidad para seleccionar el estado inicial y las transiciones entre estados.

## Archivos

- `markov_simulator.py`: algoritmo principal de simulacion.
- `modelo_clima.json`: configuracion del modelo de ejemplo.
- `informe_markov.md`: documento de la actividad con introduccion, metodologia, resultados y conclusiones.

## Requisitos

- Python 3.10 o superior.
- No requiere librerias externas.

## Ejecucion

```bash
python markov_simulator.py --steps 20 --simulations 1000 --seed 42
```

Tambien se puede ejecutar con el archivo JSON:

```bash
python markov_simulator.py --model modelo_clima.json --steps 20 --simulations 1000 --seed 42
```

## Parametros

- `--steps`: numero de transiciones por simulacion.
- `--simulations`: cantidad de simulaciones independientes.
- `--seed`: semilla opcional para obtener resultados reproducibles.
- `--show-paths`: cantidad de trayectorias de ejemplo que se muestran.
- `--model`: ruta a un archivo JSON con estados, matriz de transicion y distribucion inicial.

## Subir a GitHub

Desde esta carpeta se puede crear el repositorio local y subirlo a GitHub:

```bash
git init
git add .
git commit -m "Implementar simulador de Markov"
git branch -M main
git remote add origin https://github.com/USUARIO/NOMBRE_REPOSITORIO.git
git push -u origin main
```
