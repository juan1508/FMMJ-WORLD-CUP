# -*- coding: utf-8 -*-
import streamlit as st
import json
import os
import base64

from teams_data import TEAMS, GROUPS, HOSTS
from matches_data import generate_initial_matches
from scorers_data import TEAM_SQUADS, initialize_scorers_state, add_goal, get_top_scorers

# ---------------------------------------------------------------
# CONFIGURACIÓN DEL LOGO LOCAL (dinámico, se recarga en cada rerun)
# ---------------------------------------------------------------
import time as _time

def _get_logo_base64(logo_path="logo.png"):
    """Lee el archivo logo.png en cada ejecución para que se actualice sin reboot."""
    if os.path.exists(logo_path):
        with open(logo_path, 'rb') as f:
            data = f.read()
        timestamp = int(_time.time())  # cache-buster
        img_format = os.path.splitext(logo_path)[-1].replace('.', '')
        return f"data:image/{img_format};base64,{base64.b64encode(data).decode()}?t={timestamp}"
    return ""

LOGO_PATH = "logo.png"
LOGO_BASE64 = _get_logo_base64(LOGO_PATH)

st.set_page_config(page_title="FMMJ WORLD CUP UNITED 26", page_icon=LOGO_PATH, layout="wide")

STATE_PATH = "tournament_state.json"
GOLD = "#C9A24B"
DARK_BLUE = "#0A192F"
ACCENT_BLUE = "#172A45"
WHITE = "#FFFFFF"
PRESIDENTS_COLORS = {"Mati": "#006341", "Jnka": "#0A3161", "Dibu": "#D80621"}

STAGE_NAMES = {
    "group": "Fase de Grupos", "r16": "Octavos de Final", "qf": "Cuartos de Final",
    "sf": "Semifinal", "3rd": "Tercer Puesto", "final": "GRAN FINAL",
}

# ---------------------------------------------------------------
# CSS
# ---------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@500;700&display=swap');

