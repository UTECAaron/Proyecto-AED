"""Verifica cpp/bcc.cpp contra networkx en grafos aleatorios (solo para pruebas; no se usa en el video).
Uso: python3 tests/verify.py [num_grafos]   (compilar antes: g++ -O2 -std=c++17 -o cpp/bcc cpp/bcc.cpp)
"""
import json, random, subprocess, sys, tempfile, os
import networkx as nx

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BIN = os.path.join(ROOT, "cpp", "bcc")


def run_cpp(n, edges, root):
    with tempfile.TemporaryDirectory() as d:
        gi, go = os.path.join(d, "g.txt"), os.path.join(d, "t.json")
        with open(gi, "w") as f:
            f.write(f"{n} {len(edges)}\n" + "".join("0 0\n" for _ in range(n)) +
                    "".join(f"{u} {v}\n" for u, v in edges))
        subprocess.run([BIN, gi, go, str(root)], check=True, capture_output=True)
        t = json.load(open(go))
    comps = [frozenset(x for e in ev["edges"] for x in e) for ev in t["events"] if ev["t"] == "comp"]
    assert set(t["brute_arts"]) == set(t["articulations"]), "fuerza bruta y Tarjan no coinciden"
    return set(comps), set(t["articulations"]), len(comps)


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    random.seed(2026)
    ok = 0
    for it in range(N):
        n = random.randint(1, 12)
        pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        k = random.randint(0, len(pairs)) if random.random() < 0.3 else random.randint(0, min(len(pairs), 2 * n))
        edges = random.sample(pairs, k)
        G = nx.Graph(); G.add_nodes_from(range(n)); G.add_edges_from(edges)
        exp_c = {frozenset(c) for c in nx.biconnected_components(G)}
        exp_a = set(nx.articulation_points(G))
        got_c, got_a, cnt = run_cpp(n, edges, random.randrange(n))
        assert got_c == exp_c, f"componentes distintas en {n=} {edges=}: {got_c} vs {exp_c}"
        assert got_a == exp_a, f"articulaciones distintas en {n=} {edges=}: {got_a} vs {exp_a}"
        assert cnt == len(exp_c)
        ok += 1
    print(f"OK: {ok}/{N} grafos aleatorios coinciden con networkx (componentes y articulaciones).")


if __name__ == "__main__":
    main()
