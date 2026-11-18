"""
Componentes biconexas (Tarjan) — video educativo con Manim Community.
Algoritmos y Estructuras de Datos (Ciclo 2026-2) · UTEC

Chahuara Galdos, Sebastian Ernesto · Romano Castro, Aaron Adriano · Garcia López, Bruno William

Este archivo sigue ESCENA por ESCENA el guion de docs/GUION.md.
Los pasos de las escenas 3 y 4 NO se escriben a mano: se leen de data/trace_main.json y
data/trace_edge.json, generados por la implementación propia en cpp/bcc.cpp.

Render:  manim -qh bcc_video.py BCCVideo        (desde la carpeta manim/)
"""
import json
from pathlib import Path

import numpy as np
from manim import *

DATA = Path(__file__).resolve().parent.parent / "data"

PAUSA_K = 0.9          # factor global de pausas
SP_MAIN = 1.2          # velocidad de la demostración principal (más alto = más lento)
SP_BORDE = 0.8         # velocidad de la escena de casos borde
# Duración EXACTA de cada escena en segundos: el código rellena con pausa hasta llegar a ella,
# así los tiempos de docs/GUION.md se cumplen y la narración cabe en cada escena.
DUR = {0: 6, 1: 34, 2: 26, 3: 88, 4: 50, 5: 24, 6: 34, 7: 15, 8: 7}
BG = "#0E1117"
PANEL_BG = "#161B26"
EDGE_C = "#5A6275"
TREE_C = "#E6EDF3"
BACK_C = "#FF9F43"
ART_C = "#FFD700"
VISITED_FILL = "#1E2A44"
COMP_COLORS = ["#4DD4E8", "#7BE07B", "#B58CFF", "#FF7AB6", "#FFC857", "#6FA8FF"]
TIN_C = "#8FD3FF"
LOW_C = "#FFB86B"

config.background_color = BG


def ek(u, v):
    return (min(u, v), max(u, v))


def tint(col, k=0.35):
    return interpolate_color(ManimColor(BG), ManimColor(col), k)


