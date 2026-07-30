# -*- coding: utf-8 -*-
import streamlit as st
import json
import os
import base64

from teams_data import TEAMS, GROUPS, HOSTS
from matches_data import generate_initial_matches
from scorers_data import TEAM_SQUADS, initialize_scorers_state, add_goal, get_top_scorers

# ---------------------------------------------------------------
# LOGO: se carga con st.image() nativo (sin limitaciones de tamaño)
# ---------------------------------------------------------------
LOGO_PATH = "logo.png"

st.set_page_config(page_title="FMMJ WORLD CUP UNITED 26", page_icon=LOGO_PATH, layout="wide")

STATE_PATH = "tournament_state.json"
GOLD = "#C9A24B"
CYAN = "#00E5FF"
DARK_BG = "#0D0D1A"
CARD_BG = "rgba(15, 25, 45, 0.85)"
ACCENT = "#1A1A3E"
WHITE = "#FFFFFF"
PURPLE_GLOW = "#7B2FBE"
PRESIDENTS_COLORS = {"Mati": "#006341", "Jnka": "#0A3161", "Dibu": "#D80621"}

STAGE_NAMES = {
    "group": "Fase de Grupos", "r16": "Octavos de Final", "qf": "Cuartos de Final",
    "sf": "Semifinal", "3rd": "Tercer Puesto", "final": "GRAN FINAL",
}

# ---------------------------------------------------------------
# CSS PREMIUM
# ---------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;600&display=swap');

/* === RESET & BASE === */
.stApp {{
    background: linear-gradient(160deg, #0a0a1a 0%, #0d1b2a 30%, #1a0a2e 60%, #0a0a1a 100%);
    color: {WHITE};
    font-family: 'Rajdhani', sans-serif;
    min-height: 100vh;
}}

/* === HEADER PREMIUM === */
.main-header {{
    background: linear-gradient(135deg, rgba(10,10,26,0.95) 0%, rgba(26,10,46,0.9) 50%, rgba(10,10,26,0.95) 100%);
    border-bottom: 3px solid transparent;
    border-image: linear-gradient(90deg, {CYAN}, {GOLD}, {CYAN}) 1;
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(20px);
    margin-bottom: 25px;
    border-radius: 0 0 25px 25px;
    position: relative;
    overflow: hidden;
}}

.tournament-title {{ 
    font-family: 'Orbitron', sans-serif; 
    font-weight: 900;
    color: transparent;
    background: linear-gradient(135deg, {CYAN} 0%, {GOLD} 50%, {CYAN} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.5rem; 
    letter-spacing: 6px;
    margin: 8px 0 5px 0;
    text-shadow: none;
}}

.subtitle {{
    color: {GOLD}; 
    letter-spacing: 3px; 
    opacity: 0.7;
    font-size: 0.9rem;
    font-family: 'Inter', sans-serif;
    font-weight: 300;
}}

/* === CARDS === */
.match-card {{
    background: {CARD_BG};
    border: 1px solid rgba(0,229,255,0.15);
    border-radius: 15px;
    padding: 18px;
    margin: 12px 0;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}}
.match-card::after {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, {CYAN}, {GOLD});
}}

.score-display {{ 
    font-family: 'Orbitron', sans-serif; 
    font-size: 1.8rem; 
    font-weight: 700;
    color: {GOLD};
    text-shadow: 0 0 10px rgba(201,162,75,0.3);
}}

/* === TABLES === */
.standings-table {{ 
    width: 100%; 
    border-collapse: separate; 
    border-spacing: 0 4px;
    border-radius: 10px;
}}
.standings-table th {{ 
    background: linear-gradient(135deg, #1a0a2e, #0d1b2a); 
    color: {CYAN}; 
    padding: 14px 12px;
    font-family: 'Orbitron', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}}
.standings-table td {{ 
    background: rgba(255,255,255,0.03); 
    padding: 12px;
    border-bottom: 1px solid rgba(255,255,255,0.03);
}}
.standings-table tr:hover td {{
    background: rgba(0,229,255,0.05);
}}
.qualified-row {{ 
    border-left: 4px solid {CYAN}; 
    background: rgba(0,229,255,0.08) !important;
}}

/* === BADGES === */
.president-badge {{
    padding: 3px 10px; 
    border-radius: 20px; 
    font-size: 0.7rem; 
    font-weight: 700;
    text-transform: uppercase;
    margin-left: 8px;
    letter-spacing: 0.5px;
}}

/* === STAGE SECTIONS === */
.stage-section {{
    border-left: 3px solid {GOLD};
    padding-left: 15px;
    margin: 20px 0;
}}
.stage-title {{
    font-family: 'Orbitron', sans-serif;
    color: {GOLD};
    font-size: 1.3rem;
    letter-spacing: 2px;
}}

/* === SCORER TABLE === */
.scorer-rank {{
    font-family: 'Orbitron', sans-serif;
    font-weight: 900;
    font-size: 1.2rem;
}}

/* === TABS === */
.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    padding: 0;
}}
.stTabs [data-baseweb="tab"] {{
    font-family: 'Rajdhani', sans-serif;
    font-weight: 600;
    color: rgba(255,255,255,0.6);
    padding: 8px 16px;
    border-radius: 8px 8px 0 0;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, rgba(0,229,255,0.2), rgba(123,47,190,0.1)) !important;
    color: {CYAN} !important;
    border-bottom: 2px solid {CYAN} !important;
}}

