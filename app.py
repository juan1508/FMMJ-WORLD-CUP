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
# CSS - identidad visual con los 3 colores anfitriones + efectos
# ---------------------------------------------------------------
st.markdown(f"""
<style>
@keyframes shimmer {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(12px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}
@keyframes pulseGlow {{
    0% {{ box-shadow: 0 0 0 0 rgba(201,162,75,0.45); }}
    70% {{ box-shadow: 0 0 0 8px rgba(201,162,75,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(201,162,75,0); }}
}}
@keyframes floatFlag {{
    0%, 100% {{ transform: translateY(0px); }}
    50% {{ transform: translateY(-3px); }}
}}

.stApp {{ background: radial-gradient(circle at 20% 0%, #131a24 0%, #0d1117 45%, #0a0d12 100%); }}

.wc-header {{
    background: linear-gradient(120deg, {GREEN} 0%, {BLUE} 45%, {RED} 90%);
    background-size: 200% 200%;
    animation: shimmer 9s ease-in-out infinite;
    padding: 26px 30px; border-radius: 16px; margin-bottom: 18px;
    box-shadow: 0 8px 26px rgba(0,0,0,0.45);
    border: 1px solid rgba(255,255,255,0.08);
    animation: shimmer 9s ease-in-out infinite, fadeInUp 0.6s ease;
}}
.wc-header h1 {{ color: white; margin: 0; font-size: 2.3rem; letter-spacing: 1px; text-shadow: 1px 1px 6px rgba(0,0,0,0.55); }}
.wc-header p {{ color: #f2f2f2; margin: 6px 0 0 0; font-size: 1.02rem; }}

.host-strip {{ display:flex; height:6px; border-radius: 4px; overflow:hidden; margin-bottom: 16px;
               box-shadow: 0 0 12px rgba(201,162,75,0.35); }}
.host-strip div {{ flex:1; }}

.team-card {{
    border-radius: 12px; padding: 12px 16px; margin-bottom: 8px;
    background: rgba(255,255,255,0.045); border-left: 5px solid {GOLD};
    transition: transform 0.18s ease, background 0.18s ease, box-shadow 0.18s ease;
    animation: fadeInUp 0.45s ease;
}}
.team-card:hover {{ transform: translateX(4px) scale(1.015); background: rgba(255,255,255,0.09);
                     box-shadow: 0 4px 14px rgba(0,0,0,0.35); }}
.pres-Mati {{ border-left-color: {GREEN} !important; }}
.pres-Jnka {{ border-left-color: {BLUE} !important; }}
.pres-Dibu {{ border-left-color: {RED} !important; }}

.group-title {{
    background: linear-gradient(90deg, {GREEN}, {BLUE}, {RED});
    background-size: 200% 100%; animation: shimmer 6s ease-in-out infinite;
    padding: 7px 16px; border-radius: 8px; color: white; font-weight: 700;
    display:inline-block; margin-bottom: 10px; letter-spacing: 0.5px;
}}
.stage-banner {{
    background: linear-gradient(90deg, {RED}, {GOLD}, {BLUE});
    background-size: 200% 100%; animation: shimmer 7s ease-in-out infinite;
    color:white; padding:11px 18px; border-radius:10px; font-weight:700;
    margin: 12px 0; text-align:center; letter-spacing: 0.5px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.3);
}}
.flag-ico {{ width:22px; height:auto; vertical-align:middle; border-radius:2px; margin-right:6px;
             box-shadow:0 0 0 1px rgba(255,255,255,0.15); animation: floatFlag 3.2s ease-in-out infinite; }}
.flag-ico-lg {{ width:38px; height:auto; vertical-align:middle; border-radius:4px; margin-right:9px;
                box-shadow:0 0 0 1px rgba(255,255,255,0.18); animation: floatFlag 3.2s ease-in-out infinite; }}

.stat-pill {{
    display:inline-block; background: rgba(201,162,75,0.13); border: 1px solid {GOLD};
    color: {GOLD}; padding: 4px 12px; border-radius: 999px; font-size: 0.82rem;
    font-weight: 600; margin-right: 6px;
}}
.pending-pulse {{ animation: pulseGlow 2.4s infinite; border-radius: 10px; }}

.champion-banner {{
    background: linear-gradient(135deg, {GOLD} 0%, #f4e2ab 40%, {GOLD} 100%);
    background-size: 200% 200%; animation: shimmer 5s ease-in-out infinite, fadeInUp 0.6s ease;
    color: #1a1200; padding: 22px 26px; border-radius: 16px; text-align:center;
    box-shadow: 0 10px 30px rgba(201,162,75,0.35); margin: 14px 0;
}}
.champion-banner h2 {{ margin:0; font-size: 1.9rem; }}

.medal-1 {{ color:#FFD700; }} .medal-2 {{ color:#C7CBD1; }} .medal-3 {{ color:#CD7F32; }}

.progress-wrap {{ background: rgba(255,255,255,0.06); border-radius: 999px; height: 12px; overflow:hidden;
                   margin: 6px 0 14px 0; border: 1px solid rgba(255,255,255,0.08); }}
.progress-bar {{ height: 100%; background: linear-gradient(90deg, {GREEN}, {BLUE}, {RED});
                  background-size: 200% 100%; animation: shimmer 4s ease-in-out infinite;
                  border-radius: 999px; transition: width 0.5s ease; }}

.section-fade {{ animation: fadeInUp 0.5s ease; }}

.flag-circle {{
    display: inline-block; width: 34px; height: 34px; border-radius: 50%;
    background-size: cover !important; background-position: center !important; background-repeat: no-repeat !important;
    border: 2px solid rgba(255,255,255,0.18); box-shadow: 0 0 0 2px rgba(0,0,0,0.35), 0 2px 6px rgba(0,0,0,0.35);
    vertical-align: middle; transition: transform 0.15s ease; flex-shrink: 0;
}}
.flag-circle-sm {{
    display: inline-block; width: 24px; height: 24px; border-radius: 50%;
    background-size: cover !important; background-position: center !important; background-repeat: no-repeat !important;
    border: 1.5px solid rgba(255,255,255,0.18); box-shadow: 0 0 0 1.5px rgba(0,0,0,0.35);
    vertical-align: middle; flex-shrink: 0;
}}
.standings-table {{ width: 100%; border-collapse: collapse; animation: fadeInUp 0.5s ease; }}
.standings-table th {{
    text-align: left; padding: 9px 10px; color: #9aa4b2; font-size: 0.74rem;
    text-transform: uppercase; letter-spacing: 0.6px; border-bottom: 1px solid rgba(255,255,255,0.12);
}}
.standings-table td {{ padding: 8px 10px; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.92rem; }}
.standings-table tr.qualified {{ background: linear-gradient(90deg, rgba(0,99,65,0.16), rgba(0,99,65,0.02)); }}
.standings-table tr.qualified td:first-child {{ border-left: 3px solid {GREEN}; }}
.standings-table tr:not(.qualified) td:first-child {{ border-left: 3px solid transparent; }}
.standings-table tr:hover td {{ background: rgba(255,255,255,0.045); }}
.standings-table td.team-cell {{ display:flex; align-items:center; gap:10px; }}
.pos-badge {{
    display:inline-flex; align-items:center; justify-content:center; width:22px; height:22px;
    border-radius:50%; font-size:0.75rem; font-weight:700; background: rgba(255,255,255,0.08); color:#cdd3da;
}}
.pos-badge.gold {{ background: #FFD70033; color:#FFD700; border:1px solid #FFD70066; }}
.pos-badge.silver {{ background: #C7CBD133; color:#C7CBD1; border:1px solid #C7CBD166; }}
</style>
<div class="host-strip"><div style="background:{GREEN}"></div><div style="background:{BLUE}"></div><div style="background:{RED}"></div></div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------
# HELPERS DE BANDERA
# ---------------------------------------------------------------
def flag_html(code, size="sm"):
    url = TEAMS[code]["flag_url"]
    cls = "flag-ico" if size == "sm" else "flag-ico-lg"
    return f'<img src="{url}" class="{cls}">'


def flag_md(code):
    url = TEAMS[code]["flag_url"]
    return f'![{code}]({url})'


def flag_circle(code, size="md"):
    url = TEAMS[code]["flag_url"]
    cls = "flag-circle" if size == "md" else "flag-circle-sm"
    return f'<span class="{cls}" style="background-image:url(\'{url}\');"></span>'


# ---------------------------------------------------------------
# ESTADO PERSISTENTE (solo resultados de partidos) en un único archivo plano
# ---------------------------------------------------------------
def default_state():
    return {"matches": generate_initial_matches()}


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
    state.setdefault("matches", generate_initial_matches())
    st.session_state["tourn_state"] = state
    return state


def save_state(state):
    st.session_state["tourn_state"] = state
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def team_label(code):
    """Texto plano (sin bandera) — para selectbox, expander, dataframe."""
    return TEAMS[code]["name"]


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

    def head_to_head_points(tied_codes):
        """Mini-tabla (puntos, GF, GC) SOLO con los partidos jugados entre los
        equipos empatados en puntos — se usa como primer criterio de desempate."""
        mini = {c: {"Pts": 0, "GF": 0, "GC": 0} for c in tied_codes}
        for m in matches:
            if m["stage"] != "group" or m["group"] != group_letter or not m["played"]:
                continue
            h, a, hg, ag = m["home"], m["away"], m["home_goals"], m["away_goals"]
            if h in tied_codes and a in tied_codes:
                mini[h]["GF"] += hg; mini[h]["GC"] += ag
                mini[a]["GF"] += ag; mini[a]["GC"] += hg
                if hg > ag:
                    mini[h]["Pts"] += 3
                elif ag > hg:
                    mini[a]["Pts"] += 3
                else:
                    mini[h]["Pts"] += 1; mini[a]["Pts"] += 1
        return mini

    # Orden de desempate (dentro de cada bloque de puntos iguales):
    #   1) puntos en el duelo directo entre los empatados
    #   2) diferencia de gol general
    #   3) menos goles en contra (general)
    #   4) más goles a favor (general)
    rows = sorted(table.values(), key=lambda r: r["Pts"], reverse=True)
    result, i = [], 0
    while i < len(rows):
        j = i
        while j < len(rows) and rows[j]["Pts"] == rows[i]["Pts"]:
            j += 1
        block = rows[i:j]
        if len(block) > 1:
            mini = head_to_head_points({r["code"] for r in block})
            block = sorted(
                block,
                key=lambda r: (mini[r["code"]]["Pts"], r["GF"] - r["GC"], -r["GC"], r["GF"]),
                reverse=True,
            )
        result.extend(block)
        i = j
    return result


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


def render_standings_table(matches, group_letter):
    # OJO: st.markdown interpreta cualquier línea que empiece con 4+ espacios
    # como bloque de código, así que todo el HTML se arma SIN indentación ni
    # saltos de línea con sangría (todo en una sola línea por fila).
    standings = compute_standings(matches, group_letter)
    header = ('<table class="standings-table"><thead><tr>'
               '<th>#</th><th>Selección</th><th>PJ</th><th>PG</th><th>PE</th><th>PP</th>'
               '<th>GF</th><th>GC</th><th>DG</th><th>Pts</th>'
               '</tr></thead><tbody>')
    rows_html = []
    for i, r in enumerate(standings):
        t = TEAMS[r["code"]]
        qualified = i < 2
        badge_cls = "gold" if i == 0 else ("silver" if i == 1 else "")
        badge = f'<span class="pos-badge {badge_cls}">{i+1}</span>'
        row_cls = "qualified" if qualified else ""
        rows_html.append(
            f'<tr class="{row_cls}">'
            f'<td>{badge}</td>'
            f'<td class="team-cell">{flag_circle(r["code"])}<b>{t["name"]}</b></td>'
            f'<td>{r["PJ"]}</td><td>{r["PG"]}</td><td>{r["PE"]}</td><td>{r["PP"]}</td>'
            f'<td>{r["GF"]}</td><td>{r["GC"]}</td><td>{r["GF"] - r["GC"]}</td>'
            f'<td><b>{r["Pts"]}</b></td>'
            f'</tr>'
        )
    full_html = header + "".join(rows_html) + "</tbody></table>"
    st.markdown(full_html, unsafe_allow_html=True)


# ---------------------------------------------------------------
# BRACKET VISUAL ESTILO CHAMPIONS LEAGUE (geometría calculada en Python,
# renderizado como HTML/CSS absoluto dentro de un iframe con components.html)
# ---------------------------------------------------------------
def render_bracket(matches):
    BOX_W, BOX_H, GAP0, ROUND_GAP = 210, 60, 22, 74
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
            box_glow = f"box-shadow:0 0 12px {color}66, 0 2px 6px rgba(0,0,0,0.4);" if played else "box-shadow:0 2px 6px rgba(0,0,0,0.4);"
            top_y = center(r, i) - BOX_H / 2
            left_x = xpos(r)
            box_html = f'''
            <div style="position:absolute; left:{left_x}px; top:{top_y}px; width:{BOX_W}px; height:{BOX_H}px;
                        background:#161b22; border:1.5px solid {color}; border-radius:8px;
                        font-size:12px; color:#ddd; overflow:hidden; {box_glow} transition: transform 0.15s;">
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
    st.components.v1.html(html, height=int(total_h) + 60, scrolling=True)


# ---------------------------------------------------------------
# SIDEBAR - NAVEGACIÓN
# ---------------------------------------------------------------
st.sidebar.markdown("## 🏆 FMMJ WORLD CUP")
st.sidebar.markdown("**UNITED 26**")
st.sidebar.caption("Presidentes: Mati 🟢 · Jnka 🔵 · Dibu 🔴")
page = st.sidebar.radio(
    "Navegación",
    ["🏠 Inicio", "🌍 Grupos y Tabla", "📅 Calendario / Resultados", "🏆 Eliminatorias"],
)

state = load_state()
matches = state["matches"]
matches = annotate_knockout_teams(matches)

total_matches = len(matches)
total_jugados = sum(1 for m in matches if m["played"])
progress_pct = int(100 * total_jugados / total_matches) if total_matches else 0

st.sidebar.markdown("#### Progreso del torneo")
st.sidebar.markdown(f'<div class="progress-wrap"><div class="progress-bar" style="width:{progress_pct}%;"></div></div>', unsafe_allow_html=True)
st.sidebar.caption(f"{total_jugados} / {total_matches} partidos jugados ({progress_pct}%)")

# =================================================================
# INICIO
# =================================================================
if page == "🏠 Inicio":
    st.markdown(
        f'<div class="wc-header"><h1>🏆 FMMJ WORLD CUP UNITED 26</h1>'
        f'<p>{flag_html("MEX")}México · {flag_html("USA")}Estados Unidos · {flag_html("CAN")}Canadá — Anfitriones del torneo</p></div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("⚽ Partidos jugados", f"{total_jugados} / {total_matches}")
    grupos_completos = sum(1 for g in GROUPS if group_is_complete(matches, g))
    m2.metric("🌍 Grupos completos", f"{grupos_completos} / 8")
    final_match = get_match(matches, "final", 1)
    m3.metric("🏆 Estado de la Final", "Jugada ✅" if final_match["played"] else "Pendiente ⏳")

    if final_match["played"]:
        champ = winner_of(final_match)
        st.markdown(f'<div class="champion-banner"><h2>🏆 CAMPEÓN DEL MUNDO 🏆</h2>'
                    f'<div style="margin-top:8px; font-size:1.4rem;">{flag_html(champ, size="lg")}<b>{TEAMS[champ]["name"]}</b></div></div>',
                    unsafe_allow_html=True)

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    presidentes = {"Mati": GREEN, "Jnka": BLUE, "Dibu": RED}
    for col, (pres, color) in zip([col1, col2, col3], presidentes.items()):
        equipos = [t for t in TEAMS.values() if t["president"] == pres]
        with col:
            st.markdown(f'<div class="section-fade" style="background:{color}22; border:1px solid {color}; border-radius:12px; padding:14px;">'
                        f'<h3 style="color:{color}; margin-top:0;">👑 Presidente {pres}</h3>'
                        f'<span class="stat-pill">{len(equipos)} selecciones</span></div>', unsafe_allow_html=True)
            rows_html = "".join(
                f'<div class="team-card pres-{pres}" style="padding:6px 12px;">{flag_html(t["code"])}<b>{t["name"]}</b> '
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
    """)

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
                render_standings_table(matches, group_letter)
                st.caption("Desempate: 1) duelo directo · 2) diferencia de gol · 3) menos goles en contra · 4) más goles a favor.")
                standings = compute_standings(matches, group_letter)
                if group_is_complete(matches, group_letter):
                    st.markdown(f"✅ Clasifican: {team_label_md(standings[0]['code'])} y {team_label_md(standings[1]['code'])}")
                else:
                    st.markdown('<div class="pending-pulse">', unsafe_allow_html=True)
                    st.info("⏳ Grupo en curso, faltan partidos por jugar.")
                    st.markdown('</div>', unsafe_allow_html=True)

