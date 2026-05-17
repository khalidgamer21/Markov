# Modelo Oculto de Markov

Implementacion sencilla de un Modelo Oculto de Markov (HMM) en Python.

## Idea del modelo

El programa simula un clima oculto:

- Estados ocultos: `Soleado`, `Nublado`, `Lluvioso`.
- Observaciones visibles: `Gafas`, `Chaqueta`, `Paraguas`.

El modelo usa:

- Probabilidad inicial.
- Matriz de transicion.
- Matriz de emision.

## Archivo principal

- `markov_simulator.py`: contiene todo el codigo de la simulacion.

## Como ejecutar

```bash
python markov_simulator.py
```

El programa ejecuta 5 simulaciones de 10 pasos usando semilla `42`.

Para cambiar los valores, edita al final del archivo:

```python
pasos = 10
cantidad_simulaciones = 5
semilla = 42
```
