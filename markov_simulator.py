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
    Simula una secuencia de un Modelo Oculto de Markov.

    En cada paso:
    1. Se guarda el estado oculto actual.
    2. Se genera una observacion visible desde ese estado.
    3. Se cambia al siguiente estado oculto.
    """
    estado_actual = elegir_por_probabilidad(probabilidad_inicial)

    secuencia_estados = []
    secuencia_observaciones = []

    for _ in range(pasos):
        secuencia_estados.append(estado_actual)

        observacion = elegir_por_probabilidad(matriz_emision[estado_actual])
        secuencia_observaciones.append(observacion)

        estado_actual = elegir_por_probabilidad(matriz_transicion[estado_actual])

    return secuencia_estados, secuencia_observaciones


def imprimir_tabla_frecuencias(titulo, opciones, conteo, total):
    """
    Imprime porcentajes de forma clara y sencilla.
    """
    print(f"\n{titulo}")
    print("-" * len(titulo))

    for opcion in opciones:
        porcentaje = conteo[opcion] / total
        print(f"{opcion:<10} {porcentaje:>7.2%}")


def ejecutar_simulaciones(cantidad_simulaciones, pasos, semilla=42):
    """
    Ejecuta varias simulaciones para observar el comportamiento general
    del HMM.
    """
    validar_modelo()
    random.seed(semilla)

    conteo_estados = Counter()
    conteo_observaciones = Counter()

    print("SIMULACIONES DEL MODELO OCULTO DE MARKOV")
    print("=" * 44)
    print(f"Pasos por simulacion: {pasos}")
    print(f"Cantidad de simulaciones: {cantidad_simulaciones}")
    print(f"Semilla: {semilla}")

    for i in range(cantidad_simulaciones):
        estados, observaciones_visibles = simular_hmm(pasos)

        print(f"\nSimulacion {i + 1}")
        print("-" * 20)
        print("Estados ocultos:       ", " -> ".join(estados))
        print("Observaciones visibles:", " -> ".join(observaciones_visibles))

        conteo_estados.update(estados)
        conteo_observaciones.update(observaciones_visibles)

    total_estados = sum(conteo_estados.values())
    total_observaciones = sum(conteo_observaciones.values())

    print("\nRESUMEN GENERAL")
    print("=" * 15)

    imprimir_tabla_frecuencias(
        "Frecuencia de estados ocultos",
        estados_ocultos,
        conteo_estados,
        total_estados,
    )

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