class BCCVideo(Scene):
    # ------------------------------------------------------------------ utilidades
    def construct(self):
        self.main = json.loads((DATA / "trace_main.json").read_text())
        self.disc = json.loads((DATA / "trace_disc.json").read_text())
        self.cap_m = None
        escenas = (self.escena0_portada, self.escena1_introduccion, self.escena2_idea,
                   self.escena3_demostracion, self.escena4_casos_borde, self.escena5_aplicacion,
                   self.escena6_fuerza_bruta, self.escena7_complejidad, self.escena8_creditos)
        for i, fn in enumerate(escenas):
            self._t0 = self.renderer.time
            print(f"[TIEMPO] escena {i} ({fn.__name__}) empieza en {self.renderer.time:.1f} s")
            fn()
        print(f"[TIEMPO] fin del video en {self.renderer.time:.1f} s")

    def cierre(self, i):
        """Rellena con pausa hasta la duración fijada en DUR[i] y limpia la pantalla."""
        objetivo = DUR[i] - 0.8
        resto = objetivo - (self.renderer.time - self._t0)
        if resto > 0:
            self.wait(resto)
        else:
            print(f"[AVISO] la escena {i} excede su duración en {-resto:.1f} s")
        self.limpiar()

    def pausa(self, sec):
        self.wait(sec * PAUSA_K)

    def cap(self, text, size=24, t2c=None):
        """Subtítulo inferior. Devuelve las animaciones para reproducirlas junto a otras."""
        print(f"[CAP] {self.renderer.time:7.1f} " + text.replace(chr(10), " / "))
        new = Text(text, font_size=size, line_spacing=0.8, t2c=t2c or {}).move_to(DOWN * 3.55)
        if new.width > 12.8:
            new.scale_to_fit_width(12.8)
        new.set_z_index(10)
        anims = []
        if self.cap_m is not None:
            anims.append(FadeOut(self.cap_m))
        anims.append(FadeIn(new))
        self.cap_m = new
        return anims

    def limpiar(self, run_time=0.8):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)
        self.cap_m = None

    def build_graph(self, d, shift=ORIGIN):
        pos = [np.array([x, y, 0.0]) + shift for x, y in d["pos"]]
        V, E = {}, {}
        for i, p in enumerate(pos):
            c = Circle(radius=0.28, stroke_width=4, stroke_color=WHITE,
                       fill_color=BG, fill_opacity=1).move_to(p)
            c.set_z_index(2)
            t = Text(str(i), font_size=26).move_to(p)
            t.set_z_index(3)
            V[i] = VGroup(c, t)
        for u, v in d["edges"]:
            ln = Line(pos[u], pos[v], stroke_width=4, color=EDGE_C)
            ln.set_z_index(1)
            E[ek(u, v)] = ln
        return dict(pos=pos, V=V, E=E)

    def create_graph(self, G, run_time=2.0):
        self.play(LaggedStart(*[Create(e) for e in G["E"].values()], lag_ratio=0.08),
                  run_time=run_time * 0.55)
        self.play(LaggedStart(*[FadeIn(v, scale=0.6) for v in G["V"].values()], lag_ratio=0.08),
                  run_time=run_time * 0.45)

    # ------------------------------------------------------------------ ESCENA 0
    def escena0_portada(self):
        titulo = Text("Componentes biconexas", font_size=62, weight=BOLD)
        sub = Text("Algoritmo de Tarjan · O(|V| + |E|)", font_size=30, color=TIN_C)
        curso = Text("Algoritmos y Estructuras de Datos · UTEC · Ciclo 2026-2",
                     font_size=22, color=GREY_B)
        nombres = VGroup(
            Text("Chahuara Galdos, Sebastian Ernesto", font_size=26),
            Text("Romano Castro, Aaron Adriano", font_size=26),
            Text("Garcia López, Bruno William", font_size=26),
        ).arrange(DOWN, buff=0.15)
        g = VGroup(titulo, sub, nombres, curso).arrange(DOWN, buff=0.45)
        g.move_to(ORIGIN)
        self.play(Write(titulo), run_time=1.5)
        self.play(FadeIn(sub, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(nombres, shift=UP * 0.2), FadeIn(curso), run_time=1.0)
        self.pausa(2.0)
        self.cierre(0)

    # ------------------------------------------------------------------ ESCENA 1
    def escena1_introduccion(self):
        G = self.build_graph(self.main, RIGHT * 2.6)   # centrado en pantalla
        V, E = G["V"], G["E"]
        titulo = Text("TDA: Grafo no dirigido", font_size=38).to_edge(UP, buff=0.5)

        # 1) grafo
        self.play(Write(titulo), *self.cap("Un grafo no dirigido (TDA) guarda vértices y las relaciones entre ellos."),
                  run_time=1.2)
        self.create_graph(G, 2.0)
        self.pausa(3.0)

        # 2) articulación: se quita el vértice 3
        left = VGroup(V[0], V[1], V[2], E[ek(0, 1)], E[ek(1, 2)], E[ek(0, 2)])
        right = VGroup(*[V[i] for i in (4, 5, 6, 7, 8)],
                       *[E[k] for k in [ek(4, 5), ek(5, 6), ek(5, 7), ek(7, 8), ek(5, 8)]])
        hub = VGroup(V[3], E[ek(2, 3)], E[ek(3, 4)], E[ek(3, 6)])
        lab_art = Text("Articulación", font_size=30, color=ART_C).move_to(G["pos"][3] + UP * 1.5)
        self.play(*self.cap("Articulación: un vértice que, al quitarlo, desconecta el grafo."), run_time=0.6)
        self.play(hub.animate.set_opacity(0.15), V[3][0].animate.set_stroke(ART_C),
                  left.animate.shift(LEFT * 0.6), right.animate.shift(RIGHT * 0.6),
                  FadeIn(lab_art), run_time=1.6)
        self.pausa(3.0)
        self.play(hub.animate.set_opacity(1), left.animate.shift(RIGHT * 0.6),
                  right.animate.shift(LEFT * 0.6), FadeOut(lab_art),
                  V[3][0].animate.set_stroke(WHITE), run_time=1.2)

        # 3) puente: se quita la arista 2-3
        left2 = VGroup(V[0], V[1], V[2], E[ek(0, 1)], E[ek(1, 2)], E[ek(0, 2)])
        right2 = VGroup(*[V[i] for i in (3, 4, 5, 6, 7, 8)],
                        *[E[k] for k in [ek(3, 4), ek(4, 5), ek(5, 6), ek(3, 6),
                                          ek(5, 7), ek(7, 8), ek(5, 8)]])
        mid = (G["pos"][2] + G["pos"][3]) / 2
        lab_br = Text("Puente", font_size=30, color=BACK_C).move_to(mid + UP * 1.0 + LEFT * 0.2)
        self.play(*self.cap("Puente: una arista cuya eliminación desconecta el grafo."), run_time=0.6)
        self.play(E[ek(2, 3)].animate.set_color(BACK_C).set_stroke(width=7), FadeIn(lab_br), run_time=0.8)
        self.play(E[ek(2, 3)].animate.set_opacity(0.15), left2.animate.shift(LEFT * 0.6),
                  right2.animate.shift(RIGHT * 0.6), run_time=1.4)
        self.pausa(2.5)
        self.play(E[ek(2, 3)].animate.set_opacity(1).set_color(EDGE_C).set_stroke(width=4),
                  left2.animate.shift(RIGHT * 0.6), right2.animate.shift(LEFT * 0.6),
                  FadeOut(lab_br), run_time=1.2)

        # 4) componente biconexa
        box = SurroundingRectangle(VGroup(V[3], V[4], V[5], V[6]), color=COMP_COLORS[1],
                                   buff=0.4, corner_radius=0.3, stroke_width=5)
        self.play(*self.cap("Componente biconexa: bloque máximo que sigue conexo al quitar cualquier vértice."),
                  run_time=0.6)
        self.play(Create(box), run_time=1.2)
        self.pausa(4.5)
        self.play(FadeOut(box), run_time=0.5)

        # 5) usos
        usos = VGroup(*[Text(t, font_size=26, color=TIN_C) for t in
                        ["redes tolerantes a fallos", "mapas de carreteras", "circuitos"]]
                      ).arrange(RIGHT, buff=0.9).move_to(DOWN * 2.85)
        self.play(*self.cap("Se usan en redes tolerantes a fallos, mapas y circuitos. Un solo DFS las encuentra todas."),
                  FadeIn(usos, shift=UP * 0.2), run_time=0.9)
        self.pausa(5.0)
        self.cierre(1)

    # ------------------------------------------------------------------ ESCENA 2
    def _card(self, title, desc, color, w=12.4, h=1.05):
        r = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=color,
                             stroke_width=3, fill_color=PANEL_BG, fill_opacity=1)
        t = Text(title, font_size=30, color=color, weight=BOLD)
        d = Text(desc, font_size=25)
        t.move_to(r.get_left() + RIGHT * 0.4, aligned_edge=LEFT)
        d.next_to(t, RIGHT, buff=0.5)
        if d.get_right()[0] > r.get_right()[0] - 0.3:
            d.scale_to_fit_width(r.get_right()[0] - 0.3 - d.get_left()[0])
        return VGroup(r, t, d)

    def escena2_idea(self):
        titulo = Text("Idea del algoritmo: un DFS con tin, low y una pila", font_size=34)
        titulo.to_edge(UP, buff=0.5)
        c1 = self._card("tin[u]", "Instante en que el DFS descubre a u", TIN_C)
        c2 = self._card("low[u]", "Menor tin alcanzable desde el subárbol de u (≤ 1 retroceso)", LOW_C)
        c3 = self._card("Pila", "Cada arista se apila al recorrerla por primera vez", COMP_COLORS[1])
        cards = VGroup(c1, c2, c3).arrange(DOWN, buff=0.22).next_to(titulo, DOWN, buff=0.45)
        regla_box = RoundedRectangle(corner_radius=0.16, width=12.4, height=1.55, stroke_color=ART_C,
                                     stroke_width=4, fill_color=PANEL_BG, fill_opacity=1)
        regla = Text("Al volver del hijo v al padre u:\nsi  low[v] ≥ tin[u]  →  u separa a v:  se desapila una componente",
                     font_size=26, line_spacing=0.9, t2c={"low[v] ≥ tin[u]": ART_C})
        if regla.width > 11.6:
            regla.scale_to_fit_width(11.6)
        regla_g = VGroup(regla_box, regla)
        regla.move_to(regla_box)
        regla_g.next_to(cards, DOWN, buff=0.3)

        self.play(Write(titulo), *self.cap("El DFS numera los vértices con tin."), run_time=1.0)
        self.play(FadeIn(c1, shift=RIGHT * 0.3), run_time=0.8)
        self.pausa(2.5)
        self.play(*self.cap("low[u] guarda el vértice más alto del árbol al que se puede volver desde el subárbol de u."),
                  FadeIn(c2, shift=RIGHT * 0.3), run_time=0.8)
        self.pausa(5.0)
        self.play(*self.cap("Las aristas se guardan en una pila mientras el DFS avanza."),
                  FadeIn(c3, shift=RIGHT * 0.3), run_time=0.8)
        self.pausa(3.5)
        self.play(*self.cap("Si low[v] ≥ tin[u], nada en el subárbol de v escapa por encima de u: u es articulación."),
                  FadeIn(regla_g, shift=UP * 0.3), run_time=1.0)
        self.play(Indicate(regla, color=ART_C, scale_factor=1.05), run_time=1.2)
        self.pausa(7.0)
        self.cierre(2)

    # ------------------------------------------------------------------ panel de pila
    def _make_panel(self):
        frame = RoundedRectangle(corner_radius=0.15, width=3.1, height=5.0, stroke_color=GREY_B,
                                 stroke_width=2, fill_color=PANEL_BG, fill_opacity=1)
        frame.move_to([4.9, -0.4, 0])
        ptitle = Text("Pila de aristas", font_size=24).next_to(frame, UP, buff=0.12)
        return frame, ptitle

    # ------------------------------------------------------------------ reproductor de trazas
    def play_trace(self, d, G, sp=0.8, log=False):
        """Reproduce la traza real generada por cpp/bcc.cpp."""
        V, E, pos = G["V"], G["E"], G["pos"]
        arts_final = set(d["articulations"])
        root = d["root"]
        ys = [p[1] for p in pos]
        ymean = sum(ys) / len(ys)

        frame, ptitle = self._make_panel()
        legend_title = Text("Componentes:", font_size=22, color=GREY_B).move_to([-6.9, 2.85, 0], aligned_edge=LEFT)
        self.play(FadeIn(frame), FadeIn(ptitle), FadeIn(legend_title), run_time=0.6)

        base_y = -2.9 + 0.08 + 0.19
        step = 0.44
        items = []
        lab_tin, lab_low = {}, {}
        legend_last = [legend_title]
        cursor = Circle(radius=0.4, color=WHITE, stroke_width=5).set_z_index(4)
        cursor_on = [False]
        low_now = {}
        nroot = [0]

        def move_cursor(u):
            if not cursor_on[0]:
                cursor.move_to(pos[u])
                cursor_on[0] = True
                return [FadeIn(cursor)]
            return [cursor.animate.move_to(pos[u])]

        def make_item(u, v, n):
            r = RoundedRectangle(corner_radius=0.08, width=2.6, height=0.38, stroke_color=GREY_B,
                                 stroke_width=2, fill_color="#222A3A", fill_opacity=1)
            t = Text(f"({u}, {v})", font_size=22)
            it = VGroup(r, t).move_to([4.9, base_y + n * step, 0])
            return it

        def new_low_text(u, val):
            t = Text(f"low={val}", font_size=18, color=LOW_C)
            return t

        def hold(h):
            self.wait(h * sp)

        for ev in d["events"]:
            t = ev["t"]
            if log:
                print(f"[EV] {self.renderer.time:6.1f} s  {t:6s}" + "".join(f" {k}={ev[k]}" for k in ("u", "v") if k in ev))
            if t == "root":
                u = ev["u"]
                nroot[0] += 1
                msg = (f"Iniciamos el DFS en el vértice {u} (la raíz)." if nroot[0] == 1 else
                       f"Quedan vértices sin visitar: lanzamos un nuevo DFS desde el {u}.")
                self.play(*self.cap(msg), *move_cursor(u), run_time=0.9 * sp)
                hold(0.5)

            elif t == "visit":
                u = ev["u"]
                low_now[u] = ev["low"]
                up = pos[u][1] > ymean
                direction = UP if up else DOWN
                tt = Text(f"tin={ev['tin']}", font_size=18, color=TIN_C)
                ll = new_low_text(u, ev["low"])
                grp = VGroup(tt, ll).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
                grp.next_to(V[u], direction, buff=0.08)
                tt.move_to(grp[0].get_center()); ll.move_to(grp[1].get_center())
                lab_tin[u], lab_low[u] = tt, ll
                grado = sum(1 for a, b in d["edges"] if u in (a, b))
                msg = (f"Visitamos {u}:  tin[{u}] = low[{u}] = {ev['tin']}" if grado else
                       f"Visitamos {u}: no tiene aristas, no produce ninguna componente.")
                self.play(*self.cap(msg),
                          *move_cursor(u),
                          V[u][0].animate.set_fill(VISITED_FILL, opacity=1),
                          FadeIn(tt), FadeIn(ll), run_time=0.8 * sp)
                hold(0.5)

            elif t == "tree":
                u, v = ev["u"], ev["v"]
                it = make_item(u, v, len(items))
                items.append(it)
                self.play(*self.cap(f"Arista de árbol ({u},{v}): la apilamos y bajamos a {v}."),
                          E[ek(u, v)].animate.set_color(TREE_C).set_stroke(width=7),
                          FadeIn(it, shift=DOWN * 0.5), run_time=0.8 * sp)
                hold(0.35)

            elif t == "back":
                u, v = ev["u"], ev["v"]
                it = make_item(u, v, len(items))
                items.append(it)
                before, after = ev["lowu_before"], ev["lowu"]
                anims = [E[ek(u, v)].animate.set_color(BACK_C).set_stroke(width=7),
                         FadeIn(it, shift=DOWN * 0.5)]
                if after != before:
                    txt = f"Arista de retroceso ({u},{v}): low[{u}] = min({before}, tin[{v}]={ev['tinv']}) = {after}"
                else:
                    txt = f"Arista de retroceso ({u},{v}): low[{u}] = min({before}, tin[{v}]={ev['tinv']}) → sin cambio"
                self.play(*self.cap(txt), *anims, run_time=0.9 * sp)
                if after != before:
                    nl = new_low_text(u, after).move_to(lab_low[u]).align_to(lab_low[u], LEFT)
                    self.play(ReplacementTransform(lab_low[u], nl), Indicate(nl, color=ART_C, scale_factor=1.35),
                              run_time=0.9 * sp)
                    lab_low[u] = nl
                hold(0.4)

            elif t == "return":
                u, v = ev["u"], ev["v"]
                cut = ev["cut"]
                before, after = ev["lowu_before"], ev["lowu"]
                is_root = (u == root)
                line1 = (f"Volvemos de {v} a {u}:  ¿low[{v}]={ev['lowv']} ≥ tin[{u}]={ev['tinu']}?  →  "
                         f"{'SÍ' if cut else 'NO'}")
                if is_root and cut:
                    line2 = f"({u} es la raíz: la condición siempre se cumple, se cuentan sus hijos)"
                elif after != before:
                    line2 = f"low[{u}] = min({before}, {ev['lowv']}) = {after}"
                else:
                    line2 = f"low[{u}] se mantiene en {after}"
                self.play(*self.cap(line1 + "\n" + line2, t2c={"SÍ": "#7BE07B", "NO": "#FF6B6B"}),
                          *move_cursor(u),
                          Indicate(lab_low[v], color=ART_C, scale_factor=1.3),
                          Indicate(lab_tin[u], color=ART_C, scale_factor=1.3),
                          run_time=1.3 * sp)
                if after != before:
                    nl = new_low_text(u, after).move_to(lab_low[u]).align_to(lab_low[u], LEFT)
                    self.play(ReplacementTransform(lab_low[u], nl), Indicate(nl, color=ART_C, scale_factor=1.35),
                              run_time=0.7 * sp)
                    lab_low[u] = nl
                hold(0.7 if cut else 0.4)

            elif t == "comp":
                k = ev["id"]
                col = COMP_COLORS[k % len(COMP_COLORS)]
                es = ev["edges"]
                verts = sorted({a for a, b in es} | {b for a, b in es})
                n = len(es)
                popped = items[-n:]
                del items[-n:]
                anims = []
                for a, b in es:
                    anims.append(E[ek(a, b)].animate.set_color(col).set_stroke(width=8))
                for x in verts:
                    if x not in arts_final:
                        anims.append(V[x][0].animate.set_stroke(col).set_fill(tint(col), opacity=1))
                for it in popped:
                    anims.append(it[0].animate.set_fill(tint(col, 0.6), opacity=1).set_stroke(col))
                vs = "{" + ", ".join(str(x) for x in verts) + "}"
                last = es[-1]   # la última arista desapilada es la de árbol (u, v)
                self.play(*self.cap(f"Desapilamos hasta ({last[0]},{last[1]}): {n} arista(s) → componente C{k + 1} = {vs}"),
                          *anims, run_time=1.1 * sp)
                chip = Text(f"C{k + 1}={vs}", font_size=22, color=col)
                chip.next_to(legend_last[0], RIGHT, buff=0.35)
                legend_last[0] = chip
                self.play(FadeIn(chip, shift=UP * 0.2),
                          FadeOut(VGroup(*popped), shift=RIGHT * 1.2), run_time=0.9 * sp)
                hold(0.5)

            elif t == "art":
                u = ev["u"]
                if ev.get("why") == "root":
                    txt = f"La raíz {u} tiene {ev['children']} hijos → {u} es articulación."
                else:
                    txt = f"low[v] ≥ tin[{u}] se cumplió en un hijo → {u} es articulación."
                self.play(*self.cap(txt),
                          V[u][0].animate.set_stroke(ART_C, width=8).set_fill(tint(ART_C), opacity=1),
                          Flash(V[u], color=ART_C, flash_radius=0.7), run_time=1.0 * sp)
                hold(0.5)

            elif t == "done":
                pass

        self.play(FadeOut(cursor), run_time=0.4)
        return dict(frame=frame, ptitle=ptitle, legend=legend_title, chips=legend_last[0],
                    labels=VGroup(*lab_tin.values(), *lab_low.values()))

    # ------------------------------------------------------------------ ESCENA 3
    def escena3_demostracion(self):
        titulo = Text("Demostración: DFS + pila de aristas (raíz 0)", font_size=30)
        titulo.to_edge(UP, buff=0.35)
        G = self.build_graph(self.main, ORIGIN)
        self.play(Write(titulo), *self.cap("Grafo de 9 vértices y 11 aristas. Cada paso sale de nuestra implementación en C++."),
                  run_time=1.0)
        self.create_graph(G, 1.8)
        self.pausa(2.5)
        self.play_trace(self.main, G, sp=SP_MAIN, log=True)

        arts = self.main["articulations"]
        self.play(*self.cap(f"Resultado: {self.main['num_components']} componentes biconexas · "
                            f"articulaciones: {', '.join(map(str, arts))}"), run_time=0.8)
        self.play(*[Indicate(G["V"][a], color=ART_C, scale_factor=1.4) for a in arts], run_time=1.5)
        self.pausa(4.0)
        self.cierre(3)

    # ------------------------------------------------------------------ ESCENA 4
    def escena4_casos_borde(self):
        titulo = Text("Casos borde: raíz con 2 hijos, grafo no conexo y vértice aislado", font_size=28)
        titulo.to_edge(UP, buff=0.35)
        G = self.build_graph(self.disc, DOWN * 0.2)
        self.play(Write(titulo), *self.cap("La raíz siempre cumple la condición: solo es articulación si tiene 2 o más hijos."),
                  run_time=1.2)
        self.create_graph(G, 1.6)
        self.pausa(2.0)
        info = self.play_trace(self.disc, G, sp=SP_BORDE, log=True)
        self.play(FadeOut(info["frame"]), FadeOut(info["ptitle"]), run_time=0.5)
        notas = VGroup(
            Text("• Un puente es una\n  componente de solo\n  2 vértices: (0,1) y (0,2).", font_size=22, line_spacing=0.9),
            Text("• El vértice 6 no tiene\n  aristas: no produce\n  ninguna componente.", font_size=22, line_spacing=0.9),
            Text("• Grafo no conexo: un\n  DFS nuevo por cada\n  parte sin visitar.", font_size=22, line_spacing=0.9),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([5.1, -0.3, 0])
        self.play(*self.cap("Un puente forma una componente de 2 vértices; un vértice aislado no forma ninguna."),
                  FadeIn(notas[0], shift=LEFT * 0.3), run_time=0.9)
        self.pausa(3.0)
        self.play(FadeIn(notas[1], shift=LEFT * 0.3), run_time=0.9)
        self.pausa(3.0)
        self.play(*self.cap("Un grafo no conexo se recorre completo: un DFS nuevo por cada parte."),
                  FadeIn(notas[2], shift=LEFT * 0.3), run_time=0.9)
        self.pausa(3.5)
        self.cierre(4)

    # ------------------------------------------------------------------ ESCENA 5
    def escena5_aplicacion(self):
        d = self.main
        comps = [sorted({x for e in ev["edges"] for x in e}) for ev in d["events"] if ev["t"] == "comp"]
        comp_edges = [ev["edges"] for ev in d["events"] if ev["t"] == "comp"]
        arts = d["articulations"]
        titulo = Text("Para qué sirve: árbol de bloques y articulaciones", font_size=32).to_edge(UP, buff=0.4)

        # grafo ya coloreado con el resultado del algoritmo (reducido)
        G = self.build_graph(d, RIGHT * 2.6)
        for k, es in enumerate(comp_edges):
            col = COMP_COLORS[k % len(COMP_COLORS)]
            for a, b in es:
                G["E"][ek(a, b)].set_color(col).set_stroke(width=7)
            for x in comps[k]:
                if x not in arts:
                    G["V"][x][0].set_stroke(col).set_fill(tint(col), opacity=1)
        for a in arts:
            G["V"][a][0].set_stroke(ART_C, width=8).set_fill(tint(ART_C), opacity=1)
        graph = VGroup(*G["V"].values(), *G["E"].values()).scale(0.6).move_to([0, 1.2, 0])

        # árbol de bloques: nodos = componentes y articulaciones
        nodes = {}   # clave -> (mobject, nivel)
        adj = {}
        for k, c in enumerate(comps):
            for a in arts:
                if a in c:
                    adj.setdefault(("c", k), []).append(("a", a))
                    adj.setdefault(("a", a), []).append(("c", k))
        start = ("c", next(k for k, c in enumerate(comps) if d["root"] in c))
        level, order, queue = {start: 0}, [start], [start]
        while queue:
            cur = queue.pop(0)
            for nb in adj.get(cur, []):
                if nb not in level:
                    level[nb] = level[cur] + 1
                    order.append(nb)
                    queue.append(nb)
        nlev = max(level.values()) + 1
        step = min(1.8, 11.0 / max(1, nlev - 1))
        per_level = {}
        for key in order:
            per_level.setdefault(level[key], []).append(key)
        for key in order:
            sibs = per_level[level[key]]
            idx = sibs.index(key)
            x = -(nlev - 1) * step / 2 + level[key] * step
            y = -1.2 + (idx - (len(sibs) - 1) / 2) * 0.95
            if key[0] == "c":
                col = COMP_COLORS[key[1] % len(COMP_COLORS)]
                r = RoundedRectangle(corner_radius=0.1, width=1.7, height=0.6, stroke_color=col, stroke_width=3,
                                     fill_color=tint(col, 0.45), fill_opacity=1)
                t = Text(f"C{key[1] + 1} " + "{" + ",".join(map(str, comps[key[1]])) + "}", font_size=19)
                if t.width > 1.55:
                    t.scale_to_fit_width(1.55)
                m = VGroup(r, t)
            else:
                c = Circle(radius=0.3, stroke_color=ART_C, stroke_width=5, fill_color=tint(ART_C), fill_opacity=1)
                m = VGroup(c, Text(str(key[1]), font_size=24))
            m.move_to([x, y, 0]).set_z_index(2)
            nodes[key] = m
        lines = []
        for a_key in [k for k in order if k[0] == "a"]:
            for c_key in adj[a_key]:
                ln = Line(nodes[a_key].get_center(), nodes[c_key].get_center(), stroke_width=3, color=GREY_B)
                ln.set_z_index(1)
                lines.append((a_key, c_key, ln))

        self.play(Write(titulo), *self.cap("Con el resultado del algoritmo se arma el árbol de bloques y articulaciones."),
                  FadeIn(graph), run_time=1.4)
        self.pausa(3.0)
        self.play(*self.cap("Cada componente es un nodo cuadrado; cada articulación, un círculo que une a sus componentes."),
                  LaggedStart(*[FadeIn(nodes[k], scale=0.8) for k in order if k[0] == "c"], lag_ratio=0.2),
                  run_time=1.6)
        self.play(LaggedStart(*[FadeIn(nodes[k], scale=0.8) for k in order if k[0] == "a"], lag_ratio=0.2),
                  *[Create(ln) for _, _, ln in lines], run_time=1.6)
        self.pausa(3.5)

        # punto único de falla: se cae la articulación del medio
        fail = arts[len(arts) // 2] if 3 not in arts else 3
        fkey = ("a", fail)
        fx = nodes[fkey].get_center()[0]
        left, right = VGroup(), VGroup()
        for k, m in nodes.items():
            if k == fkey:
                continue
            (left if m.get_center()[0] < fx else right).add(m)
        for a_key, c_key, ln in lines:
            if fkey in (a_key, c_key):
                continue
            (left if ln.get_center()[0] < fx else right).add(ln)
        fade_lines = VGroup(*[ln for a_key, c_key, ln in lines if fkey in (a_key, c_key)])
        gv = G["V"][fail]
        gv_scaled = [m for m in graph if m is gv]
        self.play(*self.cap(f"Si falla el vértice {fail}, la red se parte en dos: es un punto único de falla."),
                  nodes[fkey].animate.set_opacity(0.2), fade_lines.animate.set_opacity(0.1),
                  left.animate.shift(LEFT * 0.3), right.animate.shift(RIGHT * 0.3),
                  gv.animate.set_opacity(0.2), run_time=1.6)
        self.pausa(3.5)
        self.play(*self.cap("Sirve para redes tolerantes a fallos: reforzar solo donde hay articulaciones."), run_time=0.6)
        self.pausa(4.0)
        self.cierre(5)

    # ------------------------------------------------------------------ ESCENA 6
    def escena6_fuerza_bruta(self):
        d = self.main
        base = d["base_k"]
        titulo = Text("Comparación: fuerza bruta vs. Tarjan", font_size=34).to_edge(UP, buff=0.4)
        G = self.build_graph(d, ORIGIN)
        V, E = G["V"], G["E"]
        P_V, P_K, P_R = np.array([4.3, 1.2, 0]), np.array([4.3, 0.4, 0]), np.array([4.3, -0.5, 0])
        lbl_base = Text(f"Grafo original: {base} componente" + ("s" if base != 1 else ""), font_size=22, color=GREY_B).move_to([4.3, 2.3, 0])
        lbl_v = Text("Vértice quitado: –", font_size=24).move_to(P_V)
        lbl_k = Text("Componentes que quedan: –", font_size=24).move_to(P_K)
        lbl_r = Text("–", font_size=24).move_to(P_R)

        self.play(Write(titulo), *self.cap("Fuerza bruta: quitar cada vértice y contar cuántas componentes conexas quedan."),
                  run_time=1.2)
        self.create_graph(G, 1.4)
        self.play(FadeIn(lbl_base), FadeIn(lbl_v), FadeIn(lbl_k), FadeIn(lbl_r), run_time=0.6)
        self.pausa(1.5)

        prev = None
        for ent in d["brute"]:
            v, k, label = ent["v"], ent["k"], ent["label"]
            es_art = k > base
            anims = []
            for x in range(d["n"]):
                c, t = V[x][0], V[x][1]
                if x == v:
                    anims += [c.animate.set_stroke(opacity=0.25).set_fill(opacity=0.25), t.animate.set_opacity(0.25)]
                else:
                    col = COMP_COLORS[label[x] % len(COMP_COLORS)]
                    anims += [c.animate.set_stroke(color=col, opacity=1).set_fill(tint(col), opacity=1),
                              t.animate.set_opacity(1)]
            for (a, b), ln in E.items():
                if v in (a, b):
                    anims.append(ln.animate.set_stroke(color=EDGE_C, opacity=0.12))
                else:
                    col = COMP_COLORS[label[a] % len(COMP_COLORS)]
                    anims.append(ln.animate.set_stroke(color=col, opacity=1))
            nv = Text(f"Vértice quitado: {v}", font_size=24).move_to(P_V)
            nk = Text(f"Componentes que quedan: {k}", font_size=24).move_to(P_K)
            nr = (Text(f"{k} > {base}  →  articulación", font_size=24, color=ART_C) if es_art
                  else Text(f"{k} ≤ {base}  →  no es articulación", font_size=24, color=GREY_B)).move_to(P_R)
            quedan = "queda 1 componente" if k == 1 else f"quedan {k} componentes"
            self.play(*anims, Transform(lbl_v, nv), Transform(lbl_k, nk), Transform(lbl_r, nr),
                      *self.cap(f"Quitamos el {v}: {quedan}." + ("  ¡Se partió: articulación!" if es_art else "")),
                      run_time=0.8)
            if es_art:
                self.play(Flash(V[v], color=ART_C, flash_radius=0.7), run_time=0.6)
            self.pausa(0.8)

        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.cap_m], run_time=0.7)
        titulo2 = Text("Operaciones reales en este mismo grafo", font_size=32).to_edge(UP, buff=0.5)
        ob, ot = d["ops_brute"], d["ops_tarjan"]
        wmax = 6.2
        bar_b = Rectangle(width=wmax, height=0.7, stroke_width=0, fill_color="#FF6B6B", fill_opacity=1)
        bar_t = Rectangle(width=max(0.12, wmax * ot / ob), height=0.7, stroke_width=0, fill_color="#7BE07B",
                          fill_opacity=1)
        bar_b.move_to([-3.2 + wmax / 2, 1.0, 0]); bar_t.move_to([-3.2 + bar_t.width / 2, -1.0, 0])
        name_b = Text("Fuerza bruta", font_size=26).move_to([-4.6, 1.25, 0])
        sub_b = Text("O(|V|·(|V|+|E|))", font_size=20, color=GREY_B).move_to([-4.6, 0.8, 0])
        name_t = Text("Tarjan", font_size=26).move_to([-4.6, -0.75, 0])
        sub_t = Text("O(|V|+|E|)", font_size=20, color=GREY_B).move_to([-4.6, -1.2, 0])
        num_b = Text(f"{ob} operaciones", font_size=24).next_to(bar_b, RIGHT, buff=0.2)
        num_t = Text(f"{ot} operaciones", font_size=24).next_to(bar_t, RIGHT, buff=0.2)
        ratio = Text(f"≈ {ob / ot:.0f} veces más trabajo, y la diferencia crece con el tamaño del grafo",
                     font_size=26, color=ART_C).move_to([0, -2.3, 0])
        self.play(Write(titulo2), *self.cap(f"Fuerza bruta: {d['n'] + 1} recorridos del grafo (uno por vértice más el inicial)."),
                  FadeIn(name_b), FadeIn(sub_b), GrowFromEdge(bar_b, LEFT), run_time=1.6)
        self.play(FadeIn(num_b), run_time=0.5)
        self.pausa(2.5)
        self.play(*self.cap("Tarjan: un solo recorrido. Ambos métodos encuentran las mismas articulaciones."),
                  FadeIn(name_t), FadeIn(sub_t), GrowFromEdge(bar_t, LEFT), run_time=1.4)
        self.play(FadeIn(num_t), run_time=0.5)
        self.pausa(2.5)
        self.play(FadeIn(ratio, shift=UP * 0.2), run_time=0.8)
        self.pausa(3.0)
        self.cierre(6)

    # ------------------------------------------------------------------ ESCENA 7
    def escena7_complejidad(self):
        titulo = Text("Complejidad", font_size=40).to_edge(UP, buff=0.5)
        filas = [
            ("DFS: cada vértice se visita una vez", "O(|V|)"),
            ("Cada arista: 1 push y 1 pop en la pila", "O(|E|)"),
            ("Actualizar low / comparar con tin", "O(1) por arista"),
            ("Tiempo total del algoritmo", "O(|V| + |E|)"),
            ("Memoria: adyacencia, pila, tin y low", "O(|V| + |E|)"),
        ]
        grp = VGroup()
        for i, (a, b) in enumerate(filas):
            total = (i == 3)
            ta = Text(a, font_size=28, color=ART_C if total else WHITE)
            tb = Text(b, font_size=30, color=ART_C if total else TIN_C, weight=BOLD)
            ta.move_to([-6.3, 1.7 - i * 0.95, 0], aligned_edge=LEFT)
            tb.move_to([2.7, 1.7 - i * 0.95, 0], aligned_edge=LEFT)
            ln = Line([-6.5, 1.7 - i * 0.95 - 0.45, 0], [6.5, 1.7 - i * 0.95 - 0.45, 0],
                      stroke_width=1.5, color=GREY_D)
            grp.add(VGroup(ta, tb, ln))
        self.play(Write(titulo), *self.cap("Cada vértice se visita una vez y cada arista se apila y desapila una sola vez."),
                  run_time=1.0)
        for i, fila in enumerate(grp):
            self.play(FadeIn(fila, shift=RIGHT * 0.3), run_time=0.7)
            self.pausa(1.0 if i < 3 else 0.6)
        self.play(*self.cap("Tiempo lineal: O(|V| + |E|). La memoria también es lineal."),
                  Indicate(grp[3], color=ART_C, scale_factor=1.04), run_time=1.2)
        self.pausa(2.0)
        self.cierre(7)

    # ------------------------------------------------------------------ ESCENA 8
    def escena8_creditos(self):
        t = Text("Componentes biconexas", font_size=48, weight=BOLD)
        nombres = VGroup(
            Text("Chahuara Galdos, Sebastian Ernesto", font_size=26),
            Text("Romano Castro, Aaron Adriano", font_size=26),
            Text("Garcia López, Bruno William", font_size=26),
        ).arrange(DOWN, buff=0.15)
        refs = Text("Referencias: Tarjan (1972) · cp-algorithms.com · estilo inspirado en 3Blue1Brown",
                    font_size=20, color=GREY_B)
        g = VGroup(t, nombres, refs).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(t, shift=UP * 0.2), run_time=0.8)
        self.play(FadeIn(nombres), FadeIn(refs), run_time=1.0)
        self.cierre(8)
