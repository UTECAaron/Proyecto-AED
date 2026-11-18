# Componentes biconexas — Anima tu Estructura de Datos

**CS2023 · Algoritmos y Estructuras de Datos (2026-2) · UTEC — Proyecto Final 2**

**Integrantes**
- Chahuara Galdos, Sebastian Ernesto
- Romano Castro, Aaron Adriano
- Garcia López, Bruno William

**Tema asignado:** Componentes biconexas (algoritmo de Tarjan / Hopcroft–Tarjan, O(|V|+|E|)).

## Enlaces de entrega

- **Repositorio GitHub:** [https://github.com/UTECAaron/Proyecto-AED](https://github.com/UTECAaron/Proyecto-AED)
- **Video editado (Google Drive):** [https://drive.google.com/drive/folders/1C7v52nF2rU59dl3-RbO8wI4D74jXY5No?usp=sharing](https://drive.google.com/drive/folders/1C7v52nF2rU59dl3-RbO8wI4D74jXY5No?usp=sharing)

> El video está alojado en la carpeta compartida de Google Drive. Para que el docente pueda verlo, configura el acceso general como **«Cualquier persona con el enlace – Lector»**.

## ¿Qué contiene este proyecto?

| Carpeta / archivo | Contenido |
|---|---|
| `docs/GUION.md` | Guion del video, organizado por escenas y tiempos. |
| `cpp/bcc.cpp` | Implementación propia en C++ del algoritmo, con pila de aristas propia y generación de traza JSON. |
| `data/graph_*.txt` | Grafos de entrada para la demostración y los casos borde. |
| `data/trace_*.json` | Trazas generadas por el programa C++ que consume la animación. |
| `manim/bcc_video.py` | Escenas de Manim que reproducen los eventos de la traza. |
| `docs/Informe.pdf` | Informe del proyecto. |
| `docs/generar_informe.py` | Script para regenerar el informe PDF. |
| `video/Componentes_biconexas.mp4` | Render MP4 incluido en este paquete (1080p30, aproximadamente 4 min 44 s). |
| `tests/verify.py` | Pruebas aleatorias de verificación contra NetworkX. |
| `run.sh` / `run.bat` | Scripts para compilar, generar trazas y renderizar el video. |

## Cómo se garantiza que la animación representa una ejecución real

`cpp/bcc.cpp` ejecuta el algoritmo y registra cada evento (`visit`, `tree`, `back`, `return`, `comp`, `art`), junto con una captura del estado de la pila. `manim/bcc_video.py` lee ese JSON y reproduce los eventos; no contiene los valores de `tin`, `low` ni el orden de las aristas escritos manualmente. Si se modifica el grafo de entrada y se vuelve a ejecutar el programa, se genera una nueva traza para la animación.

El mismo programa implementa una comparación por fuerza bruta (eliminar cada vértice y contar las componentes conexas) y registra las operaciones de ambos métodos.

## Requisitos de software

- Python 3.9 o superior.
- Manim Community y sus dependencias del sistema (Cairo, Pango y FFmpeg).
- Compilador compatible con C++17 (`g++` o `clang++`).
- `reportlab` para regenerar el informe.
- `networkx` para ejecutar las pruebas de verificación.

Instalación de dependencias Python:

```bash
pip install -r requirements.txt
```

Guía oficial de instalación de Manim: <https://docs.manim.community/en/stable/installation.html>

## Compilar y ejecutar

Desde la carpeta raíz del repositorio:

```bash
# Linux, macOS o WSL
./run.sh

# Vista previa rápida
./run.sh l
```

También se puede ejecutar manualmente:

```bash
g++ -O2 -std=c++17 -o cpp/bcc cpp/bcc.cpp
./cpp/bcc data/graph_main.txt data/trace_main.json 0
./cpp/bcc data/graph_disc.txt data/trace_disc.json 0
cd manim
manim -r 1920,1080 --fps 30 bcc_video.py BCCVideo
```

El video renderizado queda en `manim/media/videos/bcc_video/`.

Para regenerar el informe:

```bash
python3 docs/generar_informe.py
```

## Verificación

Con el ejecutable compilado, ejecutar:

```bash
python3 tests/verify.py 2000
```

La prueba compara las componentes biconexas y los puntos de articulación calculados por la implementación con los resultados de NetworkX en grafos aleatorios.

## Formato de entrada para grafos propios

```text
n m
x0 y0
...
x(n-1) y(n-1)
u0 v0
...
u(m-1) v(m-1)
```

La primera línea contiene el número de vértices `n` y aristas `m`. Luego se indican las posiciones de los vértices y, finalmente, las aristas usando índices desde `0` hasta `n-1`.

## Referencias

- R. E. Tarjan, *Depth-first search and linear graph algorithms*, SIAM Journal on Computing, 1(2), 146–160, 1972. [DOI: 10.1137/0201010](https://doi.org/10.1137/0201010).
- J. Hopcroft y R. E. Tarjan, *Algorithm 447: efficient algorithms for graph manipulation*, Communications of the ACM, 16(6), 372–378, 1973. [DOI: 10.1145/362248.362272](https://doi.org/10.1145/362248.362272).
- T. H. Cormen, C. E. Leiserson, R. L. Rivest y C. Stein, *Introduction to Algorithms*, 3.ª ed., MIT Press, 2009.
- [cp-algorithms — Finding articulation points](https://cp-algorithms.com/graph/cutpoints.html).
- [Manim Community Documentation](https://docs.manim.community/).
- [3Blue1Brown](https://www.3blue1brown.com/) (referencia de inspiración visual; no se reutilizó código ni animaciones).
