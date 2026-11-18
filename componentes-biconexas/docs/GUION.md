# Guion del video — Componentes biconexas (algoritmo de Tarjan / Hopcroft–Tarjan)

**Curso:** Algoritmos y Estructuras de Datos (UTEC, ciclo 2026-2)
**Integrantes:** Chahuara Galdos, Sebastian Ernesto · Romano Castro, Aaron Adriano · Garcia López, Bruno William
**Duración del video:** 4 min 44 s (el enunciado exige máximo 5 min).

> **Cómo se usa este guion**
> - Cada escena dura **exactamente** lo indicado: el código (`DUR` en `manim/bcc_video.py`) rellena con pausa hasta llegar a ese tiempo.
> - La narración está partida en tramos con su hora de inicio y fin. Cada tramo se escribió para **no pasar de ~2,3 palabras por segundo** (columna *p/s*), de modo que se pueda leer en voz alta sin ir más rápido que el video. Si un integrante lee más lento, basta con decir menos palabras: nunca hace falta más.
> - Las escenas 3 y 4 no están escritas a mano: los pasos salen de `cpp/bcc.cpp` (`data/trace_*.json`). La escena 6 usa los conteos reales de operaciones del mismo programa.
> - Al renderizar, el script imprime `[CAP] tiempo subtítulo` y `[EV] tiempo evento`; así se comprueba la concordancia entre guion y video.
> - Las horas son del video completo (mm:ss).


## ESCENA 0 — Portada (0:00 – 0:06)

| Tiempo | En pantalla | Narración | Pal. | p/s |
|---|---|---|---|---|
| 0:00 – 0:06 | Título, algoritmo, integrantes y ciclo 2026-2. | Componentes biconexas. Proyecto final de Algoritmos y Estructuras de Datos. | 10 | 1.7 |

## ESCENA 1 — Introducción conceptual (0:06 – 0:40)

| Tiempo | En pantalla | Narración | Pal. | p/s |
|---|---|---|---|---|
| 0:06 – 0:12 | Aparece el grafo de 9 vértices. Título: TDA grafo no dirigido. | Un grafo no dirigido es un TDA que guarda vértices y sus relaciones. | 13 | 2.2 |
| 0:12 – 0:18 | Se atenúa el vértice 3 y el grafo se parte en dos. | Una articulación es un vértice que, al quitarlo, desconecta el grafo. | 11 | 1.8 |
| 0:18 – 0:24 | Se resalta la arista 2–3 y se separa el grafo. | Un puente es lo mismo, pero con una arista. | 9 | 1.5 |
| 0:24 – 0:30 | Se enmarca el bloque {3, 4, 5, 6}. | Una componente biconexa es un bloque máximo que sigue conexo si quitamos cualquier vértice. | 14 | 2.2 |
| 0:30 – 0:40 | Aparecen los usos: redes tolerantes a fallos, mapas, circuitos. | Sirven para redes tolerantes a fallos, mapas y circuitos, y un solo DFS las encuentra todas. | 16 | 1.7 |

## ESCENA 2 — Idea del algoritmo (0:40 – 1:06)

| Tiempo | En pantalla | Narración | Pal. | p/s |
|---|---|---|---|---|
| 0:40 – 0:44 | Tarjeta tin[u]. | El DFS numera cada vértice con tin. | 7 | 1.8 |
| 0:44 – 0:49 | Tarjeta low[u]. | Low es el tin más bajo alcanzable desde el subárbol. | 10 | 1.9 |
| 0:49 – 0:53 | Tarjeta de la pila de aristas. | Las aristas se guardan en una pila. | 7 | 1.8 |
| 0:53 – 1:06 | Aparece la regla destacada low[v] ≥ tin[u]. | Al volver de v a u, si low de v es mayor o igual que tin de u, u separa a v: es articulación y se desapila una componente. | 29 | 2.3 |

## ESCENA 3 — Demostración animada (1:06 – 2:34)

| Tiempo | En pantalla | Narración | Pal. | p/s |
|---|---|---|---|---|
| 1:06 – 1:12 | Aparece el grafo de 9 vértices y 11 aristas. | Nuestro grafo tiene nueve vértices y once aristas. | 8 | 1.5 |
| 1:12 – 1:18 | Cursor en 0: tin=low=0. Se apila la arista (0,1) y se visita el 1. | Empezamos en el cero: tin y low valen cero. Apilamos cada arista. | 12 | 2.0 |
| 1:18 – 1:24 | Visita del 2. Arista de retroceso (2,0): low[2] baja a 0. | Del dos hay un retroceso al cero: low baja a cero. | 11 | 1.8 |
| 1:24 – 1:36 | Se visitan 3, 4, 5 y 6; cada arista de árbol entra a la pila. | Seguimos por el tres, el cuatro, el cinco y el seis, apilando cada arista. | 14 | 1.2 |
| 1:36 – 1:44 | Retroceso (6,3): low[6]=3; al volver, low[5] baja a 3. Se visita el 7. | Del seis hay un retroceso al tres: low baja a tres y sube al volver. | 15 | 1.8 |
| 1:44 – 1:55 | Se visita el 8 (retroceso a 5). Al volver al 5: ¿low[7]=5 ≥ tin[5]=5? SÍ. | Luego el siete y el ocho. Al volver al cinco, low del siete vale cinco: la condición se cumple. | 19 | 1.7 |
| 1:55 – 2:03 | Se desapila C1={5,7,8} (celeste) y el 5 se marca como articulación. | Desapilamos: sale el triángulo cinco, siete, ocho, y el cinco es articulación. | 12 | 1.6 |
| 2:03 – 2:17 | Salen C2={3,4,5,6}, C3={2,3} (puente) y se marcan 3 y 2 como articulaciones. | Al volver del cuatro al tres sale el ciclo de cuatro vértices. Luego el puente dos, tres. El tres y el dos son articulaciones. | 24 | 1.7 |
| 2:17 – 2:26 | Al volver a la raíz sale C4={0,1,2}. | Al llegar a la raíz sale el triángulo cero, uno, dos. | 11 | 1.2 |
| 2:26 – 2:34 | Resultado: 4 componentes de colores y articulaciones resaltadas. | Resultado: cuatro componentes biconexas; articulaciones en el dos, el tres y el cinco. | 13 | 1.6 |

