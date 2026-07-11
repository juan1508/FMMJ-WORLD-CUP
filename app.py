# -*- coding: utf-8 -*-
import streamlit as st
import json
import os

from teams_data import TEAMS, GROUPS, HOSTS
from matches_data import generate_initial_matches

st.set_page_config(page_title="FMMJ WORLD CUP UNITED 26", page_icon="🏆", layout="wide")

STATE_PATH = "tournament_state.json"  # archivo plano en la raíz del repo (se autogenera si no existe)

GREEN, BLUE, RED, GOLD = "#006341", "#0A3161", "#D80621", "#C9A24B"

STAGE_NAMES = {
    "group": "Fase de Grupos", "r16": "Octavos de Final", "qf": "Cuartos de Final",
    "sf": "Semifinal", "3rd": "Tercer Puesto", "final": "GRAN FINAL",
}

# ---------------------------------------------------------------
# CSS - identidad visual con los 3 colores anfitriones
# ---------------------------------------------------------------
st.markdown(f"""
<style>
.stApp {{ background: linear-gradient(180deg, #0d1117 0%, #10151c 100%); }}
.wc-header {{
    background: linear-gradient(90deg, {GREEN} 0%, {BLUE} 50%, {RED} 100%);
    padding: 22px 28px; border-radius: 14px; margin-bottom: 18px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.4);
}}
.wc-header h1 {{ color: white; margin: 0; font-size: 2.1rem; letter-spacing: 1px; text-shadow: 1px 1px 4px rgba(0,0,0,0.5); }}
.wc-header p {{ color: #f0f0f0; margin: 4px 0 0 0; }}
.host-strip {{ display:flex; height:6px; border-radius: 4px; overflow:hidden; margin-bottom: 16px; }}
.host-strip div {{ flex:1; }}
.team-card {{ border-radius: 12px; padding: 10px 14px; margin-bottom: 6px; background: rgba(255,255,255,0.04); border-left: 5px solid {GOLD}; }}
.pres-Mati {{ border-left-color: {GREEN} !important; }}
.pres-Jnka {{ border-left-color: {BLUE} !important; }}
.pres-Dibu {{ border-left-color: {RED} !important; }}
.group-title {{ background: linear-gradient(90deg, {GREEN}, {BLUE}, {RED}); padding: 6px 14px; border-radius: 8px; color: white; font-weight: 700; display:inline-block; margin-bottom: 8px; }}
.stage-banner {{ background: linear-gradient(90deg, {RED}, {GOLD}, {BLUE}); color:white; padding:10px 16px; border-radius:10px; font-weight:700; margin: 10px 0; }}
.flag-ico {{ width:22px; height:auto; vertical-align:middle; border-radius:2px; margin-right:6px; box-shadow:0 0 0 1px rgba(255,255,255,0.15); }}
.flag-ico-lg {{ width:34px; height:auto; vertical-align:middle; border-radius:3px; margin-right:8px; box-shadow:0 0 0 1px rgba(255,255,255,0.15); }}
</style>
<div class="host-strip"><div style="background:{GREEN}"></div><div style="background:{BLUE}"></div><div style="background:{RED}"></div></div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------
# HELPERS DE BANDERA
# Los emojis de bandera (🇲🇽 etc.) no renderizan en Streamlit Cloud (Linux
# headless sin fuente de emoji a color). Usamos siempre la imagen real
# (teams_data.flag_url) en vez del emoji.
#   - flag_html(code): tag <img> para insertar en bloques con unsafe_allow_html=True
#   - flag_md(code):   sintaxis markdown ![]() para insertar en st.write/st.success/etc,
#                       que SÍ renderiza imágenes sin necesitar unsafe_allow_html
# En selectbox / expander / dataframe (sin soporte de imágenes) no se usa
# ninguno de los dos: ahí se muestra solo el nombre del equipo, en texto plano.
# ---------------------------------------------------------------
def flag_html(code, size="sm"):
    url = TEAMS[code]["flag_url"]
    cls = "flag-ico" if size == "sm" else "flag-ico-lg"
    return f'<img src="{url}" class="{cls}">'


def flag_md(code):
    url = TEAMS[code]["flag_url"]
    return f'![{code}]({url})'


# ---------------------------------------------------------------
# ESTADO PERSISTENTE (matches + premios) en un único archivo plano
# Autogenerado si no existe -> imposible que falte el archivo.
# ---------------------------------------------------------------
def default_state():
    return {"matches": generate_initial_matches(), "awards": {"balon_oro": "", "guante_oro": "", "joven": ""}}


def load_state():
    if "tourn_state" in st.session_state:
        return st.session_state["tourn_state"]
    if os.path.exists(STATE_PATH):
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            state = default_state()
    else:
        state = default_state()
        with open(STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    st.session_state["tourn_state"] = state
    return state


def save_state(state):
    st.session_state["tourn_state"] = state
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def team_label(code):
    """Texto plano (sin bandera) — para selectbox, expander, dataframe."""
    t = TEAMS[code]
    return t["name"]


def team_label_md(code):
    """Bandera (imagen) + nombre, en sintaxis markdown — para st.write/st.success/st.markdown."""
    t = TEAMS[code]
    return f"{flag_md(code)} {t['name']}"


# ---------------------------------------------------------------
# TABLA DE POSICIONES / LÓGICA DE ELIMINATORIAS
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


def group_is_complete(matches, group_letter):
    return all(m["played"] for m in matches if m["stage"] == "group" and m["group"] == group_letter)


def get_qualifier(matches, group_letter, position):
    if not group_is_complete(matches, group_letter):
        return None
    return compute_standings(matches, group_letter)[position - 1]["code"]


def get_match(matches, stage, slot):
    for m in matches:
        if m["stage"] == stage and m.get("slot") == slot:
            return m
    return None


def winner_of(m):
    if not m["played"]:
        return None
    if m["home_goals"] > m["away_goals"]:
        return m["home_team"]
    if m["away_goals"] > m["home_goals"]:
        return m["away_team"]
    if m.get("pen_home") is not None and m.get("pen_away") is not None:
        return m["home_team"] if m["pen_home"] > m["pen_away"] else m["away_team"]
    return None


def loser_of(m):
    w = winner_of(m)
    if w is None:
        return None
    return m["away_team"] if w == m["home_team"] else m["home_team"]


def resolve_label(matches, label):
    if label.startswith("W-") or label.startswith("L-"):
        kind, stage, slot = label.split("-")
        m = get_match(matches, stage, int(slot))
        if m is None:
            return None
        return winner_of(m) if kind == "W" else loser_of(m)
    else:
        position, group_letter = int(label[0]), label[1]
        return get_qualifier(matches, group_letter, position)


def annotate_knockout_teams(matches):
    for m in matches:
        if m["stage"] == "group":
            m["home_team"] = m["home"]
            m["away_team"] = m["away"]
        else:
            m["home_team"] = resolve_label(matches, m["home"])
            m["away_team"] = resolve_label(matches, m["away"])
    return matches


def label_pretty(matches, label):
    resolved = resolve_label(matches, label)
    if resolved:
        return team_label_md(resolved)
    if len(label) == 2 and label[0].isdigit() and label[1].isalpha():
        return f"{label[0]}° Grupo {label[1]}"
    if label.startswith("W-"):
        _, stage, slot = label.split("-")
        return f"Ganador {STAGE_NAMES.get(stage, stage)} #{slot}"
    if label.startswith("L-"):
        _, stage, slot = label.split("-")
        return f"Perdedor {STAGE_NAMES.get(stage, stage)} #{slot}"
    return label


# ---------------------------------------------------------------
# BRACKET VISUAL ESTILO CHAMPIONS LEAGUE (geometría calculada en Python,
# renderizado como HTML/CSS absoluto dentro de un iframe con components.html)
# ---------------------------------------------------------------
def render_bracket(matches):
    BOX_W, BOX_H, GAP0, ROUND_GAP = 210, 58, 22, 74
    unit0 = BOX_H + GAP0
    N0 = 8
    stages = ["r16", "qf", "sf", "final"]
    stage_colors = {"r16": GREEN, "qf": BLUE, "sf": RED, "final": GOLD}

    def center(r, i):
        return unit0 * (2 ** r + i * (2 ** (r + 1)))

    def xpos(r):
        return r * (BOX_W + ROUND_GAP)

    total_h = unit0 * N0
    total_w = len(stages) * BOX_W + (len(stages) - 1) * ROUND_GAP + 30

    elements = []  # (html, order) order 0 = lines (back), 1 = boxes (front)

    # líneas conectoras
    for r in range(len(stages) - 1):
        N_r1 = N0 // (2 ** (r + 1))
        for j in range(N_r1):
            i0, i1 = 2 * j, 2 * j + 1
            y0, y1 = center(r, i0), center(r, i1)
            x_right = xpos(r) + BOX_W
            x_mid = x_right + ROUND_GAP / 2
            x_next_left = xpos(r + 1)
            y_next = center(r + 1, j)
            for (x1, x2, y) in [(x_right, x_mid, y0), (x_right, x_mid, y1), (x_mid, x_next_left, y_next)]:
                elements.append((f'<div style="position:absolute;left:{x1}px;top:{y-1}px;width:{x2-x1}px;height:2px;background:{GOLD};opacity:0.55;"></div>', 0))
            top_v, bot_v = min(y0, y1), max(y0, y1)
            elements.append((f'<div style="position:absolute;left:{x_mid-1}px;top:{top_v}px;width:2px;height:{bot_v-top_v}px;background:{GOLD};opacity:0.55;"></div>', 0))

    # cajas de partidos
    for r, stage in enumerate(stages):
        N_r = N0 // (2 ** r)
        color = stage_colors[stage]
        for i in range(N_r):
            slot = i + 1
            m = get_match(matches, stage, slot)
            home_code, away_code = (m["home_team"], m["away_team"]) if m else (None, None)
            home_txt = f"{flag_html(home_code)}{TEAMS[home_code]['name']}" if home_code else (label_pretty(matches, m["home"]) if m else "?")
            away_txt = f"{flag_html(away_code)}{TEAMS[away_code]['name']}" if away_code else (label_pretty(matches, m["away"]) if m else "?")
            played = m["played"] if m else False
            hg = m["home_goals"] if m and played else ""
            ag = m["away_goals"] if m and played else ""
            w = winner_of(m) if m else None
            home_bold = "font-weight:800;color:#fff;" if (w and w == home_code) else "opacity:0.85;"
            away_bold = "font-weight:800;color:#fff;" if (w and w == away_code) else "opacity:0.85;"
            top_y = center(r, i) - BOX_H / 2
            left_x = xpos(r)
            box_html = f'''
            <div style="position:absolute; left:{left_x}px; top:{top_y}px; width:{BOX_W}px; height:{BOX_H}px;
                        background:#161b22; border:1.5px solid {color}; border-radius:8px;
                        font-size:12px; color:#ddd; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,0.4);">
                <div style="display:flex; justify-content:space-between; align-items:center; padding:3px 8px; height:50%; border-bottom:1px solid #2a2f38; {home_bold}">
                    <span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{home_txt}</span>
                    <span>{hg}</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; padding:3px 8px; height:50%; {away_bold}">
                    <span style="white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{away_txt}</span>
                    <span>{ag}</span>
                </div>
            </div>'''
            elements.append((box_html, 1))
        # título de ronda
        elements.append((f'<div style="position:absolute; left:{xpos(r)}px; top:-26px; width:{BOX_W}px; text-align:center; color:{color}; font-weight:700; font-size:13px;">{STAGE_NAMES[stage]}</div>', 1))

    elements.sort(key=lambda e: e[1])
    inner_html = "".join(e[0] for e in elements)

    html = f"""
    <div style="width:100%; overflow-x:auto; padding-top:30px;">
      <div style="position:relative; width:{total_w}px; height:{total_h}px;">
        {inner_html}
      </div>
    </div>
    """
    st.iframe(html, height=int(total_h) + 60, width="stretch")


# ---------------------------------------------------------------
# SIDEBAR - NAVEGACIÓN
# ---------------------------------------------------------------
st.sidebar.markdown("## 🏆 FMMJ WORLD CUP")
st.sidebar.markdown("**UNITED 26**")
st.sidebar.caption("Presidentes: Mati 🟢 · Jnka 🔵 · Dibu 🔴")
page = st.sidebar.radio(
    "Navegación",
    ["🏠 Inicio", "🌍 Grupos y Tabla", "📅 Calendario / Resultados",
     "🏆 Eliminatorias", "👥 Convocatorias", "🥇 Premios"],
)

state = load_state()
matches = state["matches"]
matches = annotate_knockout_teams(matches)

# =================================================================
# INICIO
# =================================================================
if page == "🏠 Inicio":
    st.markdown(f"""
    <div class="wc-header"><h1>🏆 FMMJ WORLD CUP UNITED 26</h1>
    <p>{flag_html('MEX')}México · {flag_html('USA')}Estados Unidos · {flag_html('CAN')}Canadá — Anfitriones del torneo</p></div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    presidentes = {"Mati": GREEN, "Jnka": BLUE, "Dibu": RED}
    for col, (pres, color) in zip([col1, col2, col3], presidentes.items()):
        equipos = [t for t in TEAMS.values() if t["president"] == pres]
        with col:
            st.markdown(f'<div style="background:{color}22; border:1px solid {color}; border-radius:12px; padding:14px;">'
                        f'<h3 style="color:{color}; margin-top:0;">👑 Presidente {pres}</h3>'
                        f'<p>{len(equipos)} selecciones</p></div>', unsafe_allow_html=True)
            rows_html = "".join(
                f'<div style="padding:2px 0;">{flag_html(t["code"])}<b>{t["name"]}</b> '
                f'<span style="opacity:0.6;">(Grupo {t["group"]})</span></div>'
                for t in equipos
            )
            st.markdown(rows_html, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📋 Formato del torneo")
    st.markdown("""
    - **32 selecciones**, 8 grupos de 4 equipos (formato clásico FIFA).
    - Fase de grupos: todos contra todos (3 jornadas, 6 partidos por grupo).
    - Clasifican los **2 primeros** de cada grupo a **Octavos de Final**.
    - Octavos → Cuartos → Semifinales → Tercer puesto y **Gran Final**.
    - Cada selección lleva una convocatoria de **26 jugadores**.
    """)
    total_jugados = sum(1 for m in matches if m["played"])
    st.metric("Partidos jugados", f"{total_jugados} / {len(matches)}")

# =================================================================
# GRUPOS Y TABLA
# =================================================================
elif page == "🌍 Grupos y Tabla":
    st.markdown('<div class="wc-header"><h1>🌍 Grupos y Tabla de Posiciones</h1></div>', unsafe_allow_html=True)
    tabs = st.tabs([f"Grupo {g}" for g in GROUPS.keys()])
    for tab, group_letter in zip(tabs, GROUPS.keys()):
        with tab:
            st.markdown(f'<span class="group-title">GRUPO {group_letter}</span>', unsafe_allow_html=True)
            colA, colB = st.columns([1, 1.4])
            with colA:
                st.markdown("**Selecciones**")
                for t in GROUPS[group_letter]:
                    team = TEAMS[t["code"]]
                    st.markdown(f'<div class="team-card pres-{team["president"]}">{flag_html(team["code"])}<b>{team["name"]}</b><br>'
                                f'<span style="opacity:0.7; font-size:0.85rem;">Presidente: {team["president"]}</span></div>', unsafe_allow_html=True)
            with colB:
                st.markdown("**Tabla de posiciones**")
                standings = compute_standings(matches, group_letter)
                rows = []
                for i, r in enumerate(standings, start=1):
                    t = TEAMS[r["code"]]
                    rows.append({"#": i, "Bandera": t["flag_url"], "Selección": t["name"], "PJ": r["PJ"], "PG": r["PG"],
                                "PE": r["PE"], "PP": r["PP"], "GF": r["GF"], "GC": r["GC"],
                                "DG": r["GF"] - r["GC"], "Pts": r["Pts"]})
                st.dataframe(
                    rows, hide_index=True, width="stretch",
                    column_config={"Bandera": st.column_config.ImageColumn("", width="small")},
                )
                if group_is_complete(matches, group_letter):
                    st.markdown(f"✅ Clasifican: {team_label_md(standings[0]['code'])} y {team_label_md(standings[1]['code'])}")
                else:
                    st.info("⏳ Grupo en curso, faltan partidos por jugar.")

# =================================================================
# CALENDARIO / RESULTADOS (fase de grupos)
# =================================================================
elif page == "📅 Calendario / Resultados":
    st.markdown('<div class="wc-header"><h1>📅 Calendario y Registro de Goles</h1></div>', unsafe_allow_html=True)
    st.caption("Registra el marcador y los goleadores de cada partido de la fase de grupos.")

    group_letter = st.selectbox("Selecciona el grupo", list(GROUPS.keys()))
    group_matches = sorted([m for m in matches if m["stage"] == "group" and m["group"] == group_letter], key=lambda m: m["jornada"])

    for jornada in sorted(set(m["jornada"] for m in group_matches)):
        st.markdown(f'<div class="stage-banner">Jornada {jornada}</div>', unsafe_allow_html=True)
        for m in [mm for mm in group_matches if mm["jornada"] == jornada]:
            home_t, away_t = TEAMS[m["home"]], TEAMS[m["away"]]
            # Los emojis de bandera no renderizan dentro del texto del expander,
            # así que aquí se muestra solo el nombre (sin bandera).
            with st.expander(f"{home_t['name']}  vs  {away_t['name']}" + ("  ✅" if m["played"] else "  ⏳")):
                st.markdown(f"{flag_html(m['home'])}**{home_t['name']}**  vs  **{away_t['name']}**{flag_html(m['away'])}", unsafe_allow_html=True)
                with st.form(key=f"form_match_{m['id']}"):
                    c1, c2 = st.columns(2)
                    hg = c1.number_input(f"Goles {home_t['name']}", min_value=0, max_value=20, value=m["home_goals"] or 0, step=1, key=f"hg_{m['id']}")
                    ag = c2.number_input(f"Goles {away_t['name']}", min_value=0, max_value=20, value=m["away_goals"] or 0, step=1, key=f"ag_{m['id']}")

                    home_names = [f"{p['dorsal']}. {p['nombre']}" for p in home_t["squad"]]
                    away_names = [f"{p['dorsal']}. {p['nombre']}" for p in away_t["squad"]]
                    prev_goals = m.get("goals", [])
                    prev_home = [g["player"] for g in prev_goals if g["team"] == m["home"]]
                    prev_away = [g["player"] for g in prev_goals if g["team"] == m["away"]]

                    st.markdown(f"**Goleadores {home_t['name']}** (elige {int(hg)})")
                    home_scorers = []
                    for i in range(int(hg)):
                        default = prev_home[i] if i < len(prev_home) else home_names[0]
                        idx = home_names.index(default) if default in home_names else 0
                        home_scorers.append(st.selectbox(f"Gol {i+1} - {home_t['name']}", home_names, index=idx, key=f"hs_{m['id']}_{i}"))

                    st.markdown(f"**Goleadores {away_t['name']}** (elige {int(ag)})")
                    away_scorers = []
                    for i in range(int(ag)):
                        default = prev_away[i] if i < len(prev_away) else away_names[0]
                        idx = away_names.index(default) if default in away_names else 0
                        away_scorers.append(st.selectbox(f"Gol {i+1} - {away_t['name']}", away_names, index=idx, key=f"as_{m['id']}_{i}"))

                    if st.form_submit_button("💾 Guardar resultado"):
                        m["home_goals"], m["away_goals"], m["played"] = int(hg), int(ag), True
                        m["goals"] = [{"team": m["home"], "player": n.split(". ", 1)[1]} for n in home_scorers] + \
                                     [{"team": m["away"], "player": n.split(". ", 1)[1]} for n in away_scorers]
                        save_state(state)
                        st.success("Resultado guardado ✅")
                        st.rerun()

# =================================================================
# ELIMINATORIAS
# =================================================================
elif page == "🏆 Eliminatorias":
    st.markdown('<div class="wc-header"><h1>🏆 Fase de Eliminatorias</h1></div>', unsafe_allow_html=True)

    sub_tab1, sub_tab2 = st.tabs(["🎯 Bracket Visual", "📝 Cargar Resultados"])

    with sub_tab1:
        st.caption("Cuadro de eliminación directa estilo Champions League — se completa solo cuando terminan los grupos.")
        render_bracket(matches)
        tercer = get_match(matches, "3rd", 1)
        if tercer:
            h = tercer["home_team"]; a = tercer["away_team"]
            h_txt = team_label_md(h) if h else label_pretty(matches, tercer["home"])
            a_txt = team_label_md(a) if a else label_pretty(matches, tercer["away"])
            st.markdown("#### 🥉 Partido por el Tercer Puesto")
            if tercer["played"]:
                st.markdown(f"{h_txt} {tercer['home_goals']} - {tercer['away_goals']} {a_txt}")
            else:
                st.markdown(f"{h_txt}  vs  {a_txt}")

    with sub_tab2:
        stage_order = ["r16", "qf", "sf", "3rd", "final"]
        stage_slots = {"r16": 8, "qf": 4, "sf": 2, "3rd": 1, "final": 1}
        for stage in stage_order:
            st.markdown(f'<div class="stage-banner">{STAGE_NAMES[stage]}</div>', unsafe_allow_html=True)
            cols = st.columns(stage_slots[stage]) if stage_slots[stage] <= 4 else None
            for idx, slot in enumerate(range(1, stage_slots[stage] + 1)):
                m = get_match(matches, stage, slot)
                container = cols[idx] if cols else st.container()
                with container:
                    home_code, away_code = m["home_team"], m["away_team"]
                    home_txt = team_label_md(home_code) if home_code else label_pretty(matches, m["home"])
                    away_txt = team_label_md(away_code) if away_code else label_pretty(matches, m["away"])
                    st.markdown(f"**{home_txt}**  vs  **{away_txt}**")

                    if home_code is None or away_code is None:
                        st.caption("Pendiente de definir")
                        continue

                    if m["played"]:
                        extra = ""
                        if m["home_goals"] == m["away_goals"] and m.get("pen_home") is not None:
                            extra = f" (pen. {m['pen_home']}-{m['pen_away']})"
                        st.write(f"🔢 {m['home_goals']} - {m['away_goals']}{extra}")
                        st.markdown(f"Avanza: {team_label_md(winner_of(m))}")
                    else:
                        with st.form(key=f"ko_form_{m['id']}"):
                            c1, c2 = st.columns(2)
                            hg = c1.number_input(f"Goles {TEAMS[home_code]['name']}", min_value=0, max_value=20, step=1, key=f"kohg_{m['id']}")
                            ag = c2.number_input(f"Goles {TEAMS[away_code]['name']}", min_value=0, max_value=20, step=1, key=f"koag_{m['id']}")
                            st.caption("Si hay empate, define por penales:")
                            cp1, cp2 = st.columns(2)
                            pen_home = cp1.number_input("Penales local", min_value=0, max_value=15, step=1, key=f"ph_{m['id']}")
                            pen_away = cp2.number_input("Penales visita", min_value=0, max_value=15, step=1, key=f"pa_{m['id']}")

                            home_names = [f"{p['dorsal']}. {p['nombre']}" for p in TEAMS[home_code]["squad"]]
                            away_names = [f"{p['dorsal']}. {p['nombre']}" for p in TEAMS[away_code]["squad"]]
                            home_scorers, away_scorers = [], []
                            st.markdown(f"**Goleadores {TEAMS[home_code]['name']}**")
                            for i in range(int(hg)):
                                home_scorers.append(st.selectbox(f"Gol {i+1} local", home_names, key=f"kohs_{m['id']}_{i}"))
                            st.markdown(f"**Goleadores {TEAMS[away_code]['name']}**")
                            for i in range(int(ag)):
                                away_scorers.append(st.selectbox(f"Gol {i+1} visita", away_names, key=f"koas_{m['id']}_{i}"))

                            if st.form_submit_button("💾 Guardar resultado"):
                                if hg == ag and pen_home == pen_away:
                                    st.error("En eliminación directa no puede haber doble empate. Define un ganador por penales.")
                                else:
                                    m["home_goals"], m["away_goals"], m["played"] = int(hg), int(ag), True
                                    if hg == ag:
                                        m["pen_home"], m["pen_away"] = int(pen_home), int(pen_away)
                                    m["goals"] = [{"team": home_code, "player": n.split(". ", 1)[1]} for n in home_scorers] + \
                                                 [{"team": away_code, "player": n.split(". ", 1)[1]} for n in away_scorers]
                                    save_state(state)
                                    st.success("Resultado guardado ✅")
                                    st.rerun()

# =================================================================
# CONVOCATORIAS
# =================================================================
elif page == "👥 Convocatorias":
    st.markdown('<div class="wc-header"><h1>👥 Convocatorias (26 jugadores)</h1></div>', unsafe_allow_html=True)
    all_codes = sorted(TEAMS.keys(), key=lambda c: (TEAMS[c]["group"], TEAMS[c]["name"]))
    # Sin bandera en las opciones: un <select> HTML no puede mostrar imágenes,
    # y el emoji ahí se veía roto ("co Colombia"). Se agrega el código de país
    # entre corchetes para que sea fácil ubicar la selección igual.
    labels = [f"{TEAMS[c]['name']} [{c}] (Grupo {TEAMS[c]['group']})" for c in all_codes]
    sel = st.selectbox("Selecciona una selección", labels)
    code = all_codes[labels.index(sel)]
    team = TEAMS[code]
    pres_color = {"Mati": GREEN, "Jnka": BLUE, "Dibu": RED}[team["president"]]
    st.markdown(f'<div style="background:{pres_color}22; border-left:6px solid {pres_color}; padding:12px 16px; border-radius:8px;">'
                f'<h2 style="margin:0;">{flag_html(code, size="lg")}{team["name"]}</h2>'
                f'<p style="margin:0;">Grupo {team["group"]} · Presidente: <b>{team["president"]}</b></p></div>', unsafe_allow_html=True)

    st.markdown("### 📋 Lista de 26")
    por = [p for p in team["squad"] if p["posicion"] == "POR"]
    de = [p for p in team["squad"] if p["posicion"] == "DEF"]
    me = [p for p in team["squad"] if p["posicion"] == "MED"]
    de_l = [p for p in team["squad"] if p["posicion"] == "DEL"]
    c1, c2, c3, c4 = st.columns(4)
    for col, group, title in zip([c1, c2, c3, c4], [por, de, me, de_l], ["🧤 Arqueros", "🛡️ Defensas", "⚙️ Mediocampistas", "⚡ Delanteros"]):
        with col:
            st.markdown(f"**{title}**")
            for p in group:
                st.write(f"{p['dorsal']}. {p['nombre']}")

# =================================================================
# PREMIOS
# =================================================================
elif page == "🥇 Premios":
    st.markdown('<div class="wc-header"><h1>🥇 Premios del Torneo</h1></div>', unsafe_allow_html=True)

    scorer_count = {}
    for m in matches:
        for g in m.get("goals", []):
            key = (g["team"], g["player"])
            scorer_count[key] = scorer_count.get(key, 0) + 1

    st.subheader("⚽ Bota de Oro (Máximo Goleador)")
    if scorer_count:
        ranking = sorted(scorer_count.items(), key=lambda x: x[1], reverse=True)[:10]
        rows = [{"Bandera": TEAMS[team]["flag_url"], "Jugador": player, "Selección": TEAMS[team]["name"], "Goles": n} for (team, player), n in ranking]
        st.dataframe(
            rows, hide_index=True, width="stretch",
            column_config={"Bandera": st.column_config.ImageColumn("", width="small")},
        )
    else:
        st.info("Aún no hay goles registrados.")

    st.markdown("---")
    final_match = get_match(matches, "final", 1)
    tercer_match = get_match(matches, "3rd", 1)
    st.subheader("🏆 Campeón del Mundo")
    if final_match and final_match["played"]:
        champ, runner_up = winner_of(final_match), loser_of(final_match)
        st.markdown(f"🥇 **CAMPEÓN:** {team_label_md(champ)}")
        st.markdown(f"🥈 Subcampeón: {team_label_md(runner_up)}")
    else:
        st.info("La Gran Final aún no se ha jugado.")
    if tercer_match and tercer_match["played"]:
        st.markdown(f"🥉 Tercer lugar: {team_label_md(winner_of(tercer_match))}")

    st.markdown("---")
    st.subheader("🌟 Balón de Oro, Guante de Oro y Mejor Jugador Joven")
    st.caption("Estos premios los define la mesa de presidentes (Mati, Jnka y Dibu). Quedan guardados para todos.")

    # Sin bandera en las opciones del selectbox (no se pueden mostrar imágenes ahí).
    all_players = ["-- Sin definir --"] + [f"{p['nombre']} ({t['name']})" for t in TEAMS.values() for p in t["squad"]]
    awards = state.get("awards", {"balon_oro": "", "guante_oro": "", "joven": ""})

    def idx_of(val):
        return all_players.index(val) if val in all_players else 0

    with st.form("form_awards"):
        colA, colB, colC = st.columns(3)
        balon = colA.selectbox("🎖️ Balón de Oro (mejor jugador)", all_players, index=idx_of(awards.get("balon_oro", "")))
        guante = colB.selectbox("🧤 Guante de Oro (mejor arquero)", all_players, index=idx_of(awards.get("guante_oro", "")))
        joven = colC.selectbox("🌱 Mejor Jugador Joven", all_players, index=idx_of(awards.get("joven", "")))
        if st.form_submit_button("💾 Guardar premios"):
            state["awards"] = {"balon_oro": balon, "guante_oro": guante, "joven": joven}
            save_state(state)
            st.success("Premios guardados ✅")
            st.rerun()

    if awards.get("balon_oro") or awards.get("guante_oro") or awards.get("joven"):
        st.markdown("#### 🏅 Premios definidos")
        if awards.get("balon_oro"):
            st.write(f"🎖️ **Balón de Oro:** {awards['balon_oro']}")
        if awards.get("guante_oro"):
            st.write(f"🧤 **Guante de Oro:** {awards['guante_oro']}")
        if awards.get("joven"):
            st.write(f"🌱 **Mejor Jugador Joven:** {awards['joven']}")

st.markdown("---")
st.caption("FMMJ WORLD CUP UNITED 26 · Hecho con ❤️ por Mati, Jnka y Dibu · Streamlit App")