/* === SIDEBAR === */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0a0a1a 0%, #1a0a2e 100%) !important;
    border-right: 1px solid rgba(0,229,255,0.1);
}}
[data-testid="stSidebarHeader"] {{
    font-family: 'Orbitron', sans-serif;
}}

/* === EXPANDER === */
.streamlit-expanderHeader {{
    font-family: 'Rajdhani', sans-serif;
    font-weight: 700;
}}

/* === WELCOME CARD === */
.welcome-card {{
    background: {CARD_BG};
    padding: 30px; 
    border-radius: 20px; 
    border: 1px solid rgba(0,229,255,0.2);
    position: relative;
    overflow: hidden;
}}

/* === SCROLLBAR === */
::-webkit-scrollbar {{
    width: 6px;
}}
::-webkit-scrollbar-track {{
    background: rgba(0,0,0,0.2);
}}
::-webkit-scrollbar-thumb {{
    background: linear-gradient(180deg, {CYAN}, {GOLD});
    border-radius: 3px;
}}

/* === BRACKET STYLES === */
.bracket-container {{
    display: flex;
    overflow-x: auto;
    padding: 30px 20px;
    gap: 0;
    align-items: stretch;
    min-height: 900px;
    position: relative;
}}
.bracket-column {{
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    min-width: 220px;
    position: relative;
    padding: 0 20px;
}}
.bracket-column-title {{
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    color: {GOLD};
    font-size: 0.75rem;
    letter-spacing: 2px;
    margin-bottom: 15px;
    text-transform: uppercase;
    padding: 8px 12px;
    background: linear-gradient(135deg, rgba(0,229,255,0.1), rgba(123,47,190,0.1));
    border-radius: 8px;
    border: 1px solid rgba(0,229,255,0.2);
}}
.bracket-match {{
    background: rgba(10, 15, 30, 0.95);
    border: 1px solid rgba(0,229,255,0.25);
    border-radius: 10px;
    padding: 0;
    margin: 6px 0;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 15px rgba(0,229,255,0.05);
    transition: all 0.3s ease;
}}
.bracket-match:hover {{
    border-color: rgba(0,229,255,0.5);
    box-shadow: 0 0 25px rgba(0,229,255,0.1);
}}
.bracket-match::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, {CYAN}, {GOLD});
    opacity: 0.6;
}}
.bracket-team-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 12px;
    transition: all 0.2s ease;
}}
.bracket-team-row:hover {{
    background: rgba(0,229,255,0.05);
}}
.bracket-team-row.winner {{
    background: rgba(0,229,255,0.08);
}}
.bracket-team-row.loser {{
    opacity: 0.5;
}}
.bracket-team-name {{
    font-size: 0.8rem;
    font-weight: 600;
    color: rgba(255,255,255,0.9);
    display: flex;
    align-items: center;
    gap: 6px;
}}
.bracket-team-name.unknown {{
    color: rgba(255,255,255,0.35);
    font-style: italic;
}}
.bracket-score {{
    font-family: 'Orbitron', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    color: {GOLD};
    min-width: 20px;
    text-align: center;
}}
.bracket-score.pending {{
    color: rgba(255,255,255,0.25);
}}
.bracket-divider {{
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,229,255,0.2), transparent);
    margin: 0;
}}
.bracket-match-label {{
    text-align: center;
    font-size: 0.6rem;
    color: rgba(255,255,255,0.3);
    padding: 4px 0 2px 0;
    font-family: 'Inter', sans-serif;
    letter-spacing: 1px;
}}

