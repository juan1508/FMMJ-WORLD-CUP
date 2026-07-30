# -*- coding: utf-8 -*-
import streamlit as st
import json
import os
import base64
import time as _time

from teams_data import TEAMS, GROUPS, HOSTS
from matches_data import generate_initial_matches
from scorers_data import TEAM_SQUADS, initialize_scorers_state, add_goal, get_top_scorers

# ---------------------------------------------------------------
# LOGO DINÁMICO (se recarga en cada rerun, sin reboot)
# ---------------------------------------------------------------
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
    padding: 25px 20px;
    text-align: center;
    backdrop-filter: blur(20px);
    margin-bottom: 25px;
    border-radius: 0 0 25px 25px;
    position: relative;
    overflow: hidden;
}}
.main-header::before {{
    content: '';
    position: absolute;
    top: 0; left: -50%;
    width: 200%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0,229,255,0.05), transparent);
    animation: shimmer 4s infinite;
}}
@keyframes shimmer {{
    0% {{ transform: translateX(-50%); }}
    100% {{ transform: translateX(50%); }}
}}

.logo-img {{ 
    width: 160px; 
    filter: drop-shadow(0 0 15px {CYAN}) drop-shadow(0 0 30px rgba(123,47,190,0.3));
    animation: float 3s ease-in-out infinite;
}}
@keyframes float {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-5px); }}
}}

.tournament-title {{ 
    font-family: 'Orbitron', sans-serif; 
    font-weight: 900;
    color: transparent;
    background: linear-gradient(135deg, {CYAN} 0%, {GOLD} 50%, {CYAN} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2.8rem; 
    letter-spacing: 6px;
    margin: 10px 0 5px 0;
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
.match-card:hover {{
    border-color: rgba(0,229,255,0.4);
    box-shadow: 0 5px 25px rgba(0,229,255,0.1);
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
.welcome-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: radial-gradient(ellipse at top right, rgba(123,47,190,0.1), transparent 70%);
    pointer-events: none;
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
</style>

<div class="main-header">
    <img src="{LOGO_BASE64}" class="logo-img">
    <div class="tournament-title">FMMJ WORLD CUP</div>
    <p class="subtitle">UNITED 2026 &bull; EL LEGADO DE LOS PRIMOS</p>
</div>
""", unsafe_allow_html=True)

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
                        <td><b>{dg_display}</b></td>
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
    for s in STAGES_KO:
        st.markdown(f"""
        <div class='stage-section'>
            <h3 class='stage-title'>{STAGE_NAMES[s].upper()}</h3>
        </div>
        """, unsafe_allow_html=True)
        s_matches = [x for x in matches if x["stage"] == s]
        cols = st.columns(len(s_matches)) if s_matches else [st.container()]
        for idx, m in enumerate(s_matches):
            with cols[idx]:
                h = m["home_team"] if m["home_team"] else m["home"]
                a = m["away_team"] if m["away_team"] else m["away"]
                h_name = TEAMS[h]["name"] if h in TEAMS else h
                a_name = TEAMS[a]["name"] if a in TEAMS else a
                h_flag = flag_img(h, 'sm') if h in TEAMS else '❓'
                a_flag = flag_img(a, 'sm') if a in TEAMS else '❓'
                played = "✓" if m["played"] else "⏳"
                pen_str = ""
                if m.get("pen_home") is not None:
                    pen_str = f"<div style='font-size:0.7rem; color:{CYAN};'>Penales: {m['pen_home']} - {m['pen_away']}</div>"
                st.markdown(f"""
                <div class='match-card'>
                    <div style='text-align:center; font-size:0.75rem; opacity:0.5; margin-bottom:8px;'>Partido {m['slot']} {played}</div>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin:8px 0;'>
                        <div>{h_flag}<span style='font-weight:600;'>{h_name}</span></div>
                        <b style='color:{GOLD}; font-family:Orbitron,sans-serif; font-size:1.2rem;'>{m['home_goals'] if m['played'] else '-'}</b>
                    </div>
                    <hr style='border-color:rgba(255,255,255,0.05);'>
                    <div style='display:flex; justify-content:space-between; align-items:center; margin:8px 0;'>
                        <div>{a_flag}<span style='font-weight:600;'>{a_name}</span></div>
                        <b style='color:{GOLD}; font-family:Orbitron,sans-serif; font-size:1.2rem;'>{m['away_goals'] if m['played'] else '-'}</b>
                    </div>
                    {pen_str}
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
if LOGO_BASE64:
    st.sidebar.image(LOGO_BASE64, width=250)
    st.sidebar.markdown(f"""
    <div style='text-align:center; color:{GOLD}; font-family:Orbitron,sans-serif; font-size:0.75rem; letter-spacing:1px;'>
        FMMJ WORLD CUP UNITED 26
    </div>
    """, unsafe_allow_html=True)
