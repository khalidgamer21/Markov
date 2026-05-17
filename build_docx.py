from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor


OUTPUT = "informe_markov.docx"
ACCENT = RGBColor(31, 78, 121)
MUTED = RGBColor(90, 90, 90)


def set_cell_text(cell, text, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    paragraph = cell.paragraphs[0]
    paragraph.alignment = align
    run = paragraph.runs[0] if paragraph.runs else paragraph.add_run()
    run.text = text
    run.bold = bold
    run.font.name = "Arial"
    run.font.size = Pt(10)


def add_table(document, headers, rows):
    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.autofit = True
    for index, header in enumerate(headers):
        set_cell_text(table.rows[0].cells[index], header, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER)
    for row in rows:
        cells = table.add_row().cells
        for index, value in enumerate(row):
            align = WD_ALIGN_PARAGRAPH.LEFT if index == 0 else WD_ALIGN_PARAGRAPH.CENTER
            set_cell_text(cells[index], str(value), align=align)
    document.add_paragraph()
    return table


def add_heading(document, text, level=1):
    paragraph = document.add_heading(text, level=level)
    for run in paragraph.runs:
        run.font.name = "Arial"
        run.font.color.rgb = ACCENT
    return paragraph


def add_body_paragraph(document, text):
    paragraph = document.add_paragraph(text)
    paragraph.paragraph_format.space_after = Pt(6)
    paragraph.paragraph_format.line_spacing = 1.08
    for run in paragraph.runs:
        run.font.name = "Arial"
        run.font.size = Pt(12)
    return paragraph


def add_bullet(document, text):
    paragraph = document.add_paragraph(style="List Bullet")
    paragraph.paragraph_format.space_after = Pt(4)
    run = paragraph.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(12)


def add_number(document, text):
    paragraph = document.add_paragraph(style="List Number")
    paragraph.paragraph_format.space_after = Pt(4)
    run = paragraph.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(12)


def configure_document(document):
    section = document.sections[0]
    section.top_margin = Inches(1)
    section.bottom_margin = Inches(1)
    section.left_margin = Inches(1)
    section.right_margin = Inches(1)

    styles = document.styles
    styles["Normal"].font.name = "Arial"
    styles["Normal"].font.size = Pt(12)
    styles["Title"].font.name = "Arial"
    styles["Title"].font.size = Pt(22)
    styles["Title"].font.bold = True
    styles["Title"].font.color.rgb = ACCENT
    styles["Heading 1"].font.name = "Arial"
    styles["Heading 1"].font.size = Pt(16)
    styles["Heading 1"].font.bold = True
    styles["Heading 1"].font.color.rgb = ACCENT
    styles["Heading 2"].font.name = "Arial"
    styles["Heading 2"].font.size = Pt(14)
    styles["Heading 2"].font.bold = True
    styles["Heading 2"].font.color.rgb = ACCENT

    header = section.header.paragraphs[0]
    header.text = "Modelo de Markov"
    header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    header.runs[0].font.name = "Arial"
    header.runs[0].font.size = Pt(9)
    header.runs[0].font.color.rgb = MUTED

    footer = section.footer.paragraphs[0]
    footer.text = "Actividad de simulacion probabilistica"
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    footer.runs[0].font.name = "Arial"
    footer.runs[0].font.size = Pt(9)
    footer.runs[0].font.color.rgb = MUTED


def build_document():
    document = Document()
    configure_document(document)

    title = document.add_paragraph(style="Title")
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.add_run("Implementacion de un modelo de Markov usando distribuciones de probabilidad")

    subtitle = document.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run("Simulacion discreta aplicada a estados climaticos")
    run.font.name = "Arial"
    run.font.size = Pt(12)
    run.font.color.rgb = MUTED
    document.add_paragraph()

    add_heading(document, "Introduccion")
    add_body_paragraph(
        document,
        "Las cadenas de Markov son modelos probabilisticos que representan sistemas que evolucionan entre un conjunto finito de estados. "
        "Su caracteristica principal es que el siguiente estado depende del estado actual y de una distribucion de probabilidad asociada, no de toda la historia previa del sistema.",
    )
    add_body_paragraph(
        document,
        "En esta actividad se implemento una cadena de Markov discreta para simular el comportamiento del clima. "
        "El sistema tiene tres estados posibles: Soleado, Nublado y Lluvioso. Cada estado cuenta con probabilidades de transicion hacia los demas estados.",
    )
    add_body_paragraph(
        document,
        "La solucion aplica distribuciones de probabilidad porque cada paso de la simulacion se decide mediante una seleccion aleatoria ponderada.",
    )

    add_heading(document, "Metodologia")
    add_body_paragraph(
        document,
        "La solucion se desarrollo en Python sin dependencias externas para que pueda ejecutarse facilmente. El modelo se compone de estados, una distribucion inicial, una matriz de transicion, pasos por simulacion y cantidad de simulaciones.",
    )
    add_bullet(document, "Estados: Soleado, Nublado y Lluvioso.")
    add_bullet(document, "Distribucion inicial: probabilidad de comenzar en cada estado.")
    add_bullet(document, "Matriz de transicion: distribuciones condicionales que indican el siguiente estado probable.")
    add_bullet(document, "Simulaciones independientes: ejecuciones repetidas para observar resultados agregados.")

    add_heading(document, "Matriz de transicion", level=2)
    add_table(
        document,
        ["Estado actual", "Soleado", "Nublado", "Lluvioso"],
        [
            ["Soleado", "0.65", "0.25", "0.10"],
            ["Nublado", "0.30", "0.45", "0.25"],
            ["Lluvioso", "0.20", "0.35", "0.45"],
        ],
    )

    add_heading(document, "Distribucion inicial", level=2)
    add_table(
        document,
        ["Estado", "Probabilidad inicial"],
        [["Soleado", "0.50"], ["Nublado", "0.30"], ["Lluvioso", "0.20"]],
    )

    add_heading(document, "Algoritmo", level=2)
    for step in [
        "Validar que las probabilidades de la distribucion inicial y de cada fila de la matriz sumen 1.",
        "Seleccionar el estado inicial usando una distribucion ponderada.",
        "Consultar la fila de transicion correspondiente al estado actual.",
        "Seleccionar el siguiente estado mediante una nueva eleccion ponderada.",
        "Guardar la trayectoria completa y repetir el proceso en multiples simulaciones.",
        "Calcular distribuciones finales, distribuciones de visita y distribucion estacionaria aproximada.",
    ]:
        add_number(document, step)

    document.add_section(WD_SECTION.NEW_PAGE)
    add_heading(document, "Resultados y conclusiones")
    add_body_paragraph(
        document,
        "Se ejecuto una prueba con 1000 simulaciones, 20 pasos por simulacion y semilla 42. Las trayectorias individuales fueron diferentes entre si, pero los resultados agregados se aproximaron a una distribucion estable.",
    )
    add_table(
        document,
        ["Medida", "Soleado", "Nublado", "Lluvioso"],
        [
            ["Distribucion del estado final", "0.4120", "0.3410", "0.2470"],
            ["Distribucion de visitas", "0.4308", "0.3356", "0.2336"],
            ["Distribucion estacionaria aproximada", "0.4257", "0.3416", "0.2327"],
        ],
    )
    add_body_paragraph(
        document,
        "Los resultados muestran que, aunque cada simulacion individual puede producir una trayectoria distinta, el comportamiento agregado tiende a estabilizarse cuando se aumenta el numero de pasos y simulaciones.",
    )
    add_body_paragraph(
        document,
        "Como conclusion, el modelo de Markov permite representar sistemas con incertidumbre donde el futuro depende probabilisticamente del estado presente. La implementacion demuestra el papel central de las distribuciones de probabilidad en la seleccion del estado inicial y de las transiciones.",
    )
    add_body_paragraph(
        document,
        "El codigo fuente quedo organizado para incluirse en un repositorio de GitHub junto con el documento y el archivo de configuracion del modelo.",
    )

    document.save(OUTPUT)


if __name__ == "__main__":
    build_document()