.stApp {{
    background: linear-gradient(135deg, #020c1b 0%, #0a192f 50%, #020c1b 100%);
    color: {WHITE};
    font-family: 'Rajdhani', sans-serif;
}}

.main-header {{
    background: rgba(10, 25, 47, 0.85);
    border-bottom: 2px solid {GOLD};
    padding: 20px;
    text-align: center;
    backdrop-filter: blur(10px);
    margin-bottom: 30px;
    border-radius: 0 0 20px 20px;
}}

.logo-img {{ width: 180px; filter: drop-shadow(0 0 10px {GOLD}); }}
.tournament-title {{ font-family: 'Orbitron', sans-serif; color: {GOLD}; font-size: 2.5rem; letter-spacing: 4px; }}

.match-card {{
    background: rgba(10, 25, 47, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}}

.score-display {{ font-family: 'Orbitron', sans-serif; font-size: 1.5rem; color: {GOLD}; }}

.standings-table {{ width: 100%; border-collapse: separate; border-spacing: 0 5px; }}
.standings-table th {{ background: {ACCENT_BLUE}; color: {GOLD}; padding: 12px; }}
.standings-table td {{ background: rgba(255, 255, 255, 0.05); padding: 12px; }}
.qualified-row {{ border-left: 4px solid {GOLD}; background: rgba(201, 162, 75, 0.1) !important; }}

.president-badge {{
    padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;
    text-transform: uppercase; margin-left: 8px;
}}
</style>

<div class="main-header">
    <img src="{LOGO_BASE64}" class="logo-img">
    <div class="tournament-title">FMMJ WORLD CUP</div>
    <p style="color: {GOLD}; letter-spacing: 2px; opacity: 0.8;">UNITED 2026 • EL LEGADO DE LOS PRIMOS</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------
def flag_img(code, size="md"):
    """Retorna HTML con bandera circular (solo círculo, sin fondo cuadrado)."""
    if code not in TEAMS:
        return "❓"
    url = TEAMS[code]["flag_url"]
    if size == "md":
        w = "48"
    else:
        w = "32"
    return f'<img src="{url}" style="width:{w}px; height:{w}px; border-radius:50%; object-fit:cover; vertical-align:middle; margin-right:8px;">'

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

# ---------------------------------------------------------------
# APP PRINCIPAL
# ---------------------------------------------------------------
state = load_state()
matches = annotate_knockout(state["matches"])
STAGES_KO = ["r16", "qf", "sf", "final"]

page = st.sidebar.radio("NAVEGACIÓN", ["🏠 Inicio", "📊 Grupos y Tablas", "🏆 Fase Final", "👟 Bota de Oro", "⚙️ Admin"])

if page == "🏠 Inicio":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"""
        <div class='group-container' style='background:rgba(23,42,69,0.6); padding:20px; border-radius:15px; border:1px solid {GOLD};'>
            <h2 style='color:{GOLD}'>BIENVENIDOS A LA FMMJ WORLD CUP</h2>
            <p>La competición más prestigiosa de la familia. 32 selecciones, un solo objetivo: la gloria eterna.</p>
            <hr style='border-color:{GOLD}'>
            <h4>Presidentes Oficiales:</h4>
            <div style='display:flex; gap:20px;'>
                <div>{president_badge('Mati')} Mati</div>
                <div>{president_badge('Jnka')} Jnka</div>
                <div>{president_badge('Dibu')} Dibu</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "📊 Grupos y Tablas":
    tabs = st.tabs([f"GRUPO {g}" for g in GROUPS.keys()])
    for i, group_letter in enumerate(GROUPS.keys()):
        with tabs[i]:
            col_t, col_m = st.columns([3, 2])
            with col_t:
                st.markdown(f"<h3 style='color:{GOLD}'>POSICIONES GRUPO {group_letter}</h3>", unsafe_allow_html=True)
                rows = compute_standings(matches, group_letter)
                html = "<table class='standings-table'><tr><th>POS</th><th>EQUIPO</th><th>PJ</th><th>PTS</th><th>DG</th></tr>"
                for idx, r in enumerate(rows):
                    cls = "qualified-row" if idx < 2 else ""
                    dg = r["GF"] - r["GC"]
                    team_name = TEAMS[r['code']]['name']
                    president = TEAMS[r['code']]['president']
                    html += f"<tr class='{cls}'><td>{idx+1}</td><td>{flag_img(r['code'], 'sm')} {team_name} {president_badge(president)}</td><td>{r['PJ']}</td><td><b>{r['Pts']}</b></td><td>{dg}</td></tr>"
                html += "</table>"
                st.markdown(html, unsafe_allow_html=True)
            with col_m:
                st.markdown(f"<h3 style='color:{GOLD}'>PARTIDOS</h3>", unsafe_allow_html=True)
                for m in [x for x in matches if x["stage"] == "group" and x["group"] == group_letter]:
                    st.markdown(f"""
                    <div class='match-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span>{flag_img(m['home'], 'sm')} {m['home']}</span>
                            <span class='score-display'>{m['home_goals'] if m['played'] else '-'} : {m['away_goals'] if m['played'] else '-'}</span>
                            <span>{m['away']} {flag_img(m['away'], 'sm')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

elif page == "🏆 Fase Final":
    for s in STAGES_KO:
        st.markdown(f"<h3 style='border-bottom:1px solid {GOLD}; padding:10px;'>{STAGE_NAMES[s]}</h3>", unsafe_allow_html=True)
        s_matches = [x for x in matches if x["stage"] == s]
        cols = st.columns(len(s_matches)) if s_matches else [st.container()]
        for idx, m in enumerate(s_matches):
            with cols[idx]:
                h = m["home_team"] if m["home_team"] else m["home"]
                a = m["away_team"] if m["away_team"] else m["away"]
                h_name = TEAMS[h]["name"] if h in TEAMS else h
                a_name = TEAMS[a]["name"] if a in TEAMS else a
                st.markdown(f"""
                <div class='match-card'>
                    <div style='text-align:center; font-size:0.8rem; opacity:0.7;'>Partido {m['slot']}</div>
                    <div style='display:flex; justify-content:space-between; margin:10px 0;'>
                        <span>{flag_img(h, 'sm') if h in TEAMS else '❓'} {h_name}</span>
                        <b style='color:{GOLD}'>{m['home_goals'] if m['played'] else '-'}</b>
                    </div>
                    <div style='display:flex; justify-content:space-between;'>
                        <span>{flag_img(a, 'sm') if a in TEAMS else '❓'} {a_name}</span>
                        <b style='color:{GOLD}'>{m['away_goals'] if m['played'] else '-'}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)

elif page == "👟 Bota de Oro":
    st.markdown(f"<h2 style='text-align:center; color:{GOLD}'>🏅 MÁXIMOS GOLEADORES 🏅</h2>", unsafe_allow_html=True)
    top_scorers = get_top_scorers(state["scorers"])
    if top_scorers:
        html = "<table class='standings-table'><tr><th>POS</th><th>JUGADOR</th><th>SELECCIÓN</th><th>GOLES</th></tr>"
        for idx, (player, stats) in enumerate(top_scorers[:15]):
            team_code = stats["team"]
            goals = stats["goals"]
            medal = ["🥇", "🥈", "🥉"][idx] if idx < 3 else f"{idx+1}"
            html += f"<tr><td>{medal}</td><td><b>{player}</b></td><td>{flag_img(team_code, 'sm')} {TEAMS[team_code]['name']}</td><td><b>{goals}</b></td></tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
    else:
        st.info("Aún no hay goles registrados.")

elif page == "⚙️ Admin":
    st.header("PANEL DE CONTROL")
    stage = st.selectbox("Fase", ["group"] + STAGES_KO)
    if stage == "group":
        g = st.selectbox("Grupo", list(GROUPS.keys()))
        m_list = [x for x in matches if x["stage"] == "group" and x["group"] == g]
    else:
        m_list = [x for x in matches if x["stage"] == stage]
    
    for m in m_list:
        # Resolver equipo local y visitante
        h = m["home_team"] if m["home_team"] else m["home"]
        a = m["away_team"] if m["away_team"] else m["away"]
        
        with st.expander(f"Editar: {h} vs {a}", expanded=False):
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:20px; margin-bottom:15px;'>
                {flag_img(h)} <b style='font-size:1.2rem;'>{TEAMS[h]['name'] if h in TEAMS else h}</b>
                <span style='font-size:1.5rem;'>VS</span>
                <b style='font-size:1.2rem;'>{TEAMS[a]['name'] if a in TEAMS else a}</b> {flag_img(a)}
            </div>
            """, unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            hg = c1.number_input(f"Goles Local", 0, 20, m["home_goals"], key=f"admin_hg_{m['id']}")
            ag = c2.number_input(f"Goles Visita", 0, 20, m["away_goals"], key=f"admin_ag_{m['id']}")
            
            # Registro de goleadores
            h_scorers = []
            if hg > 0 and h in TEAMS:
                squad = TEAM_SQUADS.get(h, [])
                if len(squad) > 0:
                    st.markdown(f"**Goleadores {TEAMS[h]['name']}**")
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
                    st.markdown(f"**Goleadores {TEAMS[a]['name']}**")
                    for i in range(int(ag)):
                        key = f"p_a_{m['id']}_{i}"
                        p = st.selectbox(f"Goleador {i+1}", squad, key=key)
                        a_scorers.append(p)
                else:
                    st.warning(f"No hay jugadores en la plantilla de {TEAMS[a]['name']} (código: {a})")
            
            pen_h, pen_a = 0, 0
            if stage != "group" and hg == ag:
                st.markdown("**Penales:**")
                cp1, cp2 = st.columns(2)
                pen_h = cp1.number_input("Penales Local", 0, 20, m.get("pen_home", 0), key=f"admin_ph_{m['id']}")
                pen_a = cp2.number_input("Penales Visita", 0, 20, m.get("pen_away", 0), key=f"admin_pa_{m['id']}")

            if st.button(f"Guardar Partido {m['id']}", key=f"btn_{m['id']}"):
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

st.sidebar.markdown("---")
st.sidebar.image(LOGO_BASE64, use_column_width=True)
st.sidebar.caption("FMMJ WORLD CUP UNITED 26")
