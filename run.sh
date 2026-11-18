#!/usr/bin/env bash
# Compila el C++, genera las trazas y renderiza el video.
# Uso: ./run.sh [l|m|h]      l = 480p15 (rápido), m = 720p30, h = 1080p30 (por defecto)
set -euo pipefail
cd "$(dirname "$0")"
Q="${1:-h}"

echo "[1/3] Compilando la implementación C++ ..."
g++ -O2 -std=c++17 -Wall -Wextra -o cpp/bcc cpp/bcc.cpp

echo "[2/3] Generando las trazas (salida real del algoritmo) ..."
./cpp/bcc data/graph_main.txt data/trace_main.json 0
./cpp/bcc data/graph_disc.txt data/trace_disc.json 0

echo "[3/3] Renderizando con Manim ..."
cd manim
case "$Q" in
  l) manim -ql bcc_video.py BCCVideo ;;
  m) manim -qm bcc_video.py BCCVideo ;;
  *) manim -r 1920,1080 --fps 30 bcc_video.py BCCVideo ;;
esac
echo "Listo. El .mp4 queda en manim/media/videos/bcc_video/"
