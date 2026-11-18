"""Genera docs/Informe.pdf (reportlab). Uso:  python3 docs/generar_informe.py

Edita las constantes de la sección CONFIGURACIÓN (enlaces y contribuciones) y vuelve a ejecutar.
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, Image, KeepTogether, PageBreak, PageTemplate,
                                Paragraph, Preformatted, Spacer, Table, TableStyle)

# ============================ CONFIGURACIÓN (editar) ============================
REPO_URL = "https://github.com/UTECAaron/Proyecto-AED"
VIDEO_URL = "https://drive.google.com/drive/folders/1C7v52nF2rU59dl3-RbO8wI4D74jXY5No?usp=sharing"
INTEGRANTES = [
    "Chahuara Galdos, Sebastian Ernesto",
    "Romano Castro, Aaron Adriano",
    "Garcia López, Bruno William",
]
CONTRIBUCIONES = [
    ("Chahuara Galdos, Sebastian Ernesto",
     "Implementación en C++ del algoritmo (cpp/bcc.cpp): lista de adyacencia con identificadores de arista, "
     "pila de aristas propia, formato de traza JSON y pruebas contra networkx (tests/verify.py)."),
    ("Romano Castro, Aaron Adriano",
     "Animación en Manim (manim/bcc_video.py): diseño visual, reproductor de trazas, pila animada, "
     "casos borde y render final del video en 1080p."),
    ("Garcia López, Bruno William",
     "Guion del video (docs/GUION.md), análisis de complejidad, informe en PDF, README y revisión "
     "de concordancia entre guion y animación."),
]
CONTRIBUCION_COMUN = ("Todos: elección del grafo de ejemplo, revisión cruzada del código, ensayo del video "
                      "y redacción de las conclusiones.")
# ===============================================================================

BASE = Path(__file__).resolve().parent
IMG = BASE / "img"
FONTS = BASE / "fonts"

pdfmetrics.registerFont(TTFont("DV", str(FONTS / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DV-B", str(FONTS / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DV-I", str(FONTS / "DejaVuSans-Oblique.ttf")))
pdfmetrics.registerFont(TTFont("DV-BI", str(FONTS / "DejaVuSans-BoldOblique.ttf")))
pdfmetrics.registerFont(TTFont("DV-M", str(FONTS / "DejaVuSansMono.ttf")))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-B", italic="DV-I", boldItalic="DV-BI")

AZUL = colors.HexColor("#1F3A5F")
GRIS = colors.HexColor("#555555")

body = ParagraphStyle("body", fontName="DV", fontSize=9.6, leading=14.2, alignment=TA_JUSTIFY, spaceAfter=6)
h1 = ParagraphStyle("h1", fontName="DV-B", fontSize=14, leading=18, textColor=AZUL, spaceBefore=12, spaceAfter=6, keepWithNext=1)
h2 = ParagraphStyle("h2", fontName="DV-B", fontSize=11, leading=15, textColor=AZUL, spaceBefore=8, spaceAfter=4, keepWithNext=1)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=14, bulletIndent=3, spaceAfter=3, alignment=0)
cap_style = ParagraphStyle("cap", fontName="DV-I", fontSize=8.2, leading=11, alignment=TA_CENTER, textColor=GRIS,
                           spaceAfter=10)
code = ParagraphStyle("code", fontName="DV-M", fontSize=8, leading=10.2, backColor=colors.HexColor("#F3F5F8"),
                      borderPadding=6, spaceBefore=4, spaceAfter=10)
cell = ParagraphStyle("cell", fontName="DV", fontSize=8.8, leading=12)
cellb = ParagraphStyle("cellb", parent=cell, fontName="DV-B")
cover_t = ParagraphStyle("ct", fontName="DV-B", fontSize=25, leading=31, textColor=AZUL, alignment=TA_CENTER)
cover_s = ParagraphStyle("cs", fontName="DV", fontSize=12.5, leading=18, alignment=TA_CENTER, textColor=GRIS)
cover_n = ParagraphStyle("cn", fontName="DV", fontSize=12, leading=19, alignment=TA_CENTER)


def P(t, s=body):
    return Paragraph(t, s)


def B(t):
    return Paragraph(t, bullet, bulletText="•")


def fig(name, caption, width=14.6 * cm):
    from PIL import Image as PILImage
    w, h = PILImage.open(IMG / name).size
    return KeepTogether([Image(str(IMG / name), width=width, height=width * h / w), P(caption, cap_style)])


def tabla(data, widths, header=True, zebra=True):
    rows = [[Paragraph(str(c), cellb if (header and i == 0) else cell) for c in r] for i, r in enumerate(data)]
    t = Table(rows, colWidths=widths, repeatRows=1 if header else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B8C2CF")),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F2")))
    if zebra:
        for i in range(1 if header else 0, len(rows)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0, i), (-1, i), colors.HexColor("#F7F9FB")))
    t.setStyle(TableStyle(st))
    return t


def footer(canvas, doc):
    if doc.page == 1:
        return
    canvas.saveState()
    canvas.setFont("DV", 8)
    canvas.setFillColor(GRIS)
    canvas.drawString(2 * cm, 1.2 * cm, "CS2023 · Componentes biconexas · UTEC 2026-2")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


def build():
    out = BASE / "Informe.pdf"
    doc = BaseDocTemplate(str(out), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=2 * cm,
                          bottomMargin=2 * cm, title="Informe - Componentes biconexas",
                          author="; ".join(INTEGRANTES), subject="CS2023 Proyecto Final 2")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])
    s = []

    # ------------------------------------------------------------------ carátula
    s += [Spacer(1, 2.2 * cm), P("UNIVERSIDAD DE INGENIERÍA Y TECNOLOGÍA — UTEC", cover_s), Spacer(1, 0.4 * cm),
          P("CS2023 · Algoritmos y Estructuras de Datos", cover_s), P("Ciclo 2026-2", cover_s), Spacer(1, 2.0 * cm),
          P("Proyecto Final 2", cover_s), Spacer(1, 0.2 * cm),
          P("Anima tu Algoritmo o Estructura de Datos", cover_s), Spacer(1, 1.2 * cm),
          P("Componentes biconexas", cover_t), Spacer(1, 0.3 * cm),
          P("Algoritmo de Tarjan (Hopcroft–Tarjan) · O(|V| + |E|)", cover_s), Spacer(1, 2.2 * cm),
          P("<b>Estructura asignada:</b> Componentes biconexas", cover_n), Spacer(1, 0.5 * cm),
          P("<b>Integrantes</b>", cover_n)]
    s += [P(n, cover_n) for n in INTEGRANTES]
    s += [Spacer(1, 0.7 * cm), P("<b>Docente:</b> Víctor Racsó Galván Oyola", cover_n),
          P("Fecha límite de entrega: 18 de noviembre de 2026, 20:00", cover_s), Spacer(1, 2.2 * cm),
          P(f"Repositorio: {REPO_URL}<br/>Video: {VIDEO_URL}", cover_s), PageBreak()]

    # ------------------------------------------------------------------ 1. descripción
    s += [P("1. Descripción del algoritmo y su TDA", h1)]
    s += [P("<b>TDA: Grafo no dirigido.</b> Un grafo no dirigido G = (V, E) guarda un conjunto de vértices y un "
            "conjunto de aristas que los relacionan sin orden. Operaciones usadas por el algoritmo: "
            "<i>agregarArista(u, v)</i> y <i>vecinos(u)</i>. Se implementó con <b>lista de adyacencia</b>, "
            "guardando para cada entrada el vecino y un <i>identificador de arista</i> (así se distingue la arista "
            "del padre de una arista paralela)."),
          P("<b>Definiciones.</b> Una <i>articulación</i> es un vértice cuya eliminación aumenta la cantidad de "
            "componentes conexas. Un <i>puente</i> es una arista con esa propiedad. Una <i>componente biconexa</i> "
            "(bloque) es un subgrafo conexo maximal que no tiene articulaciones propias: sigue conexo al quitar "
            "cualquiera de sus vértices. Los bloques particionan las <b>aristas</b> del grafo; una articulación "
            "pertenece a dos o más bloques y un puente es un bloque de una sola arista (2 vértices)."),
          P("<b>Para qué se usa.</b> Diseño de redes tolerantes a fallos (puntos únicos de falla), análisis de "
            "mapas y redes de carreteras, circuitos, y como paso previo de otros algoritmos (árbol de bloques y "
            "articulaciones, planaridad, 2-conectividad).")]

    s += [P("1.1 Cómo funciona", h2),
          P("Se hace un único DFS que calcula para cada vértice u dos valores y mantiene una pila de aristas:"),
          B("<b>tin[u]</b>: instante en que el DFS descubre a u."),
          B("<b>low[u]</b>: menor tin alcanzable desde el subárbol de u usando a lo más una arista de retroceso."),
          B("<b>Pila de aristas</b>: se apila cada arista de árbol y cada arista de retroceso (hacia un ancestro)."),
          P("<b>Regla.</b> Al volver del hijo v al padre u, se actualiza low[u] = min(low[u], low[v]). "
            "Si <b>low[v] ≥ tin[u]</b>, ningún camino del subárbol de v escapa por encima de u: u separa a v. "
            "Se desapila hasta la arista (u, v) y esas aristas forman una componente biconexa. Si u no es la raíz, "
            "u es articulación. <b>La raíz</b> siempre cumple la condición, por eso es articulación solo si tiene "
            "dos o más hijos en el árbol DFS.")]
    s += [P("Pseudocódigo", h2), Preformatted(
        "dfs(u, aristaPadre):\n"
        "    tin[u] = low[u] = tiempo++\n"
        "    para cada (v, id) en adj[u]:\n"
        "        si id == aristaPadre: continuar\n"
        "        si tin[v] == -1:                    # arista de árbol\n"
        "            apilar(u, v); dfs(v, id)\n"
        "            low[u] = min(low[u], low[v])\n"
        "            si low[v] >= tin[u]:            # u separa a v\n"
        "                desapilar hasta (u, v) -> nueva componente\n"
        "                si u no es raíz: u es articulación\n"
        "        sino si tin[v] < tin[u]:            # arista de retroceso\n"
        "            apilar(u, v); low[u] = min(low[u], tin[v])\n"
        "    # al terminar la raíz: articulación si tiene >= 2 hijos", code)]

    # ------------------------------------------------------------------ 2. implementación
    s += [P("2. Implementación y garantía de animación real", h1),
          P("La implementación está en <b>C++17</b> (<font name='DV-M'>cpp/bcc.cpp</font>), programada por el "
            "grupo: la pila de aristas es una estructura propia con arreglos (<font name='DV-M'>EdgeStack</font>); "
            "no se usa <font name='DV-M'>std::stack</font> ni librerías de grafos. Mientras corre, el programa "
            "registra cada evento (<font name='DV-M'>visit, tree, back, return, comp, art</font>) junto con una "
            "foto de la pila y los guarda en un JSON."),
          P("El video se hace con <b>Manim Community</b> (Python): <font name='DV-M'>manim/bcc_video.py</font> "
            "lee ese JSON y lo reproduce. El código de Manim <b>no contiene</b> valores de tin/low ni el orden de "
            "las aristas, de modo que cambiar el grafo de entrada cambia la animación. Antes de programar se "
            "escribió el guion (<font name='DV-M'>docs/GUION.md</font>) y cada escena del código lleva el mismo "
            "número y nombre que el guion. Cada escena tiene una duración fija y la narración se escribió con un "
            "máximo de ~2,3 palabras por segundo, para que lo que se dice quepa en lo que se ve."),
          P("<b>Verificación.</b> Se comparó el C++ contra <font name='DV-M'>networkx</font> "
            "(<i>biconnected_components</i> y <i>articulation_points</i>) en 2000 grafos aleatorios de 1 a 12 "
            "vértices (incluidos grafos vacíos, no conexos y con raíz aleatoria): coincidieron los 2000 casos "
            "(<font name='DV-M'>tests/verify.py</font>), y la versión de fuerza bruta del mismo programa coincide con Tarjan. networkx se usó solo para probar, no para animar.")]

    # ------------------------------------------------------------------ 3. ejemplo
    s += [P("3. Instancia ilustrativa (la del video)", h1),
          P("Grafo de 9 vértices y 11 aristas, DFS desde la raíz 0. Aristas: 0–1, 1–2, 2–0, 2–3, 3–4, 4–5, 5–6, "
            "6–3, 5–7, 7–8, 8–5."),
          tabla([["Vértice", "0", "1", "2", "3", "4", "5", "6", "7", "8"],
                 ["tin", "0", "1", "2", "3", "4", "5", "6", "7", "8"],
                 ["low (final)", "0", "0", "0", "3", "3", "3", "3", "5", "5"]],
                [2.6 * cm] + [1.5 * cm] * 9),
          Spacer(1, 6),
          tabla([["Orden de salida", "Componente biconexa (aristas)", "Vértices", "Observación"],
                 ["C1", "(5,7), (7,8), (8,5)", "{5, 7, 8}", "Triángulo; 5 es articulación"],
                 ["C2", "(3,4), (4,5), (5,6), (6,3)", "{3, 4, 5, 6}", "Ciclo de 4 vértices; 3 es articulación"],
                 ["C3", "(2,3)", "{2, 3}", "Puente; 2 es articulación"],
                 ["C4", "(0,1), (1,2), (2,0)", "{0, 1, 2}", "Triángulo con la raíz"]],
                [3.0 * cm, 5.0 * cm, 3.0 * cm, 6.0 * cm]),
          Spacer(1, 4),
          P("<b>Articulaciones:</b> 2, 3 y 5. Total: <b>4 componentes biconexas</b>.")]
    s += [fig("cap_demo_no.png", "Figura 1. Demostración: al volver de 6 a 5 se evalúa low[6]=3 ≥ tin[5]=5 → NO; "
                                 "las aristas siguen en la pila."),
          fig("cap_resultado.png", "Figura 2. Resultado final: 4 componentes de colores y articulaciones 2, 3 y 5.")]
    s += [P("3.1 Aplicación: árbol de bloques y articulaciones", h2),
          P("Con el resultado se construye el <i>árbol de bloques y articulaciones</i>: cada componente es un nodo "
            "cuadrado y cada articulación un nodo circular unido a las componentes que la contienen. En el ejemplo "
            "resulta la cadena C4 – 2 – C3 – 3 – C2 – 5 – C1. Si cae una articulación (por ejemplo el 3) el árbol, y "
            "por tanto la red, se parte en dos: es un <b>punto único de falla</b>, y ahí es donde conviene reforzar."),
          fig("cap_arbol.png", "Figura 3. Árbol de bloques y articulaciones; al fallar el vértice 3 la red se parte en dos.",
              width=12.5 * cm)]

    # ------------------------------------------------------------------ 4. casos borde
    s += [P("4. Casos borde mostrados y considerados", h1),
          P("En el video se anima un segundo grafo de 7 vértices (<font name='DV-M'>data/graph_disc.txt</font>): "
            "el camino 1–0–2, el triángulo 3–4–5 y el vértice aislado 6. Con él se muestran, con la traza real del C++:"),
          B("<b>Raíz con dos hijos</b>: la condición low[v] ≥ tin[0] siempre se cumple en la raíz, por eso se cuenta "
            "cuántos hijos tiene; con 2 hijos, 0 es articulación."),
          B("<b>Puente</b>: cada arista (0,1) y (0,2) forma una componente de 2 vértices y 1 arista."),
          B("<b>Grafo no conexo</b>: al terminar el primer DFS quedan vértices sin visitar y se lanza un DFS nuevo "
            "desde el 3."),
          B("<b>Vértice aislado / grafo sin aristas</b>: el 6 no apila nada, por lo tanto no produce componentes."),
          B("<b>Aristas paralelas</b> (considerado en el código, no animado): se omite solo la arista del padre "
            "(por id), no todos los vecinos iguales al padre."),
          fig("cap_raiz.png", "Figura 4. Caso borde: la raíz 0 tiene dos hijos → articulación; el DFS reinicia en el 3 "
                              "y el 6 queda aislado.", width=13.5 * cm)]

    # ------------------------------------------------------------------ 5. complejidad
    s += [P("5. Análisis de complejidad", h1),
          tabla([["Concepto", "Costo", "Justificación"],
                 ["Visitas a vértices", "O(|V|)", "Cada vértice se descubre una sola vez (tin[v] = −1 solo la primera vez)."],
                 ["Recorrido de adyacencias", "O(|E|)", "Cada arista aparece 2 veces en las listas; cada entrada se examina una vez."],
                 ["Apilar / desapilar", "O(|E|)", "Cada arista se apila a lo más una vez (la de árbol al bajar; la de retroceso solo "
                                               "desde el descendiente) y se desapila una vez."],
                 ["Actualizar low, comparar tin", "O(1) por arista", "Solo min y comparaciones."],
                 ["<b>Tiempo total</b>", "<b>O(|V| + |E|)</b>", "Suma de lo anterior."],
                 ["<b>Memoria</b>", "<b>O(|V| + |E|)</b>", "Adyacencia O(|V|+|E|), tin y low O(|V|), pila ≤ |E|, "
                                                              "recursión ≤ |V|."]],
                [4.2 * cm, 3.0 * cm, 9.8 * cm]),
          Spacer(1, 6),
          P("<b>Observaciones.</b> (1) Con grafos muy grandes la recursión puede desbordar la pila de llamadas; "
            "en ese caso se usa una versión iterativa con la misma lógica. (2) El C++ del proyecto además copia la "
            "pila en cada evento para poder animar; ese costo adicional es solo de visualización y no forma parte "
            "del algoritmo. (3) Comparado con la fuerza bruta (quitar cada vértice y contar componentes, "
            "O(|V|·(|V|+|E|))), el algoritmo es lineal.")]

    s += [P("5.1 Comparación con fuerza bruta (medida con el mismo programa)", h2),
          P("La fuerza bruta quita cada vértice v y cuenta las componentes conexas que quedan; v es articulación si "
            "ese número aumenta. Cuesta O(|V|·(|V|+|E|)). <font name='DV-M'>cpp/bcc.cpp</font> implementa ambos "
            "métodos y cuenta operaciones (vértices etiquetados más entradas de adyacencia revisadas):"),
          tabla([["Método", "Recorridos", "Operaciones (grafo del video)", "Articulaciones"],
                 ["Fuerza bruta", "10 (1 inicial + 1 por vértice)", "279", "2, 3, 5"],
                 ["Tarjan", "1", "31", "2, 3, 5"]], [3.2 * cm, 5.4 * cm, 5.0 * cm, 3.4 * cm]),
          Spacer(1, 4),
          P("Ambos coinciden en las articulaciones y Tarjan hace unas 9 veces menos trabajo; la diferencia crece con "
            "el tamaño del grafo. La concordancia entre ambos métodos también se comprueba en "
            "<font name='DV-M'>tests/verify.py</font>."),
          fig("cap_ops.png", "Figura 5. Operaciones reales: fuerza bruta (279) vs. Tarjan (31).", width=12.5 * cm)]

    # ------------------------------------------------------------------ 6. herramientas / reproducción
    s += [P("6. Herramientas y pasos para reproducir el video", h1),
          tabla([["Herramienta", "Uso"],
                 ["C++17 (g++)", "Implementación del algoritmo y generación de la traza JSON."],
                 ["Python 3.9+ y Manim Community", "Animación y render del video (solo <i>Text</i>, sin LaTeX)."],
                 ["FFmpeg, Cairo, Pango", "Dependencias de Manim para codificar y dibujar."],
                 ["reportlab, networkx", "Informe en PDF y pruebas de verificación (opcionales)."]],
                [6.0 * cm, 11.0 * cm]),
          Spacer(1, 4),
          Preformatted("git clone " + REPO_URL + ".git\n"
                       "cd componentes-biconexas && pip install -r requirements.txt\n"
                       "./run.sh            # compila C++, genera trazas y renderiza 1080p30\n"
                       "# manual:\n"
                       "g++ -O2 -std=c++17 -o cpp/bcc cpp/bcc.cpp\n"
                       "./cpp/bcc data/graph_main.txt data/trace_main.json 0\n"
                       "./cpp/bcc data/graph_disc.txt data/trace_disc.json 0\n"
                       "cd manim && manim -r 1920,1080 --fps 30 bcc_video.py BCCVideo", code)]

    # ------------------------------------------------------------------ 7. contribuciones
    s += [P("7. Contribuciones de cada integrante", h1),
          tabla([["Integrante", "Contribución"]] + [[a, b] for a, b in CONTRIBUCIONES], [5.2 * cm, 11.8 * cm]),
          Spacer(1, 4), P(CONTRIBUCION_COMUN)]

    # ------------------------------------------------------------------ 8. evidencia
    s += [P("8. Evidencia y enlaces", h1),
          P(f"<b>Repositorio de GitHub:</b> {REPO_URL}<br/><b>Video (.mp4, 1080p30, 4 min 44 s):</b> {VIDEO_URL}"),
          fig("cap_puente.png", "Figura 6. Introducción: puente (arista 2–3) y articulaciones en el grafo no dirigido.",
              width=12.5 * cm),
          fig("cap_idea.png", "Figura 7. Idea del algoritmo: tin, low, pila de aristas y la regla low[v] ≥ tin[u].",
              width=12.5 * cm),
          fig("cap_demo_comp.png", "Figura 8. Demostración: componentes C1–C3 ya desapiladas; en la pila quedan "
                                   "solo las aristas de C4.", width=12.5 * cm)]

    # ------------------------------------------------------------------ 9. conclusiones
    s += [P("9. Conclusiones", h1),
          B("Un único DFS con los valores tin y low, más una pila de <b>aristas</b>, basta para hallar todas las "
            "componentes biconexas, articulaciones y puentes en tiempo lineal O(|V| + |E|). Apilar aristas (y no "
            "vértices) es lo que permite que una articulación aparezca en varias componentes."),
          B("Los errores típicos están en los casos borde: la raíz del DFS, la arista del padre (aristas paralelas) "
            "y los grafos no conexos. Verlos en la animación y probarlos contra networkx en 2000 grafos aleatorios "
            "dio confianza en la implementación."),
          B("Generar una traza desde el C++ y animarla en Manim garantiza que el video muestra una ejecución real "
            "(no valores escritos a mano) y mantiene la concordancia entre lo que se dice en el guion y lo que "
            "ocurre en pantalla."),
          B("Escribir el guion antes del código ordenó el trabajo en equipo: cada escena de Manim se pudo revisar "
            "contra una frase concreta del guion y los tiempos del video se midieron por escena.")]

    # ------------------------------------------------------------------ referencias
    s += [P("Referencias", h1),
          B('R. E. Tarjan, <i>Depth-first search and linear graph algorithms</i>, '
            'SIAM Journal on Computing, vol. 1, n.º 2, pp. 146–160, 1972. DOI: '
            '<link href="https://doi.org/10.1137/0201010" color="#2563a6">https://doi.org/10.1137/0201010</link>.'),
          B('J. Hopcroft y R. E. Tarjan, <i>Algorithm 447: efficient algorithms for graph manipulation</i>, '
            'Communications of the ACM, vol. 16, n.º 6, pp. 372–378, 1973. DOI: '
            '<link href="https://doi.org/10.1145/362248.362272" color="#2563a6">https://doi.org/10.1145/362248.362272</link>.'),
          B('T. H. Cormen, C. E. Leiserson, R. L. Rivest y C. Stein, <i>Introduction to Algorithms</i>, '
            '3.ª ed., MIT Press, 2009, capítulo 22 (DFS y aplicaciones).'),
          B('cp-algorithms.com, «Finding articulation points» y «Finding bridges». '
            '<link href="https://cp-algorithms.com/graph/cutpoints.html" color="#2563a6">https://cp-algorithms.com/graph/cutpoints.html</link>; '
            '<link href="https://cp-algorithms.com/graph/bridge-searching.html" color="#2563a6">https://cp-algorithms.com/graph/bridge-searching.html</link>.'),
          B('Manim Community Developers, <i>Manim Community Documentation</i>. '
            '<link href="https://docs.manim.community/" color="#2563a6">https://docs.manim.community/</link>. '
            'Referencia de inspiración visual: 3Blue1Brown, '
            '<link href="https://www.3blue1brown.com/" color="#2563a6">https://www.3blue1brown.com/</link>. '
            'No se reutilizó código ni animaciones de terceros.')]

    doc.build(s)
    print("Informe generado:", out)


if __name__ == "__main__":
    build()
