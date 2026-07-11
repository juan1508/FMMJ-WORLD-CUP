# -*- coding: utf-8 -*-
"""
teams_data.py
Datos de las 32 selecciones de FMMJ WORLD CUP UNITED 26: grupos, presidentes
y colores/banderas de anfitriones.

100% autocontenido (no depende de ningún archivo externo ni de generación
aleatoria), para evitar problemas de despliegue en Streamlit Cloud / GitHub.

--------------------------------------------------------------------------
NOTA SOBRE BANDERAS
--------------------------------------------------------------------------
Los emojis de bandera (🇲🇽, 🇰🇷, etc.) requieren una fuente de emoji a color
instalada en el sistema que renderiza. Streamlit Cloud corre sobre Linux
headless, que normalmente NO trae fuentes de emoji a color, así que esas
banderas no se ven ahí (aunque el emoji esté perfectamente escrito en el
código).

Solución: cada selección tiene "flag_url", un link a una imagen PNG real de
la bandera (servicio gratuito flagcdn.com, sin scraping ni API key):

    import streamlit as st
    team = TEAMS["MEX"]
    st.image(team["flag_url"], width=40)

El campo "flag" (emoji) se conserva como respaldo/alternativa, por si en
algún entorno sí renderiza (por ejemplo localmente en Windows/Mac).
"""

GROUPS = {
    "A": [
        {"code": "MEX", "name": "México", "flag": "🇲🇽", "president": "Mati"},
        {"code": "KOR", "name": "Corea del Sur", "flag": "🇰🇷", "president": "Jnka"},
        {"code": "UKR", "name": "Ucrania", "flag": "🇺🇦", "president": "Dibu"},
        {"code": "NOR", "name": "Noruega", "flag": "🇳🇴", "president": "Mati"},
    ],
    "B": [
        {"code": "CAN", "name": "Canadá", "flag": "🇨🇦", "president": "Jnka"},
        {"code": "SUI", "name": "Suiza", "flag": "🇨🇭", "president": "Dibu"},
        {"code": "ITA", "name": "Italia", "flag": "🇮🇹", "president": "Jnka"},
        {"code": "ARG", "name": "Argentina", "flag": "🇦🇷", "president": "Mati"},
    ],
    "C": [
        {"code": "BRA", "name": "Brasil", "flag": "🇧🇷", "president": "Jnka"},
        {"code": "MAR", "name": "Marruecos", "flag": "🇲🇦", "president": "Mati"},
        {"code": "SCO", "name": "Escocia", "flag": "🏴", "president": "Dibu"},
        {"code": "POR", "name": "Portugal", "flag": "🇵🇹", "president": "Dibu"},
    ],
    "D": [
        {"code": "USA", "name": "Estados Unidos", "flag": "🇺🇸", "president": "Mati"},
        {"code": "PAR", "name": "Paraguay", "flag": "🇵🇾", "president": "Dibu"},
        {"code": "TUR", "name": "Turquía", "flag": "🇹🇷", "president": "Mati"},
        {"code": "ENG", "name": "Inglaterra", "flag": "🏴", "president": "Jnka"},
    ],
    "E": [
        {"code": "GER", "name": "Alemania", "flag": "🇩🇪", "president": "Jnka"},
        {"code": "AUT", "name": "Austria", "flag": "🇦🇹", "president": "Mati"},
        {"code": "ECU", "name": "Ecuador", "flag": "🇪🇨", "president": "Dibu"},
        {"code": "CUW", "name": "Curazao", "flag": "🇨🇼", "president": "Dibu"},
    ],
    "F": [
        {"code": "NED", "name": "Países Bajos", "flag": "🇳🇱", "president": "Mati"},
        {"code": "JPN", "name": "Japón", "flag": "🇯🇵", "president": "Jnka"},
        {"code": "SWE", "name": "Suecia", "flag": "🇸🇪", "president": "Dibu"},
        {"code": "SEN", "name": "Senegal", "flag": "🇸🇳", "president": "Jnka"},
    ],
    "G": [
        {"code": "BEL", "name": "Bélgica", "flag": "🇧🇪", "president": "Dibu"},
        {"code": "COL", "name": "Colombia", "flag": "🇨🇴", "president": "Jnka"},
        {"code": "CRO", "name": "Croacia", "flag": "🇭🇷", "president": "Mati"},
        {"code": "CIV", "name": "Costa de Marfil", "flag": "🇨🇮", "president": "Mati"},
    ],
    "H": [
        {"code": "ESP", "name": "España", "flag": "🇪🇸", "president": "Mati"},
        {"code": "URU", "name": "Uruguay", "flag": "🇺🇾", "president": "Jnka"},
        {"code": "GHA", "name": "Ghana", "flag": "🇬🇭", "president": "Dibu"},
        {"code": "FRA", "name": "Francia", "flag": "🇫🇷", "president": "Dibu"},
    ],
}

HOSTS = {
    "MEX": {"color": "#006341", "name": "México"},   # verde
    "USA": {"color": "#0A3161", "name": "Estados Unidos"},  # azul
    "CAN": {"color": "#D80621", "name": "Canadá"},   # rojo
}

# --------------------------------------------------------------------------
# Mapeo de código FIFA/interno -> código ISO 3166-1 alpha-2 (o subdivisión)
# usado por flagcdn.com para servir la imagen real de cada bandera.
# --------------------------------------------------------------------------
ISO2_MAP = {
    "MEX": "mx", "KOR": "kr", "UKR": "ua", "NOR": "no",
    "CAN": "ca", "SUI": "ch", "ITA": "it", "ARG": "ar",
    "BRA": "br", "MAR": "ma", "SCO": "gb-sct", "POR": "pt",
    "USA": "us", "PAR": "py", "TUR": "tr", "ENG": "gb-eng",
    "GER": "de", "AUT": "at", "ECU": "ec", "CUW": "cw",
    "NED": "nl", "JPN": "jp", "SWE": "se", "SEN": "sn",
    "BEL": "be", "COL": "co", "CRO": "hr", "CIV": "ci",
    "ESP": "es", "URU": "uy", "GHA": "gh", "FRA": "fr",
}


def flag_url(code: str, width: int = 80) -> str:
    """
    Devuelve la URL de la imagen PNG de la bandera para un código de
    selección (por ejemplo "MEX"). width puede ser 20, 40, 80, 160, 320
    o 640 (tamaños que ofrece flagcdn.com).
    """
    iso2 = ISO2_MAP.get(code)
    if not iso2:
        return ""
    return f"https://flagcdn.com/w{width}/{iso2}.png"


def _build_teams():
    teams = {}
    for group_letter, teamlist in GROUPS.items():
        for t in teamlist:
            teams[t["code"]] = {
                "code": t["code"],
                "name": t["name"],
                "flag": t["flag"],                 # emoji (respaldo, puede no verse en Linux/servidor)
                "flag_url": flag_url(t["code"]),   # imagen PNG real, siempre visible
                "president": t["president"],
                "group": group_letter,
                "is_host": t["code"] in HOSTS,
            }
    return teams


TEAMS = _build_teams()