## ESCENA 4 — Casos borde (2:34 – 3:24)

| Tiempo | En pantalla | Narración | Pal. | p/s |
|---|---|---|---|---|
| 2:34 – 2:39 | Grafo con dos partes: 1–0–2 y el triángulo 3-4-5, más el vértice aislado 6. | La raíz es un caso especial: siempre cumple la condición. | 10 | 2.0 |
| 2:39 – 2:43 | DFS desde 0, se baja al 1. | Empezamos en el cero y bajamos al uno. | 8 | 1.8 |
| 2:43 – 2:54 | Al volver a la raíz: la condición es SÍ en ambos hijos. Salen C1={0,1} y C2={0,2}. La raíz tiene 2 hijos → articulación. | Al volver a la raíz la condición se cumple siempre, así que contamos sus hijos. El cero tiene dos hijos: es articulación. | 22 | 2.1 |
| 2:54 – 3:11 | Nuevo DFS desde el 3: sale el triángulo C3={3,4,5}. Luego se visita el 6, que no tiene aristas. | El grafo no es conexo: quedan vértices sin visitar, así que lanzamos un nuevo DFS desde el tres. Aquí sale el triángulo tres, cuatro, cinco. El seis no tiene aristas. | 30 | 1.8 |
| 3:11 – 3:18 | Aparece la nota sobre puentes y vértices aislados. | Un puente forma una componente de dos vértices; un vértice aislado, ninguna. | 12 | 1.7 |
| 3:18 – 3:24 | Aparece la nota sobre grafos no conexos. | Si el grafo no es conexo, hacemos un DFS por cada parte. | 12 | 1.9 |

## ESCENA 5 — Para qué sirve: árbol de bloques (3:24 – 3:48)

| Tiempo | En pantalla | Narración | Pal. | p/s |
|---|---|---|---|---|
| 3:24 – 3:28 | El grafo coloreado y reducido. | Con este resultado armamos el árbol de bloques. | 8 | 2.0 |
| 3:28 – 3:34 | Aparecen los nodos C1–C4 (cuadrados) y las articulaciones 2, 3, 5 (círculos). | Cada componente es un nodo; cada articulación, un círculo que las une. | 12 | 1.9 |
| 3:34 – 3:39 | Se cae el vértice 3: el árbol se parte en dos. | Si falla el tres, la red se parte en dos. | 10 | 2.1 |
| 3:39 – 3:48 | Texto: reforzar solo donde hay articulaciones. | Es un punto único de falla: sirve para reforzar redes solo donde hay articulaciones. | 14 | 1.6 |

## ESCENA 6 — Comparación con fuerza bruta (3:48 – 4:22)

| Tiempo | En pantalla | Narración | Pal. | p/s |
|---|---|---|---|---|
| 3:48 – 3:52 | Grafo original y panel de conteo. | Fuerza bruta: quitamos cada vértice y contamos componentes. | 8 | 1.8 |
| 3:52 – 4:08 | Se quita cada vértice del 0 al 8; el panel muestra cuántas componentes quedan (2 al quitar 2, 3 y 5). | Al quitar el dos, el tres o el cinco, el grafo se parte en dos: esos son los puntos de articulación. Con los demás vértices sigue conexo. | 27 | 1.7 |
| 4:08 – 4:13 | Barra de fuerza bruta: 279 operaciones. | Esto exige diez recorridos del grafo. | 6 | 1.4 |
| 4:13 – 4:22 | Barra de Tarjan: 31 operaciones; razón ≈ 9. | Tarjan lo logra con un solo recorrido: treinta y uno contra doscientas setenta y nueve operaciones, unas nueve veces menos. | 20 | 2.1 |

## ESCENA 7 — Complejidad (4:22 – 4:37)

| Tiempo | En pantalla | Narración | Pal. | p/s |
|---|---|---|---|---|
| 4:22 – 4:30 | Tabla fila por fila: O(|V|), O(|E|), O(1) por arista. | Cada vértice se visita una vez y cada arista se apila y desapila una vez. | 15 | 1.8 |
| 4:30 – 4:37 | Se resalta O(|V|+|E|). | Tiempo total lineal, O de V más E; la memoria también. | 11 | 1.6 |

## ESCENA 8 — Créditos (4:37 – 4:44)

| Tiempo | En pantalla | Narración | Pal. | p/s |
|---|---|---|---|---|
| 4:37 – 4:44 | Título, integrantes y referencias. | Gracias por ver. | 3 | 0.4 |

---
**Resumen:** 493 palabras en 284 s → promedio 1.74 palabras/segundo; máximo en un tramo: 2.27.
