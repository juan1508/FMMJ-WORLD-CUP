# -*- coding: utf-8 -*-
"""
matches_data.py
Genera el calendario inicial (fase de grupos + eliminatorias, formato clásico
FIFA de 32 equipos) como una estructura de Python en memoria. No lee ni
escribe archivos: la función generate_initial_matches() siempre produce el
mismo calendario base (partidos sin jugar), listo para ser usado por app.py.
"""
import itertools
from teams_data import GROUPS


def generate_initial_matches():
    matches = []
    match_id = 1

    # ---- FASE DE GRUPOS: round robin de 4 equipos, 3 jornadas x 2 partidos ----
    for group_letter, teamlist in GROUPS.items():
        codes = [t["code"] for t in teamlist]
        schedule = [
            [(codes[0], codes[1]), (codes[2], codes[3])],
            [(codes[0], codes[2]), (codes[1], codes[3])],
            [(codes[0], codes[3]), (codes[1], codes[2])],
        ]
        for jornada_idx, day_pairs in enumerate(schedule, start=1):
            for home, away in day_pairs:
                matches.append({
                    "id": match_id, "stage": "group", "group": group_letter,
                    "jornada": jornada_idx, "home": home, "away": away,
                    "home_goals": None, "away_goals": None, "played": False,
                    "goals": [],
                })
                match_id += 1

    # ---- OCTAVOS: cruces clásicos 1ro/2do de grupos cruzados ----
    r16_labels = [
        ("1A", "2B"), ("1C", "2D"), ("1E", "2F"), ("1G", "2H"),
        ("1B", "2A"), ("1D", "2C"), ("1F", "2E"), ("1H", "2G"),
    ]
    for i, (h, a) in enumerate(r16_labels, start=1):
        matches.append({
            "id": match_id, "stage": "r16", "slot": i, "home": h, "away": a,
            "home_goals": None, "away_goals": None, "played": False, "goals": [],
        })
        match_id += 1

    # ---- CUARTOS ----
    for i in range(1, 5):
        matches.append({
            "id": match_id, "stage": "qf", "slot": i,
            "home": f"W-r16-{2*i-1}", "away": f"W-r16-{2*i}",
            "home_goals": None, "away_goals": None, "played": False, "goals": [],
        })
        match_id += 1

    # ---- SEMIS ----
    for i in range(1, 3):
        matches.append({
            "id": match_id, "stage": "sf", "slot": i,
            "home": f"W-qf-{2*i-1}", "away": f"W-qf-{2*i}",
            "home_goals": None, "away_goals": None, "played": False, "goals": [],
        })
        match_id += 1

    # ---- TERCER PUESTO ----
    matches.append({
        "id": match_id, "stage": "3rd", "slot": 1,
        "home": "L-sf-1", "away": "L-sf-2",
        "home_goals": None, "away_goals": None, "played": False, "goals": [],
    })
    match_id += 1

    # ---- FINAL ----
    matches.append({
        "id": match_id, "stage": "final", "slot": 1,
        "home": "W-sf-1", "away": "W-sf-2",
        "home_goals": None, "away_goals": None, "played": False, "goals": [],
    })
    match_id += 1

    return matches
