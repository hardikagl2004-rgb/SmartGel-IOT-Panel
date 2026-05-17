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
    page_icon="https://img.icons8.com/fluency/48/dna-helix.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# GLOBAL CSS — Professional animations + polished UI
# ------------------------------------------------------------------
st.markdown("""
<style>
  /* ── Google Fonts ── */
  @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

  /* ── Root variables ── */
  :root {
    --accent:      #0ea5e9;
    --accent-dark: #0369a1;
    --success:     #10b981;
    --warning:     #f59e0b;
    --danger:      #ef4444;
    --surface:     #f8fafc;
    --border:      #e2e8f0;
    --text:        #0f172a;
    --muted:       #64748b;
    --radius:      12px;
    --radius-lg:   20px;
  }

  /* ── Base ── */
  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text);
  }

  /* ── Fade-in animation ── */
  @keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0);    }
  }
  @keyframes pulseRing {
    0%   { box-shadow: 0 0 0 0   rgba(14,165,233,0.4); }
    70%  { box-shadow: 0 0 0 14px rgba(14,165,233,0);   }
    100% { box-shadow: 0 0 0 0   rgba(14,165,233,0);    }
  }
  @keyframes shimmer {
    0%   { background-position: -400px 0; }
    100% { background-position:  400px 0; }
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  @keyframes gradientShift {
    0%   { background-position: 0%   50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0%   50%; }
  }

  /* ── Main content fade-in ── */
  .main .block-container {
    animation: fadeSlideUp 0.5s ease both;
    padding-top: 1.5rem !important;
  }

  /* ── Metric cards ── */
  [data-testid="metric-container"] {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: box-shadow 0.2s, transform 0.2s;
    animation: fadeSlideUp 0.4s ease both;
  }
  [data-testid="metric-container"]:hover {
    box-shadow: 0 6px 20px rgba(14,165,233,0.12);
    transform: translateY(-2px);
  }
  [data-testid="metric-container"] label {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
  }
  [data-testid="metric-container"] [data-testid="metric-value"] {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: var(--text) !important;
  }

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {
    background: #f1f5f9;
    border-radius: 50px;
    padding: 4px;
    gap: 2px;
  }
  .stTabs [data-baseweb="tab"] {
    border-radius: 50px !important;
    font-size: 0.83rem !important;
    font-weight: 600 !important;
    color: var(--muted) !important;
    transition: all 0.2s !important;
    padding: 0.45rem 1.1rem !important;
  }
  .stTabs [aria-selected="true"] {
    background: #ffffff !important;
    color: var(--accent-dark) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
  }

  /* ── Buttons ── */
  .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-dark) 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 50px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.55rem 1.6rem !important;
    transition: all 0.25s !important;
    box-shadow: 0 4px 14px rgba(14,165,233,0.35) !important;
    animation: pulseRing 2.5s infinite;
  }
  .stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(14,165,233,0.45) !important;
  }
  .stButton > button:not([kind="primary"]) {
    border-radius: 50px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    transition: all 0.2s !important;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f172a 0%, #1e293b 100%) !important;
    border-right: 1px solid #334155;
  }
  [data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
  }
  [data-testid="stSidebar"] h1,
  [data-testid="stSidebar"] h2,
  [data-testid="stSidebar"] h3 {
    color: #f8fafc !important;
  }
  [data-testid="stSidebar"] .stRadio label {
    color: #94a3b8 !important;
    font-size: 0.84rem !important;
  }
  [data-testid="stSidebar"] [data-baseweb="radio"] input:checked + div {
    background: var(--accent) !important;
  }

  /* ── Upload zone enhancement ── */
  [data-testid="stFileUploader"] {
    border-radius: var(--radius-lg) !important;
    border: 2px dashed var(--accent) !important;
    background: linear-gradient(135deg, #eff6ff 0%, #f0f9ff 100%) !important;
    transition: all 0.3s !important;
  }
  [data-testid="stFileUploader"]:hover {
    border-color: var(--accent-dark) !important;
    background: #e0f2fe !important;
  }

  /* ── Camera card ── */
  .camera-card {
    border-radius: var(--radius-lg);
    border: 2px dashed #6366f1;
    background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s;
    animation: fadeSlideUp 0.5s ease both;
  }
  .camera-card:hover {
    border-color: #4338ca;
    box-shadow: 0 6px 20px rgba(99,102,241,0.15);
  }

  /* ── Input mode selector ── */
  .input-mode-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1.4rem;
    border-radius: 50px;
    font-weight: 600;
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.25s;
    border: 2px solid transparent;
    user-select: none;
  }
  .input-mode-btn.active-upload {
    background: #eff6ff;
    border-color: var(--accent);
    color: var(--accent-dark);
  }
  .input-mode-btn.active-camera {
    background: #f5f3ff;
    border-color: #6366f1;
    color: #4338ca;
  }

  /* ── Result cards ── */
  .result-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.4rem 1.6rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
    animation: fadeSlideUp 0.4s ease both;
  }
  .result-card h4 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.4rem;
  }

  /* ── Severity badge ── */
  .severity-badge {
    display: inline-block;
    padding: 0.25rem 0.9rem;
    border-radius: 50px;
    font-weight: 700;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  /* ── Shimmer skeleton ── */
  .shimmer {
    background: linear-gradient(90deg, #f0f4f8 25%, #e2e8f0 50%, #f0f4f8 75%);
    background-size: 400px 100%;
    animation: shimmer 1.4s infinite;
    border-radius: 8px;
    height: 18px;
    margin-bottom: 10px;
  }

  /* ── Section headers ── */
  .section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text);
    padding-bottom: 0.4rem;
    border-bottom: 2px solid var(--accent);
    margin-bottom: 1rem;
    display: inline-block;
  }

  /* ── Alert overrides ── */
  [data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border-left-width: 4px !important;
    font-size: 0.88rem !important;
  }

  /* ── Dataframe ── */
  [data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important;
  }

  /* ── Spinner override ── */
  .stSpinner > div {
    border-top-color: var(--accent) !important;
  }

  /* ── Smooth divider ── */
  hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.4rem 0 !important;
  }

  /* ── Progress bar for healing timeline ── */
  .healing-bar {
    height: 8px;
    border-radius: 50px;
    background: linear-gradient(90deg, #10b981, #f59e0b, #ef4444);
    background-size: 200% 100%;
    animation: gradientShift 3s ease infinite;
  }

  /* ── Sidebar nav cards ── */
  .nav-card {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 12px;
    border-radius: 12px;
    margin-bottom: 5px;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 1.5px solid transparent;
  }
  .nav-card:hover {
    background: rgba(255,255,255,0.08) !important;
    border-color: rgba(255,255,255,0.15) !important;
    transform: translateX(3px);
  }
  .nav-card.active {
    border-color: rgba(255,255,255,0.25) !important;
    background: rgba(255,255,255,0.12) !important;
  }
  .nav-card .nav-icon {
    font-size: 1.15rem;
    flex-shrink: 0;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
    background: rgba(255,255,255,0.1);
  }
  .nav-card .nav-label {
    font-size: 0.83rem;
    font-weight: 600;
    color: #f1f5f9;
    line-height: 1.2;
  }
  .nav-card .nav-desc {
    font-size: 0.68rem;
    color: #64748b;
    line-height: 1.2;
  }
  .nav-active-pill {
    margin-left: auto;
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #0ea5e9;
    flex-shrink: 0;
    animation: pulseRing 1.8s infinite;
  }

  /* ── Live dot pulse ── */
  .live-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: #10b981;
    margin-right: 6px;
    animation: pulseRing 1.5s infinite;
    vertical-align: middle;
  }

  /* Step indicator */
  .step-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 26px; height: 26px;
    border-radius: 50%;
    background: var(--accent);
    color: #fff;
    font-weight: 700;
    font-size: 0.75rem;
    margin-right: 8px;
    flex-shrink: 0;
  }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SCENARIO DATA
# ------------------------------------------------------------------
SCENARIOS = {
    "Acne / Severe Pimple Spot": {
        "ph_readings":    [5.2, 5.5, 5.2, 5.3, 5.4, 5.5, 5.3, 5.2, 5.4, 5.5],
        "gel_color":      "#d946a8",
        "line_color":     "#d946a8",
        "fill_color":     "rgba(217,70,168,0.08)",
        "status":         "NORMAL",
        "status_detail":  "Stable | pH ~5.5 | Acidic Shield Active",
        "alert_type":     "success",
        "alert_msg":      "Wound healing perfectly under stable acidic conditions. No intervention required.",
        "temp_range":     (36.4, 37.1),
        "moisture_range": (60, 72),
        "bacterial_load": "LOW",
        "bl_delta":       "normal",
        "treatment":      "Salicylic Acid Hydrogel 2%",
        "healing_stage":  "Inflammatory to Proliferative",
        "reapply_hours":  3.5,
        "radar_scores":   [90, 88, 75, 92, 85, 95],
        "bar_color":      "#0891b2",
    },
    "Chronic Diabetic Foot Ulcer": {
        "ph_readings":    [5.5, 6.0, 6.8, 7.4, 7.8, 8.0, 8.2, 8.4, 8.5, 8.5],
        "gel_color":      "#dc2626",
        "line_color":     "#dc2626",
        "fill_color":     "rgba(220,38,38,0.08)",
        "status":         "CRITICAL",
        "status_detail":  "CRITICAL ALKALINITY | pH ~8.5 | Necrosis Risk",
        "alert_type":     "error",
        "alert_msg":      "CRITICAL ALERT: High bacterial load and tissue necrosis detected in diabetic ulcer. Immediate clinical evaluation recommended!",
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
        "fill_color":     "rgba(234,88,12,0.08)",
        "status":         "DANGER",
        "status_detail":  "DANGER | pH ~8.8 | Animal Saliva Contaminants Active",
        "alert_type":     "error",
        "alert_msg":      "DANGER: Animal bacterial contaminants active. Saliva penetration confirmed. High Rabies and Pasteurella risk. Seek Post-Exposure Prophylaxis IMMEDIATELY!",
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

DAYS         = ["Day " + str(i + 1) for i in range(10)]
SCENARIO_KEYS = list(SCENARIOS.keys())
CHART_COLORS  = ["#d946a8", "#dc2626", "#ea580c"]

# ------------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------------
if "selected"       not in st.session_state: st.session_state.selected       = SCENARIO_KEYS[0]
if "sim_running"    not in st.session_state: st.session_state.sim_running    = False
if "log"            not in st.session_state: st.session_state.log            = []
if "wound_analysis" not in st.session_state: st.session_state.wound_analysis = None
if "sidebar_api_key" not in st.session_state: st.session_state["sidebar_api_key"] = ""
if "image_source"   not in st.session_state: st.session_state.image_source  = "upload"
if "camera_image"   not in st.session_state: st.session_state.camera_image  = None
if "active_tab"     not in st.session_state: st.session_state.active_tab    = 0

TAB_DEFS = [
    {"icon": "📊", "label": "Dashboard",          "desc": "Live vitals & trends",       "color": "#0ea5e9", "bg": "#eff6ff"},
    {"icon": "📈", "label": "pH Trend Analysis",  "desc": "Bar chart, gauge & compare", "color": "#8b5cf6", "bg": "#f5f3ff"},
    {"icon": "🗂️", "label": "Sensor Log",         "desc": "Event log & CSV export",     "color": "#10b981", "bg": "#f0fdf4"},
    {"icon": "📋", "label": "Clinical Report",    "desc": "Summary & radar chart",      "color": "#f59e0b", "bg": "#fffbeb"},
    {"icon": "🩹", "label": "Wound Image Analysis","desc": "AI-powered image review",   "color": "#ef4444", "bg": "#fef2f2"},
]

# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1rem 0 0.5rem'>
      <div style='font-family:Space Grotesk,sans-serif;font-size:1.25rem;font-weight:700;
                  color:#f8fafc;letter-spacing:-0.02em;'>SmartGel IoT</div>
      <div style='font-size:0.72rem;color:#64748b;font-weight:500;letter-spacing:0.1em;
                  text-transform:uppercase;margin-top:2px;'>Healthcare Portal</div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Biocompatible Nanosensor Monitoring")
    st.divider()

    # ── Navigation ──────────────────────────────────────────────────
    st.markdown("""
    <div style='font-family:Space Grotesk,sans-serif;font-size:0.7rem;font-weight:700;
                color:#475569;text-transform:uppercase;letter-spacing:0.1em;
                margin-bottom:8px;'>Navigation</div>
    """, unsafe_allow_html=True)

    for idx, tab_def in enumerate(TAB_DEFS):
        is_active = st.session_state.active_tab == idx
        active_cls = "active" if is_active else ""
        dot_html = "<span class='nav-active-pill'></span>" if is_active else ""
        border_style = "border-color:rgba(255,255,255,0.28)!important;background:rgba(255,255,255,0.1)!important;" if is_active else ""
        st.markdown(f"""
        <div class='nav-card {active_cls}' style='{border_style}'>
          <div class='nav-icon'>{tab_def['icon']}</div>
          <div>
            <div class='nav-label'>{tab_def['label']}</div>
            <div class='nav-desc'>{tab_def['desc']}</div>
          </div>
          {dot_html}
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "Go →" if not is_active else "● Active",
            key=f"nav_btn_{idx}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.active_tab = idx
            st.rerun()

    st.divider()
    st.subheader("Clinical Scenario")
    selected = st.radio(
        "Select a scenario:",
        SCENARIO_KEYS,
        index=SCENARIO_KEYS.index(st.session_state.selected),
    )
    st.session_state.selected = selected
    sc_side = SCENARIOS[selected]

    st.divider()
    st.subheader("Simulation Controls")
    sim_interval = st.slider("Update interval (sec)", 1, 10, 3)
    noise_level  = st.slider("Sensor noise level",   0.0, 0.5, 0.05, 0.01)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶ Start", use_container_width=True, type="primary"):
            st.session_state.sim_running = True
    with col_b:
        if st.button("■ Stop", use_container_width=True):
            st.session_state.sim_running = False

    if st.button("Clear Log", use_container_width=True):
        st.session_state.log = []
        st.success("Log cleared.")

    st.divider()
    st.subheader("Reapplication Reminder")
    st.warning(
        "Reapply in **" + str(sc_side["reapply_hours"]) + " hours**\n\n"
        "Treatment: " + sc_side["treatment"]
    )
    st.divider()
    st.subheader("🔑 AI Analysis Key")
    st.caption("Paste your Google API key to enable wound analysis.")
    st.text_input(
        "Google API Key",
        type="password",
        placeholder="AIza...",
        key="sidebar_api_key",
        help="Get your key from console.cloud.google.com → APIs & Services → Credentials",
    )
    if st.session_state["sidebar_api_key"]:
        st.success("✅ Key entered — ready to analyse!")
    st.divider()
    st.caption("SmartGel IoT Healthcare Portal v4.0")
    st.caption("© 2025 SmartGel Medical Systems")

# ------------------------------------------------------------------
# ACTIVE SCENARIO
# ------------------------------------------------------------------
sc    = SCENARIOS[st.session_state.selected]
noise = noise_level

# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
st.markdown("""
<div style='display:flex;align-items:center;gap:12px;margin-bottom:4px;'>
  <div style='font-family:Space Grotesk,sans-serif;font-size:1.9rem;font-weight:700;
              letter-spacing:-0.03em;color:#0f172a;'>SmartGel IoT Healthcare Portal</div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "<span class='live-dot'></span>"
    "<span style='font-size:0.78rem;color:#64748b;font-weight:500;'>"
    "LIVE &nbsp;|&nbsp; BLE Uplink Active &nbsp;|&nbsp; Biocompatible Nanosensor Monitoring &nbsp;|&nbsp; "
    + datetime.now().strftime("%Y-%m-%d  %H:%M:%S") + "</span>",
    unsafe_allow_html=True,
)
st.divider()

if sc["alert_type"] == "success":
    st.success("**STATUS " + sc["status"] + "** — " + sc["alert_msg"])
else:
    st.error("**STATUS " + sc["status"] + "** — " + sc["alert_msg"])

st.divider()

# ------------------------------------------------------------------
# QUICK-JUMP NAV BAR
# ------------------------------------------------------------------
st.markdown("""
<div style='font-family:Space Grotesk,sans-serif;font-size:0.72rem;font-weight:700;
            color:#94a3b8;text-transform:uppercase;letter-spacing:0.1em;
            margin-bottom:10px;'>Quick Navigation</div>
""", unsafe_allow_html=True)

qn_cols = st.columns(5)
for _i, (_tab_def, _col) in enumerate(zip(TAB_DEFS, qn_cols)):
    with _col:
        _is_active = st.session_state.active_tab == _i
        _bg   = _tab_def["color"] if _is_active else "#f1f5f9"
        _fg   = "#ffffff"         if _is_active else "#475569"
        _bord = _tab_def["color"] if _is_active else "#e2e8f0"
        st.markdown(f"""
        <div style='background:{_bg};border:2px solid {_bord};border-radius:14px;
                    padding:10px 8px;text-align:center;
                    box-shadow:{"0 4px 14px "+_tab_def["color"]+"44" if _is_active else "none"};
                    transition:all 0.2s;'>
          <div style='font-size:1.3rem;margin-bottom:3px;'>{_tab_def["icon"]}</div>
          <div style='font-size:0.72rem;font-weight:700;color:{_fg};line-height:1.3;'>
            {_tab_def["label"]}
          </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(
            "Open" if not _is_active else "✓ Here",
            key=f"qnav_{_i}",
            use_container_width=True,
            type="primary" if _is_active else "secondary",
        ):
            st.session_state.active_tab = _i
            st.rerun()

st.divider()

# ------------------------------------------------------------------
# TABS
# ------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  📊 Dashboard  ",
    "  📈 pH Trend Analysis  ",
    "  🗂️ Sensor Log  ",
    "  📋 Clinical Report  ",
    "  🩹 Wound Image Analysis  ",
])

