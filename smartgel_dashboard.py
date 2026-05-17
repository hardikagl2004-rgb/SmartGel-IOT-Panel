# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random
import base64
import json
import re
from datetime import datetime

# ------------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title="SmartGel IoT Healthcare Portal",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# GLOBAL CSS — Clean light theme, professional, soft accents
# ------------------------------------------------------------------
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&family=Merriweather+Sans:wght@400;600;700;800&display=swap');

  :root {
    --brand:       #1d6fa4;
    --brand-light: #e8f4fb;
    --brand-mid:   #5fa8d3;
    --success:     #1b8a5a;
    --success-bg:  #e6f6ef;
    --warning:     #b45309;
    --warning-bg:  #fef3c7;
    --danger:      #c0392b;
    --danger-bg:   #fdecea;
    --purple:      #6d3fc0;
    --purple-bg:   #f0ebfb;
    --surface:     #f4f7fb;
    --card:        #ffffff;
    --border:      #dce6f0;
    --text:        #1a2b3c;
    --muted:       #5a7184;
    --muted-light: #8fa5b8;
    --radius:      10px;
    --radius-lg:   16px;
    --shadow-sm:   0 1px 4px rgba(29,111,164,0.08);
    --shadow-md:   0 4px 16px rgba(29,111,164,0.12);
  }

  html, body, [class*="css"] {
    font-family: 'Lato', sans-serif !important;
    color: var(--text);
    background-color: var(--surface) !important;
  }

  /* Page background */
  .main { background-color: var(--surface) !important; }
  .main .block-container {
    padding-top: 1.8rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
    animation: fadeUp 0.45s ease both;
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(14px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.5; }
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  @keyframes shimmerFlow {
    0%   { background-position: 0%   50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0%   50%; }
  }

  /* Metric cards */
  [data-testid="metric-container"] {
    background: var(--card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.1rem 1.3rem !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.2s, transform 0.2s;
  }
  [data-testid="metric-container"]:hover {
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-2px);
  }
  [data-testid="metric-container"] label {
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.09em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
  }
  [data-testid="metric-container"] [data-testid="metric-value"] {
    font-family: 'Merriweather Sans', sans-serif !important;
    font-size: 1.55rem !important;
    font-weight: 800 !important;
    color: var(--text) !important;
  }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {
    background: #eaf1f8;
    border-radius: 50px;
    padding: 5px;
    gap: 2px;
    border: 1px solid var(--border);
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 50px !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: var(--muted) !important;
    padding: 0.45rem 1.15rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.01em !important;
  }
  .stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: var(--brand) !important;
    box-shadow: 0 2px 8px rgba(29,111,164,0.14) !important;
  }

  /* Primary buttons */
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--brand) 0%, #155d8c 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 50px !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    padding: 0.55rem 1.5rem !important;
    box-shadow: 0 4px 14px rgba(29,111,164,0.28) !important;
    transition: all 0.22s !important;
  }
  .stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 7px 20px rgba(29,111,164,0.36) !important;
  }
  .stButton > button:not([kind="primary"]) {
    border-radius: 50px !important;
    font-weight: 600 !important;
    font-size: 0.83rem !important;
    border-color: var(--border) !important;
    color: var(--muted) !important;
    transition: all 0.2s !important;
    background: white !important;
  }
  .stButton > button:not([kind="primary"]):hover {
    border-color: var(--brand-mid) !important;
    color: var(--brand) !important;
  }

  /* Sidebar — clean light */
  [data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1.5px solid var(--border) !important;
    box-shadow: 2px 0 12px rgba(29,111,164,0.06) !important;
  }
  [data-testid="stSidebar"] * { color: var(--text) !important; }
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3 {
    color: var(--brand) !important;
    font-family: 'Merriweather Sans', sans-serif !important;
  }
  [data-testid="stSidebar"] .stRadio label {
    font-size: 0.84rem !important;
    color: var(--text) !important;
  }

  /* File uploader */
  [data-testid="stFileUploader"] {
    border-radius: var(--radius-lg) !important;
    border: 2px dashed var(--brand-mid) !important;
    background: var(--brand-light) !important;
  }

  /* Alerts */
  [data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border-left-width: 4px !important;
    font-size: 0.87rem !important;
  }

  /* Dataframe */
  [data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    overflow: hidden;
    border: 1px solid var(--border) !important;
  }

  /* Divider */
  hr {
    border: none !important;
    border-top: 1.5px solid var(--border) !important;
    margin: 1.5rem 0 !important;
  }

  /* Section header */
  .sec-hdr {
    font-family: 'Merriweather Sans', sans-serif;
    font-size: 0.93rem;
    font-weight: 800;
    color: var(--brand);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding-bottom: 0.35rem;
    border-bottom: 2.5px solid var(--brand-mid);
    margin-bottom: 0.9rem;
    display: inline-block;
  }

  /* Live badge */
  .live-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: #e6f6ef;
    border: 1px solid #a7dfbe;
    border-radius: 50px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--success);
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }
  .live-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: #1b8a5a;
    animation: pulse 1.4s infinite;
    flex-shrink: 0;
  }

  /* Nav cards in sidebar */
  .nav-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 11px;
    border-radius: var(--radius);
    border: 1.5px solid transparent;
    margin-bottom: 4px;
    transition: all 0.2s;
  }
  .nav-item:hover {
    background: var(--brand-light);
    border-color: var(--border);
  }
  .nav-item.nav-active {
    background: var(--brand-light);
    border-color: var(--brand-mid);
  }
  .nav-icon {
    width: 30px; height: 30px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 8px;
    background: #eaf1f8;
    font-size: 1rem;
    flex-shrink: 0;
  }
  .nav-label { font-size: 0.82rem; font-weight: 700; color: var(--text); }
  .nav-desc  { font-size: 0.68rem; color: var(--muted-light); }
  .nav-pip {
    margin-left: auto;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--brand);
    flex-shrink: 0;
  }

  /* Step pill */
  .step-pill {
    display: inline-flex; align-items: center; justify-content: center;
    width: 24px; height: 24px;
    border-radius: 50%;
    background: var(--brand);
    color: #fff;
    font-weight: 800;
    font-size: 0.72rem;
    margin-right: 8px;
    flex-shrink: 0;
  }

  /* Card container */
  .card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.3rem 1.5rem;
    box-shadow: var(--shadow-sm);
  }

  /* Healing bar */
  .healing-bar {
    height: 7px;
    border-radius: 50px;
    background: linear-gradient(90deg, #1b8a5a, #f59e0b, #c0392b);
    background-size: 200% 100%;
    animation: shimmerFlow 3s ease infinite;
  }

  /* Info chip */
  .chip {
    display: inline-flex; align-items: center; gap: 5px;
    background: var(--brand-light);
    border: 1px solid #b8d9ef;
    border-radius: 50px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--brand);
  }

  /* Spinner */
  .stSpinner > div { border-top-color: var(--brand) !important; }

  /* Image preview placeholder */
  .img-placeholder {
    border: 2px dashed var(--border);
    border-radius: var(--radius-lg);
    background: #f8fbfe;
    padding: 3.5rem 1rem;
    text-align: center;
  }

  /* Action item */
  .action-item {
    display: flex; align-items: flex-start; gap: 10px;
    border-radius: 10px; padding: 9px 13px; margin-bottom: 6px; font-size: 0.84rem;
  }
  .action-num { font-weight: 800; flex-shrink: 0; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SCENARIO DATA
# ------------------------------------------------------------------
SCENARIOS = {
    "Acne / Severe Pimple Spot": {
        "ph_readings":    [5.2, 5.5, 5.2, 5.3, 5.4, 5.5, 5.3, 5.2, 5.4, 5.5],
        "gel_color":      "#c026d3",
        "line_color":     "#c026d3",
        "fill_color":     "rgba(192,38,211,0.07)",
        "status":         "NORMAL",
        "status_detail":  "Stable | pH ~5.5 | Acidic Shield Active",
        "alert_type":     "success",
        "alert_msg":      "Wound healing under stable acidic conditions. No intervention required.",
        "temp_range":     (36.4, 37.1),
        "moisture_range": (60, 72),
        "bacterial_load": "LOW",
        "bl_delta":       "normal",
        "treatment":      "Salicylic Acid Hydrogel 2%",
        "healing_stage":  "Inflammatory → Proliferative",
        "reapply_hours":  3.5,
        "radar_scores":   [90, 88, 75, 92, 85, 95],
        "bar_color":      "#0891b2",
    },
    "Chronic Diabetic Foot Ulcer": {
        "ph_readings":    [5.5, 6.0, 6.8, 7.4, 7.8, 8.0, 8.2, 8.4, 8.5, 8.5],
        "gel_color":      "#dc2626",
        "line_color":     "#dc2626",
        "fill_color":     "rgba(220,38,38,0.07)",
        "status":         "CRITICAL",
        "status_detail":  "CRITICAL ALKALINITY | pH ~8.5 | Necrosis Risk",
        "alert_type":     "error",
        "alert_msg":      "CRITICAL: High bacterial load & tissue necrosis detected. Immediate clinical evaluation required.",
        "temp_range":     (37.8, 39.2),
        "moisture_range": (85, 95),
        "bacterial_load": "CRITICAL",
        "bl_delta":       "inverse",
        "treatment":      "Antimicrobial Silver Hydrogel",
        "healing_stage":  "Chronic Inflammatory (Stalled)",
        "reapply_hours":  1.0,
        "radar_scores":   [30, 35, 25, 15, 20, 50],
        "bar_color":      "#dc2626",
    },
    "Ignored Dog Bite Scratch": {
        "ph_readings":    [5.0, 5.2, 6.0, 6.5, 7.2, 7.8, 8.2, 8.5, 8.8, 8.8],
        "gel_color":      "#ea580c",
        "line_color":     "#ea580c",
        "fill_color":     "rgba(234,88,12,0.07)",
        "status":         "DANGER",
        "status_detail":  "DANGER | pH ~8.8 | Animal Contaminants Detected",
        "alert_type":     "error",
        "alert_msg":      "DANGER: Animal bacterial contaminants active. High Rabies & Pasteurella risk. Seek Post-Exposure Prophylaxis IMMEDIATELY.",
        "temp_range":     (38.2, 40.1),
        "moisture_range": (88, 98),
        "bacterial_load": "EXTREME",
        "bl_delta":       "inverse",
        "treatment":      "Antiseptic Hydrogel + PEP Protocol",
        "healing_stage":  "Acute Contamination",
        "reapply_hours":  0.5,
        "radar_scores":   [15, 20, 18, 10, 12, 40],
        "bar_color":      "#ea580c",
    },
}

DAYS          = ["Day " + str(i + 1) for i in range(10)]
SCENARIO_KEYS = list(SCENARIOS.keys())
CHART_COLORS  = ["#c026d3", "#dc2626", "#ea580c"]

# ------------------------------------------------------------------
# SESSION STATE INITIALISATION
# ------------------------------------------------------------------
defaults = {
    "selected":       SCENARIO_KEYS[0],
    "sim_running":    False,
    "log":            [],
    "wound_analysis": None,
    "sidebar_api_key": "",
    "image_source":   "upload",
    "camera_image":   None,
    "active_tab":     0,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

TAB_DEFS = [
    {"icon": "📊", "label": "Dashboard",           "desc": "Live vitals & telemetry"},
    {"icon": "📈", "label": "pH Trend Analysis",   "desc": "Bar chart, gauge & comparison"},
    {"icon": "🗂️", "label": "Sensor Log",          "desc": "Event log & CSV export"},
    {"icon": "📋", "label": "Clinical Report",     "desc": "Summary & radar chart"},
    {"icon": "🩹", "label": "Wound Image Analysis","desc": "AI-powered image review"},
]

# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
    # Logo / title
    st.markdown("""
    <div style='padding:1.2rem 0 0.6rem;'>
      <div style='font-family:Merriweather Sans,sans-serif;font-size:1.3rem;font-weight:800;
                  color:#1d6fa4;letter-spacing:-0.02em;'>SmartGel IoT</div>
      <div style='font-size:0.7rem;color:#8fa5b8;font-weight:700;letter-spacing:0.1em;
                  text-transform:uppercase;margin-top:2px;'>Healthcare Portal</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='live-badge' style='margin-bottom:1rem;'>
      <div class='live-dot'></div>BLE Uplink Active
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Navigation
    st.markdown("""
    <div style='font-size:0.68rem;font-weight:800;color:#8fa5b8;
                text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;'>
      Navigation
    </div>
    """, unsafe_allow_html=True)

    for idx, tdef in enumerate(TAB_DEFS):
        is_active = st.session_state.active_tab == idx
        ac = "nav-active" if is_active else ""
        pip = "<div class='nav-pip'></div>" if is_active else ""
        st.markdown(f"""
        <div class='nav-item {ac}'>
          <div class='nav-icon'>{tdef['icon']}</div>
          <div style='flex:1;'>
            <div class='nav-label'>{tdef['label']}</div>
            <div class='nav-desc'>{tdef['desc']}</div>
          </div>
          {pip}
        </div>
        """, unsafe_allow_html=True)
        btn_lbl = "● Active" if is_active else "Open →"
        if st.button(btn_lbl, key=f"nav_{idx}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active_tab = idx
            st.rerun()

    st.divider()

    # Scenario selector — this is the FIX: we use on_change to update selected
    st.markdown("#### 🧪 Clinical Scenario")
    scenario_idx = SCENARIO_KEYS.index(st.session_state.selected)
    chosen = st.radio(
        "Select a wound scenario to monitor:",
        SCENARIO_KEYS,
        index=scenario_idx,
        key="scenario_radio",
    )
    # Always sync selected from radio (this fixes the non-working selection)
    if chosen != st.session_state.selected:
        st.session_state.selected = chosen
        st.session_state.wound_analysis = None  # clear stale analysis
        st.rerun()

    sc_side = SCENARIOS[st.session_state.selected]

    st.divider()

    st.markdown("#### ⚙️ Simulation Controls")
    sim_interval = st.slider("Update interval (sec)", 1, 10, 3, key="sim_interval")
    noise_level  = st.slider("Sensor noise level",   0.0, 0.5, 0.05, 0.01, key="noise_level")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶ Start", use_container_width=True, type="primary", key="btn_start"):
            st.session_state.sim_running = True
    with col_b:
        if st.button("■ Stop", use_container_width=True, key="btn_stop"):
            st.session_state.sim_running = False
    if st.button("Clear Log", use_container_width=True, key="btn_clear"):
        st.session_state.log = []
        st.success("Log cleared.")

    st.divider()
    st.markdown(f"""
    <div style='background:#fff8f0;border:1.5px solid #fcd9a0;border-radius:{TAB_DEFS[0]["icon"] and "10px"};
                padding:10px 13px;font-size:0.83rem;color:#92400e;border-radius:10px;'>
      <b>⏱ Reapply in {sc_side["reapply_hours"]} hrs</b><br>
      <span style='color:#a16207;'>{sc_side["treatment"]}</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 🔑 AI Analysis Key")
    st.caption("Enter your Google API key to enable wound image analysis.")
    api_key_input = st.text_input(
        "Google API Key",
        type="password",
        placeholder="AIza...",
        key="sidebar_api_key",
        help="Get your key from console.cloud.google.com → APIs & Services → Credentials",
    )
    if st.session_state["sidebar_api_key"]:
        st.success("✅ Key entered — ready to analyse!")

    st.divider()
    st.caption("SmartGel IoT Healthcare Portal v4.1")
    st.caption("© 2025 SmartGel Medical Systems")

# ------------------------------------------------------------------
# ACTIVE SCENARIO (computed after sidebar so selection is up-to-date)
# ------------------------------------------------------------------
sc    = SCENARIOS[st.session_state.selected]
noise = st.session_state.get("noise_level", 0.05)

# ------------------------------------------------------------------
# PAGE HEADER
# ------------------------------------------------------------------
hdr_col, badge_col = st.columns([3, 1])
with hdr_col:
    st.markdown("""
    <div style='font-family:Merriweather Sans,sans-serif;font-size:2rem;font-weight:800;
                letter-spacing:-0.03em;color:#1a2b3c;margin-bottom:2px;'>
      SmartGel IoT Healthcare Portal
    </div>
    <div style='font-size:0.82rem;color:#5a7184;'>
      Biocompatible Nanosensor Monitoring · Real-time Wound pH Telemetry
    </div>
    """, unsafe_allow_html=True)
with badge_col:
    st.markdown(f"""
    <div style='text-align:right;padding-top:8px;'>
      <div class='live-badge' style='float:right;'>
        <div class='live-dot'></div>LIVE
      </div>
      <div style='clear:both;font-size:0.7rem;color:#8fa5b8;margin-top:6px;'>
        {datetime.now().strftime("%Y-%m-%d  %H:%M:%S")}
      </div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# Status alert
if sc["alert_type"] == "success":
    st.success(f"**Status {sc['status']}** — {sc['alert_msg']}")
else:
    st.error(f"**Status {sc['status']}** — {sc['alert_msg']}")

st.divider()

# Quick nav bar
st.markdown("""
<div style='font-size:0.7rem;font-weight:800;color:#8fa5b8;
            text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;'>
  Quick Navigation
</div>
""", unsafe_allow_html=True)

nav_cols = st.columns(5)
tab_colors = ["#1d6fa4", "#6d3fc0", "#1b8a5a", "#b45309", "#c0392b"]
tab_bgs    = ["#e8f4fb", "#f0ebfb", "#e6f6ef", "#fef3c7", "#fdecea"]
for i, (tdef, ncol) in enumerate(zip(TAB_DEFS, nav_cols)):
    with ncol:
        active = st.session_state.active_tab == i
        bg   = tab_colors[i] if active else "#ffffff"
        fg   = "#ffffff"     if active else "#5a7184"
        bord = tab_colors[i] if active else "#dce6f0"
        shad = f"0 4px 12px {tab_colors[i]}33" if active else "none"
        st.markdown(f"""
        <div style='background:{bg};border:1.5px solid {bord};border-radius:12px;
                    padding:10px 6px;text-align:center;box-shadow:{shad};
                    transition:all 0.2s;'>
          <div style='font-size:1.25rem;margin-bottom:3px;'>{tdef["icon"]}</div>
          <div style='font-size:0.7rem;font-weight:700;color:{fg};line-height:1.3;'>
            {tdef["label"]}
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "✓ Here" if active else "Open",
            key=f"qnav_{i}",
            use_container_width=True,
            type="primary" if active else "secondary",
        ):
            st.session_state.active_tab = i
            st.rerun()

st.divider()

# ------------------------------------------------------------------
# TAB RENDERING
# ------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  📊 Dashboard  ",
    "  📈 pH Trend Analysis  ",
    "  🗂️ Sensor Log  ",
    "  📋 Clinical Report  ",
    "  🩹 Wound Image Analysis  ",
])

# ── JS tab switcher (more reliable version) ──────────────────────
_active_tab = st.session_state.active_tab
st.markdown(f"""
<script>
(function() {{
  var idx = {_active_tab};
  function tryClick(attempt) {{
    var tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
    if (tabs.length > idx) {{
      tabs[idx].click();
    }} else if (attempt < 15) {{
      setTimeout(function() {{ tryClick(attempt + 1); }}, 150);
    }}
  }}
  setTimeout(function() {{ tryClick(0); }}, 100);
}})();
</script>
""", unsafe_allow_html=True)


# ==================================================================
# TAB 1 — DASHBOARD
# ==================================================================
with tab1:
    cur_ph   = round(sc["ph_readings"][-1] + random.uniform(-noise, noise), 2)
    cur_temp = round(random.uniform(*sc["temp_range"]), 1)
    cur_mois = round(random.uniform(*sc["moisture_range"]), 1)

    k1, k2, k3, k4 = st.columns(4)
    ph_delta_color = "inverse" if cur_ph > 7.0 else "normal"
    k1.metric("Current pH",       str(cur_ph),          f"{round(cur_ph - 7.0, 2):+.2f} vs neutral", delta_color=ph_delta_color)
    k2.metric("Wound Temp (°C)",  f"{cur_temp} °C",     f"{round(cur_temp - 37.0, 1):+.1f} vs normal", delta_color="inverse")
    k3.metric("Moisture Level",   f"{cur_mois} %",      f"{round(cur_mois - 75.0, 1):+.1f} vs target", delta_color="inverse")
    k4.metric("Bacterial Load",   sc["bacterial_load"])

    st.divider()
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.markdown('<span class="sec-hdr">Hydrogel Status</span>', unsafe_allow_html=True)
        gc = sc["gel_color"]
        r_v = int(gc[1:3], 16); g_v = int(gc[3:5], 16); b_v = int(gc[5:7], 16)
        fig_orb = go.Figure()
        fig_orb.add_shape(type="circle", x0=0.2, y0=0.5, x1=0.8, y1=0.97,
                          xref="paper", yref="paper", fillcolor=gc,
                          line_color=f"rgba({r_v},{g_v},{b_v},0.35)", line_width=6)
        fig_orb.add_annotation(x=0.5, y=0.76, xref="paper", yref="paper",
                                text=f"<b>pH {cur_ph}</b>", showarrow=False,
                                font=dict(size=24, color="#ffffff"))
        fig_orb.add_annotation(x=0.5, y=0.38, xref="paper", yref="paper",
                                text=f"<b>STATUS: {sc['status']}</b>", showarrow=False,
                                font=dict(size=13, color=gc))
        fig_orb.add_annotation(x=0.5, y=0.22, xref="paper", yref="paper",
                                text=sc["status_detail"], showarrow=False,
                                font=dict(size=9, color="#5a7184"))
        fig_orb.update_layout(
            paper_bgcolor="#eaf3fb", plot_bgcolor="#eaf3fb", height=220,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False), yaxis=dict(visible=False),
        )
        st.plotly_chart(fig_orb, use_container_width=True, config={"displayModeBar": False})
        for label, val in [
            ("🧴 Treatment",      sc["treatment"]),
            ("🔬 Healing Stage",  sc["healing_stage"]),
            ("📡 Connection",     "BLE Active · 2.4 GHz · Nominal"),
            ("⏱ Reapply In",     f"{sc['reapply_hours']} hours"),
        ]:
            st.markdown(f"""
            <div class='chip' style='margin-bottom:6px;display:flex;border-radius:8px;padding:7px 12px;'>
              <span style='font-weight:700;min-width:110px;'>{label}</span>
              <span style='color:#1a2b3c;font-weight:400;'>{val}</span>
            </div>
            """, unsafe_allow_html=True)

    with right_col:
        st.markdown('<span class="sec-hdr">pH Telemetry — 10-Day Trend</span>', unsafe_allow_html=True)
        ph_vals = [round(v + random.uniform(-noise, noise), 2) for v in sc["ph_readings"]]
        fig_trend = go.Figure()
        fig_trend.add_hrect(y0=7.0, y1=10.5, fillcolor="rgba(220,38,38,0.06)", line_width=0,
                             annotation_text="Alkaline Danger Zone (pH > 7)",
                             annotation_position="top left",
                             annotation_font_color="#c0392b", annotation_font_size=11)
        fig_trend.add_hrect(y0=4.0, y1=6.0, fillcolor="rgba(27,138,90,0.06)", line_width=0,
                             annotation_text="Healthy Acidic Range (pH < 6)",
                             annotation_position="bottom left",
                             annotation_font_color="#1b8a5a", annotation_font_size=11)
        fig_trend.add_trace(go.Scatter(
            x=DAYS, y=ph_vals, mode="lines+markers", name="pH Reading",
            line=dict(color=sc["line_color"], width=3, shape="spline"),
            marker=dict(size=10, color=ph_vals,
                        colorscale=[[0.0,"#1b8a5a"],[0.4,"#0891b2"],[0.7,"#d97706"],[1.0,"#dc2626"]],
                        cmin=5, cmax=9, line=dict(color="#ffffff", width=2), showscale=False),
            fill="tozeroy", fillcolor=sc["fill_color"],
            hovertemplate="<b>%{x}</b><br>pH = %{y:.2f}<extra></extra>",
        ))
        fig_trend.add_hline(y=7.0, line_dash="dash", line_color="#dc2626", line_width=1.5)
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#f4f8fc", height=340,
            margin=dict(l=10, r=20, t=20, b=10),
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#5a7184"), color="#5a7184"),
            yaxis=dict(gridcolor="#dce6f0", range=[4, 10.5], title="pH Value",
                       color="#5a7184", tickfont=dict(size=11)),
            showlegend=False,
        )
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
        s1, s2, s3 = st.columns(3)
        s1.metric("Min pH (10-day)",  str(min(sc["ph_readings"])))
        s2.metric("Max pH (10-day)",  str(max(sc["ph_readings"])))
        s3.metric("Mean pH (10-day)", str(round(sum(sc["ph_readings"]) / 10, 2)))