/* Third Place Column */
.bracket-column-third {{
    min-width: 220px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 20px;
}}

/* Final Column */
.bracket-column-final {{
    min-width: 240px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 20px;
}}
.bracket-champion {{
    background: linear-gradient(135deg, rgba(201,162,75,0.2), rgba(0,229,255,0.1));
    border: 2px solid {GOLD};
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    margin-top: 15px;
    box-shadow: 0 0 30px rgba(201,162,75,0.15);
}}
.bracket-champion-title {{
    font-family: 'Orbitron', sans-serif;
    font-size: 0.65rem;
    color: {GOLD};
    letter-spacing: 2px;
    margin-bottom: 8px;
}}
.bracket-champion-name {{
    font-family: 'Orbitron', sans-serif;
    font-size: 1.1rem;
    font-weight: 900;
    color: {GOLD};
    text-shadow: 0 0 15px rgba(201,162,75,0.4);
}}
</style>
""", unsafe_allow_html=True)

# Logo con st.image() nativo (no tiene limitaciones de tamaño)
if os.path.exists(LOGO_PATH):
    col_logo_left, col_logo_img, col_logo_right = st.columns([3, 1, 3])
    with col_logo_img:
        st.image(LOGO_PATH, width=180)

# ---------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------
def flag_img(code, size="md"):
    """Retorna HTML con bandera circular."""
    if code not in TEAMS:
        return "❓"
    url = TEAMS[code]["flag_url"]
    if size == "md":
        w = "48"
    else:
        w = "32"
    return f'<img src="{url}" style="width:{w}px; height:{w}px; border-radius:50%; object-fit:cover; vertical-align:middle; margin-right:8px; border:1px solid rgba(0,229,255,0.3);">'

def president_badge(president):
    color = PRESIDENTS_COLORS.get(president, "#666666")
    return f'<span class="president-badge" style="background-color:{color}; color:white;">{president}</span>'

def load_state():
    if "tourn_state" in st.session_state:
        return st.session_state["tourn_state"]
    if os.path.exists(STATE_PATH):
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
    else:
        state = {"matches": generate_initial_matches(), "scorers": initialize_scorers_state()}
        save_state(state)
    st.session_state["tourn_state"] = state
    return state

def save_state(state):
    st.session_state["tourn_state"] = state
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)

def team_label_md(code):
    t = TEAMS[code]
    return f"{flag_img(code, 'sm')} **{t['name']}** {president_badge(t['president'])}"

# ---------------------------------------------------------------
# LÓGICA DE TORNEO
# ---------------------------------------------------------------
def compute_standings(matches, group_letter):
    codes = [t["code"] for t in GROUPS[group_letter]]
    table = {c: {"code": c, "PJ": 0, "PG": 0, "PE": 0, "PP": 0, "GF": 0, "GC": 0, "Pts": 0} for c in codes}
    for m in matches:
        if m["stage"] != "group" or m["group"] != group_letter or not m["played"]:
            continue
        h, a, hg, ag = m["home"], m["away"], m["home_goals"], m["away_goals"]
        table[h]["PJ"] += 1; table[a]["PJ"] += 1
        table[h]["GF"] += hg; table[h]["GC"] += ag
        table[a]["GF"] += ag; table[a]["GC"] += hg
        if hg > ag:
            table[h]["PG"] += 1; table[h]["Pts"] += 3; table[a]["PP"] += 1
        elif ag > hg:
            table[a]["PG"] += 1; table[a]["Pts"] += 3; table[h]["PP"] += 1
        else:
            table[h]["PE"] += 1; table[h]["Pts"] += 1; table[a]["PE"] += 1; table[a]["Pts"] += 1
    return sorted(table.values(), key=lambda r: (r["Pts"], r["GF"] - r["GC"], r["GF"]), reverse=True)

def get_qualifier(matches, group_letter, position):
    complete = all(m["played"] for m in matches if m["stage"] == "group" and m["group"] == group_letter)
    if not complete: return None
    return compute_standings(matches, group_letter)[position - 1]["code"]

def resolve_label(matches, label):
    if label.startswith("W-") or label.startswith("L-"):
        kind, stage, slot = label.split("-")
        m = next((x for x in matches if x["stage"] == stage and x["slot"] == int(slot)), None)
        if not m or not m["played"]: return None
        if m["home_goals"] > m["away_goals"]: w, l = m["home_team"], m["away_team"]
        elif m["away_goals"] > m["home_goals"]: w, l = m["away_team"], m["home_team"]
        else:
            w = m["home_team"] if m.get("pen_home", 0) > m.get("pen_away", 0) else m["away_team"]
            l = m["away_team"] if w == m["home_team"] else m["home_team"]
        return w if kind == "W" else l
    return get_qualifier(matches, label[1], int(label[0]))

def annotate_knockout(matches):
    for m in matches:
        if m["stage"] == "group":
            m["home_team"], m["away_team"] = m["home"], m["away"]
        else:
            m["home_team"] = resolve_label(matches, m["home"])
            m["away_team"] = resolve_label(matches, m["away"])
    return matches

def get_winner(match):
    """Retorna el ganador de un partido (team_code o None)."""
    if not match["played"]:
        return None
    if match["home_goals"] > match["away_goals"]:
        return match["home_team"]
    elif match["away_goals"] > match["home_goals"]:
        return match["away_team"]
    else:
        # Penales
        if match.get("pen_home") is not None and match.get("pen_away") is not None:
            if match["pen_home"] > match["pen_away"]:
                return match["home_team"]
            elif match["pen_away"] > match["pen_home"]:
                return match["away_team"]
        return None

def get_loser(match):
    """Retorna el perdedor de un partido (team_code o None)."""
    if not match["played"]:
        return None
    winner = get_winner(match)
    if winner is None:
        return None
    if winner == match["home_team"]:
        return match["away_team"]
    return match["home_team"]

def team_display_name(code):
    if code and code in TEAMS:
        return TEAMS[code]["name"]
    return "Por definir..."

def bracket_match_html(match, label=""):
    """Genera HTML para un partido del bracket."""
    h = match["home_team"]
    a = match["away_team"]
    h_name = team_display_name(h)
    a_name = team_display_name(a)
    
    h_known = h is not None and h in TEAMS
    a_known = a is not None and a in TEAMS
    
    h_class = ""
    a_class = ""
    h_score_class = ""
    a_score_class = ""
    
    if match["played"]:
        winner = get_winner(match)
        if winner == h:
            h_class = "winner"
            a_class = "loser"
        elif winner == a:
            a_class = "winner"
            h_class = "loser"
    
    if match["played"]:
        h_score_str = str(match["home_goals"])
        a_score_str = str(match["away_goals"])
    else:
        h_score_str = "-"
        a_score_str = "-"
        h_score_class = "pending"
        a_score_class = "pending"
    
    h_flag = flag_img(h, 'sm') if h_known else ""
    a_flag = flag_img(a, 'sm') if a_known else ""
    
    name_class = "" if h_known else "unknown"
    name_class2 = "" if a_known else "unknown"
    
    status = "✓" if match["played"] else "⏳"
    
    html = f"""
    <div class="bracket-match">
        <div class="bracket-match-label">{label} {status}</div>
        <div class="bracket-team-row {h_class}">
            <div class="bracket-team-name {name_class}">{h_flag if h_known else '<span style="opacity:0.4">?</span>'} {h_name}</div>
            <div class="bracket-score {h_score_class}">{h_score_str}</div>
        </div>
        <div class="bracket-divider"></div>
        <div class="bracket-team-row {a_class}">
            <div class="bracket-team-name {name_class2}">{a_flag if a_known else '<span style="opacity:0.4">?</span>'} {a_name}</div>
            <div class="bracket-score {a_score_class}">{a_score_str}</div>
        </div>
    </div>
    """
    return html


def generate_bracket_html(matches):
    """Genera el HTML completo del bracket visual."""
    
    r16_matches = [m for m in matches if m["stage"] == "r16"]
    qf_matches = [m for m in matches if m["stage"] == "qf"]
    sf_matches = [m for m in matches if m["stage"] == "sf"]
    final_match = next((m for m in matches if m["stage"] == "final"), None)
    third_match = next((m for m in matches if m["stage"] == "3rd"), None)
    
    # Calcular ganadores para mostrar campeón
    champion = None
    third_winner = None
    if final_match and final_match["played"]:
        champion = get_winner(final_match)
    if third_match and third_match["played"]:
        third_winner = get_winner(third_match)
    
    html = """
    <div class="bracket-container">
    """
    
    # Columna Octavos (8 partidos)
    html += '<div class="bracket-column">'
    html += '<div class="bracket-column-title">🔥 OCTAVOS DE FINAL</div>'
    for i, m in enumerate(r16_matches):
        html += bracket_match_html(m, f"MATCH {i+1}")
    html += '</div>'
    
    # Columna Cuartos (4 partidos)
    html += '<div class="bracket-column">'
    html += '<div class="bracket-column-title">⚡ CUARTOS DE FINAL</div>'
    for i, m in enumerate(qf_matches):
        html += bracket_match_html(m, f"CF {i+1}")
    html += '</div>'
    
    # Columna Semifinales (2 partidos)
    html += '<div class="bracket-column">'
    html += '<div class="bracket-column-title">🏆 SEMIFINALES</div>'
    for i, m in enumerate(sf_matches):
        html += bracket_match_html(m, f"SF {i+1}")
    html += '</div>'
    
    # Columna Tercer Puesto
    html += '<div class="bracket-column-third">'
    html += '<div class="bracket-column-title">🥉 TERCER PUESTO</div>'
    if third_match:
        html += bracket_match_html(third_match, "3rd")
    if third_winner:
        w_name = team_display_name(third_winner)
        w_flag = flag_img(third_winner, 'sm') if third_winner in TEAMS else ""
        html += f"""
        <div class="bracket-champion" style="border-color:{CYAN};">
            <div class="bracket-champion-title" style="color:{CYAN};">TERCER LUGAR</div>
            <div class="bracket-champion-name" style="color:{CYAN}; font-size:0.9rem;">{w_flag} {w_name}</div>
        </div>
        """
    html += '</div>'
    
    # Columna Final
    html += '<div class="bracket-column-final">'
    html += '<div class="bracket-column-title">👑 GRAN FINAL</div>'
    if final_match:
        html += bracket_match_html(final_match, "FINAL")
    if champion:
        c_name = team_display_name(champion)
        c_flag = flag_img(champion, 'sm') if champion in TEAMS else ""
        html += f"""
        <div class="bracket-champion">
            <div class="bracket-champion-title">🏆 CAMPEÓN FMMJ WORLD CUP 🏆</div>
            <div class="bracket-champion-name">{c_flag} {c_name}</div>
        </div>
        """
    html += '</div>'
    
    html += '</div>'
    return html


# ---------------------------------------------------------------
# APP PRINCIPAL
# ---------------------------------------------------------------
state = load_state()
matches = annotate_knockout(state["matches"])
STAGES_KO = ["r16", "qf", "sf", "final"]

page = st.sidebar.radio("🧭 NAVEGACIÓN", ["🏠 Inicio", "📊 Grupos y Tablas", "🏆 Fase Final", "👟 Bota de Oro", "⚙️ Admin"])

if page == "🏠 Inicio":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"""
        <div class='welcome-card'>
            <h2 style='color:{CYAN}; font-family:Orbitron,sans-serif; font-size:2rem; letter-spacing:3px;'>FMMJ WORLD CUP</h2>
            <p style='font-size:1.1rem; line-height:1.8; color:rgba(255,255,255,0.8);'>
                La competición más prestigiosa de la familia. 
                <b style='color:{GOLD};'>32 selecciones</b>, un solo objetivo: 
                <b style='color:{CYAN};'>la gloria eterna</b>.
            </p>
            <hr style='border-color:rgba(0,229,255,0.3); margin:20px 0;'>
            <h4 style='color:{GOLD}; font-family:Orbitron,sans-serif; letter-spacing:2px;'>PRESIDENTES OFICIALES</h4>
            <div style='display:flex; gap:25px; margin-top:15px;'>
                <div style='text-align:center;'>
                    <span style='font-size:2rem;'>🇲🇽</span>
                    <br>{president_badge('Mati')} Mati
                </div>
                <div style='text-align:center;'>
                    <span style='font-size:2rem;'>🇨🇦</span>
                    <br>{president_badge('Jnka')} Jnka
                </div>
                <div style='text-align:center;'>
                    <span style='font-size:2rem;'>🇺🇸</span>
                    <br>{president_badge('Dibu')} Dibu
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div style='background:{CARD_BG}; border:1px solid rgba(201,162,75,0.2); border-radius:15px; padding:20px; text-align:center;'>
            <h4 style='color:{GOLD}; font-family:Orbitron,sans-serif;'>ESTADÍSTICAS</h4>
            <div style='margin:15px 0;'>
                <div style='font-size:2.5rem; font-family:Orbitron,sans-serif; color:{CYAN}; font-weight:900;'>32</div>
                <div style='color:rgba(255,255,255,0.5); font-size:0.8rem;'>EQUIPOS</div>
            </div>
            <div style='margin:15px 0;'>
                <div style='font-size:2.5rem; font-family:Orbitron,sans-serif; color:{GOLD}; font-weight:900;'>8</div>
                <div style='color:rgba(255,255,255,0.5); font-size:0.8rem;'>GRUPOS</div>
            </div>
            <div style='margin:15px 0;'>
                <div style='font-size:2.5rem; font-family:Orbitron,sans-serif; color:{PURPLE_GLOW}; font-weight:900;'>64</div>
                <div style='color:rgba(255,255,255,0.5); font-size:0.8rem;'>PARTIDOS</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "📊 Grupos y Tablas":
    tabs = st.tabs([f"GRUPO {g}" for g in GROUPS.keys()])
    for i, group_letter in enumerate(GROUPS.keys()):
        with tabs[i]:
            col_t, col_m = st.columns([3, 2])
            with col_t:
                st.markdown(f"<h3 style='color:{CYAN}; font-family:Orbitron,sans-serif; letter-spacing:2px;'>POSICIONES GRUPO {group_letter}</h3>", unsafe_allow_html=True)
                rows = compute_standings(matches, group_letter)
                html = "<table class='standings-table'><tr><th>POS</th><th>EQUIPO</th><th>PJ</th><th>PG</th><th>PE</th><th>PP</th><th>GF</th><th>GC</th><th>DG</th><th>PTS</th></tr>"
                for idx, r in enumerate(rows):
                    cls = "qualified-row" if idx < 2 else ""
                    dg = r["GF"] - r["GC"]
                    dg_display = f"+{dg}" if dg > 0 else str(dg)
                    team_name = TEAMS[r['code']]['name']
                    president = TEAMS[r['code']]['president']
                    html += f"""<tr class='{cls}'>
                        <td><b>{idx+1}</b></td>
                        <td>{flag_img(r['code'], 'sm')} {team_name} {president_badge(president)}</td>
                        <td>{r['PJ']}</td>
                        <td>{r['PG']}</td>
                        <td>{r['PE']}</td>
                        <td>{r['PP']}</td>
                        <td>{r['GF']}</td>
                        <td>{r['GC']}</td>
                        <td>{dg_display}</td>
                        <td><b style='color:{GOLD};'>{r['Pts']}</b></td>
                    </tr>"""
                html += "</table>"
                st.markdown(html, unsafe_allow_html=True)
            with col_m:
                st.markdown(f"<h3 style='color:{GOLD}; font-family:Orbitron,sans-serif; letter-spacing:2px;'>PARTIDOS</h3>", unsafe_allow_html=True)
                for m in [x for x in matches if x["stage"] == "group" and x["group"] == group_letter]:
                    status_color = CYAN if m["played"] else "rgba(255,255,255,0.4)"
                    status_text = f"{m['home_goals']} - {m['away_goals']}" if m["played"] else "VS"
                    st.markdown(f"""
                    <div class='match-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <div style='display:flex; align-items:center; gap:8px;'>
                                {flag_img(m['home'], 'sm')}
                                <span style='font-weight:600;'>{m['home']}</span>
                            </div>
                            <span class='score-display' style='font-size:1.3rem; color:{status_color};'>{status_text}</span>
                            <div style='display:flex; align-items:center; gap:8px;'>
                                <span style='font-weight:600;'>{m['away']}</span>
                                {flag_img(m['away'], 'sm')}
                            </div>
                        </div>
                        <div style='text-align:center; margin-top:8px; font-size:0.7rem; color:rgba(255,255,255,0.4);'>
                            Jornada {m['jornada']} {'✓' if m['played'] else '⏳ Pendiente'}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

elif page == "🏆 Fase Final":
    # Mostrar progreso del torneo
    groups_complete = sum(1 for g in GROUPS.keys() 
                         if all(m["played"] for m in matches if m["stage"] == "group" and m["group"] == g))
    r16_played = sum(1 for m in matches if m["stage"] == "r16" and m["played"])
    qf_played = sum(1 for m in matches if m["stage"] == "qf" and m["played"])
    sf_played = sum(1 for m in matches if m["stage"] == "sf" and m["played"])
    final_played = sum(1 for m in matches if m["stage"] == "final" and m["played"])
    third_played = sum(1 for m in matches if m["stage"] == "3rd" and m["played"])
    
    st.markdown(f"""
    <div style='text-align:center; margin-bottom:20px;'>
        <h2 style='color:{GOLD}; font-family:Orbitron,sans-serif; font-size:1.8rem; letter-spacing:3px;'>
            🏆 FASE ELIMINATORIA 🏆
        </h2>
        <p style='color:rgba(255,255,255,0.5); font-size:0.9rem;'>
            Grupos completos: {groups_complete}/8 &bull; Octavos: {r16_played}/8 &bull; Cuartos: {qf_played}/4 &bull; Semis: {sf_played}/2 &bull; Final: {final_played}/1
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Bracket visual completo
    bracket_html = generate_bracket_html(matches)
    st.markdown(bracket_html, unsafe_allow_html=True)
    
    # Detalle de cada partido como expander
    st.markdown(f"""
    <h3 style='color:{CYAN}; font-family:Orbitron,sans-serif; letter-spacing:2px; margin-top:30px;'>
        📋 DETALLE DE PARTIDOS
    </h3>
    """, unsafe_allow_html=True)
    
    for s in STAGES_KO:
        st.markdown(f"""
        <div class='stage-section'>
            <h4 class='stage-title' style='font-size:1.1rem;'>{STAGE_NAMES[s].upper()}</h4>
        </div>
        """, unsafe_allow_html=True)
        s_matches = [x for x in matches if x["stage"] == s]
        for m in s_matches:
            h = m["home_team"] if m["home_team"] else m["home"]
            a = m["away_team"] if m["away_team"] else m["away"]
            h_name = TEAMS[h]["name"] if h in TEAMS else "Por definir..."
            a_name = TEAMS[a]["name"] if a in TEAMS else "Por definir..."
            
            with st.expander(f"⚽ {h_name} vs {a_name} ({'✓ Jugado' if m['played'] else '⏳ Pendiente'})", expanded=False):
                h_resolved = h in TEAMS if h else False
                a_resolved = a in TEAMS if a else False
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; align-items:center; padding:10px; background:rgba(0,0,0,0.3); border-radius:10px; margin-bottom:10px;'>
                    <div style='text-align:center;'>
                        {flag_img(h, 'md') if h_resolved else '❓'}
                        <br><b>{h_name}</b>
                    </div>
                    <div class='score-display'>
                        {'{m[home_goals]} - {m[away_goals]}'.format(**m) if m['played'] else 'VS'}
                    </div>
                    <div style='text-align:center;'>
                        {flag_img(a, 'md') if a_resolved else '❓'}
                        <br><b>{a_name}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

elif page == "👟 Bota de Oro":
    st.markdown(f"""
    <h2 style='text-align:center; color:{GOLD}; font-family:Orbitron,sans-serif; letter-spacing:3px;'>
        🏅 MÁXIMOS GOLEADORES 🏅
    </h2>
    <p style='text-align:center; color:rgba(255,255,255,0.5); margin-bottom:25px;'>
        La carrera por la Bota de Oro FMMJ
    </p>
    """, unsafe_allow_html=True)
    top_scorers = get_top_scorers(state["scorers"])
    if top_scorers:
        html = "<table class='standings-table'><tr><th>#</th><th>JUGADOR</th><th>SELECCIÓN</th><th>GOLES</th></tr>"
        for idx, (player, stats) in enumerate(top_scorers[:20]):
            team_code = stats["team"]
            goals = stats["goals"]
            if idx == 0:
                medal = f'<span class="scorer-rank" style="color:#FFD700;">🥇</span>'
            elif idx == 1:
                medal = f'<span class="scorer-rank" style="color:#C0C0C0;">🥈</span>'
            elif idx == 2:
                medal = f'<span class="scorer-rank" style="color:#CD7F32;">🥉</span>'
            else:
                medal = f'<span class="scorer-rank" style="color:rgba(255,255,255,0.4);">{idx+1}</span>'
            html += f"<tr><td>{medal}</td><td><b>{player}</b></td><td>{flag_img(team_code, 'sm')} {TEAMS[team_code]['name']}</td><td><b style='color:{CYAN}; font-family:Orbitron,sans-serif;'>{goals}</b></td></tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("Aún no hay goles registrados. ¡El torneo apenas comienza!")

elif page == "⚙️ Admin":
    st.markdown(f"<h2 style='color:{CYAN}; font-family:Orbitron,sans-serif; letter-spacing:2px;'>⚙️ PANEL DE CONTROL</h2>", unsafe_allow_html=True)
    stage = st.selectbox("Fase", ["group"] + STAGES_KO)
    if stage == "group":
        g = st.selectbox("Grupo", list(GROUPS.keys()))
        m_list = [x for x in matches if x["stage"] == "group" and x["group"] == g]
    else:
        m_list = [x for x in matches if x["stage"] == stage]
    
    for m in m_list:
        h = m["home_team"] if m["home_team"] else m["home"]
        a = m["away_team"] if m["away_team"] else m["away"]
        
        with st.expander(f"Editar: {h} vs {a}", expanded=False):
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:20px; margin-bottom:20px; padding:15px; background:rgba(0,0,0,0.3); border-radius:12px;'>
                <div style='text-align:center;'>
                    {flag_img(h)}
                    <br><b style='font-size:1rem;'>{TEAMS[h]['name'] if h in TEAMS else h}</b>
                </div>
                <span style='font-size:1.5rem; color:{GOLD}; font-family:Orbitron,sans-serif;'>VS</span>
                <div style='text-align:center;'>
                    <b style='font-size:1rem;'>{TEAMS[a]['name'] if a in TEAMS else a}</b>
                    <br>{flag_img(a)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            hg = c1.number_input(f"Goles {TEAMS[h]['name'] if h in TEAMS else h}", 0, 20, m["home_goals"], key=f"admin_hg_{m['id']}")
            ag = c2.number_input(f"Goles {TEAMS[a]['name'] if a in TEAMS else a}", 0, 20, m["away_goals"], key=f"admin_ag_{m['id']}")
            
            # Registro de goleadores
            h_scorers = []
            if hg > 0 and h in TEAMS:
                squad = TEAM_SQUADS.get(h, [])
                if len(squad) > 0:
                    st.markdown(f"<h4 style='color:{CYAN};'>⚽ Goleadores {TEAMS[h]['name']}</h4>", unsafe_allow_html=True)
                    for i in range(int(hg)):
                        key = f"p_h_{m['id']}_{i}"
                        p = st.selectbox(f"Goleador {i+1}", squad, key=key)
                        h_scorers.append(p)
                else:
                    st.warning(f"No hay jugadores en la plantilla de {TEAMS[h]['name']} (código: {h})")
            
            a_scorers = []
            if ag > 0 and a in TEAMS:
                squad = TEAM_SQUADS.get(a, [])
                if len(squad) > 0:
                    st.markdown(f"<h4 style='color:{CYAN};'>⚽ Goleadores {TEAMS[a]['name']}</h4>", unsafe_allow_html=True)
                    for i in range(int(ag)):
                        key = f"p_a_{m['id']}_{i}"
                        p = st.selectbox(f"Goleador {i+1}", squad, key=key)
                        a_scorers.append(p)
                else:
                    st.warning(f"No hay jugadores en la plantilla de {TEAMS[a]['name']} (código: {a})")
            
            pen_h, pen_a = 0, 0
            if stage != "group" and hg == ag:
                st.markdown(f"<h4 style='color:{CYAN};'>🎯 Penales</h4>", unsafe_allow_html=True)
                cp1, cp2 = st.columns(2)
                pen_h = cp1.number_input("Penales Local", 0, 20, m.get("pen_home", 0), key=f"admin_ph_{m['id']}")
                pen_a = cp2.number_input("Penales Visita", 0, 20, m.get("pen_away", 0), key=f"admin_pa_{m['id']}")

            if st.button(f"Guardar Partido {m['id']}", key=f"btn_{m['id']}", type="primary"):
                # 1. Limpiar y Guardar Goles
                state["scorers"]["scorers"] = [g for g in state["scorers"]["scorers"] if g["match_id"] != m["id"]]
                for p in h_scorers: add_goal(state["scorers"], m["id"], h, p, 45)
                for p in a_scorers: add_goal(state["scorers"], m["id"], a, p, 45)
                
                # 2. Guardar Resultado
                m["home_goals"], m["away_goals"], m["played"] = int(hg), int(ag), True
                if stage != "group" and hg == ag:
                    m["pen_home"], m["pen_away"] = int(pen_h), int(pen_a)
                
                save_state(state)
                st.success(f"¡Partido {m['id']} actualizado!")
                st.rerun()

# ---------------------------------------------------------------
# SIDEBAR LOGO
# ---------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.image(LOGO_PATH, width=200)
st.sidebar.markdown(f"""
<div style='text-align:center; color:{GOLD}; font-family:Orbitron,sans-serif; font-size:0.75rem; letter-spacing:1px;'>
    FMMJ WORLD CUP UNITED 26
</div>
""", unsafe_allow_html=True)
