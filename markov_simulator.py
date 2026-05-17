import argparse
import json
import random
from collections import Counter
from typing import Dict, List, Sequence, Tuple


# En un Modelo Oculto de Markov hay dos mundos:
# - El estado oculto: lo que realmente pasa, pero no vemos directamente.
# - La observacion: la pista visible que si podemos registrar.
EstadoOculto = str
Observacion = str
Distribucion = Dict[str, float]
MatrizTransicion = Dict[EstadoOculto, Dict[EstadoOculto, float]]
MatrizEmision = Dict[EstadoOculto, Dict[Observacion, float]]


MODELO_POR_DEFECTO = {
    "hidden_states": ["Soleado", "Nublado", "Lluvioso"],
    "observations": ["Gafas", "Chaqueta", "Paraguas"],
    "initial_distribution": {
        "Soleado": 0.50,
        "Nublado": 0.30,
        "Lluvioso": 0.20,
    },
    "transition_matrix": {
        "Soleado": {"Soleado": 0.65, "Nublado": 0.25, "Lluvioso": 0.10},
        "Nublado": {"Soleado": 0.30, "Nublado": 0.45, "Lluvioso": 0.25},
        "Lluvioso": {"Soleado": 0.20, "Nublado": 0.35, "Lluvioso": 0.45},
    },
    "emission_matrix": {
        "Soleado": {"Gafas": 0.70, "Chaqueta": 0.20, "Paraguas": 0.10},
        "Nublado": {"Gafas": 0.25, "Chaqueta": 0.50, "Paraguas": 0.25},
        "Lluvioso": {"Gafas": 0.10, "Chaqueta": 0.25, "Paraguas": 0.65},
    },
}


def validar_distribucion(distribucion: Distribucion, opciones: Sequence[str]) -> None:
    """Revisa que una distribucion sea usable.

    Dicho de forma simple: deben aparecer todas las opciones, no puede
    haber probabilidades negativas y el total debe sumar 1, es decir, 100%.
    """
    faltantes = set(opciones) - set(distribucion)
    sobrantes = set(distribucion) - set(opciones)
    if faltantes or sobrantes:
        raise ValueError(
            f"La distribucion no coincide con las opciones. Faltan={faltantes}, sobran={sobrantes}"
        )

    total = sum(distribucion.values())
    if any(probabilidad < 0 for probabilidad in distribucion.values()):
        raise ValueError("Las probabilidades no pueden ser negativas.")
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"Las probabilidades deben sumar 1. Suma actual={total:.6f}")


def validar_matriz_transicion(
    matriz: MatrizTransicion,
    estados_ocultos: Sequence[EstadoOculto],
) -> None:
    """Valida como se mueve el proceso entre estados ocultos.

    Esta matriz responde una pregunta concreta: si el sistema esta en un
    estado oculto hoy, que tan probable es que siga o cambie en el siguiente
    paso?
    """
    if set(matriz) != set(estados_ocultos):
        raise ValueError("La matriz de transicion debe tener una fila por cada estado oculto.")

    for estado, fila in matriz.items():
        validar_distribucion(fila, estados_ocultos)
        if not fila:
            raise ValueError(f"La fila de transicion para {estado} esta vacia.")


def validar_matriz_emision(
    matriz: MatrizEmision,
    estados_ocultos: Sequence[EstadoOculto],
    observaciones: Sequence[Observacion],
) -> None:
    """Valida las pistas visibles que puede producir cada estado oculto.

    En un HMM no vemos directamente el estado oculto. Lo que vemos son
    observaciones. Por eso esta matriz dice que puede observarse cuando el
    sistema esta en cada estado oculto.
    """
    if set(matriz) != set(estados_ocultos):
        raise ValueError("La matriz de emision debe tener una fila por cada estado oculto.")

    for estado, fila in matriz.items():
        validar_distribucion(fila, observaciones)
        if not fila:
            raise ValueError(f"La fila de emision para {estado} esta vacia.")