# Inject JS to click the correct tab on load when active_tab changes
_tab_labels = ["  📊 Dashboard  ", "  📈 pH Trend Analysis  ", "  🗂️ Sensor Log  ",
                "  📋 Clinical Report  ", "  🩹 Wound Image Analysis  "]
_active = st.session_state.active_tab
st.markdown(f"""
<script>
(function() {{
  const idx = {_active};
  function clickTab() {{
    const buttons = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
    if (buttons.length > idx) {{
      buttons[idx].click();
    }} else {{
      setTimeout(clickTab, 120);
    }}
  }}
  setTimeout(clickTab, 80);
}})();
</script>
""", unsafe_allow_html=True)

# ==================================================================
# TAB 1 — DASHBOARD  (unchanged logic, slightly polished labels)
# ==================================================================
with tab1:
    cur_ph   = round(sc["ph_readings"][-1] + random.uniform(-noise, noise), 2)
    cur_temp = round(random.uniform(*sc["temp_range"]), 1)
    cur_mois = round(random.uniform(*sc["moisture_range"]), 1)

    k1, k2, k3, k4 = st.columns(4)
    ph_delta_color = "inverse" if cur_ph > 7.0 else "normal"
    k1.metric("Current pH",       str(cur_ph),         str(round(cur_ph - 7.0, 2)) + " vs neutral", delta_color=ph_delta_color)
    k2.metric("Wound Temp (°C)",  str(cur_temp) + " °C", str(round(cur_temp - 37.0, 1)) + " vs normal", delta_color="inverse")
    k3.metric("Moisture Level",   str(cur_mois) + " %", str(round(cur_mois - 75.0, 1)) + " vs target", delta_color="inverse")
    k4.metric("Bacterial Load",   sc["bacterial_load"])

    st.divider()
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.markdown('<span class="section-header">Hydrogel Physical Status</span>', unsafe_allow_html=True)
        gc    = sc["gel_color"]
        r_val = int(gc[1:3], 16); g_val = int(gc[3:5], 16); b_val = int(gc[5:7], 16)
        fig_orb = go.Figure()
        fig_orb.add_shape(type="circle", x0=0.25, y0=0.55, x1=0.75, y1=0.95,
                          xref="paper", yref="paper", fillcolor=gc,
                          line_color="rgba("+str(r_val)+","+str(g_val)+","+str(b_val)+",0.4)", line_width=6)
        fig_orb.add_annotation(x=0.5, y=0.75, xref="paper", yref="paper",
                                text="<b>pH " + str(cur_ph) + "</b>", showarrow=False,
                                font=dict(size=22, color="#ffffff"))
        fig_orb.add_annotation(x=0.5, y=0.35, xref="paper", yref="paper",
                                text="<b>STATUS: " + sc["status"] + "</b>", showarrow=False,
                                font=dict(size=14, color=gc))
        fig_orb.add_annotation(x=0.5, y=0.18, xref="paper", yref="paper",
                                text=sc["status_detail"], showarrow=False,
                                font=dict(size=10, color="#475569"))
        fig_orb.update_layout(paper_bgcolor="#dbeafe", plot_bgcolor="#dbeafe", height=220,
                               margin=dict(l=10,r=10,t=10,b=10),
                               xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig_orb, use_container_width=True, config={"displayModeBar": False})
        st.info("**Treatment:** " + sc["treatment"])
        st.info("**Healing Stage:** " + sc["healing_stage"])
        st.info("**Connection:** BLE Active | 2.4 GHz | All Nominal")
        st.info("**Reapply in:** " + str(sc["reapply_hours"]) + " hours")

    with right_col:
        st.markdown('<span class="section-header">pH Telemetry — 10-Day Trend</span>', unsafe_allow_html=True)
        ph_vals = [round(v + random.uniform(-noise, noise), 2) for v in sc["ph_readings"]]
        fig_trend = go.Figure()
        fig_trend.add_hrect(y0=7.0, y1=10.5, fillcolor="rgba(220,38,38,0.07)", line_width=0,
                             annotation_text="Alkaline Danger Zone (pH > 7)", annotation_position="top left",
                             annotation_font_color="#dc2626", annotation_font_size=11)
        fig_trend.add_hrect(y0=4.0, y1=6.0, fillcolor="rgba(22,163,74,0.07)", line_width=0,
                             annotation_text="Healthy Acidic Range (pH < 6)", annotation_position="bottom left",
                             annotation_font_color="#16a34a", annotation_font_size=11)
        fig_trend.add_trace(go.Scatter(
            x=DAYS, y=ph_vals, mode="lines+markers", name="pH Reading",
            line=dict(color=sc["line_color"], width=3, shape="spline"),
            marker=dict(size=10, color=ph_vals,
                        colorscale=[[0.0,"#16a34a"],[0.4,"#0891b2"],[0.7,"#d97706"],[1.0,"#dc2626"]],
                        cmin=5, cmax=9, line=dict(color="#ffffff", width=2), showscale=False),
            fill="tozeroy", fillcolor=sc["fill_color"],
            hovertemplate="<b>%{x}</b><br>pH = %{y:.2f}<extra></extra>",
        ))
        fig_trend.add_hline(y=7.0, line_dash="dash", line_color="#dc2626", line_width=1)
        fig_trend.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#f0f6fb", height=340,
                                 margin=dict(l=10,r=20,t=20,b=10),
                                 xaxis=dict(showgrid=False, tickfont=dict(size=11,color="#475569"), color="#475569"),
                                 yaxis=dict(gridcolor="#cbd5e1", range=[4,10.5], title="pH Value",
                                            color="#475569", tickfont=dict(size=11)),
                                 showlegend=False)
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
        s1, s2, s3 = st.columns(3)
        s1.metric("Min pH (10-day)",  str(min(sc["ph_readings"])))
        s2.metric("Max pH (10-day)",  str(max(sc["ph_readings"])))
        s3.metric("Mean pH (10-day)", str(round(sum(sc["ph_readings"]) / 10, 2)))

