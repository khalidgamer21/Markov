# ============================================================
# Simulacion interactiva de un Modelo Oculto de Markov (HMM)
# Para Google Colab
#
# Caso: clima visible generado por estados atmosfericos ocultos
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import ipywidgets as widgets
from IPython.display import display, clear_output


# Activar widgets en Google Colab.
# Si el codigo se ejecuta fuera de Colab, simplemente continua sin problema.
try:
    from google.colab import output

    output.enable_custom_widget_manager()
except Exception:
    pass


# ============================================================
# Funciones para leer y validar datos
# ============================================================

def leer_lista(texto):
    """
    Lee elementos escritos uno por linea.

    Sirve tanto para estados ocultos como para observaciones visibles.
    """
    return [elemento.strip() for elemento in texto.splitlines() if elemento.strip()]


def leer_matriz(texto):
    """
    Lee una matriz escrita por filas.

    Cada fila puede escribirse con comas, espacios o punto y coma.
    """
    filas = []

    for linea in texto.splitlines():
        linea = linea.strip()
        if not linea:
            continue

        linea = linea.replace(";", ",")
        partes = [x.strip() for x in linea.replace(" ", ",").split(",") if x.strip()]
        filas.append([float(x) for x in partes])

    return np.array(filas, dtype=float)


def validar_distribucion(nombre, valores, opciones):
    """
    Valida una distribucion de probabilidad.

    En palabras simples: no puede tener valores negativos y debe sumar 1.
    """
    if len(valores) != len(opciones):
        raise ValueError(
            f"{nombre} debe tener {len(opciones)} valores, uno por cada opcion."
        )

    if np.any(valores < 0):
        raise ValueError(f"{nombre} no puede tener probabilidades negativas.")

    if not np.isclose(valores.sum(), 1):
        raise ValueError(
            f"{nombre} debe sumar 1. Actualmente suma {valores.sum():.4f}."
        )


def validar_matriz(nombre, matriz, filas, columnas):
    """
    Valida una matriz de probabilidades.

    Cada fila debe sumar 1 porque representa una decision probabilistica.
    """
    forma_esperada = (len(filas), len(columnas))

    if matriz.shape != forma_esperada:
        raise ValueError(
            f"{nombre} debe tener tamano {forma_esperada}. Actualmente tiene {matriz.shape}."
        )

    if np.any(matriz < 0):
        raise ValueError(f"{nombre} no puede tener probabilidades negativas.")

    sumas = matriz.sum(axis=1)
    if not np.allclose(sumas, 1):
        display(pd.DataFrame({
            "Fila": filas,
            "Suma": sumas,
        }))
        raise ValueError(f"Cada fila de {nombre} debe sumar 1.")


def validar_hmm(estados_ocultos, observaciones, pi, A, B):
    """
    Revisa que el HMM tenga sentido antes de simular.
    """
    if not estados_ocultos:
        raise ValueError("Debes escribir al menos un estado oculto.")

    if not observaciones:
        raise ValueError("Debes escribir al menos una observacion visible.")

    validar_distribucion("La distribucion inicial", pi, estados_ocultos)
    validar_matriz("La matriz de transicion", A, estados_ocultos, estados_ocultos)
    validar_matriz("La matriz de emision", B, estados_ocultos, observaciones)


# ============================================================
# Simulacion y calculos del HMM
# ============================================================

def simular_hmm(estados_ocultos, observaciones, pi, A, B, pasos, num_simulaciones, semilla):
    """
    Simula varias trayectorias de un Modelo Oculto de Markov.

    Devuelve dos arreglos:
    - Trayectorias de estados ocultos.
    - Trayectorias de observaciones visibles.
    """
    rng = np.random.default_rng(semilla)
    n_estados = len(estados_ocultos)
    n_observaciones = len(observaciones)

    trayectorias_ocultas = []
    trayectorias_observadas = []

    for _ in range(num_simulaciones):
        estado_actual = rng.choice(n_estados, p=pi)
        trayectoria_oculta = [estado_actual]
        trayectoria_observada = [rng.choice(n_observaciones, p=B[estado_actual])]

        for _ in range(pasos):
            estado_actual = rng.choice(n_estados, p=A[estado_actual])
            observacion = rng.choice(n_observaciones, p=B[estado_actual])

            trayectoria_oculta.append(estado_actual)
            trayectoria_observada.append(observacion)

        trayectorias_ocultas.append(trayectoria_oculta)
        trayectorias_observadas.append(trayectoria_observada)

    return np.array(trayectorias_ocultas), np.array(trayectorias_observadas)


