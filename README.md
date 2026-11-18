# Componentes biconexas — Anima tu Estructura de Datos

**CS2023 · Algoritmos y Estructuras de Datos (2026-2) · UTEC — Proyecto Final 2**
Profesor: Víctor Racsó Galván Oyola · Sección: Teo. 3 – Lab. 365

**Integrantes**
- Chahuara Galdos, Sebastian Ernesto 
- Romano Castro, Aaron Adriano 
- Garcia López, Bruno William 

**Tema asignado:** Componentes biconexas (algoritmo de Tarjan / Hopcroft–Tarjan, O(|V|+|E|)).

## Enlaces de entrega

- **Repositorio GitHub:** <https://github.com/UTECAaron/Proyecto-AED>
- **Video (Google Drive):** <https://drive.google.com/drive/folders/1C7v52nF2rU59dl3-RbO8wI4D74jXY5No?usp=sharing>
- **Video (copia en este repositorio):** [`video/Componentes_biconexas.mp4`](video/Componentes_biconexas.mp4) (1080p30, ≈ 4 min 44 s)
- **Informe:** [`docs/Informe.pdf`](docs/Informe.pdf)

## ¿Qué contiene este proyecto?

| Carpeta / archivo | Contenido |
|---|---|
| `cpp/bcc.cpp` | Implementación propia en C++17 del algoritmo, con una **pila de aristas propia** (`EdgeStack`, basada en arreglos) y generación de la traza JSON. |
| `data/graph_main.txt` | Grafo de la demostración principal (9 vértices, 11 aristas). |
| `data/graph_disc.txt` | Grafo de casos borde: raíz con 2 hijos, grafo no conexo, puente y vértice aislado. |
| `data/trace_*.json` | Trazas generadas por el programa C++ que consume la animación. |
| `manim/bcc_video.py` | Escena de Manim (`BCCVideo`) que reproduce los eventos de la traza. |
| `video/Componentes_biconexas.mp4` | Render MP4 incluido en el repositorio. |
| `tests/verify.py` | Pruebas aleatorias de verificación contra NetworkX. |
| `docs/Informe.pdf` | Informe del proyecto. |
| `run.sh` / `run.bat` | Scripts para compilar, generar trazas y renderizar el video. |
| `requirements.txt` | Dependencias de Python. |

## Cómo se garantiza que la animación representa una ejecución real

`cpp/bcc.cpp` ejecuta el algoritmo y registra cada evento (`visit`, `tree`, `back`, `return`, `comp`, `art`) junto con una captura del estado de la pila. `manim/bcc_video.py` lee ese JSON y reproduce los eventos; no contiene los valores de `tin`, `low` ni el orden de las aristas escritos a mano. Si se modifica el grafo de entrada y se vuelve a ejecutar el programa, se genera una nueva traza y la animación cambia en consecuencia.

La pila de aristas es propia (`struct EdgeStack` en `cpp/bcc.cpp`); no se usa `std::stack` ni ninguna librería de grafos. El mismo programa implementa también la solución ingenua por fuerza bruta (eliminar cada vértice y contar componentes conexas) y registra las operaciones de ambos métodos para compararlos.

## Requisitos de software

- Python 3.9 o superior.
- Manim Community (≥ 0.19) y sus dependencias del sistema (Cairo, Pango y FFmpeg).
- Compilador compatible con C++17 (`g++` o `clang++`).
- `networkx` (solo para ejecutar las pruebas de verificación).

Guía oficial de instalación de Manim: <https://docs.manim.community/en/stable/installation.html>

```bash
pip install -r requirements.txt
```

## Compilar y ejecutar

Desde la carpeta raíz del repositorio:

```bash
git clone https://github.com/UTECAaron/Proyecto-AED.git
cd Proyecto-AED

# Linux, macOS o WSL  (renderiza en 1080p30)
./run.sh

# Vista previa rápida (480p15)
./run.sh l

# Windows
run.bat
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

## Verificación

Con el ejecutable compilado, desde la raíz:

```bash
python3 tests/verify.py 2000
```

La prueba compara las componentes biconexas y las articulaciones calculadas por la implementación con los resultados de NetworkX en grafos aleatorios, y comprueba que Tarjan y la fuerza bruta coincidan.

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

La primera línea contiene el número de vértices `n` y aristas `m`. Luego se indican las posiciones de los vértices (solo para el dibujo) y, finalmente, las aristas con índices de `0` a `n-1`.

## Referencias

- R. E. Tarjan, *Depth-first search and linear graph algorithms*, SIAM Journal on Computing, 1(2), 146–160, 1972. [DOI: 10.1137/0201010](https://doi.org/10.1137/0201010).
- J. Hopcroft y R. E. Tarjan, *Algorithm 447: efficient algorithms for graph manipulation*, Communications of the ACM, 16(6), 372–378, 1973. [DOI: 10.1145/362248.362272](https://doi.org/10.1145/362248.362272).
- T. H. Cormen, C. E. Leiserson, R. L. Rivest y C. Stein, *Introduction to Algorithms*, 3.ª ed., MIT Press, 2009.
- [cp-algorithms — Finding articulation points](https://cp-algorithms.com/graph/cutpoints.html).
- [Manim Community Documentation](https://docs.manim.community/).
- [3Blue1Brown](https://www.3blue1brown.com/) (referencia de estilo visual; no se reutilizó código ni animaciones).