# ==================================================================
# TAB 2 — pH TREND ANALYSIS
# ==================================================================
with tab2:
    st.markdown('<span class="section-header">Advanced pH Trend Analysis</span>', unsafe_allow_html=True)
    ph_vals2 = [round(v + random.uniform(-noise_level, noise_level), 2) for v in sc["ph_readings"]]
    col_bar, col_gauge = st.columns(2)

    with col_bar:
        st.markdown("**Daily pH Bar Chart**")
        bar_colors = ["#16a34a" if v < 6.0 else ("#d97706" if v < 7.0 else "#dc2626") for v in ph_vals2]
        fig_bar = go.Figure(go.Bar(x=DAYS, y=ph_vals2, marker_color=bar_colors,
                                   marker_line_color="#ffffff", marker_line_width=2,
                                   text=["pH " + str(v) for v in ph_vals2], textposition="outside",
                                   textfont=dict(size=10, color="#334155")))
        fig_bar.add_hline(y=7.0, line_dash="dash", line_color="#dc2626", line_width=2,
                          annotation_text="pH 7.0 — Danger Threshold",
                          annotation_font_color="#dc2626", annotation_font_size=11)
        fig_bar.add_hline(y=6.0, line_dash="dot", line_color="#d97706", line_width=1,
                          annotation_text="pH 6.0 — Warning",
                          annotation_font_color="#d97706", annotation_font_size=10)
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#f0f6fb", height=360,
                               margin=dict(l=10,r=10,t=20,b=10),
                               xaxis=dict(showgrid=False, color="#475569", tickfont=dict(size=10)),
                               yaxis=dict(gridcolor="#cbd5e1", range=[4,11.5], color="#475569"),
                               showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

    with col_gauge:
        st.markdown("**Live pH Gauge**")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=ph_vals2[-1],
            delta={"reference": 7.0, "valueformat": ".2f",
                   "increasing": {"color": "#dc2626"}, "decreasing": {"color": "#16a34a"}},
            number={"font": {"color": "#0f172a", "size": 56}, "valueformat": ".2f"},
            gauge={"axis": {"range": [4, 10], "tickwidth": 1, "tickcolor": "#64748b",
                            "tickfont": {"color": "#64748b", "size": 11}, "nticks": 7},
                   "bar": {"color": sc["gel_color"], "thickness": 0.3},
                   "bgcolor": "#f0f6fb", "borderwidth": 1, "bordercolor": "#cbd5e1",
                   "steps": [{"range": [4.0,6.0],"color":"#dcfce7"},
                              {"range": [6.0,7.0],"color":"#fef9c3"},
                              {"range": [7.0,10.0],"color":"#fee2e2"}],
                   "threshold": {"line": {"color": "#dc2626","width": 4},
                                 "thickness": 0.8, "value": 7.4}},
            title={"text": "Current pH Reading<br><span style='font-size:12px;color:#64748b'>"
                           "Green = Healthy | Yellow = Warning | Red = Danger</span>",
                   "font": {"color": "#334155","size": 14}},
        ))
        fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=360,
                                 margin=dict(l=20,r=20,t=50,b=20))
        st.plotly_chart(fig_gauge, use_container_width=True, config={"displayModeBar": False})

    st.divider()
    st.markdown('<span class="section-header">All-Scenario Comparison</span>', unsafe_allow_html=True)
    fig_comp = go.Figure()
    for i, (sname, sval) in enumerate(SCENARIOS.items()):
        fig_comp.add_trace(go.Scatter(x=DAYS, y=sval["ph_readings"], mode="lines+markers",
                                      name=sname, line=dict(width=2.5, shape="spline", color=CHART_COLORS[i]),
                                      marker=dict(size=8, color=CHART_COLORS[i],
                                                  line=dict(color="#ffffff", width=1)),
                                      hovertemplate="<b>" + sname + "</b><br>%{x}: pH %{y}<extra></extra>"))
    fig_comp.add_hline(y=7.0, line_dash="dot", line_color="#94a3b8", line_width=2,
                       annotation_text="Neutral pH 7.0", annotation_font_color="#64748b",
                       annotation_font_size=11)
    fig_comp.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#f0f6fb", height=320,
                            margin=dict(l=10,r=10,t=10,b=10),
                            xaxis=dict(showgrid=False, color="#475569", tickfont=dict(size=10)),
                            yaxis=dict(gridcolor="#cbd5e1", range=[4,10], title="pH Value", color="#475569"),
                            legend=dict(bgcolor="rgba(255,255,255,0.95)", bordercolor="#cbd5e1",
                                        borderwidth=1, font=dict(size=12, color="#334155")))
    st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})