def evolucion_teorica_estados(pi, A, pasos):
    """
    Calcula como cambia la distribucion teorica de estados ocultos.

    Formula usada: pi_{t+1} = pi_t A
    """
    distribucion = pi.copy()
    evolucion = [distribucion.copy()]

    for _ in range(pasos):
        distribucion = distribucion @ A
        evolucion.append(distribucion.copy())

    return np.array(evolucion)


def evolucion_teorica_observaciones(evolucion_estados, B):
    """
    Calcula la probabilidad teorica de observar cada clima visible.

    Si conocemos la probabilidad de cada estado oculto en un paso, podemos
    combinarla con la matriz de emision para estimar las observaciones.
    """
    return evolucion_estados @ B


def distribucion_empirica(trayectorias, cantidad_opciones):
    """
    Calcula la frecuencia relativa del ultimo valor de cada simulacion.
    """
    finales = trayectorias[:, -1]
    conteos = pd.Series(finales).value_counts(normalize=True).sort_index()
    return np.array([conteos.get(i, 0) for i in range(cantidad_opciones)])


# ============================================================
# Graficas
# ============================================================

def graficar_diagrama_transicion(estados_ocultos, A, umbral=0.01):
    """
    Dibuja el diagrama de transiciones entre estados ocultos.
    """
    G = nx.DiGraph()

    for estado in estados_ocultos:
        G.add_node(estado)

    for i, origen in enumerate(estados_ocultos):
        for j, destino in enumerate(estados_ocultos):
            probabilidad = A[i, j]
            if probabilidad >= umbral:
                G.add_edge(origen, destino, label=f"{probabilidad:.2f}")

    plt.figure(figsize=(7, 5))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2800,
        node_color="#D7EAFB",
        edge_color="#555555",
        font_size=10,
        arrows=True,
        arrowsize=20,
    )
    etiquetas = nx.get_edge_attributes(G, "label")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas, font_size=9)
    plt.title("Transiciones entre estados ocultos")
    plt.show()


def graficar_emisiones(estados_ocultos, observaciones, B):
    """
    Grafica que observaciones puede emitir cada estado oculto.
    """
    df = pd.DataFrame(B, index=estados_ocultos, columns=observaciones)
    df.plot(kind="bar", figsize=(9, 5))
    plt.title("Probabilidades de emision")
    plt.xlabel("Estado oculto")
    plt.ylabel("Probabilidad")
    plt.ylim(0, 1)
    plt.grid(axis="y")
    plt.xticks(rotation=0)
    plt.legend(title="Observacion visible")
    plt.show()


def graficar_evolucion(titulo, etiquetas, evolucion, eje_y):
    """
    Grafica como cambian probabilidades teoricas paso a paso.
    """
    plt.figure(figsize=(9, 5))

    for i, etiqueta in enumerate(etiquetas):
        plt.plot(evolucion[:, i], marker="o", label=etiqueta)

    plt.xlabel("Paso")
    plt.ylabel(eje_y)
    plt.title(titulo)
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(True)
    plt.show()


def graficar_barras(titulo, etiquetas, valores):
    """
    Grafica una distribucion final como barras.
    """
    plt.figure(figsize=(8, 5))
    plt.bar(etiquetas, valores, color="#6FA8DC")
    plt.xlabel("Categoria")
    plt.ylabel("Frecuencia relativa")
    plt.title(titulo)
    plt.ylim(0, 1)
    plt.grid(axis="y")
    plt.show()