# ==================================================================
# TAB 2 — pH TREND ANALYSIS
# ==================================================================
with tab2:
    st.markdown('<span class="sec-hdr">Advanced pH Trend Analysis</span>', unsafe_allow_html=True)
    ph_vals2 = [round(v + random.uniform(-noise, noise), 2) for v in sc["ph_readings"]]
    col_bar, col_gauge = st.columns(2)

    with col_bar:
        st.markdown("**Daily pH Bar Chart**")
        bar_colors = ["#1b8a5a" if v < 6.0 else ("#d97706" if v < 7.0 else "#dc2626") for v in ph_vals2]
        fig_bar = go.Figure(go.Bar(
            x=DAYS, y=ph_vals2,
            marker_color=bar_colors, marker_line_color="#ffffff", marker_line_width=2,
            text=[f"pH {v}" for v in ph_vals2], textposition="outside",
            textfont=dict(size=10, color="#334155"),
        ))
        fig_bar.add_hline(y=7.0, line_dash="dash", line_color="#dc2626", line_width=2,
                          annotation_text="pH 7.0 — Danger Threshold",
                          annotation_font_color="#dc2626", annotation_font_size=11)
        fig_bar.add_hline(y=6.0, line_dash="dot", line_color="#d97706", line_width=1.5,
                          annotation_text="pH 6.0 — Warning",
                          annotation_font_color="#d97706", annotation_font_size=10)
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#f4f8fc", height=360,
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis=dict(showgrid=False, color="#5a7184", tickfont=dict(size=10)),
            yaxis=dict(gridcolor="#dce6f0", range=[4, 11.5], color="#5a7184"),
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with col_gauge:
        st.markdown("**Live pH Gauge**")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=ph_vals2[-1],
            delta={"reference": 7.0, "valueformat": ".2f",
                   "increasing": {"color": "#dc2626"}, "decreasing": {"color": "#1b8a5a"}},
            number={"font": {"color": "#1a2b3c", "size": 54}, "valueformat": ".2f"},
            gauge={
                "axis": {"range": [4, 10], "tickwidth": 1, "tickcolor": "#5a7184",
                         "tickfont": {"color": "#5a7184", "size": 11}, "nticks": 7},
                "bar": {"color": sc["gel_color"], "thickness": 0.3},
                "bgcolor": "#f4f8fc", "borderwidth": 1, "bordercolor": "#dce6f0",
                "steps": [
                    {"range": [4.0, 6.0], "color": "#dcfce7"},
                    {"range": [6.0, 7.0], "color": "#fef9c3"},
                    {"range": [7.0, 10.0], "color": "#fee2e2"},
                ],
                "threshold": {"line": {"color": "#dc2626", "width": 4}, "thickness": 0.8, "value": 7.4},
            },
            title={
                "text": "Current pH Reading<br>"
                        "<span style='font-size:12px;color:#5a7184'>"
                        "Green = Healthy · Yellow = Warning · Red = Danger</span>",
                "font": {"color": "#1a2b3c", "size": 14},
            },
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", height=360, margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    st.divider()
    st.markdown('<span class="sec-hdr">All-Scenario Comparison</span>', unsafe_allow_html=True)
    fig_comp = go.Figure()
    for i, (sname, sval) in enumerate(SCENARIOS.items()):
        fig_comp.add_trace(go.Scatter(
            x=DAYS, y=sval["ph_readings"], mode="lines+markers", name=sname,
            line=dict(width=2.5, shape="spline", color=CHART_COLORS[i]),
            marker=dict(size=8, color=CHART_COLORS[i], line=dict(color="#ffffff", width=1)),
            hovertemplate=f"<b>{sname}</b><br>%{{x}}: pH %{{y}}<extra></extra>",
        ))
    fig_comp.add_hline(y=7.0, line_dash="dot", line_color="#94a3b8", line_width=2,
                       annotation_text="Neutral pH 7.0", annotation_font_color="#64748b",
                       annotation_font_size=11)
    fig_comp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#f4f8fc", height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, color="#5a7184", tickfont=dict(size=10)),
        yaxis=dict(gridcolor="#dce6f0", range=[4, 10], title="pH Value", color="#5a7184"),
        legend=dict(bgcolor="rgba(255,255,255,0.96)", bordercolor="#dce6f0",
                    borderwidth=1, font=dict(size=12, color="#1a2b3c")),
    )
    st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})


