import random
from collections import Counter


# ============================================================
# MODELO OCULTO DE MARKOV - HMM
# ============================================================

# Estados ocultos: son el clima real, pero en este ejemplo no se observan
# directamente. El modelo los usa por dentro para decidir que puede pasar.
estados_ocultos = ["Soleado", "Nublado", "Lluvioso"]

# Observaciones visibles: son las pistas que si podemos ver.
# Por ejemplo, una persona puede llevar gafas, chaqueta o paraguas.
observaciones = ["Gafas", "Chaqueta", "Paraguas"]

# Probabilidad inicial: indica con que probabilidad empieza el clima
# en cada estado oculto.
probabilidad_inicial = {
    "Soleado": 0.50,
    "Nublado": 0.30,
    "Lluvioso": 0.20,
}

# Matriz de transicion: indica la probabilidad de pasar de un estado
# oculto a otro en el siguiente paso.
matriz_transicion = {
    "Soleado": {
        "Soleado": 0.65,
        "Nublado": 0.25,
        "Lluvioso": 0.10,
    },
    "Nublado": {
        "Soleado": 0.30,
        "Nublado": 0.45,
        "Lluvioso": 0.25,
    },
    "Lluvioso": {
        "Soleado": 0.20,
        "Nublado": 0.35,
        "Lluvioso": 0.45,
    },
}

# Matriz de emision: indica que observacion visible puede aparecer
# segun el estado oculto actual.
matriz_emision = {
    "Soleado": {
        "Gafas": 0.70,
        "Chaqueta": 0.20,
        "Paraguas": 0.10,
    },
    "Nublado": {
        "Gafas": 0.25,
        "Chaqueta": 0.50,
        "Paraguas": 0.25,
    },
    "Lluvioso": {
        "Gafas": 0.10,
        "Chaqueta": 0.25,
        "Paraguas": 0.65,
    },
}


def validar_distribucion(nombre, distribucion, opciones):
    """
    Revisa que una distribucion tenga todas las opciones esperadas,
    que no tenga probabilidades negativas y que sume 1.
    """
    if set(distribucion) != set(opciones):
        raise ValueError(f"{nombre} no tiene las mismas opciones del modelo.")

    if any(probabilidad < 0 for probabilidad in distribucion.values()):
        raise ValueError(f"{nombre} no puede tener probabilidades negativas.")

    total = sum(distribucion.values())
    if abs(total - 1) > 0.000001:
        raise ValueError(f"{nombre} debe sumar 1. Actualmente suma {total:.4f}.")


def validar_matriz(nombre, matriz, opciones):
    """
    Revisa todas las filas de una matriz de probabilidades.
    Asi evitamos repetir el mismo ciclo para transicion y emision.
    """
    for estado, fila in matriz.items():
        validar_distribucion(f"{nombre} de {estado}", fila, opciones)


def validar_modelo():
    """
    Valida las tres partes principales del HMM:
    probabilidad inicial, matriz de transicion y matriz de emision.
    """
    validar_distribucion("La probabilidad inicial", probabilidad_inicial, estados_ocultos)
    validar_matriz("La fila de transicion", matriz_transicion, estados_ocultos)
    validar_matriz("La fila de emision", matriz_emision, observaciones)


def elegir_por_probabilidad(distribucion):
    """
    Elige un elemento segun sus probabilidades.

    Si una opcion tiene una probabilidad alta, no significa que siempre
    saldra, pero si que tendra mas oportunidad de aparecer.
    """
    numero = random.random()
    acumulado = 0

    for elemento, probabilidad in distribucion.items():
        acumulado += probabilidad
        if numero <= acumulado:
            return elemento

    # Respaldo por si aparece una diferencia pequena por decimales.
    return elemento