# ==================================================================
# TAB 3 — SENSOR LOG
# ==================================================================
with tab3:
    st.markdown('<span class="section-header">Live Sensor Event Log</span>', unsafe_allow_html=True)
    btn1, btn2, btn3 = st.columns([1, 1, 2])

    with btn1:
        if st.button("➕ Add Reading", use_container_width=True, type="primary"):
            ph_new   = round(sc["ph_readings"][-1] + random.uniform(-0.35, 0.35), 2)
            temp_new = round(random.uniform(*sc["temp_range"]), 1)
            mois_new = round(random.uniform(*sc["moisture_range"]), 1)
            status_new = "CRITICAL" if ph_new > 7.0 else "OK"
            st.session_state.log.append({
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Scenario":  st.session_state.selected[:32],
                "pH": ph_new, "Temp (°C)": temp_new, "Moisture (%)": mois_new,
                "Status": status_new,
            })
            st.success("Reading logged — pH " + str(ph_new) + " | Status: " + status_new)

    with btn2:
        if st.session_state.log:
            df_export = pd.DataFrame(st.session_state.log)
            st.download_button("⬇ Export CSV", df_export.to_csv(index=False),
                               "smartgel_sensor_log.csv", "text/csv", use_container_width=True)

    st.divider()
    if st.session_state.log:
        df_log = pd.DataFrame(st.session_state.log)
        total = len(df_log); ok_cnt = len(df_log[df_log["Status"] == "OK"]); crit_cnt = total - ok_cnt
        lm1, lm2, lm3 = st.columns(3)
        lm1.metric("Total Readings", total)
        lm2.metric("OK Readings", ok_cnt)
        lm3.metric("Critical Readings", crit_cnt,
                   delta=str(crit_cnt) + " need attention",
                   delta_color="inverse" if crit_cnt > 0 else "normal")
        st.divider()
        st.dataframe(df_log, use_container_width=True, height=420)
        if len(df_log) > 1:
            st.markdown("**pH Over Time (from log)**")
            fig_log = go.Figure(go.Scatter(x=df_log["Timestamp"], y=df_log["pH"],
                                           mode="lines+markers", line=dict(color="#0891b2", width=2),
                                           marker=dict(size=8, color=df_log["pH"],
                                                       colorscale=[[0,"#16a34a"],[0.5,"#d97706"],[1,"#dc2626"]],
                                                       cmin=5, cmax=9, line=dict(color="#ffffff",width=1),
                                                       showscale=True, colorbar=dict(title="pH",thickness=12)),
                                           hovertemplate="<b>%{x}</b><br>pH = %{y:.2f}<extra></extra>"))
            fig_log.add_hline(y=7.0, line_dash="dash", line_color="#dc2626",
                              annotation_text="Danger Threshold", annotation_font_color="#dc2626")
            fig_log.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#f0f6fb", height=280,
                                   margin=dict(l=10,r=10,t=10,b=10),
                                   xaxis=dict(showgrid=False, color="#475569", tickfont=dict(size=9)),
                                   yaxis=dict(gridcolor="#cbd5e1", range=[4,10], title="pH", color="#475569"),
                                   showlegend=False)
            st.plotly_chart(fig_log, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No readings logged yet. Click 'Add Reading' above or start the live simulation.")

    if st.session_state.sim_running:
        with st.spinner("Live simulation active — auto-logging readings..."):
            time.sleep(sim_interval)
        ph_sim   = round(sc["ph_readings"][-1] + random.uniform(-0.35, 0.35), 2)
        temp_sim = round(random.uniform(*sc["temp_range"]), 1)
        mois_sim = round(random.uniform(*sc["moisture_range"]), 1)
        st.session_state.log.append({
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Scenario":  st.session_state.selected[:32],
            "pH": ph_sim, "Temp (°C)": temp_sim, "Moisture (%)": mois_sim,
            "Status": "CRITICAL" if ph_sim > 7.0 else "OK",
        })
        st.rerun()

# ==================================================================
# TAB 4 — CLINICAL REPORT
# ==================================================================
with tab4:
    st.markdown('<span class="section-header">Auto-Generated Clinical Summary</span>', unsafe_allow_html=True)

    ph_mean_val = round(sum(sc["ph_readings"]) / 10, 2)
    ph_max_val  = max(sc["ph_readings"])
    ph_min_val  = min(sc["ph_readings"])
    ph_trend    = ("Alkaline Drift Detected (worsening)"
                   if sc["ph_readings"][-1] > sc["ph_readings"][0]
                   else "Stable or Improving")
    recommendation = (
        "Continue current protocol. Wound environment is stable. Healing progresses normally. Weekly monitoring recommended."
        if sc["bacterial_load"] == "LOW"
        else "IMMEDIATE clinical evaluation required. Alkaline pH shift confirms active bacterial colonisation. Consider systemic antibiotics and advanced wound debridement. Do not delay treatment."
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
            ("Reapplication Every", str(sc["reapply_hours"]) + " hours"),
            ("Sensor Connection",   "BLE Active — All sensors nominal"),
            ("Report Generated",    datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]
        df_report = pd.DataFrame(rows, columns=["Parameter", "Value"])
        st.dataframe(df_report, use_container_width=True, hide_index=True, height=410)
        st.divider()
        if sc["bacterial_load"] == "LOW":
            st.success("**RECOMMENDATION:** " + recommendation)
        else:
            st.error("**RECOMMENDATION:** " + recommendation)
        st.divider()
        st.download_button("⬇ Download Clinical Report (CSV)", df_report.to_csv(index=False),
                           "smartgel_clinical_report.csv", "text/csv", type="primary",
                           use_container_width=True)

    with radar_col:
        st.markdown("**Wound Health Radar**")
        categories = ["pH Safety","Temperature","Moisture Control","Bacterial Defence","Healing Rate","Gel Integrity"]
        scores = sc["radar_scores"]
        gc2 = sc["gel_color"]
        r2=int(gc2[1:3],16); g2=int(gc2[3:5],16); b2=int(gc2[5:7],16)
        fill2 = "rgba("+str(r2)+","+str(g2)+","+str(b2)+",0.22)"
        fig_radar = go.Figure(go.Scatterpolar(
            r=scores+[scores[0]], theta=categories+[categories[0]],
            fill="toself", fillcolor=fill2,
            line=dict(color=gc2,width=2.5),
            marker=dict(size=9,color=gc2,line=dict(color="#ffffff",width=1)),
        ))
        fig_radar.update_layout(
            polar=dict(bgcolor="#f0f6fb",
                       radialaxis=dict(visible=True,range=[0,100],gridcolor="#cbd5e1",
                                       tickfont=dict(size=9,color="#64748b"),
                                       tickvals=[0,25,50,75,100]),
                       angularaxis=dict(gridcolor="#cbd5e1",
                                        tickfont=dict(size=11,color="#334155"))),
            paper_bgcolor="rgba(0,0,0,0)", height=430, margin=dict(l=50,r=50,t=30,b=30),
            showlegend=False)
        st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})
        radar_df = pd.DataFrame({
            "Category":    categories,
            "Score / 100": scores,
            "Rating":      ["Excellent" if s>=80 else ("Good" if s>=60 else ("Fair" if s>=40 else "Poor"))
                            for s in scores],
        })
        st.dataframe(radar_df, use_container_width=True, hide_index=True, height=245)

