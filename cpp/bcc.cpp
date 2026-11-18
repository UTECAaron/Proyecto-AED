// Componentes biconexas (algoritmo de Tarjan / Hopcroft-Tarjan) — implementación propia.
// Entrada : archivo con "n m", n líneas "x y" (posición para el dibujo) y m líneas "u v".
// Salida  : JSON con la traza paso a paso del algoritmo (la usa Manim para animar).
// Uso     : ./bcc data/graph_main.txt data/trace_main.json [raiz]
// No se usa std::stack ni ninguna librería de grafos: la pila de aristas es propia.
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

// ---------- Pila de aristas propia (TDA Pila con arreglo) ----------
struct EdgeStack {
    int *a, *b;
    int sz;
    explicit EdgeStack(int cap) : a(new int[cap + 1]), b(new int[cap + 1]), sz(0) {}
    ~EdgeStack() { delete[] a; delete[] b; }
    void push(int u, int v) { a[sz] = u; b[sz] = v; ++sz; }
    void pop() { --sz; }
    int topU() const { return a[sz - 1]; }
    int topV() const { return b[sz - 1]; }
    bool empty() const { return sz == 0; }
};

struct Adj { int to, id; };

int n, m, timer_ = 0;
vector<vector<Adj>> adj;
vector<int> tin, low, rootChildren;
vector<char> isArt;
vector<string> events;
vector<vector<pair<int,int>>> comps;
long long opsT = 0;   // operaciones del algoritmo de Tarjan (vértices visitados + entradas de adyacencia revisadas)
EdgeStack *S;

static string stackJson() {
    string s = "[";
    for (int i = 0; i < S->sz; ++i) {
        if (i) s += ",";
        s += "[" + to_string(S->a[i]) + "," + to_string(S->b[i]) + "]";
    }
    return s + "]";
}

// Cada evento guarda además una "foto" de la pila para que la animación sea fiel.
static void emit(const string &body) {
    events.push_back("{" + body + ",\"stack\":" + stackJson() + "}");
}

void dfs(int u, int parentEdge) {
    tin[u] = low[u] = timer_++;
    ++opsT;
    emit("\"t\":\"visit\",\"u\":" + to_string(u) + ",\"tin\":" + to_string(tin[u]) +
         ",\"low\":" + to_string(low[u]));
    for (const Adj &e : adj[u]) {
        int v = e.to;
        ++opsT;
        if (e.id == parentEdge) continue;                 // no volver por la arista del padre
        if (tin[v] == -1) {                               // arista de árbol
            if (parentEdge == -1) rootChildren[u]++;
            S->push(u, v);
            emit("\"t\":\"tree\",\"u\":" + to_string(u) + ",\"v\":" + to_string(v));
            dfs(v, e.id);
            int before = low[u];
            low[u] = min(low[u], low[v]);
            bool cut = low[v] >= tin[u];                  // condición de articulación / bloque
            emit("\"t\":\"return\",\"u\":" + to_string(u) + ",\"v\":" + to_string(v) +
                 ",\"lowv\":" + to_string(low[v]) + ",\"tinu\":" + to_string(tin[u]) +
                 ",\"lowu_before\":" + to_string(before) + ",\"lowu\":" + to_string(low[u]) +
                 ",\"cut\":" + (cut ? "true" : "false"));
            if (cut) {
                vector<pair<int,int>> comp;               // desapilar hasta la arista (u,v)
                while (true) {
                    int x = S->topU(), y = S->topV();
                    S->pop();
                    comp.push_back({x, y});
                    if (x == u && y == v) break;
                }
                comps.push_back(comp);
                string es = "[";
                for (size_t i = 0; i < comp.size(); ++i) {
                    if (i) es += ",";
                    es += "[" + to_string(comp[i].first) + "," + to_string(comp[i].second) + "]";
                }
                es += "]";
                emit("\"t\":\"comp\",\"id\":" + to_string(comps.size() - 1) + ",\"u\":" +
                     to_string(u) + ",\"edges\":" + es);
                if (parentEdge != -1 && !isArt[u]) {      // no raíz: articulación
                    isArt[u] = 1;
                    emit("\"t\":\"art\",\"u\":" + to_string(u) + ",\"why\":\"cut\"");
                }
            }
        } else if (tin[v] < tin[u]) {                     // arista de retroceso (hacia ancestro)
            S->push(u, v);
            int before = low[u];
            low[u] = min(low[u], tin[v]);
            emit("\"t\":\"back\",\"u\":" + to_string(u) + ",\"v\":" + to_string(v) +
                 ",\"tinv\":" + to_string(tin[v]) + ",\"lowu_before\":" + to_string(before) +
                 ",\"lowu\":" + to_string(low[u]));
        }
        // tin[v] > tin[u]: la arista ya se procesó desde el descendiente v.
    }
}

