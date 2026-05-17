# Guion breve para video de sustentacion

## 1. Presentacion del problema

En este trabajo implemente un Modelo Oculto de Markov aplicado al clima. La idea principal es que no siempre se observa directamente la condicion atmosferica que causa el clima, pero si se pueden observar resultados visibles como dias soleados, nublados o lluviosos.

## 2. Explicacion del HMM

Un HMM tiene estados ocultos y observaciones. Los estados ocultos son las condiciones reales del sistema, pero no se ven directamente. Las observaciones son las pistas visibles que produce el sistema.

En mi modelo, los estados ocultos son Alta presion y Baja presion. Las observaciones visibles son Soleado, Nublado y Lluvioso.

## 3. Matrices usadas

Use tres tipos de probabilidades.

Primero, la distribucion inicial: Alta presion tiene 0.60 y Baja presion tiene 0.40.

Segundo, la matriz de transicion: esta indica como cambia el sistema entre Alta presion y Baja presion.

Tercero, la matriz de emision: esta indica que clima visible puede aparecer dependiendo del estado oculto. Por ejemplo, si hay Alta presion, es mas probable observar un dia Soleado. Si hay Baja presion, aumenta la probabilidad de lluvia.

## 4. Simulacion

El programa elige un estado oculto inicial, genera una observacion visible y luego repite el proceso paso a paso. En cada paso cambia el estado oculto usando la matriz de transicion y genera una observacion usando la matriz de emision.

Ejecute 1000 simulaciones con 20 pasos cada una. El programa muestra secuencias de estados ocultos y observaciones visibles.

## 5. Resultados

Los resultados muestran que el sistema pasa mas tiempo en Alta presion. Tambien se observa que Soleado aparece con mayor frecuencia, lo cual tiene sentido porque Alta presion emite Soleado con probabilidad alta.

## 6. Conclusion

El HMM permite representar procesos donde existe informacion que no se observa directamente. En este caso, no se observa directamente la presion atmosferica, pero si el clima visible. El modelo logra conectar esas dos partes mediante probabilidades de transicion y emision.