def elegir_opcion_ponderada(distribucion: Distribucion, generador: random.Random) -> str:
    """Elige una opcion respetando sus probabilidades.

    Si una opcion tiene 70% de probabilidad, no significa que siempre salga;
    significa que, al repetir muchas veces, deberia aparecer con mas frecuencia
    que las opciones con probabilidades menores.
    """
    punto_de_corte = generador.random()
    acumulado = 0.0
    ultima_opcion = next(reversed(distribucion))

    for opcion, probabilidad in distribucion.items():
        acumulado += probabilidad
        if punto_de_corte <= acumulado:
            return opcion

    # Respaldo por si aparece una pequena diferencia decimal al sumar.
    return ultima_opcion


def validar_modelo(modelo: dict) -> None:
    """Comprueba que el HMM tenga todas sus piezas importantes."""
    estados_ocultos = modelo["hidden_states"]
    observaciones = modelo["observations"]

    validar_distribucion(modelo["initial_distribution"], estados_ocultos)
    validar_matriz_transicion(modelo["transition_matrix"], estados_ocultos)
    validar_matriz_emision(modelo["emission_matrix"], estados_ocultos, observaciones)


def simular_hmm(
    estados_ocultos: Sequence[EstadoOculto],
    observaciones: Sequence[Observacion],
    distribucion_inicial: Dict[EstadoOculto, float],
    matriz_transicion: MatrizTransicion,
    matriz_emision: MatrizEmision,
    pasos: int,
    generador: random.Random,
) -> Tuple[List[EstadoOculto], List[Observacion]]:
    """Crea una historia posible del HMM.

    Primero se elige el estado oculto. Luego, desde ese estado oculto, se
    genera una observacion visible. Ese par se repite paso a paso.
    """
    if pasos < 0:
        raise ValueError("El numero de pasos debe ser mayor o igual a cero.")

    validar_distribucion(distribucion_inicial, estados_ocultos)
    validar_matriz_transicion(matriz_transicion, estados_ocultos)
    validar_matriz_emision(matriz_emision, estados_ocultos, observaciones)

    estado_actual = elegir_opcion_ponderada(distribucion_inicial, generador)
    secuencia_estados = [estado_actual]
    secuencia_observaciones = [
        elegir_opcion_ponderada(matriz_emision[estado_actual], generador)
    ]

    for _ in range(pasos):
        estado_actual = elegir_opcion_ponderada(matriz_transicion[estado_actual], generador)
        observacion = elegir_opcion_ponderada(matriz_emision[estado_actual], generador)

        secuencia_estados.append(estado_actual)
        secuencia_observaciones.append(observacion)

    return secuencia_estados, secuencia_observaciones


def ejecutar_experimentos(
    modelo: dict,
    pasos: int,
    simulaciones: int,
    semilla: int | None,
) -> Tuple[
    List[Tuple[List[EstadoOculto], List[Observacion]]],
    Dict[EstadoOculto, float],
    Dict[Observacion, float],
]:
    """Ejecuta muchas simulaciones para ver el comportamiento general.

    Una simulacion muestra una historia posible. Muchas simulaciones ayudan
    a ver si el modelo se comporta como esperamos.
    """
    if simulaciones <= 0:
        raise ValueError("El numero de simulaciones debe ser mayor que cero.")

    validar_modelo(modelo)
    generador = random.Random(semilla)
    resultados = [
        simular_hmm(
            estados_ocultos=modelo["hidden_states"],
            observaciones=modelo["observations"],
            distribucion_inicial=modelo["initial_distribution"],
            matriz_transicion=modelo["transition_matrix"],
            matriz_emision=modelo["emission_matrix"],
            pasos=pasos,
            generador=generador,
        )
        for _ in range(simulaciones)
    ]

    conteo_estados = Counter(
        estado
        for secuencia_estados, _ in resultados
        for estado in secuencia_estados
    )
    total_estados = sum(conteo_estados.values())
    distribucion_estados = {
        estado: conteo_estados[estado] / total_estados
        for estado in modelo["hidden_states"]
    }

    conteo_observaciones = Counter(
        observacion
        for _, secuencia_observaciones in resultados
        for observacion in secuencia_observaciones
    )
    total_observaciones = sum(conteo_observaciones.values())
    distribucion_observaciones = {
        observacion: conteo_observaciones[observacion] / total_observaciones
        for observacion in modelo["observations"]
    }

    return resultados, distribucion_estados, distribucion_observaciones