# ============================================================
# Interfaz interactiva
# ============================================================

estilo = {"description_width": "115px"}
layout_largo = widgets.Layout(width="520px")
layout_textarea_chico = widgets.Layout(width="520px", height="90px")
layout_textarea_medio = widgets.Layout(width="520px", height="110px")

estados_widget = widgets.Textarea(
    value="""Alta presion
Baja presion""",
    description="Estados:",
    layout=layout_textarea_chico,
    style=estilo,
)

observaciones_widget = widgets.Textarea(
    value="""Soleado
Nublado
Lluvioso""",
    description="Observaciones:",
    layout=layout_textarea_medio,
    style=estilo,
)

inicial_widget = widgets.Text(
    value="0.60, 0.40",
    description="Inicial:",
    layout=layout_largo,
    style=estilo,
)

transicion_widget = widgets.Textarea(
    value="""0.75, 0.25
0.35, 0.65""",
    description="Transicion:",
    layout=layout_textarea_chico,
    style=estilo,
)

emision_widget = widgets.Textarea(
    value="""0.70, 0.25, 0.05
0.15, 0.35, 0.50""",
    description="Emision:",
    layout=layout_textarea_chico,
    style=estilo,
)

pasos_widget = widgets.IntSlider(
    value=20,
    min=1,
    max=50,
    step=1,
    description="Pasos:",
    continuous_update=False,
    layout=layout_largo,
    style=estilo,
)

simulaciones_widget = widgets.IntSlider(
    value=1000,
    min=10,
    max=10000,
    step=10,
    description="Simulacion...",
    continuous_update=False,
    layout=layout_largo,
    style=estilo,
)

semilla_widget = widgets.IntText(
    value=42,
    description="Semilla:",
    layout=layout_largo,
    style=estilo,
)

umbral_widget = widgets.FloatSlider(
    value=0.01,
    min=0,
    max=1,
    step=0.01,
    description="Umbral grafo:",
    readout_format=".2f",
    continuous_update=False,
    layout=layout_largo,
    style=estilo,
)

boton = widgets.Button(
    description="Ejecutar simulacion",
    button_style="success",
    layout=widgets.Layout(width="180px"),
)

salida = widgets.Output()