// ---------- Fuerza bruta (solo para comparar): componentes conexas de G sin el vértice 'rem' ----------
// rem = -1 usa el grafo completo. 'ops' cuenta vértices etiquetados + entradas de adyacencia revisadas.
static int countComps(int rem, vector<int> &label, long long &ops) {
    label.assign(n, -1);
    int k = 0;
    vector<int> st;                                   // pila manual para un DFS iterativo
    for (int s = 0; s < n; ++s) {
        if (s == rem || label[s] != -1) continue;
        label[s] = k; ++ops; st.push_back(s);
        while (!st.empty()) {
            int u = st.back(); st.pop_back();
            for (const Adj &e : adj[u]) {
                ++ops;
                if (e.to == rem || label[e.to] != -1) continue;
                label[e.to] = k; ++ops; st.push_back(e.to);
            }
        }
        ++k;
    }
    return k;
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "uso: %s grafo.txt traza.json [raiz]\n", argv[0]); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("entrada"); return 1; }
    int root = argc > 3 ? atoi(argv[3]) : 0;
    if (fscanf(f, "%d %d", &n, &m) != 2) return 1;
    vector<pair<double,double>> pos(n);
    for (int i = 0; i < n; ++i)
        if (fscanf(f, "%lf %lf", &pos[i].first, &pos[i].second) != 2) return 1;
    vector<pair<int,int>> edges(m);
    adj.assign(n, {});
    for (int i = 0; i < m; ++i) {
        int u, v;
        if (fscanf(f, "%d %d", &u, &v) != 2) return 1;
        edges[i] = {u, v};
        adj[u].push_back({v, i});
        adj[v].push_back({u, i});
    }
    fclose(f);

    tin.assign(n, -1); low.assign(n, -1); rootChildren.assign(n, 0); isArt.assign(n, 0);
    S = new EdgeStack(m);

    // Orden de raíces: primero la pedida; luego cualquier vértice sin visitar (grafo no conexo).
    vector<int> order;
    order.push_back(root);
    for (int i = 0; i < n; ++i) if (i != root) order.push_back(i);
    for (int r : order) {
        if (tin[r] != -1) continue;
        emit("\"t\":\"root\",\"u\":" + to_string(r));
        dfs(r, -1);
        if (rootChildren[r] >= 2) {                       // regla especial de la raíz
            isArt[r] = 1;
            emit("\"t\":\"art\",\"u\":" + to_string(r) + ",\"why\":\"root\",\"children\":" +
                 to_string(rootChildren[r]));
        }
    }
    emit("\"t\":\"done\"");

    // Fuerza bruta: v es articulación si al quitarlo aumenta la cantidad de componentes conexas.
    long long opsB = 0;
    vector<int> lab;
    int baseK = countComps(-1, lab, opsB);
    string bj = "[";
    vector<int> bruteArts;
    for (int v = 0; v < n; ++v) {
        int k = countComps(v, lab, opsB);
        if (k > baseK) bruteArts.push_back(v);
        bj += string(v ? "," : "") + "{\"v\":" + to_string(v) + ",\"k\":" + to_string(k) + ",\"label\":[";
        for (int i = 0; i < n; ++i) bj += (i ? "," : "") + to_string(lab[i]);
        bj += "]}";
    }
    bj += "]";
    string ba = "[";
    for (size_t i = 0; i < bruteArts.size(); ++i) ba += (i ? "," : "") + to_string(bruteArts[i]);
    ba += "]";

    FILE *o = fopen(argv[2], "w");
    if (!o) { perror("salida"); return 1; }
    fprintf(o, "{\"n\":%d,\"m\":%d,\"root\":%d,\"pos\":[", n, m, root);
    for (int i = 0; i < n; ++i) fprintf(o, "%s[%.3f,%.3f]", i ? "," : "", pos[i].first, pos[i].second);
    fprintf(o, "],\"edges\":[");
    for (int i = 0; i < m; ++i) fprintf(o, "%s[%d,%d]", i ? "," : "", edges[i].first, edges[i].second);
    fprintf(o, "],\"articulations\":[");
    bool first = true;
    for (int i = 0; i < n; ++i) if (isArt[i]) { fprintf(o, "%s%d", first ? "" : ",", i); first = false; }
    fprintf(o, "],\"num_components\":%zu,", comps.size());
    fprintf(o, "\"base_k\":%d,\"ops_tarjan\":%lld,\"ops_brute\":%lld,\"brute_arts\":%s,\"brute\":%s,\"events\":[\n",
            baseK, opsT, opsB, ba.c_str(), bj.c_str());
    for (size_t i = 0; i < events.size(); ++i)
        fprintf(o, "%s%s\n", events[i].c_str(), i + 1 < events.size() ? "," : "");
    fprintf(o, "]}\n");
    fclose(o);
    delete S;
    fprintf(stderr, "componentes: %zu | articulaciones:", comps.size());
    for (int i = 0; i < n; ++i) if (isArt[i]) fprintf(stderr, " %d", i);
    fprintf(stderr, "\n");
    return 0;
}
