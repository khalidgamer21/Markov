import argparse
import json
import random
from collections import Counter
from typing import Dict, List, Sequence, Tuple


# Estos alias solo ayudan a leer mejor el codigo:
# un "Estado" es un texto como "Soleado", y una "MatrizTransicion"
# guarda las probabilidades de pasar de un estado a otro.
Estado = str
MatrizTransicion = Dict[Estado, Dict[Estado, float]]


MODELO_POR_DEFECTO = {
    "states": ["Soleado", "Nublado", "Lluvioso"],
    "transition_matrix": {
        "Soleado": {"Soleado": 0.65, "Nublado": 0.25, "Lluvioso": 0.10},
        "Nublado": {"Soleado": 0.30, "Nublado": 0.45, "Lluvioso": 0.25},
        "Lluvioso": {"Soleado": 0.20, "Nublado": 0.35, "Lluvioso": 0.45},
    },
    "initial_distribution": {"Soleado": 0.50, "Nublado": 0.30, "Lluvioso": 0.20},
}


def validar_distribucion(distribucion: Dict[Estado, float], estados: Sequence[Estado]) -> None:
    """Revisa que una lista de probabilidades tenga sentido.

    En palabras sencillas: cada estado debe aparecer una vez, ninguna
    probabilidad puede ser negativa y todas juntas deben sumar 1.
    """
    faltantes = set(estados) - set(distribucion)
    sobrantes = set(distribucion) - set(estados)
    if faltantes or sobrantes:
        raise ValueError(
            f"La distribucion no coincide con los estados. Faltan={faltantes}, sobran={sobrantes}"
        )

    total = sum(distribucion.values())
    if any(probabilidad < 0 for probabilidad in distribucion.values()):
        raise ValueError("Las probabilidades no pueden ser negativas.")
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Las probabilidades deben sumar 1. Suma actual={total:.6f}")


def validar_matriz_transicion(matriz: MatrizTransicion, estados: Sequence[Estado]) -> None:
    """Comprueba que la matriz tenga una fila valida para cada estado.

    Cada fila funciona como una pequena receta de probabilidades:
    si hoy estoy en ese estado, la fila dice a donde puedo ir despues.
    """
    if set(matriz) != set(estados):
        raise ValueError("La matriz de transicion debe tener una fila por cada estado.")
    for estado, fila in matriz.items():
        validar_distribucion(fila, estados)
        if not fila:
            raise ValueError(f"La fila de transicion para {estado} esta vacia.")


def elegir_estado_ponderado(distribucion: Dict[Estado, float], generador: random.Random) -> Estado:
    """Elige un estado respetando sus probabilidades.

    No todos los estados tienen la misma oportunidad de salir. Por eso
    no usamos una eleccion simple, sino una eleccion ponderada: los estados
    con mayor probabilidad aparecen con mas frecuencia.
    """
    punto_de_corte = generador.random()
    acumulado = 0.0
    ultimo_estado = next(reversed(distribucion))

    for estado, probabilidad in distribucion.items():
        acumulado += probabilidad
        if punto_de_corte <= acumulado:
            return estado

    # Esta linea casi nunca se usa; queda como respaldo por pequenos redondeos
    # de decimales cuando se trabaja con probabilidades.
    return ultimo_estado


def simular_cadena(
    estados: Sequence[Estado],
    matriz_transicion: MatrizTransicion,
    distribucion_inicial: Dict[Estado, float],
    pasos: int,
    generador: random.Random,
) -> List[Estado]:
    """Crea una sola historia posible del sistema.

    Por ejemplo, una trayectoria puede verse asi:
    Soleado -> Soleado -> Nublado -> Lluvioso
    """
    validar_distribucion(distribucion_inicial, estados)
    validar_matriz_transicion(matriz_transicion, estados)
    if pasos < 0:
        raise ValueError("El numero de pasos debe ser mayor o igual a cero.")

    estado_actual = elegir_estado_ponderado(distribucion_inicial, generador)
    trayectoria = [estado_actual]

    for _ in range(pasos):
        estado_actual = elegir_estado_ponderado(matriz_transicion[estado_actual], generador)
        trayectoria.append(estado_actual)

    return trayectoria


