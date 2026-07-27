# -*- coding: utf-8 -*-
"""
matches_data.py
Genera el calendario inicial (vacío, sin jugar) de FMMJ WORLD CUP UNITED 26:
- Fase de grupos: 8 grupos x 6 partidos (todos contra todos, 3 jornadas).
- Eliminatorias: Octavos (8) -> Cuartos (4) -> Semifinal (2) -> Tercer puesto (1)
  y Gran Final (1), con los cruces clásicos de un mundial de 32 equipos.

Cada partido es un dict con, como mínimo:
    id, stage, group, jornada, slot, home, away,
    home_goals, away_goals, played, goals, pen_home, pen_away

En fase de grupos "home"/"away" son códigos de selección (p.ej. "MEX").
En eliminatorias "home"/"away" son etiquetas que se resuelven en tiempo real:
    - "1A" / "2B"  -> 1° o 2° lugar del grupo A / B
    - "W-r16-3"    -> ganador del partido de Octavos #3
    - "L-sf-1"     -> perdedor del partido de Semifinal #1
"""

from teams_data import GROUPS

_next_id = 0


def _new_id():
    global _next_id
    _next_id += 1
    return _next_id


def _group_stage_matches():
    matches = []
    # Orden clásico de round-robin para 4 equipos (3 jornadas, 2 partidos c/u)
    schedule = [(0, 1), (2, 3), (0, 2), (3, 1), (0, 3), (1, 2)]
    for group_letter, teamlist in GROUPS.items():
        codes = [t["code"] for t in teamlist]
        for idx, (i, j) in enumerate(schedule):
            jornada = idx // 2 + 1
            matches.append({
                "id": _new_id(),
                "stage": "group",
                "group": group_letter,
                "jornada": jornada,
                "slot": None,
                "home": codes[i],
                "away": codes[j],
                "home_goals": 0,
                "away_goals": 0,
                "played": False,
                "goals": [],
                "pen_home": None,
                "pen_away": None,
            })
    return matches


def _knockout_matches():
    matches = []

    # Octavos de Final - cruces clásicos 1°/2° de cada grupo (8 grupos)
    r16_pairs = [
        ("1A", "2B"), ("1C", "2D"), ("1E", "2F"), ("1G", "2H"),
        ("1B", "2A"), ("1D", "2C"), ("1F", "2E"), ("1H", "2G"),
    ]
    for slot, (home, away) in enumerate(r16_pairs, start=1):
        matches.append({
            "id": _new_id(), "stage": "r16", "group": None, "jornada": None,
            "slot": slot, "home": home, "away": away,
            "home_goals": 0, "away_goals": 0, "played": False,
            "goals": [], "pen_home": None, "pen_away": None,
        })

    # Cuartos de Final: (r16-1,r16-2)->qf1, (r16-3,r16-4)->qf2, ...
    for slot in range(1, 5):
        s1, s2 = 2 * slot - 1, 2 * slot
        matches.append({
            "id": _new_id(), "stage": "qf", "group": None, "jornada": None,
            "slot": slot, "home": f"W-r16-{s1}", "away": f"W-r16-{s2}",
            "home_goals": 0, "away_goals": 0, "played": False,
            "goals": [], "pen_home": None, "pen_away": None,
        })

    # Semifinal: (qf1,qf2)->sf1, (qf3,qf4)->sf2
    for slot in range(1, 3):
        s1, s2 = 2 * slot - 1, 2 * slot
        matches.append({
            "id": _new_id(), "stage": "sf", "group": None, "jornada": None,
            "slot": slot, "home": f"W-qf-{s1}", "away": f"W-qf-{s2}",
            "home_goals": 0, "away_goals": 0, "played": False,
            "goals": [], "pen_home": None, "pen_away": None,
        })

    # Tercer puesto (perdedores de semis)
    matches.append({
        "id": _new_id(), "stage": "3rd", "group": None, "jornada": None,
        "slot": 1, "home": "L-sf-1", "away": "L-sf-2",
        "home_goals": 0, "away_goals": 0, "played": False,
        "goals": [], "pen_home": None, "pen_away": None,
    })

    # Gran Final (ganadores de semis)
    matches.append({
        "id": _new_id(), "stage": "final", "group": None, "jornada": None,
        "slot": 1, "home": "W-sf-1", "away": "W-sf-2",
        "home_goals": 0, "away_goals": 0, "played": False,
        "goals": [], "pen_home": None, "pen_away": None,
    })

    return matches


def generate_initial_matches():
    global _next_id
    _next_id = 0
    return _group_stage_matches() + _knockout_matches()