def calcular_distribucion_estacionaria(
    estados_ocultos: Sequence[EstadoOculto],
    matriz_transicion: MatrizTransicion,
    iteraciones: int = 1000,
    tolerancia: float = 1e-12,
) -> Dict[EstadoOculto, float]:
    """Aproxima la distribucion estable de los estados ocultos.

    Sirve para entender donde tiende a pasar mas tiempo el proceso si se
    deja avanzar durante muchos pasos.
    """
    validar_matriz_transicion(matriz_transicion, estados_ocultos)
    distribucion = {estado: 1 / len(estados_ocultos) for estado in estados_ocultos}

    for _ in range(iteraciones):
        actualizada = {estado: 0.0 for estado in estados_ocultos}
        for origen in estados_ocultos:
            for destino in estados_ocultos:
                actualizada[destino] += distribucion[origen] * matriz_transicion[origen][destino]

        diferencia = max(abs(actualizada[estado] - distribucion[estado]) for estado in estados_ocultos)
        distribucion = actualizada
        if diferencia < tolerancia:
            break

    return distribucion


def cargar_modelo(ruta: str | None) -> dict:
    """Carga el HMM desde un JSON o usa el modelo de ejemplo incluido."""
    if ruta is None:
        return MODELO_POR_DEFECTO
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def linea(ancho: int = 78, caracter: str = "=") -> str:
    """Crea una linea separadora para que la salida respire mejor."""
    return caracter * ancho


def imprimir_titulo(titulo: str) -> None:
    """Muestra el titulo principal de la ejecucion."""
    print(linea())
    print(titulo.center(78))
    print(linea())


def imprimir_seccion(titulo: str) -> None:
    """Separa visualmente cada parte del resultado."""
    print()
    print(titulo)
    print(linea(len(titulo), "-"))


def barra_porcentaje(probabilidad: float, ancho: int = 24) -> str:
    """Convierte una probabilidad en una barra sencilla de leer."""
    llenos = round(probabilidad * ancho)
    vacios = ancho - llenos
    return "#" * llenos + "." * vacios


def imprimir_tabla(encabezados: Sequence[str], filas: Sequence[Sequence[str]]) -> None:
    """Imprime una tabla alineada sin necesitar librerias externas."""
    anchos = [
        max(len(str(encabezados[indice])), *(len(str(fila[indice])) for fila in filas))
        for indice in range(len(encabezados))
    ]

    def formatear_fila(valores: Sequence[str]) -> str:
        celdas = [
            str(valor).ljust(anchos[indice])
            for indice, valor in enumerate(valores)
        ]
        return "| " + " | ".join(celdas) + " |"

    separador = "+-" + "-+-".join("-" * ancho for ancho in anchos) + "-+"
    print(separador)
    print(formatear_fila(encabezados))
    print(separador)
    for fila in filas:
        print(formatear_fila(fila))
    print(separador)


def imprimir_distribucion(titulo: str, distribucion: Dict[str, float]) -> None:
    """Imprime probabilidades como tabla y con barra visual."""
    imprimir_seccion(titulo)
    filas = [
        [
            opcion,
            f"{probabilidad:.4f}",
            f"{probabilidad * 100:6.2f}%",
            barra_porcentaje(probabilidad),
        ]
        for opcion, probabilidad in distribucion.items()
    ]
    imprimir_tabla(["Opcion", "Prob.", "Porcentaje", "Grafico"], filas)