# ==================================================================
# TAB 5 — WOUND IMAGE ANALYSIS  ← ENHANCED
# ==================================================================
with tab5:
    # ── Header ──────────────────────────────────────────────────────
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 100%);
                border-radius:20px;padding:1.8rem 2rem;margin-bottom:1.2rem;'>
      <div style='font-family:Space Grotesk,sans-serif;font-size:1.4rem;font-weight:700;
                  color:#f8fafc;letter-spacing:-0.02em;margin-bottom:4px;'>
        🩹 AI-Powered Wound Image Analysis
      </div>
      <div style='font-size:0.85rem;color:#94a3b8;line-height:1.6;'>
        Upload a photo <em>or</em> capture with your camera. Our AI assesses severity,
        estimates healing time, and provides personalised care recommendations.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "⚠️ **Medical Disclaimer** — This AI analysis is for informational purposes only and does "
        "**NOT** replace professional medical advice. Always consult a qualified healthcare provider "
        "for diagnosis and treatment, especially for serious wounds."
    )

    st.divider()

    # ── Input mode selector ──────────────────────────────────────────
    st.markdown("#### 📥 Choose Image Source")
    mode_col1, mode_col2, mode_col3 = st.columns([1, 1, 4])
    with mode_col1:
        if st.button("📁  Upload File", use_container_width=True,
                     type="primary" if st.session_state.image_source == "upload" else "secondary"):
            st.session_state.image_source = "upload"
            st.session_state.camera_image = None
            st.rerun()
    with mode_col2:
        if st.button("📷  Use Camera", use_container_width=True,
                     type="primary" if st.session_state.image_source == "camera" else "secondary"):
            st.session_state.image_source = "camera"
            st.rerun()

    # ── Mode badge ──────────────────────────────────────────────────
    if st.session_state.image_source == "upload":
        st.markdown("""
        <div style='display:inline-flex;align-items:center;gap:8px;background:#eff6ff;
                    border:1.5px solid #0ea5e9;border-radius:50px;padding:5px 16px;
                    font-size:0.8rem;font-weight:600;color:#0369a1;margin-top:4px;
                    animation:fadeSlideUp 0.3s ease;'>
          📁 &nbsp;File Upload Mode Active
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='display:inline-flex;align-items:center;gap:8px;background:#f5f3ff;
                    border:1.5px solid #6366f1;border-radius:50px;padding:5px 16px;
                    font-size:0.8rem;font-weight:600;color:#4338ca;margin-top:4px;
                    animation:fadeSlideUp 0.3s ease;'>
          📷 &nbsp;Camera Capture Mode Active
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Image input + context ────────────────────────────────────────
    upload_col, preview_col = st.columns([1, 1])

    uploaded_file  = None
    camera_bytes   = None

    with upload_col:
        # ── STEP 1 ──
        if st.session_state.image_source == "upload":
            st.markdown("""
            <div style='display:flex;align-items:center;margin-bottom:10px;'>
              <span class='step-pill'>1</span>
              <span style='font-weight:600;font-size:0.95rem;'>Upload Wound Image</span>
            </div>
            """, unsafe_allow_html=True)
            uploaded_file = st.file_uploader(
                "Drag & drop or click to browse",
                type=["jpg", "jpeg", "png", "webp", "bmp"],
                help="Supported: JPG, PNG, WEBP, BMP — Max 10 MB",
                label_visibility="visible",
            )
            if uploaded_file:
                st.markdown("""
                <div style='display:inline-flex;align-items:center;gap:6px;
                            background:#dcfce7;border-radius:8px;padding:6px 12px;
                            font-size:0.8rem;font-weight:600;color:#15803d;margin-top:4px;
                            animation:fadeSlideUp 0.3s ease;'>
                  ✅ &nbsp;Image ready for analysis
                </div>
                """, unsafe_allow_html=True)

        else:
            # Camera mode
            st.markdown("""
            <div style='display:flex;align-items:center;margin-bottom:10px;'>
              <span class='step-pill' style='background:#6366f1;'>1</span>
              <span style='font-weight:600;font-size:0.95rem;'>Capture Wound with Camera</span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class='camera-card' style='margin-bottom:0.8rem;'>
              <div style='font-size:2.5rem;margin-bottom:8px;'>📷</div>
              <div style='font-size:0.88rem;font-weight:600;color:#4338ca;margin-bottom:4px;'>
                Live Camera Capture
              </div>
              <div style='font-size:0.78rem;color:#64748b;'>
                Point your camera at the wound and take a photo
              </div>
            </div>
            """, unsafe_allow_html=True)

            camera_image = st.camera_input(
                "Take a photo of the wound",
                help="Allow camera access when prompted. Take a clear, well-lit photo.",
                label_visibility="collapsed",
            )
            if camera_image:
                st.session_state.camera_image = camera_image
                st.markdown("""
                <div style='display:inline-flex;align-items:center;gap:6px;
                            background:#dcfce7;border-radius:8px;padding:6px 12px;
                            font-size:0.8rem;font-weight:600;color:#15803d;margin-top:4px;
                            animation:fadeSlideUp 0.3s ease;'>
                  ✅ &nbsp;Photo captured — ready for analysis
                </div>
                """, unsafe_allow_html=True)
            elif st.session_state.camera_image:
                camera_image = st.session_state.camera_image

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

        # ── STEP 2 ──
        st.markdown("""
        <div style='display:flex;align-items:center;margin-bottom:10px;'>
          <span class='step-pill'>2</span>
          <span style='font-weight:600;font-size:0.95rem;'>Provide Context (Optional)</span>
        </div>
        """, unsafe_allow_html=True)

        wound_age = st.selectbox(
            "How old is this wound?",
            ["Just occurred (< 1 hour)", "Few hours old (1–12 hours)",
             "1 day old", "2–3 days old", "4–7 days old",
             "More than 1 week old", "Chronic / Unknown"],
            label_visibility="visible",
        )
        patient_context = st.text_area(
            "Additional context",
            placeholder="E.g.: diabetic patient, animal bite, burn from hot water, not cleaned yet, on blood thinners...",
            height=90,
        )

        # ── STEP 3 — Analyse button ──
        st.markdown("""
        <div style='display:flex;align-items:center;margin:12px 0 8px;'>
          <span class='step-pill'>3</span>
          <span style='font-weight:600;font-size:0.95rem;'>Run AI Analysis</span>
        </div>
        """, unsafe_allow_html=True)

        has_image = (uploaded_file is not None) or (st.session_state.camera_image is not None and st.session_state.image_source == "camera")
        analyze_btn = st.button(
            "🔬  Analyse Wound with AI",
            type="primary",
            use_container_width=True,
            disabled=not has_image,
        )

        if not has_image:
            st.markdown("""
            <div style='font-size:0.77rem;color:#94a3b8;text-align:center;margin-top:4px;'>
              ☝️ Provide an image above to enable analysis
            </div>
            """, unsafe_allow_html=True)

    with preview_col:
        st.markdown("""
        <div style='display:flex;align-items:center;margin-bottom:10px;'>
          <span style='font-weight:600;font-size:0.95rem;color:#334155;'>🖼️  Image Preview</span>
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.image_source == "upload" and uploaded_file:
            st.image(uploaded_file, caption="Uploaded wound image", use_column_width=True)
        elif st.session_state.image_source == "camera" and st.session_state.camera_image:
            st.image(st.session_state.camera_image, caption="Captured wound image", use_column_width=True)
        else:
            st.markdown("""
            <div style='border:2px dashed #cbd5e1;border-radius:16px;padding:3rem 1rem;
                        text-align:center;background:#f8fafc;'>
              <div style='font-size:2.5rem;margin-bottom:10px;opacity:0.4;'>🩺</div>
              <div style='font-size:0.85rem;color:#94a3b8;font-weight:500;'>
                Your image will appear here
              </div>
              <div style='font-size:0.75rem;color:#cbd5e1;margin-top:4px;'>
                Upload or capture a photo to get started
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ── AI Analysis Logic ────────────────────────────────────────────
    if analyze_btn and has_image:
        # Determine image bytes + mime type
        if st.session_state.image_source == "upload" and uploaded_file:
            image_bytes = uploaded_file.read()
            fname = uploaded_file.name.lower()
            if fname.endswith(".png"):   mime_type = "image/png"
            elif fname.endswith(".webp"): mime_type = "image/webp"
            elif fname.endswith(".bmp"):  mime_type = "image/bmp"
            else:                         mime_type = "image/jpeg"
        else:
            image_bytes = st.session_state.camera_image.getvalue()
            mime_type   = "image/jpeg"

        b64_image   = base64.standard_b64encode(image_bytes).decode("utf-8")
        context_str = ("\n\nAdditional context provided by the user: " + patient_context.strip()
                       if patient_context.strip() else "")

        prompt = f"""You are a clinical wound assessment AI assistant integrated into the SmartGel IoT Healthcare Portal.
A patient has uploaded a photo of their wound/injury and it is {wound_age}.{context_str}

Carefully analyse the wound image and provide a structured JSON response ONLY — no preamble, no markdown fences, no extra text.

Return a JSON object with exactly these keys:

{{
  "wound_type": "Short label e.g. Laceration / Abrasion / Burn / Puncture / Ulcer / Contusion / Infected wound / etc.",
  "severity_level": "MILD | MODERATE | SEVERE | CRITICAL",
  "severity_score": <integer 1-10>,
  "affected_area": "Brief description of body area and size estimate",
  "visible_signs": ["list", "of", "visible", "clinical", "signs"],
  "infection_risk": "LOW | MEDIUM | HIGH | VERY HIGH",
  "healing_time_min_days": <integer>,
  "healing_time_max_days": <integer>,
  "healing_phase": "Current wound healing phase: Haemostasis / Inflammatory / Proliferative / Remodelling",
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

        # ── Animated loading ──
        loading_html = """
        <div style='background:linear-gradient(135deg,#eff6ff,#f0f9ff);border-radius:16px;
                    padding:2rem;text-align:center;border:1px solid #bae6fd;margin:1rem 0;
                    animation:fadeSlideUp 0.3s ease;'>
          <div style='width:44px;height:44px;border:4px solid #e2e8f0;
                      border-top-color:#0ea5e9;border-radius:50%;
                      animation:spin 0.9s linear infinite;margin:0 auto 1rem;'></div>
          <div style='font-family:Space Grotesk,sans-serif;font-size:1rem;font-weight:600;
                      color:#0369a1;margin-bottom:6px;'>Analysing wound with AI...</div>
          <div style='font-size:0.8rem;color:#64748b;'>
            Processing image data &nbsp;·&nbsp; Assessing severity &nbsp;·&nbsp; Generating recommendations
          </div>
          <div style='margin-top:14px;height:4px;border-radius:50px;background:#e2e8f0;overflow:hidden;'>
            <div class='healing-bar' style='height:100%;width:100%;'></div>
          </div>
        </div>
        """
        loading_placeholder = st.empty()
        loading_placeholder.markdown(loading_html, unsafe_allow_html=True)

        try:
            import urllib.request, urllib.error

            api_key = st.session_state.get("sidebar_api_key", "") or st.secrets.get("GOOGLE_API_KEY", "")
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

            gemini_url = ("https://generativelanguage.googleapis.com/v1beta/models/"
                          "gemini-2.0-flash:generateContent?key=" + api_key)
            req = urllib.request.Request(gemini_url, data=payload,
                                         headers={"Content-Type": "application/json"}, method="POST")

            with urllib.request.urlopen(req) as resp:
                raw = json.loads(resp.read().decode("utf-8"))

            full_text = raw["candidates"][0]["content"]["parts"][0]["text"]
            clean     = re.sub(r"```(?:json)?", "", full_text).strip().rstrip("`").strip()
            result    = json.loads(clean)
            st.session_state.wound_analysis = result
            loading_placeholder.empty()

        except Exception as e:
            loading_placeholder.empty()
            st.error("Analysis failed: " + str(e))
            st.session_state.wound_analysis = None

    # ── Display Results ──────────────────────────────────────────────
    if st.session_state.wound_analysis:
        r = st.session_state.wound_analysis

        # ── Animated results header ──
        st.markdown("""
        <div style='background:linear-gradient(135deg,#f0fdf4,#dcfce7);
                    border:1.5px solid #86efac;border-radius:16px;
                    padding:1rem 1.4rem;margin-bottom:1rem;
                    display:flex;align-items:center;gap:12px;
                    animation:fadeSlideUp 0.4s ease;'>
          <div style='font-size:1.5rem;'>📋</div>
          <div>
            <div style='font-family:Space Grotesk,sans-serif;font-weight:700;
                        font-size:1.05rem;color:#15803d;'>AI Wound Assessment Complete</div>
            <div style='font-size:0.78rem;color:#16a34a;'>Results generated · Review carefully</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        sev = r.get("severity_level", "MODERATE")
        sev_color_map = {
            "MILD":     ("#16a34a", "#dcfce7"),
            "MODERATE": ("#d97706", "#fef9c3"),
            "SEVERE":   ("#dc2626", "#fee2e2"),
            "CRITICAL": ("#7c3aed", "#ede9fe"),
        }
        sev_color, sev_bg = sev_color_map.get(sev, ("#475569", "#f1f5f9"))

        if r.get("seek_emergency"):
            st.error("🚨 **EMERGENCY**: This wound requires **IMMEDIATE** emergency medical attention. "
                     "Call emergency services or go to the nearest emergency room NOW.")

        # ── KPI row ──
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Wound Type",     r.get("wound_type", "Unknown"))
        m2.metric("Severity Score", str(r.get("severity_score", 5)) + " / 10")
        m3.metric("Infection Risk", r.get("infection_risk", "Unknown"))
        m4.metric("Est. Healing",
                  str(r.get("healing_time_min_days","?")) + "–" +
                  str(r.get("healing_time_max_days","?")) + " days")

        st.divider()

        detail_col, action_col = st.columns([1, 1])

        with detail_col:
            st.markdown("""
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:12px;'>
              <span style='font-size:1.1rem;'>🔍</span>
              <span class='section-header' style='border-bottom:2px solid #6366f1;'>Clinical Details</span>
            </div>
            """, unsafe_allow_html=True)

            details_rows = [
                ("Severity Level",      r.get("severity_level",   "—")),
                ("Severity Score",      str(r.get("severity_score","—")) + " / 10"),
                ("Wound Type",          r.get("wound_type",        "—")),
                ("Affected Area",       r.get("affected_area",     "—")),
                ("Healing Phase",       r.get("healing_phase",     "—")),
                ("Infection Risk",      r.get("infection_risk",    "—")),
                ("Healing Time (Est.)", str(r.get("healing_time_min_days","?")) + "–" +
                                        str(r.get("healing_time_max_days","?")) + " days"),
                ("See Doctor Within",   r.get("seek_doctor_within","—")),
                ("SmartGel Protocol",   r.get("smartgel_recommendation","—")),
                ("Recommended Tx",      r.get("recommended_treatment","—")),
            ]
            df_details = pd.DataFrame(details_rows, columns=["Parameter", "Value"])
            st.dataframe(df_details, use_container_width=True, hide_index=True, height=380)

            signs = r.get("visible_signs", [])
            if signs:
                st.markdown("**🩺 Visible Clinical Signs Detected:**")
                for s in signs:
                    st.markdown(
                        "<div style='background:#f8fafc;border-left:3px solid #0ea5e9;"
                        "padding:5px 10px;border-radius:0 8px 8px 0;font-size:0.84rem;"
                        "margin-bottom:4px;'>• " + str(s) + "</div>",
                        unsafe_allow_html=True
                    )

        with action_col:
            st.markdown("""
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:12px;'>
              <span style='font-size:1.1rem;'>⚡</span>
              <span class='section-header' style='border-bottom:2px solid #f59e0b;'>Immediate Actions</span>
            </div>
            """, unsafe_allow_html=True)
            for i, step in enumerate(r.get("immediate_actions", []), 1):
                st.markdown(
                    "<div style='display:flex;align-items:flex-start;gap:10px;"
                    "background:#fffbeb;border:1px solid #fde68a;border-radius:10px;"
                    "padding:8px 12px;margin-bottom:6px;font-size:0.85rem;'>"
                    "<span style='font-weight:700;color:#d97706;flex-shrink:0;'>" + str(i) + ".</span>"
                    "<span>" + str(step) + "</span></div>",
                    unsafe_allow_html=True
                )

            st.divider()
            st.markdown("""
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:12px;'>
              <span style='font-size:1.1rem;'>🏥</span>
              <span class='section-header' style='border-bottom:2px solid #10b981;'>Daily Care Instructions</span>
            </div>
            """, unsafe_allow_html=True)
            for i, step in enumerate(r.get("care_instructions", []), 1):
                st.markdown(
                    "<div style='display:flex;align-items:flex-start;gap:10px;"
                    "background:#f0fdf4;border:1px solid #86efac;border-radius:10px;"
                    "padding:8px 12px;margin-bottom:6px;font-size:0.85rem;'>"
                    "<span style='font-weight:700;color:#16a34a;flex-shrink:0;'>" + str(i) + ".</span>"
                    "<span>" + str(step) + "</span></div>",
                    unsafe_allow_html=True
                )

            st.divider()
            st.markdown("""
            <div style='display:flex;align-items:center;gap:8px;margin-bottom:12px;'>
              <span style='font-size:1.1rem;'>⚠️</span>
              <span class='section-header' style='border-bottom:2px solid #ef4444;'>Warning Signs</span>
            </div>
            """, unsafe_allow_html=True)
            for sign in r.get("warning_signs", []):
                st.markdown(
                    "<div style='display:flex;align-items:flex-start;gap:8px;"
                    "background:#fef2f2;border:1px solid #fca5a5;border-radius:10px;"
                    "padding:8px 12px;margin-bottom:6px;font-size:0.85rem;'>"
                    "<span style='color:#ef4444;flex-shrink:0;'>🔴</span>"
                    "<span>" + str(sign) + "</span></div>",
                    unsafe_allow_html=True
                )

        st.divider()

        # ── Severity gauge + confidence ──
        st.markdown("""
        <div style='display:flex;align-items:center;gap:8px;margin-bottom:4px;'>
          <span class='section-header'>📊 Severity Visualisation</span>
        </div>
        """, unsafe_allow_html=True)

        gauge_col, note_col = st.columns([2, 1])
        with gauge_col:
            score_val = r.get("severity_score", 5)
            fig_sev = go.Figure(go.Indicator(
                mode="gauge+number", value=score_val,
                number={"font": {"size": 52, "color": sev_color}, "suffix": "/10"},
                gauge={"axis": {"range": [0, 10], "tickwidth": 1, "tickcolor": "#64748b",
                                "tickfont": {"size": 11}, "nticks": 11},
                       "bar": {"color": sev_color, "thickness": 0.28},
                       "bgcolor": "#f0f6fb", "borderwidth": 1, "bordercolor": "#cbd5e1",
                       "steps": [{"range": [0,3.5],"color":"#dcfce7"},
                                  {"range": [3.5,6.0],"color":"#fef9c3"},
                                  {"range": [6.0,8.5],"color":"#fee2e2"},
                                  {"range": [8.5,10],"color":"#ede9fe"}]},
                title={"text": "Wound Severity Score<br>"
                               "<span style='font-size:12px;color:#64748b'>"
                               "1–3 Mild | 4–6 Moderate | 7–8 Severe | 9–10 Critical</span>",
                       "font": {"size": 14, "color": "#334155"}},
            ))
            fig_sev.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=300,
                                   margin=dict(l=20,r=20,t=60,b=10))
            st.plotly_chart(fig_sev, use_container_width=True, config={"displayModeBar": False})

        with note_col:
            st.markdown("""
            <div style='font-family:Space Grotesk,sans-serif;font-size:0.8rem;font-weight:600;
                        color:#64748b;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:6px;'>
              📝 Confidence Note
            </div>
            """, unsafe_allow_html=True)
            st.info(r.get("confidence_note", "No note available."))

            heal_min = r.get("healing_time_min_days", 0)
            heal_max = r.get("healing_time_max_days", 0)
            st.markdown("""
            <div style='font-family:Space Grotesk,sans-serif;font-size:0.8rem;font-weight:600;
                        color:#64748b;text-transform:uppercase;letter-spacing:0.06em;
                        margin-bottom:6px;margin-top:12px;'>
              ⏱️ Healing Timeline
            </div>
            """, unsafe_allow_html=True)
            st.success(
                "**" + str(heal_min) + " – " + str(heal_max) + " days** estimated\n\n"
                "Phase: " + r.get("healing_phase", "Unknown")
            )

            # Healing progress bar
            progress_pct = min(int((heal_min / max(heal_max, 1)) * 100), 100)
            st.markdown(
                "<div style='background:#f1f5f9;border-radius:50px;height:8px;overflow:hidden;margin-top:8px;'>"
                "<div class='healing-bar' style='height:100%;width:" + str(progress_pct) + "%;'></div>"
                "</div>"
                "<div style='font-size:0.7rem;color:#94a3b8;margin-top:3px;text-align:right;'>"
                "Healing progress estimate</div>",
                unsafe_allow_html=True
            )

        st.divider()

        # ── Export ──
        export_rows = [
            ("Wound Type",          r.get("wound_type", "")),
            ("Severity Level",      r.get("severity_level", "")),
            ("Severity Score",      str(r.get("severity_score", ""))),
            ("Affected Area",       r.get("affected_area", "")),
            ("Infection Risk",      r.get("infection_risk", "")),
            ("Healing Time (days)", str(r.get("healing_time_min_days","")) + "–" + str(r.get("healing_time_max_days",""))),
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
                "📥  Download AI Wound Analysis Report (CSV)",
                df_export_report.to_csv(index=False),
                "smartgel_wound_analysis.csv", "text/csv",
                type="primary", use_container_width=True,
            )
        with exp2:
            if st.button("🔄  Clear Analysis & Upload New Image", use_container_width=True):
                st.session_state.wound_analysis = None
                st.session_state.camera_image   = None
                st.rerun()