def ejecutar_simulacion(b):
    """
    Lee la interfaz, valida el HMM, ejecuta la simulacion y presenta resultados.
    """
    with salida:
        clear_output()

        try:
            estados_ocultos = leer_lista(estados_widget.value)
            observaciones = leer_lista(observaciones_widget.value)
            pi = leer_matriz(inicial_widget.value).reshape(-1)
            A = leer_matriz(transicion_widget.value)
            B = leer_matriz(emision_widget.value)

            validar_hmm(estados_ocultos, observaciones, pi, A, B)

            pasos = pasos_widget.value
            num_simulaciones = simulaciones_widget.value
            semilla = semilla_widget.value
            umbral = umbral_widget.value

            display(widgets.HTML("<h3>1. Modelo definido</h3>"))

            display(pd.DataFrame({
                "Indice": range(len(estados_ocultos)),
                "Estado oculto": estados_ocultos,
                "Probabilidad inicial": pi,
            }).round(4))

            print("Matriz de transicion entre estados ocultos:")
            display(pd.DataFrame(A, index=estados_ocultos, columns=estados_ocultos).round(4))

            print("Matriz de emision hacia observaciones visibles:")
            display(pd.DataFrame(B, index=estados_ocultos, columns=observaciones).round(4))

            display(widgets.HTML("<h3>2. Diagramas del HMM</h3>"))
            graficar_diagrama_transicion(estados_ocultos, A, umbral)
            graficar_emisiones(estados_ocultos, observaciones, B)

            trayectorias_ocultas, trayectorias_observadas = simular_hmm(
                estados_ocultos,
                observaciones,
                pi,
                A,
                B,
                pasos,
                num_simulaciones,
                semilla,
            )

            evolucion_estados = evolucion_teorica_estados(pi, A, pasos)
            evolucion_observaciones = evolucion_teorica_observaciones(evolucion_estados, B)

            display(widgets.HTML("<h3>3. Secuencias simuladas</h3>"))
            ejemplos = []
            for i in range(min(10, num_simulaciones)):
                estados_ruta = " -> ".join(estados_ocultos[x] for x in trayectorias_ocultas[i])
                observaciones_ruta = " -> ".join(observaciones[x] for x in trayectorias_observadas[i])
                ejemplos.append({
                    "Simulacion": i + 1,
                    "Estados ocultos": estados_ruta,
                    "Observaciones visibles": observaciones_ruta,
                })

            display(pd.DataFrame(ejemplos))

            display(widgets.HTML("<h3>4. Evolucion teorica</h3>"))
            df_evolucion_estados = pd.DataFrame(evolucion_estados, columns=estados_ocultos)
            df_evolucion_estados.index.name = "Paso"
            print("Probabilidad teorica de estados ocultos:")
            display(df_evolucion_estados.round(4))
            graficar_evolucion(
                "Evolucion teorica de estados ocultos",
                estados_ocultos,
                evolucion_estados,
                "Probabilidad",
            )

            df_evolucion_observaciones = pd.DataFrame(evolucion_observaciones, columns=observaciones)
            df_evolucion_observaciones.index.name = "Paso"
            print("Probabilidad teorica de observaciones visibles:")
            display(df_evolucion_observaciones.round(4))
            graficar_evolucion(
                "Evolucion teorica de observaciones visibles",
                observaciones,
                evolucion_observaciones,
                "Probabilidad",
            )

            display(widgets.HTML("<h3>5. Resultados finales</h3>"))

            final_estados_empirico = distribucion_empirica(trayectorias_ocultas, len(estados_ocultos))
            final_observaciones_empirico = distribucion_empirica(
                trayectorias_observadas,
                len(observaciones),
            )

            graficar_barras(
                "Distribucion empirica final de estados ocultos",
                estados_ocultos,
                final_estados_empirico,
            )

            graficar_barras(
                "Distribucion empirica final de observaciones visibles",
                observaciones,
                final_observaciones_empirico,
            )

            comparacion_estados = pd.DataFrame({
                "Estado oculto": estados_ocultos,
                "Probabilidad teorica final": evolucion_estados[-1],
                "Probabilidad empirica final": final_estados_empirico,
            })

            comparacion_observaciones = pd.DataFrame({
                "Observacion visible": observaciones,
                "Probabilidad teorica final": evolucion_observaciones[-1],
                "Probabilidad empirica final": final_observaciones_empirico,
            })

            print("Comparacion final de estados ocultos:")
            display(comparacion_estados.round(4))

            print("Comparacion final de observaciones visibles:")
            display(comparacion_observaciones.round(4))

            print("\nConclusion breve:")
            print(
                "El modelo permite simular una causa no observable directamente "
                "(la presion atmosferica) y las pistas visibles que genera "
                "(soleado, nublado o lluvioso)."
            )

        except Exception as error:
            print("Error en la simulacion:")
            print(error)


boton.on_click(ejecutar_simulacion)

display(widgets.HTML("<h2>Simulacion interactiva de un Modelo Oculto de Markov</h2>"))
display(widgets.HTML("""
<p>
Modifica los estados ocultos, observaciones, distribucion inicial, matriz de transicion,
matriz de emision y parametros de simulacion. Cada distribucion debe sumar 1.
</p>
"""))

display(widgets.HTML("<h3>Modelo</h3>"))
display(estados_widget)
display(observaciones_widget)
display(inicial_widget)
display(transicion_widget)
display(emision_widget)
display(widgets.HTML("<h3>Parametros de simulacion</h3>"))
display(pasos_widget)
display(simulaciones_widget)
display(semilla_widget)
display(umbral_widget)
display(boton)
display(salida)