def imprimir_matriz(titulo: str, matriz: Dict[str, Dict[str, float]]) -> None:
    """Muestra una matriz de probabilidades con formato de tabla."""
    imprimir_seccion(titulo)
    columnas = list(next(iter(matriz.values())).keys())
    filas = [
        [fila] + [f"{matriz[fila][columna]:.2f}" for columna in columnas]
        for fila in matriz
    ]
    imprimir_tabla(["Desde / Estado"] + columnas, filas)


def imprimir_resumen(modelo: dict, pasos: int, simulaciones: int, semilla: int | None) -> None:
    """Muestra los datos generales de la corrida."""
    imprimir_titulo("Simulacion de Modelo Oculto de Markov (HMM)")
    filas = [
        ["Estados ocultos", ", ".join(modelo["hidden_states"])],
        ["Observaciones visibles", ", ".join(modelo["observations"])],
        ["Pasos por simulacion", str(pasos)],
        ["Cantidad de simulaciones", str(simulaciones)],
        ["Semilla", str(semilla) if semilla is not None else "No definida"],
    ]
    imprimir_tabla(["Dato", "Valor"], filas)


def imprimir_secuencias(
    resultados: List[Tuple[List[EstadoOculto], List[Observacion]]],
    cantidad: int,
) -> None:
    """Muestra algunas secuencias paso a paso.

    Asi evitamos una linea larguisima y queda mas facil explicar que en cada
    paso existe un estado oculto y una observacion visible.
    """
    imprimir_seccion("Secuencias de ejemplo")
    for indice, (secuencia_estados, secuencia_observaciones) in enumerate(
        resultados[:cantidad],
        start=1,
    ):
        print(f"Simulacion {indice}")
        filas = [
            [str(paso), estado, observacion]
            for paso, (estado, observacion) in enumerate(
                zip(secuencia_estados, secuencia_observaciones)
            )
        ]
        imprimir_tabla(
            ["Paso", "Estado oculto", "Observacion visible"],
            filas,
        )
        print()


def principal() -> None:
    """Punto de entrada cuando el archivo se ejecuta desde la terminal."""
    parser = argparse.ArgumentParser(
        description="Simulador de Modelo Oculto de Markov con clima oculto y observaciones visibles."
    )
    parser.add_argument("--model", help="Ruta a un archivo JSON con el HMM.")
    parser.add_argument("--steps", type=int, default=20, help="Numero de transiciones por simulacion.")
    parser.add_argument("--simulations", type=int, default=1000, help="Cantidad de simulaciones.")
    parser.add_argument("--seed", type=int, default=None, help="Semilla para repetir resultados.")
    parser.add_argument("--show-paths", type=int, default=5, help="Cantidad de secuencias a mostrar.")
    args = parser.parse_args()

    modelo = cargar_modelo(args.model)
    resultados, distribucion_estados, distribucion_observaciones = ejecutar_experimentos(
        modelo=modelo,
        pasos=args.steps,
        simulaciones=args.simulations,
        semilla=args.seed,
    )
    estacionaria = calcular_distribucion_estacionaria(
        modelo["hidden_states"],
        modelo["transition_matrix"],
    )

    imprimir_resumen(modelo, args.steps, args.simulations, args.seed)
    imprimir_distribucion("Probabilidades iniciales:", modelo["initial_distribution"])
    imprimir_matriz("Matriz de transicion:", modelo["transition_matrix"])
    imprimir_matriz("Matriz de emision:", modelo["emission_matrix"])
    imprimir_secuencias(resultados, args.show_paths)
    imprimir_distribucion("Distribucion observada de estados ocultos:", distribucion_estados)
    imprimir_distribucion("Distribucion observada de observaciones visibles:", distribucion_observaciones)
    imprimir_distribucion("Distribucion estacionaria aproximada de estados ocultos:", estacionaria)


if __name__ == "__main__":
    principal()