# ==================================================================
# TAB 3 — SENSOR LOG
# ==================================================================
with tab3:
    st.markdown('<span class="sec-hdr">Live Sensor Event Log</span>', unsafe_allow_html=True)
    btn1, btn2, btn3 = st.columns([1, 1, 2])

    with btn1:
        if st.button("➕ Add Reading", use_container_width=True, type="primary", key="add_reading"):
            ph_new   = round(sc["ph_readings"][-1] + random.uniform(-0.35, 0.35), 2)
            temp_new = round(random.uniform(*sc["temp_range"]), 1)
            mois_new = round(random.uniform(*sc["moisture_range"]), 1)
            status_new = "CRITICAL" if ph_new > 7.0 else "OK"
            st.session_state.log.append({
                "Timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Scenario":     st.session_state.selected[:32],
                "pH":           ph_new,
                "Temp (°C)":    temp_new,
                "Moisture (%)": mois_new,
                "Status":       status_new,
            })
            st.success(f"Reading logged — pH {ph_new} · Status: {status_new}")

    with btn2:
        if st.session_state.log:
            df_export = pd.DataFrame(st.session_state.log)
            st.download_button(
                "⬇ Export CSV", df_export.to_csv(index=False),
                "smartgel_sensor_log.csv", "text/csv", use_container_width=True,
            )

    st.divider()

    if st.session_state.log:
        df_log  = pd.DataFrame(st.session_state.log)
        total   = len(df_log)
        ok_cnt  = len(df_log[df_log["Status"] == "OK"])
        crit_cnt = total - ok_cnt
        lm1, lm2, lm3 = st.columns(3)
        lm1.metric("Total Readings",    total)
        lm2.metric("OK Readings",       ok_cnt)
        lm3.metric("Critical Readings", crit_cnt,
                   delta=f"{crit_cnt} need attention" if crit_cnt > 0 else "All clear",
                   delta_color="inverse" if crit_cnt > 0 else "normal")
        st.divider()
        st.dataframe(df_log, use_container_width=True, height=400)
        if len(df_log) > 1:
            st.markdown("**pH Over Time (from log)**")
            fig_log = go.Figure(go.Scatter(
                x=df_log["Timestamp"], y=df_log["pH"],
                mode="lines+markers", line=dict(color="#1d6fa4", width=2),
                marker=dict(size=8, color=df_log["pH"],
                            colorscale=[[0, "#1b8a5a"], [0.5, "#d97706"], [1, "#dc2626"]],
                            cmin=5, cmax=9, line=dict(color="#ffffff", width=1),
                            showscale=True, colorbar=dict(title="pH", thickness=12)),
                hovertemplate="<b>%{x}</b><br>pH = %{y:.2f}<extra></extra>",
            ))
            fig_log.add_hline(y=7.0, line_dash="dash", line_color="#dc2626",
                              annotation_text="Danger Threshold", annotation_font_color="#dc2626")
            fig_log.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#f4f8fc", height=280,
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=False, color="#5a7184", tickfont=dict(size=9)),
                yaxis=dict(gridcolor="#dce6f0", range=[4, 10], title="pH", color="#5a7184"),
                showlegend=False,
            )
            st.plotly_chart(fig_log, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No readings logged yet. Click **Add Reading** above, or start the live simulation from the sidebar.")

    # Live simulation auto-log
    if st.session_state.sim_running:
        with st.spinner("Live simulation active — auto-logging readings…"):
            time.sleep(st.session_state.get("sim_interval", 3))
        ph_sim   = round(sc["ph_readings"][-1] + random.uniform(-0.35, 0.35), 2)
        temp_sim = round(random.uniform(*sc["temp_range"]), 1)
        mois_sim = round(random.uniform(*sc["moisture_range"]), 1)
        st.session_state.log.append({
            "Timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Scenario":     st.session_state.selected[:32],
            "pH":           ph_sim,
            "Temp (°C)":    temp_sim,
            "Moisture (%)": mois_sim,
            "Status":       "CRITICAL" if ph_sim > 7.0 else "OK",
        })
        st.rerun()


# ==================================================================
# TAB 4 — CLINICAL REPORT
# ==================================================================
with tab4:
    st.markdown('<span class="sec-hdr">Auto-Generated Clinical Summary</span>', unsafe_allow_html=True)

    ph_mean_val = round(sum(sc["ph_readings"]) / 10, 2)
    ph_max_val  = max(sc["ph_readings"])
    ph_min_val  = min(sc["ph_readings"])
    ph_trend    = ("Alkaline Drift Detected (worsening)"
                   if sc["ph_readings"][-1] > sc["ph_readings"][0]
                   else "Stable or Improving")
    recommendation = (
        "Continue current protocol. Wound environment is stable and healing is progressing normally. "
        "Weekly monitoring is recommended."
        if sc["bacterial_load"] == "LOW"
        else "IMMEDIATE clinical evaluation required. Alkaline pH shift confirms active bacterial colonisation. "
             "Consider systemic antibiotics and advanced wound debridement. Do not delay treatment."
    )

    rep_col, radar_col = st.columns([1, 1])

    with rep_col:
        st.markdown("**Clinical Data Summary**")
        rows = [
            ("Patient Scenario",    st.session_state.selected),
            ("Treatment Protocol",  sc["treatment"]),
            ("Healing Stage",       sc["healing_stage"]),
            ("pH Min (10-day)",     str(ph_min_val)),
            ("pH Max (10-day)",     str(ph_max_val)),
            ("Mean pH (10-day)",    str(ph_mean_val)),
            ("pH Trend",            ph_trend),
            ("Bacterial Load",      sc["bacterial_load"]),
            ("Reapplication Every", f"{sc['reapply_hours']} hours"),
            ("Sensor Connection",   "BLE Active — All sensors nominal"),
            ("Report Generated",    datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]
        df_report = pd.DataFrame(rows, columns=["Parameter", "Value"])
        st.dataframe(df_report, use_container_width=True, hide_index=True, height=410)
        st.divider()
        if sc["bacterial_load"] == "LOW":
            st.success(f"**Recommendation:** {recommendation}")
        else:
            st.error(f"**Recommendation:** {recommendation}")
        st.divider()
        st.download_button(
            "⬇ Download Clinical Report (CSV)", df_report.to_csv(index=False),
            "smartgel_clinical_report.csv", "text/csv",
            type="primary", use_container_width=True,
        )

    with radar_col:
        st.markdown("**Wound Health Radar**")
        categories = ["pH Safety", "Temperature", "Moisture Control",
                      "Bacterial Defence", "Healing Rate", "Gel Integrity"]
        scores = sc["radar_scores"]
        gc2 = sc["gel_color"]
        r2 = int(gc2[1:3], 16); g2 = int(gc2[3:5], 16); b2 = int(gc2[5:7], 16)
        fill2 = f"rgba({r2},{g2},{b2},0.18)"
        fig_radar = go.Figure(go.Scatterpolar(
            r=scores + [scores[0]], theta=categories + [categories[0]],
            fill="toself", fillcolor=fill2,
            line=dict(color=gc2, width=2.5),
            marker=dict(size=9, color=gc2, line=dict(color="#ffffff", width=1)),
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#f4f8fc",
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="#dce6f0",
                                tickfont=dict(size=9, color="#5a7184"),
                                tickvals=[0, 25, 50, 75, 100]),
                angularaxis=dict(gridcolor="#dce6f0", tickfont=dict(size=11, color="#1a2b3c")),
            ),
            paper_bgcolor="rgba(0,0,0,0)", height=420,
            margin=dict(l=50, r=50, t=30, b=30), showlegend=False,
        )
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
        radar_df = pd.DataFrame({
            "Category":    categories,
            "Score / 100": scores,
            "Rating":      ["Excellent" if s >= 80 else ("Good" if s >= 60 else ("Fair" if s >= 40 else "Poor"))
                            for s in scores],
        })
        st.dataframe(radar_df, use_container_width=True, hide_index=True, height=245)


# ==================================================================
# TAB 5 — WOUND IMAGE ANALYSIS
# ==================================================================
with tab5:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1d6fa4 0%,#0a4a73 100%);
                border-radius:16px;padding:1.6rem 2rem;margin-bottom:1.2rem;'>
      <div style='font-family:Merriweather Sans,sans-serif;font-size:1.3rem;font-weight:800;
                  color:#ffffff;margin-bottom:5px;'>
        🩹 AI-Powered Wound Image Analysis
      </div>
      <div style='font-size:0.84rem;color:#a8d4ed;line-height:1.6;'>
        Upload a photo or capture with your camera. The AI assesses severity, estimates
        healing time, and provides personalised care recommendations.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "⚠️ **Medical Disclaimer** — This AI analysis is for informational purposes only and does "
        "**not** replace professional medical advice. Always consult a qualified healthcare provider "
        "for diagnosis and treatment, especially for serious wounds."
    )
    st.divider()

    # ── Input mode toggle ──────────────────────────────────────────
    st.markdown("#### 📥 Choose Image Source")
    mode_c1, mode_c2, mode_c3 = st.columns([1, 1, 4])
    with mode_c1:
        if st.button(
            "📁 Upload File", use_container_width=True, key="mode_upload",
            type="primary" if st.session_state.image_source == "upload" else "secondary",
        ):
            st.session_state.image_source = "upload"
            st.session_state.camera_image = None
            st.rerun()
    with mode_c2:
        if st.button(
            "📷 Use Camera", use_container_width=True, key="mode_camera",
            type="primary" if st.session_state.image_source == "camera" else "secondary",
        ):
            st.session_state.image_source = "camera"
            st.rerun()

    # Mode badge
    if st.session_state.image_source == "upload":
        st.markdown("""
        <div style='display:inline-flex;align-items:center;gap:7px;
                    background:#e8f4fb;border:1.5px solid #5fa8d3;border-radius:50px;
                    padding:5px 16px;font-size:0.78rem;font-weight:700;color:#1d6fa4;
                    margin:6px 0 0;'>
          📁 &nbsp;File Upload Mode
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='display:inline-flex;align-items:center;gap:7px;
                    background:#f0ebfb;border:1.5px solid #9d74d8;border-radius:50px;
                    padding:5px 16px;font-size:0.78rem;font-weight:700;color:#6d3fc0;
                    margin:6px 0 0;'>
          📷 &nbsp;Camera Capture Mode
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Image input + context ──────────────────────────────────────
    input_col, preview_col = st.columns([1, 1])

    with input_col:
        # STEP 1 — Image source
        step1_color = "#1d6fa4" if st.session_state.image_source == "upload" else "#6d3fc0"
        st.markdown(f"""
        <div style='display:flex;align-items:center;margin-bottom:10px;'>
          <span class='step-pill' style='background:{step1_color};'>1</span>
          <span style='font-weight:700;font-size:0.93rem;'>
            {"Upload Wound Image" if st.session_state.image_source == "upload" else "Capture Wound Photo"}
          </span>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.image_source == "upload":
            uploaded_file = st.file_uploader(
                "Drag & drop or click to browse",
                type=["jpg", "jpeg", "png", "webp", "bmp"],
                help="Supported formats: JPG, PNG, WEBP, BMP — Max 10 MB",
                key="wound_uploader",
            )
            if uploaded_file:
                st.markdown("""
                <div style='display:inline-flex;align-items:center;gap:6px;
                            background:#e6f6ef;border-radius:8px;padding:6px 12px;
                            font-size:0.8rem;font-weight:700;color:#1b8a5a;margin-top:4px;'>
                  ✅ &nbsp;Image ready for analysis
                </div>
                """, unsafe_allow_html=True)
        else:
            # Camera mode — st.camera_input is the correct Streamlit widget
            st.markdown("""
            <div style='background:#f0ebfb;border:2px dashed #9d74d8;border-radius:14px;
                        padding:1.2rem;text-align:center;margin-bottom:10px;'>
              <div style='font-size:2rem;margin-bottom:6px;'>📷</div>
              <div style='font-size:0.85rem;font-weight:700;color:#6d3fc0;margin-bottom:3px;'>
                Camera Capture
              </div>
              <div style='font-size:0.76rem;color:#5a7184;'>
                Allow camera access when prompted and take a clear, well-lit photo.
              </div>
            </div>
            """, unsafe_allow_html=True)
            # NOTE: st.camera_input returns a UploadedFile or None
            # We store separately to survive reruns
            cam_result = st.camera_input(
                "Take a photo of the wound",
                key="camera_widget",
                help="Point camera at wound and click the shutter button.",
            )
            if cam_result is not None:
                # New capture — save to session state
                st.session_state.camera_image = cam_result
                st.markdown("""
                <div style='display:inline-flex;align-items:center;gap:6px;
                            background:#e6f6ef;border-radius:8px;padding:6px 12px;
                            font-size:0.8rem;font-weight:700;color:#1b8a5a;margin-top:4px;'>
                  ✅ &nbsp;Photo captured — ready for analysis
                </div>
                """, unsafe_allow_html=True)
            uploaded_file = None  # not used in camera mode

        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

        # STEP 2 — Context
        st.markdown("""
        <div style='display:flex;align-items:center;margin-bottom:10px;'>
          <span class='step-pill'>2</span>
          <span style='font-weight:700;font-size:0.93rem;'>Provide Context (Optional)</span>
        </div>
        """, unsafe_allow_html=True)
        wound_age = st.selectbox(
            "How old is this wound?",
            ["Just occurred (< 1 hour)", "Few hours old (1–12 hours)",
             "1 day old", "2–3 days old", "4–7 days old",
             "More than 1 week old", "Chronic / Unknown"],
            key="wound_age_select",
        )
        patient_context = st.text_area(
            "Additional clinical context",
            placeholder="e.g. Diabetic patient, animal bite, burn injury, not cleaned yet, on blood thinners…",
            height=85,
            key="patient_ctx",
        )

        # STEP 3 — Analyse
        st.markdown("""
        <div style='display:flex;align-items:center;margin:12px 0 8px;'>
          <span class='step-pill'>3</span>
          <span style='font-weight:700;font-size:0.93rem;'>Run AI Analysis</span>
        </div>
        """, unsafe_allow_html=True)

        # Determine whether we have an image
        has_upload = (st.session_state.image_source == "upload" and uploaded_file is not None)
        has_camera = (st.session_state.image_source == "camera" and st.session_state.camera_image is not None)
        has_image  = has_upload or has_camera

        analyze_btn = st.button(
            "🔬 Analyse Wound with AI",
            type="primary", use_container_width=True,
            disabled=not has_image, key="analyse_btn",
        )
        if not has_image:
            st.caption("☝️ Provide an image above to enable analysis.")

    with preview_col:
        st.markdown("""
        <div style='font-weight:700;font-size:0.93rem;color:#1a2b3c;margin-bottom:10px;'>
          🖼️ Image Preview
        </div>
        """, unsafe_allow_html=True)
        if has_upload:
            st.image(uploaded_file, caption="Uploaded wound image", use_container_width=True)
        elif has_camera:
            st.image(st.session_state.camera_image, caption="Captured wound image",
                     use_container_width=True)
        else:
            st.markdown("""
            <div class='img-placeholder'>
              <div style='font-size:2.5rem;margin-bottom:10px;opacity:0.3;'>🩺</div>
              <div style='font-size:0.85rem;color:#8fa5b8;font-weight:600;'>
                Your image will appear here
              </div>
              <div style='font-size:0.73rem;color:#b8cdd8;margin-top:4px;'>
                Upload or capture a photo to get started
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── AI Analysis ───────────────────────────────────────────────
    if analyze_btn and has_image:
        # Determine bytes + mime
        if has_upload:
            image_bytes = uploaded_file.read()
            fname = uploaded_file.name.lower()
            mime_type = ("image/png" if fname.endswith(".png") else
                         "image/webp" if fname.endswith(".webp") else
                         "image/bmp"  if fname.endswith(".bmp")  else "image/jpeg")
        else:
            image_bytes = st.session_state.camera_image.getvalue()
            mime_type   = "image/jpeg"

        b64_image   = base64.standard_b64encode(image_bytes).decode("utf-8")
        context_str = (f"\n\nAdditional context from the user: {patient_context.strip()}"
                       if patient_context.strip() else "")

        prompt = f"""You are a clinical wound assessment AI assistant integrated into the SmartGel IoT Healthcare Portal.
A patient has uploaded a photo of their wound/injury and it is {wound_age}.{context_str}

Carefully analyse the wound image and provide a structured JSON response ONLY — no preamble, no markdown fences, no extra text.

Return a JSON object with exactly these keys:

{{
  "wound_type": "Short label e.g. Laceration / Abrasion / Burn / Puncture / Ulcer / Contusion / Infected wound",
  "severity_level": "MILD | MODERATE | SEVERE | CRITICAL",
  "severity_score": <integer 1-10>,
  "affected_area": "Brief description of body area and size estimate",
  "visible_signs": ["list", "of", "visible", "clinical", "signs"],
  "infection_risk": "LOW | MEDIUM | HIGH | VERY HIGH",
  "healing_time_min_days": <integer>,
  "healing_time_max_days": <integer>,
  "healing_phase": "Current phase: Haemostasis / Inflammatory / Proliferative / Remodelling",
  "immediate_actions": ["step 1", "step 2", "step 3"],
  "recommended_treatment": "Concise treatment recommendation including dressing type",
  "smartgel_recommendation": "Which SmartGel product or protocol from the portal is most relevant",
  "seek_emergency": true or false,
  "seek_doctor_within": "Immediately | Within 24 hours | Within 48-72 hours | Within 1 week | Monitor at home",
  "care_instructions": ["daily care step 1", "daily care step 2", "daily care step 3", "daily care step 4"],
  "warning_signs": ["sign to watch for 1", "sign to watch for 2", "sign to watch for 3"],
  "confidence_note": "One sentence on confidence / limitations of this visual assessment"
}}

Be medically accurate, conservative, and safety-first. If the wound appears serious, do not downplay it."""

        loading_placeholder = st.empty()
        loading_placeholder.markdown("""
        <div style='background:#eaf3fb;border:1.5px solid #b8d9ef;border-radius:14px;
                    padding:2rem;text-align:center;margin:1rem 0;'>
          <div style='width:42px;height:42px;border:4px solid #dce6f0;border-top-color:#1d6fa4;
                      border-radius:50%;animation:spin 0.9s linear infinite;margin:0 auto 1rem;'></div>
          <div style='font-family:Merriweather Sans,sans-serif;font-size:1rem;font-weight:700;
                      color:#1d6fa4;margin-bottom:5px;'>Analysing wound with AI…</div>
          <div style='font-size:0.8rem;color:#5a7184;'>
            Processing image · Assessing severity · Generating recommendations
          </div>
          <div style='margin-top:14px;height:5px;border-radius:50px;background:#dce6f0;overflow:hidden;'>
            <div class='healing-bar' style='height:100%;width:100%;'></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        try:
            import urllib.request, urllib.error

            api_key = st.session_state.get("sidebar_api_key", "")
            if not api_key:
                try:
                    api_key = st.secrets.get("GOOGLE_API_KEY", "")
                except Exception:
                    api_key = ""

            if not api_key:
                loading_placeholder.empty()
                st.error("**API Key Missing.** Paste your Google API key into the 🔑 AI Analysis Key field in the left sidebar.")
                st.stop()

            payload = json.dumps({
                "contents": [{"parts": [
                    {"inline_data": {"mime_type": mime_type, "data": b64_image}},
                    {"text": prompt},
                ]}],
                "generationConfig": {"maxOutputTokens": 1500, "temperature": 0.2},
            }).encode("utf-8")

            gemini_url = (
                "https://generativelanguage.googleapis.com/v1beta/models/"
                f"gemini-2.0-flash:generateContent?key={api_key}"
            )
            req = urllib.request.Request(
                gemini_url, data=payload,
                headers={"Content-Type": "application/json"}, method="POST",
            )
            with urllib.request.urlopen(req) as resp:
                raw = json.loads(resp.read().decode("utf-8"))

            full_text = raw["candidates"][0]["content"]["parts"][0]["text"]
            clean     = re.sub(r"```(?:json)?", "", full_text).strip().rstrip("`").strip()
            result    = json.loads(clean)
            st.session_state.wound_analysis = result
            loading_placeholder.empty()

        except Exception as e:
            loading_placeholder.empty()
            st.error(f"Analysis failed: {e}")
            st.session_state.wound_analysis = None

    # ── Display Results ───────────────────────────────────────────
    if st.session_state.wound_analysis:
        r = st.session_state.wound_analysis

        st.markdown("""
        <div style='background:#e6f6ef;border:1.5px solid #86efac;border-radius:14px;
                    padding:0.9rem 1.3rem;margin-bottom:1rem;
                    display:flex;align-items:center;gap:12px;'>
          <div style='font-size:1.4rem;'>📋</div>
          <div>
            <div style='font-family:Merriweather Sans,sans-serif;font-weight:800;
                        font-size:1rem;color:#1b8a5a;'>AI Wound Assessment Complete</div>
            <div style='font-size:0.76rem;color:#16a34a;'>Review all findings carefully before taking action.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        sev = r.get("severity_level", "MODERATE")
        sev_color_map = {
            "MILD":     ("#1b8a5a", "#e6f6ef"),
            "MODERATE": ("#b45309", "#fef3c7"),
            "SEVERE":   ("#c0392b", "#fdecea"),
            "CRITICAL": ("#6d3fc0", "#f0ebfb"),
        }
        sev_color, sev_bg = sev_color_map.get(sev, ("#5a7184", "#f4f7fb"))

        if r.get("seek_emergency"):
            st.error("🚨 **EMERGENCY** — This wound requires **IMMEDIATE** emergency medical attention. "
                     "Call emergency services or go to the nearest A&E department NOW.")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Wound Type",     r.get("wound_type", "Unknown"))
        m2.metric("Severity Score", f"{r.get('severity_score', 5)} / 10")
        m3.metric("Infection Risk", r.get("infection_risk", "Unknown"))
        m4.metric("Est. Healing",
                  f"{r.get('healing_time_min_days','?')}–{r.get('healing_time_max_days','?')} days")

        st.divider()
        detail_col, action_col = st.columns([1, 1])

        with detail_col:
            st.markdown('<span class="sec-hdr" style="border-bottom-color:#6d3fc0;">Clinical Details</span>',
                        unsafe_allow_html=True)
            details_rows = [
                ("Severity Level",      r.get("severity_level", "—")),
                ("Severity Score",      f"{r.get('severity_score','—')} / 10"),
                ("Wound Type",          r.get("wound_type", "—")),
                ("Affected Area",       r.get("affected_area", "—")),
                ("Healing Phase",       r.get("healing_phase", "—")),
                ("Infection Risk",      r.get("infection_risk", "—")),
                ("Healing Time (Est.)", f"{r.get('healing_time_min_days','?')}–{r.get('healing_time_max_days','?')} days"),
                ("See Doctor Within",   r.get("seek_doctor_within", "—")),
                ("SmartGel Protocol",   r.get("smartgel_recommendation", "—")),
                ("Recommended Tx",      r.get("recommended_treatment", "—")),
            ]
            df_details = pd.DataFrame(details_rows, columns=["Parameter", "Value"])
            st.dataframe(df_details, use_container_width=True, hide_index=True, height=375)

            signs = r.get("visible_signs", [])
            if signs:
                st.markdown("**🩺 Visible Clinical Signs Detected:**")
                for s in signs:
                    st.markdown(
                        f"<div style='background:#f4f8fc;border-left:3px solid #1d6fa4;"
                        f"padding:6px 11px;border-radius:0 8px 8px 0;font-size:0.83rem;"
                        f"margin-bottom:4px;color:#1a2b3c;'>• {s}</div>",
                        unsafe_allow_html=True,
                    )

        with action_col:
            st.markdown('<span class="sec-hdr" style="border-bottom-color:#b45309;">Immediate Actions</span>',
                        unsafe_allow_html=True)
            for i, step in enumerate(r.get("immediate_actions", []), 1):
                st.markdown(
                    f"<div class='action-item' style='background:#fef3c7;border:1px solid #fde68a;'>"
                    f"<span class='action-num' style='color:#b45309;'>{i}.</span>"
                    f"<span style='color:#1a2b3c;'>{step}</span></div>",
                    unsafe_allow_html=True,
                )

            st.divider()
            st.markdown('<span class="sec-hdr" style="border-bottom-color:#1b8a5a;">Daily Care</span>',
                        unsafe_allow_html=True)
            for i, step in enumerate(r.get("care_instructions", []), 1):
                st.markdown(
                    f"<div class='action-item' style='background:#e6f6ef;border:1px solid #a7dfbe;'>"
                    f"<span class='action-num' style='color:#1b8a5a;'>{i}.</span>"
                    f"<span style='color:#1a2b3c;'>{step}</span></div>",
                    unsafe_allow_html=True,
                )

            st.divider()
            st.markdown('<span class="sec-hdr" style="border-bottom-color:#c0392b;">Warning Signs</span>',
                        unsafe_allow_html=True)
            for sign in r.get("warning_signs", []):
                st.markdown(
                    f"<div class='action-item' style='background:#fdecea;border:1px solid #fca5a5;'>"
                    f"<span style='color:#c0392b;flex-shrink:0;'>🔴</span>"
                    f"<span style='color:#1a2b3c;'>{sign}</span></div>",
                    unsafe_allow_html=True,
                )

        st.divider()

        gauge_col, note_col = st.columns([2, 1])
        with gauge_col:
            score_val = r.get("severity_score", 5)
            fig_sev = go.Figure(go.Indicator(
                mode="gauge+number", value=score_val,
                number={"font": {"size": 52, "color": sev_color}, "suffix": "/10"},
                gauge={
                    "axis": {"range": [0, 10], "tickwidth": 1, "tickcolor": "#5a7184",
                             "tickfont": {"size": 11}, "nticks": 11},
                    "bar":  {"color": sev_color, "thickness": 0.28},
                    "bgcolor": "#f4f8fc", "borderwidth": 1, "bordercolor": "#dce6f0",
                    "steps": [
                        {"range": [0, 3.5],  "color": "#dcfce7"},
                        {"range": [3.5, 6.0], "color": "#fef9c3"},
                        {"range": [6.0, 8.5], "color": "#fee2e2"},
                        {"range": [8.5, 10],  "color": "#f0ebfb"},
                    ],
                },
                title={
                    "text": "Wound Severity Score<br>"
                            "<span style='font-size:12px;color:#5a7184'>"
                            "1–3 Mild · 4–6 Moderate · 7–8 Severe · 9–10 Critical</span>",
                    "font": {"size": 14, "color": "#1a2b3c"},
                },
            ))
            fig_sev.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", height=290,
                margin=dict(l=20, r=20, t=60, b=10),
            )
            st.plotly_chart(fig_sev, use_container_width=True, config={"displayModeBar": False})

        with note_col:
            st.markdown("**📝 Confidence Note**")
            st.info(r.get("confidence_note", "No note available."))
            heal_min = r.get("healing_time_min_days", 0)
            heal_max = r.get("healing_time_max_days", 0)
            st.markdown("**⏱ Healing Timeline**")
            st.success(
                f"**{heal_min} – {heal_max} days** estimated\n\n"
                f"Phase: {r.get('healing_phase', 'Unknown')}"
            )
            progress_pct = min(int((heal_min / max(heal_max, 1)) * 100), 100)
            st.markdown(
                f"<div style='background:#dce6f0;border-radius:50px;height:7px;overflow:hidden;margin-top:8px;'>"
                f"<div class='healing-bar' style='height:100%;width:{progress_pct}%;'></div></div>"
                f"<div style='font-size:0.68rem;color:#8fa5b8;margin-top:3px;text-align:right;'>"
                f"Healing progress estimate</div>",
                unsafe_allow_html=True,
            )

        st.divider()

        # Export
        export_rows = [
            ("Wound Type",          r.get("wound_type", "")),
            ("Severity Level",      r.get("severity_level", "")),
            ("Severity Score",      str(r.get("severity_score", ""))),
            ("Affected Area",       r.get("affected_area", "")),
            ("Infection Risk",      r.get("infection_risk", "")),
            ("Healing Time (days)", f"{r.get('healing_time_min_days','')}–{r.get('healing_time_max_days','')}"),
            ("Healing Phase",       r.get("healing_phase", "")),
            ("See Doctor Within",   r.get("seek_doctor_within", "")),
            ("Recommended Tx",      r.get("recommended_treatment", "")),
            ("SmartGel Protocol",   r.get("smartgel_recommendation", "")),
            ("Seek Emergency",      str(r.get("seek_emergency", False))),
            ("Visible Signs",       "; ".join(r.get("visible_signs", []))),
            ("Immediate Actions",   "; ".join(r.get("immediate_actions", []))),
            ("Care Instructions",   "; ".join(r.get("care_instructions", []))),
            ("Warning Signs",       "; ".join(r.get("warning_signs", []))),
            ("Confidence Note",     r.get("confidence_note", "")),
            ("Wound Age",           wound_age),
            ("Image Source",        "Camera" if st.session_state.image_source == "camera" else "Upload"),
            ("Analysis Time",       datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]
        df_export_report = pd.DataFrame(export_rows, columns=["Parameter", "Value"])

        exp1, exp2 = st.columns(2)
        with exp1:
            st.download_button(
                "📥 Download AI Wound Analysis Report (CSV)",
                df_export_report.to_csv(index=False),
                "smartgel_wound_analysis.csv", "text/csv",
                type="primary", use_container_width=True,
                key="dl_analysis",
            )
        with exp2:
            if st.button("🔄 Clear Analysis & Upload New Image", use_container_width=True, key="clear_analysis"):
                st.session_state.wound_analysis = None
                st.session_state.camera_image   = None
                st.rerun()
