@echo off
REM Windows: compila el C++ (g++ de MinGW), genera trazas y renderiza el video 1080p30.
cd /d %~dp0
g++ -O2 -std=c++17 -o cpp\bcc.exe cpp\bcc.cpp || exit /b 1
cpp\bcc.exe data\graph_main.txt data\trace_main.json 0
cpp\bcc.exe data\graph_disc.txt data\trace_disc.json 0
cd manim
manim -r 1920,1080 --fps 30 bcc_video.py BCCVideo