def ejecutar_experimentos(
    estados: Sequence[Estado],
    matriz_transicion: MatrizTransicion,
    distribucion_inicial: Dict[Estado, float],
    pasos: int,
    simulaciones: int,
    semilla: int | None,
) -> Tuple[List[List[Estado]], Dict[Estado, float], Dict[Estado, float]]:
    """Ejecuta muchas simulaciones para mirar el comportamiento general.

    Una sola simulacion puede ser curiosa, pero muchas simulaciones juntas
    muestran mejor la tendencia del modelo.
    """
    if simulaciones <= 0:
        raise ValueError("El numero de simulaciones debe ser mayor que cero.")

    generador = random.Random(semilla)
    trayectorias = [
        simular_cadena(estados, matriz_transicion, distribucion_inicial, pasos, generador)
        for _ in range(simulaciones)
    ]

    conteo_final = Counter(trayectoria[-1] for trayectoria in trayectorias)
    distribucion_final = {
        estado: conteo_final[estado] / simulaciones
        for estado in estados
    }

    conteo_visitas = Counter(estado for trayectoria in trayectorias for estado in trayectoria)
    total_visitas = sum(conteo_visitas.values())
    distribucion_visitas = {
        estado: conteo_visitas[estado] / total_visitas
        for estado in estados
    }

    return trayectorias, distribucion_final, distribucion_visitas


def calcular_distribucion_estacionaria(
    estados: Sequence[Estado],
    matriz_transicion: MatrizTransicion,
    iteraciones: int = 1000,
    tolerancia: float = 1e-12,
) -> Dict[Estado, float]:
    """Aproxima la mezcla estable del sistema a largo plazo.

    La idea es preguntar: si dejamos correr el modelo por mucho tiempo,
    que porcentaje del tiempo terminaria pasando en cada estado?
    """
    validar_matriz_transicion(matriz_transicion, estados)
    distribucion = {estado: 1 / len(estados) for estado in estados}

    for _ in range(iteraciones):
        actualizada = {estado: 0.0 for estado in estados}
        for origen in estados:
            for destino in estados:
                actualizada[destino] += distribucion[origen] * matriz_transicion[origen][destino]

        diferencia = max(abs(actualizada[estado] - distribucion[estado]) for estado in estados)
        distribucion = actualizada
        if diferencia < tolerancia:
            break

    return distribucion


def cargar_modelo(ruta: str | None) -> dict:
    """Carga el modelo desde un JSON o usa el ejemplo incluido en el codigo."""
    if ruta is None:
        return MODELO_POR_DEFECTO
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def imprimir_distribucion(titulo: str, distribucion: Dict[Estado, float]) -> None:
    """Muestra una distribucion en pantalla con cuatro decimales."""
    print(titulo)
    for estado, probabilidad in distribucion.items():
        print(f"  {estado}: {probabilidad:.4f}")


def principal() -> None:
    """Punto de entrada del programa cuando se ejecuta desde la terminal."""
    parser = argparse.ArgumentParser(
        description="Simulador de cadena de Markov para estados climaticos."
    )
    parser.add_argument("--model", help="Ruta a un archivo JSON con estados, matriz e inicial.")
    parser.add_argument("--steps", type=int, default=20, help="Numero de transiciones por simulacion.")
    parser.add_argument("--simulations", type=int, default=1000, help="Cantidad de simulaciones.")
    parser.add_argument("--seed", type=int, default=None, help="Semilla para reproducibilidad.")
    parser.add_argument("--show-paths", type=int, default=5, help="Cantidad de trayectorias a mostrar.")
    args = parser.parse_args()

    modelo = cargar_modelo(args.model)
    estados = modelo["states"]
    matriz_transicion = modelo["transition_matrix"]
    distribucion_inicial = modelo["initial_distribution"]

    trayectorias, distribucion_final, distribucion_visitas = ejecutar_experimentos(
        estados=estados,
        matriz_transicion=matriz_transicion,
        distribucion_inicial=distribucion_inicial,
        pasos=args.steps,
        simulaciones=args.simulations,
        semilla=args.seed,
    )
    estacionaria = calcular_distribucion_estacionaria(estados, matriz_transicion)

    print("Simulacion de cadena de Markov")
    print(f"Estados: {', '.join(estados)}")
    print(f"Pasos por simulacion: {args.steps}")
    print(f"Cantidad de simulaciones: {args.simulations}")
    if args.seed is not None:
        print(f"Semilla: {args.seed}")

    print("\nTrayectorias de ejemplo")
    for indice, trayectoria in enumerate(trayectorias[: args.show_paths], start=1):
        print(f"  {indice}. {' -> '.join(trayectoria)}")

    print()
    imprimir_distribucion("Distribucion del estado final:", distribucion_final)
    print()
    imprimir_distribucion("Distribucion de visitas durante toda la simulacion:", distribucion_visitas)
    print()
    imprimir_distribucion("Distribucion estacionaria aproximada:", estacionaria)


if __name__ == "__main__":
    principal()
