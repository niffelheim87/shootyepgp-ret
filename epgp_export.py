#!/usr/bin/env python3
"""
epgp_export.py
--------------
Convierte el SavedVariables de shootyepgp a CSV y JSON.

Modos de uso:
  1. Pon este script en la misma carpeta que shootyepgp.lua y ejecútalo.
  2. Ejecútalo desde cualquier carpeta y te pedirá la ruta de WoW.
"""

import re
import json
import csv
import os
import sys

CSV_OUT  = "epgp_export.csv"
JSON_OUT = "epgp_export.json"

RUTAS_WOW_COMUNES = [
    r"C:\Program Files\World of Warcraft",
    r"C:\Program Files (x86)\World of Warcraft",
    r"C:\WoW",
    r"D:\World of Warcraft",
    r"D:\WoW",
    r"D:\Games\World of Warcraft",
    r"D:\Games\WoW",
]


def buscar_lua_en_wow(ruta_wow):
    """Busca shootyepgp.lua dentro de la carpeta WTF de una instalación de WoW."""
    wtf = os.path.join(ruta_wow, "WTF", "Account")
    if not os.path.exists(wtf):
        return None
    for root, dirs, files in os.walk(wtf):
        for f in files:
            if f == "shootyepgp.lua":
                return os.path.join(root, f)
    return None


def encontrar_lua():
    """
    Busca el archivo shootyepgp.lua en este orden:
      1. Misma carpeta que el script
      2. Rutas de WoW comunes en disco
      3. Pregunta al usuario
    """

    # 1. Misma carpeta que el script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    local = os.path.join(script_dir, "shootyepgp.lua")
    if os.path.exists(local):
        print(f"[OK] Archivo encontrado junto al script: {local}")
        return local

    # 2. Rutas comunes de WoW
    print("Buscando WoW en rutas comunes...")
    for ruta in RUTAS_WOW_COMUNES:
        resultado = buscar_lua_en_wow(ruta)
        if resultado:
            print(f"[OK] Archivo encontrado automaticamente: {resultado}")
            return resultado

    # 3. Preguntar al usuario
    print()
    print("No se encontro shootyepgp.lua automaticamente.")
    print("Opciones:")
    print("  A) Indica la carpeta raiz de tu WoW  (ej: C:\\WoW  o  D:\\Games\\WoW)")
    print("  B) Indica la ruta completa al archivo shootyepgp.lua")
    print()

    while True:
        ruta = input("Introduce la ruta y pulsa Enter: ").strip().strip('"')

        if not ruta:
            print("Ruta vacia, intentalo de nuevo.")
            continue

        # Si apunta directamente al .lua
        if ruta.lower().endswith(".lua") and os.path.exists(ruta):
            return ruta

        # Si apunta a la carpeta raiz del WoW
        resultado = buscar_lua_en_wow(ruta)
        if resultado:
            print(f"[OK] Archivo encontrado: {resultado}")
            return resultado

        # Si apunta a una carpeta que contiene directamente el .lua
        candidato = os.path.join(ruta, "shootyepgp.lua")
        if os.path.exists(candidato):
            print(f"[OK] Archivo encontrado: {candidato}")
            return candidato

        print(f"No se encontro shootyepgp.lua en: {ruta}")
        print("Comprueba la ruta e intentalo de nuevo.")
        print()


def parse_export_block(content):
    """
    Extrae el bloque shootyepgp_export_data del archivo .lua
    y parsea cada entrada { name="X", class="Y", ep=N, gp=N, pr=N }
    """
    start = content.find("shootyepgp_export_data =")
    if start == -1:
        return None

    pattern = re.compile(
        r'\{\s*'
        r'name\s*=\s*"([^"]+)"\s*,\s*'
        r'class\s*=\s*"([^"]+)"\s*,\s*'
        r'ep\s*=\s*([\d.]+)\s*,\s*'
        r'gp\s*=\s*([\d.]+)\s*,\s*'
        r'pr\s*=\s*([\d.e+\-]+)\s*'
        r'\}'
    )

    players = []
    for m in pattern.finditer(content, start):
        players.append({
            "name":  m.group(1),
            "class": m.group(2),
            "ep":    float(m.group(3)),
            "gp":    float(m.group(4)),
            "pr":    float(m.group(5)),
        })

    return players


def main():
    print("=" * 55)
    print("  shootyepgp - Exportador EP/GP")
    print("=" * 55)
    print()

    lua_path = encontrar_lua()

    print(f"\nLeyendo: {lua_path}")
    with open(lua_path, "r", encoding="utf-8") as f:
        content = f.read()

    players = parse_export_block(content)

    if players is None:
        print("\nERROR: No se encontro 'shootyepgp_export_data' en el archivo.")
        print("Asegurate de haber ejecutado /shootyexport en el juego y luego /quit.")
        input("\nPulsa Enter para salir...")
        sys.exit(1)

    if len(players) == 0:
        print("\nAVISO: Se encontro la variable pero esta vacia.")
        input("\nPulsa Enter para salir...")
        sys.exit(0)

    players.sort(key=lambda x: x["pr"], reverse=True)

    # Guardar los archivos de salida junto al script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path   = os.path.join(script_dir, CSV_OUT)
    json_path  = os.path.join(script_dir, JSON_OUT)

    # CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "class", "ep", "gp", "pr"])
        writer.writeheader()
        for p in players:
            writer.writerow({
                "name":  p["name"],
                "class": p["class"],
                "ep":    int(p["ep"]),
                "gp":    int(p["gp"]),
                "pr":    round(p["pr"], 4),
            })
    print(f"CSV  guardado en: {csv_path}")

    # JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(players, f, indent=2, ensure_ascii=False)
    print(f"JSON guardado en: {json_path}")

    print(f"\nTotal jugadores exportados: {len(players)}")

    print("\n--- Top 5 por PR ---")
    print(f"{'Nombre':<20} {'Clase':<10} {'EP':>6} {'GP':>6} {'PR':>8}")
    print("-" * 55)
    for p in players[:5]:
        print(f"{p['name']:<20} {p['class']:<10} {int(p['ep']):>6} {int(p['gp']):>6} {p['pr']:>8.4f}")

    print()
    input("Pulsa Enter para salir...")


if __name__ == "__main__":
    main()