def simular_hmm(pasos):
    """
    Aqui hago una simulacion completa del modelo.

    Yo parto de un estado inicial, por ejemplo Soleado, Nublado o Lluvioso.
    Despues, en cada paso, guardo ese estado, genero una observacion visible
    y paso al siguiente estado segun las probabilidades del modelo.
    """
    # Primero elijo como empieza la simulacion. No lo fijo manualmente,
    # sino que lo saco usando la probabilidad inicial.
    estado_actual = elegir_por_probabilidad(probabilidad_inicial)

    # En estas listas voy guardando el camino que siguio el modelo.
    # Una lista guarda el clima oculto y la otra guarda lo que se observo.
    secuencia_estados = []
    secuencia_observaciones = []

    for _ in range(pasos):
        # Guardo el estado oculto actual. Este seria el clima interno
        # que el modelo esta manejando en este momento.
        secuencia_estados.append(estado_actual)

        # Con el estado actual genero una pista visible.
        # Por ejemplo, si el estado es Lluvioso, es mas probable ver Paraguas.
        observacion = elegir_por_probabilidad(matriz_emision[estado_actual])
        secuencia_observaciones.append(observacion)

        # Despues cambio al siguiente estado usando la matriz de transicion.
        # Asi el clima puede quedarse igual o pasar a otro estado.
        estado_actual = elegir_por_probabilidad(matriz_transicion[estado_actual])

    # Devuelvo las dos secuencias para poder mostrarlas en pantalla.
    return secuencia_estados, secuencia_observaciones


def imprimir_tabla_frecuencias(titulo, opciones, conteo, total):
    """
    Aqui muestro el resumen final en porcentajes.

    Esta funcion no simula nada. Solo toma los conteos que ya tengo y los
    convierte en porcentajes para que el resultado sea mas facil de leer.
    """
    print(f"\n{titulo}")
    print("-" * len(titulo))

    for opcion in opciones:
        # Divido cuantas veces aparecio una opcion entre el total.
        # Asi puedo decir que porcentaje representa.
        porcentaje = conteo[opcion] / total
        print(f"{opcion:<10} {porcentaje:>7.2%}")


def ejecutar_simulaciones(cantidad_simulaciones, pasos, semilla=42):
    """
    Esta es la funcion que controla la ejecucion completa.

    Yo la uso para correr varias simulaciones, imprimir cada resultado y al
    final mostrar un resumen general de lo que paso.
    """
    # Antes de empezar, reviso que las probabilidades del modelo esten bien.
    validar_modelo()

    # La semilla permite repetir los mismos resultados.
    # Esto ayuda mucho cuando vamos a explicar la salida al profesor.
    random.seed(semilla)

    # Estos contadores me sirven para acumular cuantas veces aparece cada
    # estado oculto y cada observacion visible en todas las simulaciones.
    conteo_estados = Counter()
    conteo_observaciones = Counter()

    print("SIMULACIONES DEL MODELO OCULTO DE MARKOV")
    print("=" * 44)
    print(f"Pasos por simulacion: {pasos}")
    print(f"Cantidad de simulaciones: {cantidad_simulaciones}")
    print(f"Semilla: {semilla}")

    for i in range(cantidad_simulaciones):
        # Aqui ejecuto una simulacion individual.
        estados, observaciones_visibles = simular_hmm(pasos)

        # Muestro la simulacion en dos partes:
        # primero el clima oculto y luego las pistas visibles.
        print(f"\nSimulacion {i + 1}")
        print("-" * 20)
        print("Estados ocultos:       ", " -> ".join(estados))
        print("Observaciones visibles:", " -> ".join(observaciones_visibles))

        # Guardo los resultados en los contadores para sacar el resumen final.
        conteo_estados.update(estados)
        conteo_observaciones.update(observaciones_visibles)

    # Calculo el total de datos generados para poder sacar porcentajes.
    total_estados = sum(conteo_estados.values())
    total_observaciones = sum(conteo_observaciones.values())

    print("\nRESUMEN GENERAL")
    print("=" * 15)

    # Primero muestro que tanto aparecio cada clima oculto.
    imprimir_tabla_frecuencias(
        "Frecuencia de estados ocultos",
        estados_ocultos,
        conteo_estados,
        total_estados,
    )

    # Luego muestro que tanto aparecio cada observacion visible.
    imprimir_tabla_frecuencias(
        "Frecuencia de observaciones visibles",
        observaciones,
        conteo_observaciones,
        total_observaciones,
    )


# ============================================================
# EJECUCION DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    pasos = 10
    cantidad_simulaciones = 5
    semilla = 42

    ejecutar_simulaciones(cantidad_simulaciones, pasos, semilla)