# =================================================================
# CALENDARIO / RESULTADOS (fase de grupos)
# =================================================================
elif page == "📅 Calendario / Resultados":
    st.markdown('<div class="wc-header"><h1>📅 Calendario y Resultados</h1></div>', unsafe_allow_html=True)
    st.caption("Registra el marcador de cada partido de la fase de grupos.")

    group_letter = st.selectbox("Selecciona el grupo", list(GROUPS.keys()))
    group_matches = sorted([m for m in matches if m["stage"] == "group" and m["group"] == group_letter], key=lambda m: m["jornada"])

    for jornada in sorted(set(m["jornada"] for m in group_matches)):
        st.markdown(f'<div class="stage-banner">Jornada {jornada}</div>', unsafe_allow_html=True)
        for m in [mm for mm in group_matches if mm["jornada"] == jornada]:
            home_t, away_t = TEAMS[m["home"]], TEAMS[m["away"]]
            marcador = f"  ({m['home_goals']} - {m['away_goals']})  ✅" if m["played"] else "  ⏳"
            with st.expander(f"{home_t['name']}  vs  {away_t['name']}{marcador}"):
                st.markdown(f"{flag_html(m['home'])}**{home_t['name']}**  vs  **{away_t['name']}**{flag_html(m['away'])}", unsafe_allow_html=True)
                with st.form(key=f"form_match_{m['id']}"):
                    c1, c2 = st.columns(2)
                    hg = c1.number_input(f"Goles {home_t['name']}", min_value=0, max_value=20, value=m["home_goals"] or 0, step=1, key=f"hg_{m['id']}")
                    ag = c2.number_input(f"Goles {away_t['name']}", min_value=0, max_value=20, value=m["away_goals"] or 0, step=1, key=f"ag_{m['id']}")
                    if st.form_submit_button("💾 Guardar resultado"):
                        m["home_goals"], m["away_goals"], m["played"] = int(hg), int(ag), True
                        save_state(state)
                        st.success("Resultado guardado ✅")
                        st.balloons()
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

        final_match = get_match(matches, "final", 1)
        if final_match and final_match["played"]:
            champ, runner_up = winner_of(final_match), loser_of(final_match)
            st.markdown(f'<div class="champion-banner"><h2>🏆 CAMPEÓN DEL MUNDO 🏆</h2>'
                        f'<div style="margin-top:8px; font-size:1.4rem;">{flag_html(champ, size="lg")}<b>{TEAMS[champ]["name"]}</b></div>'
                        f'<div style="margin-top:6px; opacity:0.85;">🥈 Subcampeón: {TEAMS[runner_up]["name"]}</div></div>',
                        unsafe_allow_html=True)

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

                            if st.form_submit_button("💾 Guardar resultado"):
                                if hg == ag and pen_home == pen_away:
                                    st.error("En eliminación directa no puede haber doble empate. Define un ganador por penales.")
                                else:
                                    m["home_goals"], m["away_goals"], m["played"] = int(hg), int(ag), True
                                    if hg == ag:
                                        m["pen_home"], m["pen_away"] = int(pen_home), int(pen_away)
                                    save_state(state)
                                    st.success("Resultado guardado ✅")
                                    st.balloons()
                                    st.rerun()

st.markdown("---")
st.caption("FMMJ WORLD CUP UNITED 26 · Hecho con ❤️ por Mati, Jnka y Dibu · Streamlit App")
