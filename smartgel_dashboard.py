# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
import random
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
# GLOBAL CSS
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

  [data-testid="stAlert"] {
    border-radius: var(--radius) !important;
    border-left-width: 4px !important;
    font-size: 0.87rem !important;
  }

  [data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    overflow: hidden;
    border: 1px solid var(--border) !important;
  }

  hr {
    border: none !important;
    border-top: 1.5px solid var(--border) !important;
    margin: 1.5rem 0 !important;
  }

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
  .nav-item:hover { background: var(--brand-light); border-color: var(--border); }
  .nav-item.nav-active { background: var(--brand-light); border-color: var(--brand-mid); }
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

  .card {
    background: var(--card);
    border: 1.5px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 1.3rem 1.5rem;
    box-shadow: var(--shadow-sm);
  }

  .healing-bar {
    height: 7px;
    border-radius: 50px;
    background: linear-gradient(90deg, #1b8a5a, #f59e0b, #c0392b);
    background-size: 200% 100%;
    animation: shimmerFlow 3s ease infinite;
  }

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

  .action-item {
    display: flex; align-items: flex-start; gap: 10px;
    border-radius: 10px; padding: 9px 13px; margin-bottom: 6px; font-size: 0.84rem;
  }
  .action-num { font-weight: 800; flex-shrink: 0; }

  .wound-card {
    background: #fff;
    border: 1.5px solid var(--border);
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: all 0.2s;
  }
  .wound-card:hover {
    border-color: var(--brand-mid);
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
  }
  .wound-card.selected {
    border-color: var(--brand);
    background: var(--brand-light);
    box-shadow: 0 0 0 3px rgba(29,111,164,0.12);
  }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
# SCENARIO DATA (IoT Monitoring)
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
        "treatment":      "Salicylic Acid Hydrogel 2%",
        "healing_stage":  "Inflammatory → Proliferative",
        "reapply_hours":  3.5,
        "radar_scores":   [90, 88, 75, 92, 85, 95],
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
        "treatment":      "Antimicrobial Silver Hydrogel",
        "healing_stage":  "Chronic Inflammatory (Stalled)",
        "reapply_hours":  1.0,
        "radar_scores":   [30, 35, 25, 15, 20, 50],
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
        "treatment":      "Antiseptic Hydrogel + PEP Protocol",
        "healing_stage":  "Acute Contamination",
        "reapply_hours":  0.5,
        "radar_scores":   [15, 20, 18, 10, 12, 40],
    },
}

DAYS          = ["Day " + str(i + 1) for i in range(10)]
SCENARIO_KEYS = list(SCENARIOS.keys())
CHART_COLORS  = ["#c026d3", "#dc2626", "#ea580c"]

# ------------------------------------------------------------------
# COMPREHENSIVE WOUND KNOWLEDGE BASE
# ------------------------------------------------------------------
WOUND_DATABASE = {
    # ── TRAUMATIC / ACUTE ──────────────────────────────────────────
    "Abrasion (Road Rash / Graze)": {
        "category": "Traumatic",
        "emoji": "🛤️",
        "severity_level": "MILD",
        "severity_score": 2,
        "description": "Superficial wound caused by skin scraping against a rough surface. Affects only the epidermis or upper dermis.",
        "causes": ["Falling on pavement", "Cycling accident", "Sports fall", "Friction against rough surface"],
        "visible_signs": [
            "Raw, red abraded skin surface",
            "Oozing serum or blood (not heavy bleeding)",
            "Embedded dirt/gravel particles",
            "Burning or stinging sensation",
            "Irregular wound edges",
        ],
        "infection_risk": "LOW to MEDIUM",
        "healing_time_min_days": 5,
        "healing_time_max_days": 14,
        "healing_phases": [
            ("Haemostasis", "Day 0–1", "Bleeding stops, clotting begins"),
            ("Inflammatory", "Day 1–3", "Redness, swelling, warmth — normal immune response"),
            ("Proliferative", "Day 3–10", "New skin cells grow, scab forms"),
            ("Remodelling", "Day 10–14", "Skin matures, scar fades"),
        ],
        "immediate_actions": [
            "Rinse under clean running water for 5–10 minutes",
            "Gently remove visible debris with clean tweezers (sterilised)",
            "Apply antiseptic solution (povidone-iodine or chlorhexidine)",
            "Cover with a non-stick sterile dressing",
            "Do NOT scrub — pat gently to avoid deeper damage",
        ],
        "recommended_dressing": "Non-adherent absorbent dressing (e.g. Mepitel, Melolin) + foam secondary layer",
        "smartgel_protocol": "SmartGel pH 5.5 Hydrogel — maintains moist healing environment, reduces scarring",
        "daily_care": [
            "Change dressing daily or when saturated",
            "Clean with saline solution before redressing",
            "Keep wound moist — do not let scab dry and crack",
            "Avoid submerging in water (baths/swimming) until closed",
            "Apply SPF 30+ sunscreen once healed to prevent hyperpigmentation",
        ],
        "medications": [
            "Topical antiseptic: Povidone-iodine 10% or Chlorhexidine 0.05%",
            "Pain relief: Paracetamol 500mg–1g every 4–6 hours as needed",
            "Tetanus booster if not updated within 5 years",
            "Topical antibiotic (if infection signs): Mupirocin 2% cream",
        ],
        "warning_signs": [
            "Increasing redness spreading beyond wound edge (>2 cm)",
            "Yellow/green purulent discharge with foul odour",
            "Fever above 38°C",
            "Red streaks radiating from wound (lymphangitis)",
            "Wound not healing after 2 weeks",
        ],
        "seek_doctor_within": "Monitor at home — see GP if infection signs develop",
        "seek_emergency": False,
        "nutrition_tips": [
            "Protein: 1.2–1.5g/kg body weight daily (eggs, chicken, legumes)",
            "Vitamin C: 500–1000mg daily (citrus, bell peppers) — collagen synthesis",
            "Zinc: 15–25mg daily (nuts, seeds, red meat) — tissue repair",
            "Hydration: 2–3 litres water daily",
        ],
        "do_not": [
            "Do NOT pick or remove scabs prematurely",
            "Do NOT use hydrogen peroxide directly (damages new cells)",
            "Do NOT cover with cotton wool (fibres stick)",
            "Do NOT ignore embedded debris",
        ],
        "prognosis": "Excellent — heals completely with minimal scarring if kept clean and moist.",
    },

    "Laceration (Deep Cut)": {
        "category": "Traumatic",
        "emoji": "🔪",
        "severity_level": "MODERATE to SEVERE",
        "severity_score": 6,
        "description": "A full-thickness cut through skin caused by a sharp object. May involve subcutaneous tissue, muscle, tendons or vessels.",
        "causes": ["Knife/glass cut", "Industrial accident", "Sports injury", "Fall on sharp edge"],
        "visible_signs": [
            "Deep, gaping wound with defined edges",
            "Active bleeding (may be heavy)",
            "Possible exposure of subcutaneous fat (yellow tissue)",
            "Wound edges may not oppose naturally",
            "Possible tendon or bone visibility in severe cases",
        ],
        "infection_risk": "MEDIUM to HIGH",
        "healing_time_min_days": 10,
        "healing_time_max_days": 42,
        "healing_phases": [
            ("Haemostasis", "0–2 hours", "Platelet plug formation, clotting cascade"),
            ("Inflammatory", "Day 1–4", "Neutrophils clear bacteria, macrophages debride"),
            ("Proliferative", "Day 4–21", "Fibroblasts deposit collagen, wound contracts"),
            ("Remodelling", "Day 21–365", "Collagen reorganisation, scar softens"),
        ],
        "immediate_actions": [
            "Apply FIRM direct pressure with clean cloth for 10–15 minutes continuously",
            "Do NOT remove cloth if soaked — add more on top",
            "Elevate injured limb above heart level",
            "Do NOT attempt to close deep wounds yourself",
            "Seek emergency care if: bleeding won't stop, wound is >2cm, gaping, or on face/hand/joint",
        ],
        "recommended_dressing": "Sterile gauze under pressure → sutures/steri-strips applied by clinician → non-adherent dressing",
        "smartgel_protocol": "SmartGel Antimicrobial Hydrogel post-closure — maintains pH 5.5, prevents biofilm formation",
        "daily_care": [
            "Keep wound dry for 24–48 hours post-suture",
            "Clean with saline twice daily after 48 hours",
            "Apply thin layer of petroleum jelly to prevent drying",
            "Protect from sun exposure for 12 months (prevents hyperpigmentation)",
            "Suture removal: face 5–7 days, body 10–14 days, over joint 14 days",
        ],
        "medications": [
            "Local anaesthetic for closure: Lidocaine 1–2% (administered by clinician)",
            "Oral antibiotics if contaminated: Amoxicillin-clavulanate 625mg 3×/day for 5 days",
            "Pain relief: Ibuprofen 400mg every 6–8 hours + Paracetamol 1g",
            "Tetanus prophylaxis if due",
        ],
        "warning_signs": [
            "Suture line opening (dehiscence)",
            "Pus or purulent discharge between sutures",
            "Wound edges turning black (necrosis)",
            "Fever, rigors, malaise",
            "Numbness or loss of function distal to wound",
        ],
        "seek_doctor_within": "Immediately — requires assessment for sutures/closure",
        "seek_emergency": True,
        "nutrition_tips": [
            "High protein intake: 1.5–2g/kg/day for tissue repair",
            "Vitamin A: liver, dairy, carrots — supports epithelialisation",
            "Iron: red meat, leafy greens — prevents anaemia from blood loss",
            "Omega-3 fatty acids: reduce excessive inflammation",
        ],
        "do_not": [
            "Do NOT close wound with tape if deep (traps infection inside)",
            "Do NOT explore wound depth yourself",
            "Do NOT remove embedded objects — stabilise and go to A&E",
            "Do NOT use antiseptic inside deep wound tissue",
        ],
        "prognosis": "Good with proper closure. Risk of hypertrophic scar if closed under tension or infected.",
    },

    "Puncture Wound": {
        "category": "Traumatic",
        "emoji": "📍",
        "severity_level": "MODERATE",
        "severity_score": 5,
        "description": "A small-diameter but deep wound caused by a sharp pointed object. High infection risk due to depth and sealed surface.",
        "causes": ["Nail/nail gun", "Needle/syringe", "Thorn", "Animal bite/sting", "Splinter"],
        "visible_signs": [
            "Small surface entry point, deceptively deep",
            "Minimal surface bleeding",
            "Swelling around entry point",
            "Possible foreign body inside",
            "Localised warmth and tenderness",
        ],
        "infection_risk": "HIGH",
        "healing_time_min_days": 7,
        "healing_time_max_days": 21,
        "healing_phases": [
            ("Haemostasis", "0–1 hour", "Limited due to small opening — risk of anaerobic bacteria"),
            ("Inflammatory", "Day 1–5", "Deep tissue inflammation, risk of abscess formation"),
            ("Proliferative", "Day 5–14", "Internal tissue repair, granulation from inside out"),
            ("Remodelling", "Day 14–21", "Scar tissue formation"),
        ],
        "immediate_actions": [
            "Encourage gentle bleeding by mild pressure around wound (flushes bacteria out)",
            "Irrigate vigorously with large volume of saline or clean water",
            "Do NOT seal wound — allow drainage",
            "Remove superficial splinters with sterilised tweezers",
            "Seek medical review for foot punctures, deep hand wounds, or any suspected foreign body",
        ],
        "recommended_dressing": "Loose, non-occlusive dressing — allow wound to drain. Antiseptic wick if prescribed.",
        "smartgel_protocol": "SmartGel Antiseptic Hydrogel — fills wound cavity, maintains acidic pH to prevent anaerobic growth",
        "daily_care": [
            "Irrigate wound opening daily with saline",
            "Watch for signs of abscess (fluctuant swelling, increasing pain after Day 3)",
            "Keep weight off foot punctures for 48–72 hours",
            "Monitor temperature twice daily",
            "X-ray may be needed to rule out retained foreign body",
        ],
        "medications": [
            "Antibiotics for foot/hand punctures: Amoxicillin-clavulanate or Cefalexin 500mg 4×/day",
            "Anti-tetanus immunoglobulin if high-risk (dirty wound, no prior vaccination)",
            "Pain relief: Paracetamol + Ibuprofen combination",
            "Deep wound abscess: incision and drainage by clinician",
        ],
        "warning_signs": [
            "Increasing pain after Day 2–3 (suggests infection/abscess)",
            "Hot, tense, fluctuant swelling",
            "Red tracking lines from wound",
            "Fever and malaise",
            "Loss of movement in affected foot/hand",
        ],
        "seek_doctor_within": "Within 24 hours for foot/hand wounds; immediately if foreign body suspected",
        "seek_emergency": False,
        "nutrition_tips": [
            "Protein-rich diet for deep tissue healing",
            "Vitamin C for collagen synthesis",
            "Avoid alcohol — impairs immune response",
            "Adequate hydration supports lymphatic drainage",
        ],
        "do_not": [
            "Do NOT seal entry wound with occlusive dressing",
            "Do NOT soak foot in bath (softens healthy tissue)",
            "Do NOT attempt to probe wound depth",
            "Do NOT ignore worsening pain after Day 2",
        ],
        "prognosis": "Good if cleaned properly. Risk of abscess, osteomyelitis (bone infection) in foot punctures if neglected.",
    },

    "Burn — First Degree (Superficial)": {
        "category": "Thermal",
        "emoji": "🔥",
        "severity_level": "MILD",
        "severity_score": 3,
        "description": "Injury to the epidermis only. Characterised by redness, pain, and dry skin without blisters.",
        "causes": ["Brief sun exposure (sunburn)", "Brief contact with hot surface", "Hot liquid splash (brief)", "Chemical splash (mild)"],
        "visible_signs": [
            "Uniform redness (erythema)",
            "Dry, intact skin surface",
            "Painful to touch",
            "Mild swelling",
            "No blisters",
            "Blanches (turns white) under pressure",
        ],
        "infection_risk": "LOW",
        "healing_time_min_days": 3,
        "healing_time_max_days": 7,
        "healing_phases": [
            ("Inflammatory", "Day 0–2", "Vasodilation causes redness and pain"),
            ("Proliferative", "Day 2–5", "Epidermis regenerates from below"),
            ("Remodelling", "Day 5–7", "Superficial peeling, new skin revealed"),
        ],
        "immediate_actions": [
            "Cool under running cold water for 20 minutes IMMEDIATELY",
            "Do NOT use ice, butter, toothpaste, or any home remedy",
            "Remove jewellery/clothing from burned area (before swelling)",
            "Cover loosely with cling film or clean non-fluffy material",
            "Take OTC pain relief",
        ],
        "recommended_dressing": "Cling film or non-adherent low-tack dressing; aloe vera gel for sunburn",
        "smartgel_protocol": "SmartGel Cooling Hydrogel — provides sustained pain relief and maintains optimal skin moisture",
        "daily_care": [
            "Moisturise with unperfumed lotion or aloe vera twice daily",
            "Keep out of sun until fully healed",
            "Drink extra fluids (burns increase fluid loss)",
            "Avoid picking or peeling skin",
            "Use SPF 50+ for 6–12 months on healed area",
        ],
        "medications": [
            "Paracetamol 500–1000mg every 4–6 hours for pain",
            "Ibuprofen 400mg every 8 hours (anti-inflammatory)",
            "Aloe vera gel (pure, no alcohol) applied liberally",
            "Hydrocortisone 1% cream for severe sunburn (short term)",
        ],
        "warning_signs": [
            "Blistering developing (suggests 2nd degree — seek review)",
            "Burn covering large area (>1% body surface = palm of hand)",
            "Burns on face, hands, feet, genitals, or joints",
            "Chemical or electrical cause",
        ],
        "seek_doctor_within": "Monitor at home — see GP if blistering develops or covers large area",
        "seek_emergency": False,
        "nutrition_tips": [
            "Increase fluid intake to compensate for evaporative loss",
            "Vitamin E: nuts, seeds — antioxidant skin repair",
            "Vitamin C: boosts collagen and immune healing",
        ],
        "do_not": [
            "Do NOT apply ice directly (causes frostbite on damaged skin)",
            "Do NOT use butter, toothpaste, or petroleum jelly acutely",
            "Do NOT burst blisters if they form",
            "Do NOT wrap tightly",
        ],
        "prognosis": "Excellent — heals completely in 3–7 days without scarring.",
    },

    "Burn — Second Degree (Partial Thickness)": {
        "category": "Thermal",
        "emoji": "🔥🔥",
        "severity_level": "MODERATE to SEVERE",
        "severity_score": 7,
        "description": "Involves epidermis and partial dermis. Characterised by blisters, intense pain, and weeping wound surface.",
        "causes": ["Scalding with boiling water", "Flame contact", "Chemical burns", "Prolonged sun exposure"],
        "visible_signs": [
            "Blisters — intact or ruptured",
            "Bright red, pink, or mottled weeping surface",
            "Intense pain (very sensitive to touch)",
            "Wet, shiny wound base",
            "Possible oedema (swelling)",
        ],
        "infection_risk": "HIGH",
        "healing_time_min_days": 14,
        "healing_time_max_days": 42,
        "healing_phases": [
            ("Haemostasis + Inflammatory", "Day 0–3", "Intense fluid loss, exudate, pain"),
            ("Proliferative", "Day 3–21", "Re-epithelialisation from hair follicle remnants (superficial) or from edges (deep)"),
            ("Remodelling", "Day 21–365", "Scar maturation — may take 12–18 months"),
        ],
        "immediate_actions": [
            "Cool under running water 20 minutes — call 999/112 if large area (>5% body)",
            "Remove clothing and jewellery GENTLY (cut around anything stuck)",
            "Do NOT burst blisters — they protect underlying tissue",
            "Cover with cling film or burns dressing",
            "Go to Burns Unit or Emergency Department",
        ],
        "recommended_dressing": "Silver sulfadiazine dressing (Flamazine) or Mepilex Transfer Ag — changed every 2–3 days by clinician",
        "smartgel_protocol": "SmartGel Antimicrobial Silver Hydrogel — pH-buffering, antimicrobial, reduces pain on dressing change",
        "daily_care": [
            "Dressings changed by clinician every 2–3 days initially",
            "Compression garments after healing to reduce hypertrophic scarring",
            "Scar massage with moisturiser from 3 weeks post-healing",
            "Strict sun avoidance for 2 years on healed area",
            "Physiotherapy for burns over joints to prevent contracture",
        ],
        "medications": [
            "Analgesia: Morphine or Oxycodone for dressing changes",
            "Regular: Paracetamol + Ibuprofen combination",
            "Topical: Silver sulfadiazine 1% (Flamazine) or Mafenide acetate",
            "IV fluids: Parkland formula if >15% body surface area (hospital)",
            "Prophylactic antibiotics: not routinely recommended",
        ],
        "warning_signs": [
            "Wound turning pale/white/leathery (converting to 3rd degree)",
            "Increasing foul odour from wound",
            "Systemic infection: fever, tachycardia, confusion",
            "Wound failing to heal by Day 21 (may need skin grafting)",
        ],
        "seek_doctor_within": "Immediately — all blistering burns require medical assessment",
        "seek_emergency": True,
        "nutrition_tips": [
            "Very high protein: 2–3g/kg/day (burns dramatically increase metabolic demand)",
            "High calorie intake: burns can increase metabolic rate by 100–200%",
            "Vitamin C: 1–2g daily — accelerates collagen",
            "Zinc, Selenium, Copper supplements for epithelial repair",
            "Nasogastric feeding if >20% body surface area burned",
        ],
        "do_not": [
            "Do NOT burst blisters",
            "Do NOT use ice",
            "Do NOT apply home remedies (butter, egg white, toothpaste)",
            "Do NOT remove stuck clothing forcibly",
            "Do NOT leave wound open/exposed",
        ],
        "prognosis": "Superficial 2nd degree — heals well with minimal scarring. Deep 2nd degree — high scarring risk, may need skin grafting.",
    },

    "Animal Bite (Dog / Cat / Human)": {
        "category": "Contaminated / Bite",
        "emoji": "🐕",
        "severity_level": "MODERATE to SEVERE",
        "severity_score": 6,
        "description": "Crushing, tearing, or puncture injuries from animal teeth. Carry high bacterial load including Pasteurella, Capnocytophaga, and potential Rabies risk.",
        "causes": ["Dog bite", "Cat bite", "Human bite", "Wild animal attack"],
        "visible_signs": [
            "Tooth puncture marks (multiple)",
            "Crushing / tearing injury pattern",
            "Possible avulsion (tissue torn away)",
            "Immediate swelling and bruising",
            "Significant pain",
        ],
        "infection_risk": "VERY HIGH",
        "healing_time_min_days": 10,
        "healing_time_max_days": 56,
        "healing_phases": [
            ("Contamination control", "0–6 hours", "CRITICAL window — aggressive irrigation reduces infection rate by 80%"),
            ("Inflammatory", "Day 1–5", "High risk of Pasteurella multocida infection (cats especially)"),
            ("Proliferative", "Day 5–21", "Granulation tissue, wound contraction"),
            ("Remodelling", "Day 21+", "Scar formation"),
        ],
        "immediate_actions": [
            "Wash wound VIGOROUSLY with soap and water for 15 full minutes",
            "Irrigate with large volume saline or clean water under pressure",
            "Do NOT close wound primarily — leave open unless on face",
            "Go to A&E or urgent care within 2–4 hours",
            "Report dog/cat bite to local authority if unprovoked",
            "Inform clinician: vaccination status of animal if known",
        ],
        "recommended_dressing": "Loose non-occlusive dressing — do not seal. Irrigate before every dressing change.",
        "smartgel_protocol": "SmartGel Antiseptic Hydrogel + Antimicrobial Silver — reduces Pasteurella and polymicrobial load",
        "daily_care": [
            "Elevate bitten limb to reduce swelling",
            "Irrigate wound twice daily with saline",
            "Watch closely for Pasteurella infection: rapid onset (6–24 hours)",
            "Complete full antibiotic course even if improving",
            "Rabies Post-Exposure Prophylaxis (PEP) as directed by clinician",
        ],
        "medications": [
            "Antibiotics (mandatory): Co-amoxiclav (Amoxicillin-Clavulanate) 625mg 3×/day × 5–7 days",
            "Penicillin allergy: Doxycycline 100mg 2×/day + Metronidazole 400mg 3×/day",
            "Rabies PEP: Day 0, 3, 7, 14 vaccine schedule ± Rabies Immunoglobulin (Day 0)",
            "Tetanus booster if not up to date",
            "Pain relief: Ibuprofen + Paracetamol",
        ],
        "warning_signs": [
            "Rapid onset pain + redness within 6–24 hours (Pasteurella multocida)",
            "Fever, shaking chills",
            "Red streaks from wound",
            "Swollen lymph nodes",
            "Black/grey skin discolouration (Capnocytophaga — rare but life-threatening in immunocompromised)",
        ],
        "seek_doctor_within": "Within 2–4 hours — all bite wounds require medical assessment",
        "seek_emergency": True,
        "nutrition_tips": [
            "Maintain high protein intake while on antibiotics",
            "Probiotic yogurt to protect gut during antibiotic course",
            "Vitamin C and zinc for immune support",
        ],
        "do_not": [
            "Do NOT close bite wound with tape or sutures at home",
            "Do NOT delay medical assessment",
            "Do NOT ignore cat bites — they cause rapid deep infection",
            "Do NOT assume vaccinated dog cannot transmit disease",
        ],
        "prognosis": "Good with prompt treatment. Delayed treatment risks osteomyelitis, septic arthritis, sepsis.",
    },

    "Chronic Diabetic Foot Ulcer": {
        "category": "Chronic / Diabetic",
        "emoji": "🦶",
        "severity_level": "SEVERE to CRITICAL",
        "severity_score": 8,
        "description": "Chronic non-healing wounds on diabetic feet caused by peripheral neuropathy (loss of sensation), vascular insufficiency, and impaired immune response.",
        "causes": ["Uncontrolled diabetes mellitus", "Peripheral neuropathy (no pain sensation)", "Poor peripheral circulation", "Pressure from ill-fitting footwear", "Repetitive minor trauma"],
        "visible_signs": [
            "Deep ulcer, often painless (neuropathy)",
            "Callus formation around wound edges",
            "Surrounding skin: shiny, hairless, cold (vascular) or warm (neuropathic)",
            "Possible slough (yellow dead tissue) or eschar (black necrosis)",
            "Wound may probe to tendon or bone",
            "Malodour from polymicrobial infection",
        ],
        "infection_risk": "CRITICAL",
        "healing_time_min_days": 42,
        "healing_time_max_days": 365,
        "healing_phases": [
            ("Chronic Inflammatory Arrest", "Weeks to months", "Wound stalls in inflammatory phase — fails to progress"),
            ("Debridement Phase", "Ongoing", "Slough and necrotic tissue must be removed regularly"),
            ("Proliferative", "Weeks–months after infection control", "Granulation tissue only when glucose controlled"),
            ("Remodelling", "Months–years", "Fragile scar prone to re-ulceration"),
        ],
        "immediate_actions": [
            "OFFLOAD immediately — no weight-bearing on affected foot",
            "Assess vascular status (ABI — Ankle-Brachial Index)",
            "Debride slough and necrotic tissue (by clinician only)",
            "Blood glucose optimisation is essential for any healing",
            "Wound swab for microbiology before starting antibiotics",
        ],
        "recommended_dressing": "Antimicrobial silver dressings (Aquacel Ag+) or cadexomer iodine; hydrogel for dry necrosis; NPWT (vacuum) for deep cavity wounds",
        "smartgel_protocol": "SmartGel Antimicrobial Silver Hydrogel — pH sensor alerts for biofilm formation; auto-alerts clinician above pH 7.5",
        "daily_care": [
            "Blood glucose monitoring: target HbA1c < 7%",
            "Total contact casting or specialised offloading footwear",
            "Dressing change every 2–3 days or as directed",
            "Daily foot inspection (use mirror for soles)",
            "Optimal nutrition — see below",
            "Specialist diabetic foot clinic review every 1–2 weeks",
        ],
        "medications": [
            "Systemic antibiotics for infected ulcer: Amoxicillin-Clavulanate or Piperacillin-Tazobactam (IV for severe)",
            "MRSA coverage: Vancomycin or Daptomycin (if MRSA risk)",
            "Blood glucose control: Insulin optimisation, HbA1c target <7%",
            "Peripheral vascular disease: Antiplatelet (aspirin), statin, revascularisation if indicated",
            "Growth factors: Becaplermin gel (PDGF) for resistant ulcers",
        ],
        "warning_signs": [
            "Black necrosis / gangrene spreading proximally",
            "Fever, elevated WBC, CRP (signs of systemic sepsis)",
            "Gas in wound tissue on X-ray (gas-forming bacteria — emergency)",
            "Bone visible or probe-to-bone positive (osteomyelitis)",
            "Rapidly worsening odour",
        ],
        "seek_doctor_within": "Immediately — diabetic foot ulcers require urgent specialist assessment",
        "seek_emergency": True,
        "nutrition_tips": [
            "Protein: 1.5–2g/kg/day — essential for impaired healing",
            "Strict glycaemic diet: low glycaemic index carbohydrates",
            "Vitamin D supplementation (common deficiency in diabetes — impairs immunity)",
            "Zinc 15–30mg/day for tissue repair",
            "Omega-3 fatty acids for vascular inflammation reduction",
            "Avoid alcohol — worsens neuropathy and glycaemic control",
        ],
        "do_not": [
            "Do NOT walk on an active diabetic ulcer without offloading",
            "Do NOT soak foot in water (maceration worsens healing)",
            "Do NOT cut corns/callus yourself",
            "Do NOT apply strong antiseptics like neat hydrogen peroxide or iodine directly",
            "Do NOT delay — 15–20% of diabetic ulcers lead to amputation if untreated",
        ],
        "prognosis": "Guarded — healing depends on glucose control and vascular status. Risk of amputation without prompt specialist care.",
    },

    "Pressure Ulcer (Bedsore)": {
        "category": "Chronic / Pressure",
        "emoji": "🛏️",
        "severity_level": "MODERATE to CRITICAL",
        "severity_score": 7,
        "description": "Localised tissue injury caused by sustained pressure, shear, or friction over bony prominences. Common in immobile/hospitalised patients.",
        "causes": ["Prolonged immobility", "Reduced sensation (paralysis, sedation)", "Malnutrition", "Moisture (incontinence)", "Poor skin integrity"],
        "visible_signs": [
            "Stage 1: Non-blanchable redness, intact skin",
            "Stage 2: Shallow open ulcer, pink wound bed or blister",
            "Stage 3: Full thickness skin loss, subcutaneous tissue visible, no bone/tendon",
            "Stage 4: Full thickness, bone/tendon/muscle exposed",
            "DTI (Deep Tissue Injury): Purple/maroon intact or blister over bony prominence",
        ],
        "infection_risk": "HIGH (Stage 3–4)",
        "healing_time_min_days": 14,
        "healing_time_max_days": 365,
        "healing_phases": [
            ("Pressure removal", "Immediate", "No healing possible without offloading"),
            ("Debridement", "Days 1–14", "Remove necrotic tissue (surgical/enzymatic/autolytic)"),
            ("Granulation", "Weeks", "Wound fills from base up"),
            ("Epithelialisation", "Weeks–months", "Surface closes inward from edges"),
        ],
        "immediate_actions": [
            "REMOVE PRESSURE IMMEDIATELY — reposition patient every 2 hours",
            "Use pressure-redistributing mattress or cushion",
            "Clean wound with saline — no harsh antiseptics on open ulcer",
            "Refer to tissue viability nurse specialist",
            "Nutritional assessment — malnutrition major risk factor",
        ],
        "recommended_dressing": "Stage 1–2: Foam dressings, transparent film. Stage 3–4: Alginate/hydrofibre, NPWT, surgical debridement",
        "smartgel_protocol": "SmartGel Hydrogel for autolytic debridement of Stage 2–3 ulcers — maintains moist wound environment",
        "daily_care": [
            "Reposition every 2 hours (chair) or 4 hours (pressure-relieving mattress)",
            "Barrier cream for incontinence protection",
            "Daily wound assessment and documentation",
            "Nutritional supplementation (protein, Vitamin C, Zinc)",
            "Physiotherapy to improve mobility",
        ],
        "medications": [
            "Antibiotics only if clinically infected (wound swab first)",
            "Enzymatic debridement: Collagenase ointment",
            "Pain management: Opioid analgesia for dressing changes if needed",
            "Nutritional supplements: Oral protein supplements, Zinc, Vitamin C",
        ],
        "warning_signs": [
            "Rapid wound extension",
            "Systemic sepsis from wound",
            "Osteomyelitis (bone infection) — may need bone biopsy",
            "Tunnelling or undermining beneath wound edges",
        ],
        "seek_doctor_within": "Within 24 hours for Stage 2+; Immediately for Stage 3–4 or systemically unwell patient",
        "seek_emergency": False,
        "nutrition_tips": [
            "Protein: 1.5–2g/kg/day — severely malnourished patients at highest risk",
            "Vitamin C: 500–1000mg daily — essential for collagen synthesis",
            "Zinc: 15–30mg/day",
            "Consider high-calorie, high-protein oral supplements (Ensure, Fortisip)",
            "Nasogastric feeding if unable to eat",
        ],
        "do_not": [
            "Do NOT massage bony prominences (worsens microvascular damage)",
            "Do NOT use ring/donut cushions (cause pressure ring)",
            "Do NOT use hydrogen peroxide or Dakin's solution on granulating tissue",
            "Do NOT ignore Stage 1 — it can progress rapidly",
        ],
        "prognosis": "Stage 1–2: Good with offloading and care. Stage 3–4: Prolonged healing, high morbidity, may require surgical closure (flap).",
    },

    "Infected Wound / Cellulitis": {
        "category": "Infected",
        "emoji": "🦠",
        "severity_level": "MODERATE to SEVERE",
        "severity_score": 6,
        "description": "Bacterial infection of wound extending into surrounding skin and soft tissue. Requires systemic antibiotic treatment.",
        "causes": ["Any wound that becomes colonised then infected", "Streptococcus or Staphylococcus most common", "MRSA in healthcare settings", "Gram-negative organisms in diabetic/immunocompromised"],
        "visible_signs": [
            "Spreading redness (erythema) beyond wound edges — mark with pen to monitor",
            "Warmth and tenderness",
            "Oedema (swelling)",
            "Purulent (yellow/green) discharge",
            "Wound may have foul odour",
            "Possibly — red streaking (lymphangitis)",
        ],
        "infection_risk": "Already infected — HIGH risk of spreading",
        "healing_time_min_days": 7,
        "healing_time_max_days": 42,
        "healing_phases": [
            ("Active Infection", "Day 0–7 with antibiotics", "Bacterial load must be reduced for healing to begin"),
            ("Resolution", "Day 5–14", "Redness recedes, wound starts to close"),
            ("Proliferative", "Day 10–28", "Granulation and epithelialisation"),
            ("Remodelling", "Weeks–months", "Scar formation"),
        ],
        "immediate_actions": [
            "Mark the advancing edge of redness with a pen — date and time it",
            "Take oral temperature — if >38°C or systemically unwell, go to A&E",
            "Clean wound with saline",
            "Start antibiotics as prescribed — do NOT delay",
            "Elevate affected limb",
        ],
        "recommended_dressing": "Antimicrobial dressings (silver, iodine). Drainage of abscess if fluctuant. Wound swab before antibiotic start.",
        "smartgel_protocol": "SmartGel Antimicrobial Silver Hydrogel — pH sensor monitors biofilm activity, alerts if pH >7.2",
        "daily_care": [
            "Check redness marking twice daily — if spreading, return to A&E",
            "Complete FULL antibiotic course",
            "Change dressings daily with saline cleaning",
            "Ensure wound can drain — do not occlude if producing pus",
            "Monitor blood sugar (infection spikes glucose even in non-diabetics)",
        ],
        "medications": [
            "Non-purulent cellulitis (Strep): Phenoxymethylpenicillin 500mg 4×/day × 5–7 days",
            "Purulent / Staphylococcal: Flucloxacillin 500mg 4×/day × 5–7 days",
            "Penicillin allergy: Clarithromycin 500mg 2×/day",
            "MRSA suspected: Trimethoprim-Sulfamethoxazole or Doxycycline",
            "Severe (IV): Benzylpenicillin + Flucloxacillin or Piperacillin-Tazobactam",
        ],
        "warning_signs": [
            "Redness spreading despite 48 hours of antibiotics",
            "Blistering over infected area (bullous cellulitis — more severe)",
            "Black discolouration (necrotising fasciitis — emergency)",
            "Severe systemic illness: rigors, confusion, hypotension",
            "Crepitus (crackling sensation in tissue — gas gangrene)",
        ],
        "seek_doctor_within": "Within 24 hours — all spreading infections require medical review",
        "seek_emergency": True,
        "nutrition_tips": [
            "High protein to fuel immune response",
            "Vitamin C and Zinc for immune cell function",
            "Probiotic foods during and after antibiotics",
            "Adequate hydration — 2–3 litres/day",
        ],
        "do_not": [
            "Do NOT squeeze or manually express pus (spreads infection)",
            "Do NOT stop antibiotics early if improving",
            "Do NOT use topical antibiotics alone for spreading infection",
            "Do NOT ignore worsening redness 48h into treatment",
        ],
        "prognosis": "Good with prompt antibiotics. Risk of necrotising fasciitis if Streptococcal — life-threatening if delayed.",
    },

    "Surgical Wound / Post-Op Incision": {
        "category": "Surgical",
        "emoji": "🏥",
        "severity_level": "MODERATE",
        "severity_score": 5,
        "description": "Planned incision made by surgeon — typically closed with sutures, staples, or adhesive strips. Requires careful post-operative wound care.",
        "causes": ["Elective surgery", "Emergency surgery", "Caesarean section", "Laparoscopic port sites"],
        "visible_signs": [
            "Clean linear incision, closed by sutures/staples/glue",
            "Mild redness and swelling at wound edges (normal Day 1–5)",
            "Serosanguinous (blood-tinged clear) discharge initially normal",
            "Possible drains in situ",
        ],
        "infection_risk": "LOW (clean), MEDIUM (contaminated surgery)",
        "healing_time_min_days": 7,
        "healing_time_max_days": 42,
        "healing_phases": [
            ("Haemostasis", "Intraoperative", "Surgeon achieves haemostasis at closure"),
            ("Inflammatory", "Day 1–4", "Expected redness, warmth, mild oedema around incision"),
            ("Proliferative", "Day 4–21", "Wound gains tensile strength rapidly — 80% at 6 weeks"),
            ("Remodelling", "Day 21–365", "Scar matures and softens"),
        ],
        "immediate_actions": [
            "Keep wound dry for 24–48 hours post-surgery",
            "Do NOT remove dressing placed by surgeon prematurely",
            "Do NOT probe or pick at wound edges",
            "Report fever > 38°C to surgical team",
            "If wound opens (dehiscence) — cover with clean cloth, seek care immediately",
        ],
        "recommended_dressing": "Post-op absorbent dressing for 48h; then transparent film or simple dry dressing until suture removal",
        "smartgel_protocol": "SmartGel pH 5.5 Post-Surgical Hydrogel — maintains optimal acidic environment, prevents SSI (surgical site infection)",
        "daily_care": [
            "Clean with saline from Day 2 — wipe gently along incision (not across)",
            "Pat dry — do NOT rub",
            "Leave scab/crusting alone — do not pick",
            "Scar massage from 6 weeks: circular firm massage with moisturiser",
            "Silicone gel strips from 2 weeks — proven to reduce hypertrophic scarring",
        ],
        "medications": [
            "Surgical team prescribes: antibiotics only if contaminated case",
            "Pain: Regular Paracetamol + NSAIDs (follow discharge plan)",
            "Blood clot prevention: LMWH (Tinzaparin/Enoxaparin) as prescribed",
            "Wound closure: Do NOT remove sutures — done at 5–14 days by clinician",
        ],
        "warning_signs": [
            "Purulent discharge between sutures",
            "Wound edges separating (dehiscence)",
            "Temperature >38°C at Day 3+",
            "Increasing rather than decreasing pain",
            "Haematoma: firm, expanding painful swelling under wound",
        ],
        "seek_doctor_within": "Contact surgical team within 24 hours if concerns; Emergency if wound fully opens",
        "seek_emergency": False,
        "nutrition_tips": [
            "Pre-op optimisation: protein loading improves post-op healing",
            "Post-op: protein 1.5–2g/kg/day",
            "Vitamin C 500mg daily from Day 1 post-op",
            "Avoid alcohol for minimum 4 weeks (impairs immune response)",
            "Stay well-hydrated — reduces risk of wound breakdown",
        ],
        "do_not": [
            "Do NOT submerge in bath/pool until fully healed and sutures removed",
            "Do NOT apply antiseptic cream to clean healing incision",
            "Do NOT lift heavy objects (increases wound tension)",
            "Do NOT smoke (dramatically impairs wound healing)",
        ],
        "prognosis": "Excellent for clean surgical wounds. Risk of hypertrophic/keloid scarring depends on location, genetics, and closure technique.",
    },

    "Venous Leg Ulcer": {
        "category": "Chronic / Vascular",
        "emoji": "🦵",
        "severity_level": "MODERATE to SEVERE",
        "severity_score": 6,
        "description": "Chronic ulceration of the lower leg due to sustained venous hypertension and venous insufficiency. Most common chronic wound in adults.",
        "causes": ["Chronic venous insufficiency (varicose veins)", "Deep vein thrombosis (DVT) history", "Obesity", "Immobility", "Heart failure"],
        "visible_signs": [
            "Shallow ulcer, typically above medial malleolus (inner ankle)",
            "Irregular, sloping wound edges",
            "Haemosiderin staining — brown discolouration of surrounding skin",
            "Lipodermatosclerosis — indurated, woody, red-brown skin",
            "Leg oedema (ankle swelling)",
            "Exudate level: moderate to heavy",
        ],
        "infection_risk": "MEDIUM to HIGH",
        "healing_time_min_days": 42,
        "healing_time_max_days": 365,
        "healing_phases": [
            ("Chronic stall", "Ongoing until compression applied", "Venous hypertension prevents healing"),
            ("Compression therapy initiation", "Day 0", "Multi-layer compression ESSENTIAL — without it, healing impossible"),
            ("Granulation", "Weeks 2–12", "Wound fills under compression"),
            ("Epithelialisation", "Months", "Surface closure"),
        ],
        "immediate_actions": [
            "Assess ABI (Ankle-Brachial Index) BEFORE compression — arterial disease must be excluded",
            "Start 4-layer compression bandaging (40mmHg) if ABI >0.8",
            "Clean wound with saline — remove slough with dressing selection",
            "Elevate leg when resting — above heart level",
            "Refer to specialist tissue viability or vascular service",
        ],
        "recommended_dressing": "Under compression: Non-adherent contact layer (Mepitel One) + absorbent secondary. Cadexomer iodine for sloughy wounds. Silver for infected.",
        "smartgel_protocol": "SmartGel pH-Sensing Hydrogel — continuous pH monitoring flags infection early; supports autolytic debridement",
        "daily_care": [
            "Compression bandaging: changed 1–2 times weekly by specialist nurse",
            "Elevate legs when seated — rest foot on stool",
            "Regular walking exercise improves calf muscle pump",
            "Weight loss if BMI >30",
            "After healing: compression stockings CLASS 2–3 for life to prevent recurrence",
        ],
        "medications": [
            "Antibiotics only if clinically infected (not colonised)",
            "Aspirin 300mg/day: reduces ulcer healing time (evidence-based)",
            "Pentoxifylline 400mg 3×/day: improves microcirculation (use with compression)",
            "Diuretics: if cardiac oedema contributing",
        ],
        "warning_signs": [
            "Rapidly enlarging ulcer despite compression",
            "Systemic cellulitis spreading beyond wound",
            "Change in wound character — raised, rolled edges (consider malignancy/squamous cell carcinoma)",
            "Worsening pain (may indicate arterial involvement or infection)",
        ],
        "seek_doctor_within": "Within 1 week — all chronic leg ulcers require specialist assessment",
        "seek_emergency": False,
        "nutrition_tips": [
            "Protein: 1.5g/kg/day",
            "Vitamin C and Zinc for tissue repair",
            "Low sodium diet to reduce oedema",
            "Weight management — obesity increases venous pressure",
        ],
        "do_not": [
            "Do NOT apply compression without ABI measurement (arterial disease risk)",
            "Do NOT use zinc paste bandages without specialist guidance",
            "Do NOT rest with legs dependent (hanging down) for long periods",
            "Do NOT stop compression when wound heals — highest risk of recurrence",
        ],
        "prognosis": "70–80% heal within 12 weeks with proper compression therapy. 70% recur within 3 years without ongoing compression stockings.",
    },

    "Minor Blister": {
        "category": "Friction / Minor",
        "emoji": "🫧",
        "severity_level": "MILD",
        "severity_score": 1,
        "description": "Fluid-filled bubble of skin caused by friction, heat, or pressure. Protective fluid-filled pocket under epidermis.",
        "causes": ["New or ill-fitting footwear", "Prolonged friction (hiking, running)", "Burn (heat blister)", "Frostbite", "Contact dermatitis"],
        "visible_signs": [
            "Tense, dome-shaped fluid-filled bubble",
            "Clear (serous) or blood-tinged fluid",
            "Surrounding redness",
            "Painful under pressure",
            "Intact or ruptured",
        ],
        "infection_risk": "LOW",
        "healing_time_min_days": 3,
        "healing_time_max_days": 10,
        "healing_phases": [
            ("Blister formation", "0–24h", "Fluid accumulates as protective response"),
            ("Resolution (intact)", "Day 1–7", "Body reabsorbs fluid, new skin forms underneath"),
            ("Healed", "Day 7–10", "Old skin sloughs, new skin pink and tender"),
        ],
        "immediate_actions": [
            "Do NOT burst if intact and not too painful — it heals faster intact",
            "If large and painful, sterilise needle with alcohol, pierce at edge, drain fluid, leave roof intact",
            "Clean with antiseptic wipe",
            "Cover with hydrocolloid blister plaster (Compeed or similar)",
            "Address the cause: change footwear, add padding",
        ],
        "recommended_dressing": "Hydrocolloid blister plaster (Compeed) — best option; maintains moist environment, reduces pain",
        "smartgel_protocol": "SmartGel Hydrogel Sheet — conforms to contour, maintains pH 5.5, reduces friction recurrence",
        "daily_care": [
            "Change hydrocolloid dressing when gel pad is fully saturated",
            "If ruptured: clean with saline, apply non-adherent dressing",
            "Keep roof of blister intact as long as possible",
            "Moleskin padding around (not over) blister for pressure relief",
            "Gradually break in new footwear",
        ],
        "medications": [
            "Topical antiseptic if ruptured (Savlon or dilute Betadine)",
            "Topical antibiotic cream if showing infection signs",
            "Paracetamol for pain",
        ],
        "warning_signs": [
            "Redness spreading beyond blister margin",
            "Pus or foul-smelling discharge",
            "Multiple blisters without obvious friction cause (consider dermatological condition)",
            "Fever (blistering diseases can be systemic)",
        ],
        "seek_doctor_within": "Monitor at home — see GP if infection signs develop",
        "seek_emergency": False,
        "nutrition_tips": [
            "No specific nutritional intervention needed for minor blisters",
            "Vitamin E oil on healed area may reduce tenderness",
        ],
        "do_not": [
            "Do NOT rip blister roof off",
            "Do NOT use plasters with glue directly over blister (painful removal)",
            "Do NOT continue activity that caused blister without protection",
        ],
        "prognosis": "Excellent — heals completely within 1–2 weeks with no scarring.",
    },

    "Insect Sting / Bite Reaction": {
        "category": "Envenomation",
        "emoji": "🐝",
        "severity_level": "MILD to SEVERE",
        "severity_score": 3,
        "description": "Local or systemic reaction to insect venom or saliva. Usually mild but can be life-threatening in anaphylactic individuals.",
        "causes": ["Bee/wasp sting", "Mosquito bite", "Hornet sting", "Fire ant", "Spider bite", "Tick bite"],
        "visible_signs": [
            "Central sting/bite mark",
            "Localised wheal and flare (raised red bump)",
            "Itching and burning",
            "Possible retained stinger (bee)",
            "Mild swelling in local area",
            "SEVERE: urticaria (hives), facial swelling, difficulty breathing",
        ],
        "infection_risk": "LOW (unless scratched and broken)",
        "healing_time_min_days": 1,
        "healing_time_max_days": 7,
        "healing_phases": [
            ("Acute reaction", "0–2 hours", "Venom/saliva triggers histamine release"),
            ("Resolution", "Day 1–5", "Local inflammation subsides"),
            ("Complete healing", "Day 5–7", "Return to normal"),
        ],
        "immediate_actions": [
            "Remove stinger if visible — scrape out sideways (tweezers may squeeze venom sac)",
            "Wash area with soap and water",
            "Apply cold pack wrapped in cloth — 10 minutes on, 10 off",
            "Antihistamine tablet immediately (Cetirizine or Loratadine)",
            "ANAPHYLAXIS: Use Epipen if available, call 999/112 immediately",
        ],
        "recommended_dressing": "Hydrocortisone cream + non-adherent dressing if skin broken",
        "smartgel_protocol": "SmartGel Cooling Hydrogel — topical pain and itch relief, anti-inflammatory action",
        "daily_care": [
            "Avoid scratching — breaks skin and introduces infection",
            "Antihistamine for 3–5 days for persistent itch",
            "Calamine lotion for itch relief",
            "Check for tick: if embedded tick found — remove with tick removal tool, not hands",
            "After tick bite: watch for bullseye rash (erythema migrans) — indicates Lyme disease",
        ],
        "medications": [
            "Antihistamine: Cetirizine 10mg once daily or Loratadine 10mg",
            "Topical: Hydrocortisone 1% cream 2×/day for up to 7 days",
            "Severe local reaction: Oral prednisolone 30–40mg for 3 days",
            "Anaphylaxis: Adrenaline (Epinephrine) 0.3–0.5mg IM — EpiPen",
            "Post-anaphylaxis: Chlorphenamine 10mg IV + Hydrocortisone 200mg IV (hospital)",
        ],
        "warning_signs": [
            "Difficulty breathing or wheezing within minutes of sting",
            "Swelling of lips, tongue, throat",
            "Dizziness, collapse, loss of consciousness",
            "Widespread hives beyond sting site",
            "Bullseye rash after tick bite (Lyme disease)",
        ],
        "seek_doctor_within": "Monitor at home (mild); IMMEDIATELY if any signs of anaphylaxis",
        "seek_emergency": False,
        "nutrition_tips": [
            "Anti-inflammatory diet: omega-3 rich foods during reaction",
            "Avoid alcohol — worsens histamine response",
        ],
        "do_not": [
            "Do NOT squeeze stinger out (forces more venom in)",
            "Do NOT apply vinegar/bicarb (minimal evidence, can irritate)",
            "Do NOT ignore worsening symptoms over first hour",
            "Do NOT pull out embedded tick with bare hands (risk of pathogen transfer)",
        ],
        "prognosis": "Excellent for local reactions. Life-threatening if anaphylactic and Epipen not available. Lyme disease risk if tick not removed promptly.",
    },
}

WOUND_CATEGORIES = {
    "Traumatic": ["Abrasion (Road Rash / Graze)", "Laceration (Deep Cut)", "Puncture Wound"],
    "Thermal / Burns": ["Burn — First Degree (Superficial)", "Burn — Second Degree (Partial Thickness)"],
    "Contaminated / Bite": ["Animal Bite (Dog / Cat / Human)"],
    "Chronic / Complex": ["Chronic Diabetic Foot Ulcer", "Pressure Ulcer (Bedsore)", "Venous Leg Ulcer"],
    "Infected": ["Infected Wound / Cellulitis"],
    "Surgical": ["Surgical Wound / Post-Op Incision"],
    "Minor": ["Minor Blister", "Insect Sting / Bite Reaction"],
}

# ------------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------------
defaults = {
    "selected":        SCENARIO_KEYS[0],
    "sim_running":     False,
    "log":             [],
    "active_tab":      0,
    "wound_selected":  None,
    "wound_category":  None,
    "image_source":    "upload",
    "camera_image":    None,
    "image_received":  False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

TAB_DEFS = [
    {"icon": "📊", "label": "Dashboard",           "desc": "Live vitals & telemetry"},
    {"icon": "📈", "label": "pH Trend Analysis",   "desc": "Bar chart, gauge & comparison"},
    {"icon": "🗂️", "label": "Sensor Log",          "desc": "Event log & CSV export"},
    {"icon": "📋", "label": "Clinical Report",     "desc": "Summary & radar chart"},
    {"icon": "🩹", "label": "Wound Diagnosis",     "desc": "Full wound reference database"},
]

# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
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

    st.markdown("""
    <div style='font-size:0.68rem;font-weight:800;color:#8fa5b8;
                text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;'>Navigation</div>
    """, unsafe_allow_html=True)

    for idx, tdef in enumerate(TAB_DEFS):
        is_active = st.session_state.active_tab == idx
        ac  = "nav-active" if is_active else ""
        pip = "<div class='nav-pip'></div>" if is_active else ""
        st.markdown(f"""
        <div class='nav-item {ac}'>
          <div class='nav-icon'>{tdef['icon']}</div>
          <div style='flex:1;'>
            <div class='nav-label'>{tdef['label']}</div>
            <div class='nav-desc'>{tdef['desc']}</div>
          </div>{pip}
        </div>
        """, unsafe_allow_html=True)
        btn_lbl = "● Active" if is_active else "Open →"
        if st.button(btn_lbl, key=f"nav_{idx}", use_container_width=True,
                     type="primary" if is_active else "secondary"):
            st.session_state.active_tab = idx
            st.rerun()

    st.divider()
    st.markdown("#### 🧪 Clinical Scenario")
    scenario_idx = SCENARIO_KEYS.index(st.session_state.selected)
    chosen = st.radio("Select wound scenario:", SCENARIO_KEYS, index=scenario_idx, key="scenario_radio")
    if chosen != st.session_state.selected:
        st.session_state.selected = chosen
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
    <div style='background:#fff8f0;border:1.5px solid #fcd9a0;border-radius:10px;
                padding:10px 13px;font-size:0.83rem;color:#92400e;'>
      <b>⏱ Reapply in {sc_side["reapply_hours"]} hrs</b><br>
      <span style='color:#a16207;'>{sc_side["treatment"]}</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.caption("SmartGel IoT Healthcare Portal v4.2")
    st.caption("© 2025 SmartGel Medical Systems")

# ------------------------------------------------------------------
# ACTIVE SCENARIO
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

if sc["alert_type"] == "success":
    st.success(f"**Status {sc['status']}** — {sc['alert_msg']}")
else:
    st.error(f"**Status {sc['status']}** — {sc['alert_msg']}")

st.divider()

st.markdown("""
<div style='font-size:0.7rem;font-weight:800;color:#8fa5b8;
            text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;'>
  Quick Navigation
</div>
""", unsafe_allow_html=True)

nav_cols   = st.columns(5)
tab_colors = ["#1d6fa4", "#6d3fc0", "#1b8a5a", "#b45309", "#c0392b"]
for i, (tdef, ncol) in enumerate(zip(TAB_DEFS, nav_cols)):
    with ncol:
        active = st.session_state.active_tab == i
        bg   = tab_colors[i] if active else "#ffffff"
        fg   = "#ffffff"     if active else "#5a7184"
        bord = tab_colors[i] if active else "#dce6f0"
        shad = f"0 4px 12px {tab_colors[i]}33" if active else "none"
        st.markdown(f"""
        <div style='background:{bg};border:1.5px solid {bord};border-radius:12px;
                    padding:10px 6px;text-align:center;box-shadow:{shad};transition:all 0.2s;'>
          <div style='font-size:1.25rem;margin-bottom:3px;'>{tdef["icon"]}</div>
          <div style='font-size:0.7rem;font-weight:700;color:{fg};line-height:1.3;'>{tdef["label"]}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("✓ Here" if active else "Open", key=f"qnav_{i}",
                     use_container_width=True, type="primary" if active else "secondary"):
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
    "  🩹 Wound Diagnosis  ",
])

_active_tab = st.session_state.active_tab
st.markdown(f"""
<script>
(function() {{
  var idx = {_active_tab};
  function tryClick(attempt) {{
    var tabs = window.parent.document.querySelectorAll('[data-baseweb="tab"]');
    if (tabs.length > idx) {{ tabs[idx].click(); }}
    else if (attempt < 15) {{ setTimeout(function() {{ tryClick(attempt + 1); }}, 150); }}
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
    k1.metric("Current pH",      str(cur_ph),         f"{round(cur_ph - 7.0, 2):+.2f} vs neutral", delta_color=ph_delta_color)
    k2.metric("Wound Temp (°C)", f"{cur_temp} °C",    f"{round(cur_temp - 37.0, 1):+.1f} vs normal", delta_color="inverse")
    k3.metric("Moisture Level",  f"{cur_mois} %",     f"{round(cur_mois - 75.0, 1):+.1f} vs target", delta_color="inverse")
    k4.metric("Bacterial Load",  sc["bacterial_load"])

    st.divider()
    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.markdown('<span class="sec-hdr">Hydrogel Status</span>', unsafe_allow_html=True)
        gc   = sc["gel_color"]
        r_v  = int(gc[1:3], 16); g_v = int(gc[3:5], 16); b_v = int(gc[5:7], 16)
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
            ("🧴 Treatment",     sc["treatment"]),
            ("🔬 Healing Stage", sc["healing_stage"]),
            ("📡 Connection",    "BLE Active · 2.4 GHz · Nominal"),
            ("⏱ Reapply In",    f"{sc['reapply_hours']} hours"),
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
                    {"range": [4.0, 6.0],  "color": "#dcfce7"},
                    {"range": [6.0, 7.0],  "color": "#fef9c3"},
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
        df_log   = pd.DataFrame(st.session_state.log)
        total    = len(df_log)
        ok_cnt   = len(df_log[df_log["Status"] == "OK"])
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
                            colorscale=[[0,"#1b8a5a"],[0.5,"#d97706"],[1,"#dc2626"]],
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
        "Continue current protocol. Wound environment is stable and healing is progressing normally. Weekly monitoring recommended."
        if sc["bacterial_load"] == "LOW"
        else "IMMEDIATE clinical evaluation required. Alkaline pH shift confirms active bacterial colonisation. Consider systemic antibiotics and advanced wound debridement."
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
        r2  = int(gc2[1:3], 16); g2 = int(gc2[3:5], 16); b2 = int(gc2[5:7], 16)
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
# TAB 5 — WOUND DIAGNOSIS (built-in knowledge base, no AI/API)
# ==================================================================
with tab5:
    st.markdown("""
    <div style='background:linear-gradient(135deg,#1d6fa4 0%,#0a4a73 100%);
                border-radius:16px;padding:1.6rem 2rem;margin-bottom:1.2rem;'>
      <div style='font-family:Merriweather Sans,sans-serif;font-size:1.3rem;font-weight:800;
                  color:#ffffff;margin-bottom:5px;'>
        🩹 Clinical Wound Diagnosis & Reference Guide
      </div>
      <div style='font-size:0.84rem;color:#a8d4ed;line-height:1.6;'>
        Upload or capture a photo of the wound, then select a wound type to view comprehensive
        clinical guidance — causes, visible signs, treatment, medications, healing timeline,
        nutrition, and warning signs. All built-in, no internet required.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.warning(
        "⚠️ **Medical Disclaimer** — This reference guide is for informational and educational purposes only. "
        "It does **not** replace professional medical advice. Always consult a qualified healthcare provider "
        "for diagnosis and treatment, especially for serious wounds."
    )

    st.divider()

    # ── IMAGE UPLOAD / CAMERA SECTION ─────────────────────────────
    st.markdown("""
    <div style='font-size:0.7rem;font-weight:800;color:#8fa5b8;
                text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;'>
      📷 Step 1 — Provide Wound Image (Optional)
    </div>
    """, unsafe_allow_html=True)

    mode_c1, mode_c2, mode_c3 = st.columns([1, 1, 4])
    with mode_c1:
        if st.button(
            "📁 Upload File", use_container_width=True, key="mode_upload",
            type="primary" if st.session_state.image_source == "upload" else "secondary",
        ):
            st.session_state.image_source  = "upload"
            st.session_state.camera_image  = None
            st.session_state.image_received = False
            st.rerun()
    with mode_c2:
        if st.button(
            "📷 Use Camera", use_container_width=True, key="mode_camera",
            type="primary" if st.session_state.image_source == "camera" else "secondary",
        ):
            st.session_state.image_source  = "camera"
            st.session_state.image_received = False
            st.rerun()

    img_left, img_right = st.columns([1, 1])

    with img_left:
        if st.session_state.image_source == "upload":
            uploaded_file = st.file_uploader(
                "Drag & drop or click to browse",
                type=["jpg", "jpeg", "png", "webp", "bmp"],
                help="Supported: JPG, PNG, WEBP, BMP",
                key="wound_uploader",
            )
            if uploaded_file is not None:
                st.session_state.image_received = True
            else:
                st.session_state.image_received = False
            has_image   = uploaded_file is not None
            image_to_show = uploaded_file
        else:
            cam_result = st.camera_input(
                "Take a photo of the wound",
                key="camera_widget",
            )
            if cam_result is not None:
                st.session_state.camera_image   = cam_result
                st.session_state.image_received = True
            has_image   = st.session_state.camera_image is not None
            image_to_show = st.session_state.camera_image

    with img_right:
        if has_image and image_to_show is not None:
            st.image(image_to_show, caption="Wound image received", use_container_width=True)

    # ── GOT IT confirmation — shown immediately after image provided ──
    if st.session_state.image_received and has_image:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1b8a5a 0%,#0f5c3a 100%);
                    border-radius:14px;padding:1.4rem 1.8rem;margin:1rem 0;
                    display:flex;align-items:center;gap:16px;'>
          <div style='font-size:2.8rem;'>✅</div>
          <div>
            <div style='font-family:Merriweather Sans,sans-serif;font-weight:800;
                        font-size:1.25rem;color:#ffffff;letter-spacing:-0.01em;'>
              Got it!
            </div>
            <div style='font-size:0.85rem;color:#a7dfbe;margin-top:4px;line-height:1.5;'>
              Your wound image has been received. Now select a wound type below
              to get the full diagnosis, treatment plan, and healing timeline.
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div style='font-size:0.7rem;font-weight:800;color:#8fa5b8;
                text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;'>
      🩹 Step 2 — Select Wound Type for Diagnosis
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    cat_cols = st.columns(len(WOUND_CATEGORIES))
    cat_colors = {
        "Traumatic":         ("#1d6fa4", "#e8f4fb"),
        "Thermal / Burns":   ("#c0392b", "#fdecea"),
        "Contaminated / Bite": ("#ea580c", "#fff7ed"),
        "Chronic / Complex": ("#6d3fc0", "#f0ebfb"),
        "Infected":          ("#dc2626", "#fdecea"),
        "Surgical":          ("#1b8a5a", "#e6f6ef"),
        "Minor":             ("#b45309", "#fef3c7"),
    }

    for col, (cat_name, _) in zip(cat_cols, WOUND_CATEGORIES.items()):
        with col:
            is_sel = st.session_state.wound_category == cat_name
            fc, bc = cat_colors.get(cat_name, ("#1d6fa4", "#e8f4fb"))
            bg     = fc if is_sel else "#ffffff"
            fg     = "#ffffff" if is_sel else "#1a2b3c"
            brd    = fc
            st.markdown(f"""
            <div style='background:{bg};border:2px solid {brd};border-radius:12px;
                        padding:10px 6px;text-align:center;font-size:0.75rem;
                        font-weight:700;color:{fg};min-height:55px;
                        display:flex;align-items:center;justify-content:center;
                        line-height:1.3;cursor:pointer;transition:all 0.2s;'>
              {cat_name}
            </div>
            """, unsafe_allow_html=True)
            if st.button("Select" if not is_sel else "✓ Selected",
                         key=f"cat_{cat_name}",
                         use_container_width=True,
                         type="primary" if is_sel else "secondary"):
                st.session_state.wound_category = cat_name
                st.session_state.wound_selected = None
                st.rerun()

    st.divider()

    # ── STEP 2: Wound type selection ────────────────────────────────
    if st.session_state.wound_category:
        wound_list = WOUND_CATEGORIES[st.session_state.wound_category]
        wnd_cols   = st.columns(min(len(wound_list), 3))
        for i, wname in enumerate(wound_list):
            wdata  = WOUND_DATABASE[wname]
            is_sel = st.session_state.wound_selected == wname
            sev    = wdata["severity_level"]
            sev_color = ("#1b8a5a" if "MILD" in sev else
                         "#b45309" if "MODERATE" in sev else
                         "#c0392b" if "SEVERE" in sev else "#dc2626")
            with wnd_cols[i % 3]:
                st.markdown(f"""
                <div style='background:{"#e8f4fb" if is_sel else "#fff"};
                            border:{"2px solid #1d6fa4" if is_sel else "1.5px solid #dce6f0"};
                            border-radius:12px;padding:14px;margin-bottom:6px;'>
                  <div style='font-size:1.5rem;margin-bottom:4px;'>{wdata["emoji"]}</div>
                  <div style='font-weight:700;font-size:0.85rem;color:#1a2b3c;margin-bottom:4px;'>{wname}</div>
                  <div style='font-size:0.72rem;font-weight:700;color:{sev_color};
                              background:{sev_color}18;border-radius:50px;
                              padding:2px 8px;display:inline-block;'>{sev}</div>
                  <div style='font-size:0.72rem;color:#5a7184;margin-top:4px;'>
                    🕐 {wdata["healing_time_min_days"]}–{wdata["healing_time_max_days"]} days
                  </div>
                </div>
                """, unsafe_allow_html=True)
                btn_label = "✓ Viewing" if is_sel else "View Diagnosis →"
                if st.button(btn_label, key=f"wnd_{wname}",
                             use_container_width=True,
                             type="primary" if is_sel else "secondary"):
                    st.session_state.wound_selected = wname
                    st.rerun()

        st.divider()
    else:
        st.info("☝️ Select a wound category above to begin.")

    # ── STEP 3: Full diagnosis display ──────────────────────────────
    if st.session_state.wound_selected:
        wd = WOUND_DATABASE[st.session_state.wound_selected]

        sev_color_map = {
            "MILD":     ("#1b8a5a", "#e6f6ef"),
            "MODERATE": ("#b45309", "#fef3c7"),
            "SEVERE":   ("#c0392b", "#fdecea"),
            "CRITICAL": ("#6d3fc0", "#f0ebfb"),
        }
        sev_key   = wd["severity_level"].split()[0]
        sev_c, sev_bg = sev_color_map.get(sev_key, ("#5a7184", "#f4f7fb"))

        # Header card
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,{sev_c}22 0%,{sev_c}08 100%);
                    border:2px solid {sev_c}44;border-radius:16px;
                    padding:1.4rem 1.8rem;margin-bottom:1rem;'>
          <div style='display:flex;align-items:center;gap:16px;'>
            <div style='font-size:3rem;'>{wd["emoji"]}</div>
            <div>
              <div style='font-family:Merriweather Sans,sans-serif;font-size:1.4rem;
                          font-weight:800;color:#1a2b3c;'>{st.session_state.wound_selected}</div>
              <div style='margin-top:6px;'>
                <span style='background:{sev_c};color:#fff;font-weight:700;font-size:0.75rem;
                             border-radius:50px;padding:3px 14px;margin-right:8px;'>
                  {wd["severity_level"]}
                </span>
                <span style='background:#eaf1f8;color:#1d6fa4;font-weight:700;font-size:0.75rem;
                             border-radius:50px;padding:3px 14px;margin-right:8px;'>
                  {wd["category"]}
                </span>
                <span style='background:#f4f7fb;color:#5a7184;font-weight:600;font-size:0.75rem;
                             border-radius:50px;padding:3px 14px;'>
                  ⏱ {wd["healing_time_min_days"]}–{wd["healing_time_max_days"]} days to heal
                </span>
              </div>
              <div style='font-size:0.84rem;color:#5a7184;margin-top:8px;line-height:1.5;'>
                {wd["description"]}
              </div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Emergency banner
        if wd["seek_emergency"]:
            st.error("🚨 **SEEK EMERGENCY CARE** — This wound type requires immediate medical attention. "
                     "Go to A&E / Emergency Department or call emergency services.")

        # Top metrics row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Severity Score",  f"{wd['severity_score']} / 10")
        m2.metric("Infection Risk",  wd["infection_risk"])
        m3.metric("Healing (min)",   f"{wd['healing_time_min_days']} days")
        m4.metric("Healing (max)",   f"{wd['healing_time_max_days']} days")

        st.divider()

        # ── Severity gauge + Healing Phases ──
        gauge_col, phases_col = st.columns([1, 1])

        with gauge_col:
            st.markdown('<span class="sec-hdr">Severity Assessment</span>', unsafe_allow_html=True)
            fig_sev = go.Figure(go.Indicator(
                mode="gauge+number", value=wd["severity_score"],
                number={"font": {"size": 52, "color": sev_c}, "suffix": "/10"},
                gauge={
                    "axis": {"range": [0, 10], "nticks": 11,
                             "tickfont": {"size": 10}, "tickcolor": "#5a7184"},
                    "bar":  {"color": sev_c, "thickness": 0.28},
                    "bgcolor": "#f4f8fc", "borderwidth": 1, "bordercolor": "#dce6f0",
                    "steps": [
                        {"range": [0, 3.5],  "color": "#dcfce7"},
                        {"range": [3.5, 6.0],"color": "#fef9c3"},
                        {"range": [6.0, 8.5],"color": "#fee2e2"},
                        {"range": [8.5, 10], "color": "#f0ebfb"},
                    ],
                },
                title={
                    "text": "Wound Severity<br>"
                            "<span style='font-size:11px;color:#5a7184'>"
                            "1–3 Mild · 4–6 Moderate · 7–8 Severe · 9–10 Critical</span>",
                    "font": {"size": 13, "color": "#1a2b3c"},
                },
            ))
            fig_sev.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", height=280,
                margin=dict(l=20, r=20, t=60, b=10),
            )
            st.plotly_chart(fig_sev, use_container_width=True, config={"displayModeBar": False})

            # Doctor timeline
            st.markdown(f"""
            <div style='background:#fff8f0;border:1.5px solid #fcd9a0;border-radius:10px;
                        padding:12px 15px;margin-top:8px;'>
              <div style='font-size:0.8rem;font-weight:800;color:#92400e;margin-bottom:4px;'>
                ⏰ When to See a Doctor
              </div>
              <div style='font-size:0.84rem;color:#a16207;font-weight:600;'>
                {wd["seek_doctor_within"]}
              </div>
            </div>
            """, unsafe_allow_html=True)

        with phases_col:
            st.markdown('<span class="sec-hdr">Healing Phases & Timeline</span>', unsafe_allow_html=True)
            phase_colors = ["#1d6fa4", "#d97706", "#1b8a5a", "#6d3fc0"]
            for pi, phase in enumerate(wd["healing_phases"]):
                pc = phase_colors[pi % len(phase_colors)]
                st.markdown(f"""
                <div style='display:flex;gap:12px;margin-bottom:10px;'>
                  <div style='width:32px;height:32px;border-radius:50%;background:{pc};
                              color:#fff;font-weight:800;font-size:0.75rem;
                              display:flex;align-items:center;justify-content:center;
                              flex-shrink:0;margin-top:2px;'>{pi+1}</div>
                  <div style='flex:1;background:#f4f8fc;border-radius:10px;padding:9px 12px;
                              border-left:3px solid {pc};'>
                    <div style='font-weight:700;font-size:0.84rem;color:{pc};'>{phase[0]}</div>
                    <div style='font-size:0.76rem;font-weight:700;color:#5a7184;'>{phase[1]}</div>
                    <div style='font-size:0.79rem;color:#1a2b3c;margin-top:3px;'>{phase[2]}</div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # ── Causes + Visible Signs ──
        causes_col, signs_col = st.columns(2)

        with causes_col:
            st.markdown('<span class="sec-hdr">Common Causes</span>', unsafe_allow_html=True)
            for cause in wd["causes"]:
                st.markdown(f"""
                <div style='background:#f4f8fc;border-left:3px solid #1d6fa4;
                            padding:7px 12px;border-radius:0 8px 8px 0;
                            font-size:0.83rem;margin-bottom:5px;color:#1a2b3c;'>
                  🔹 {cause}
                </div>
                """, unsafe_allow_html=True)

        with signs_col:
            st.markdown('<span class="sec-hdr">Visible Signs to Look For</span>', unsafe_allow_html=True)
            for sign in wd["visible_signs"]:
                st.markdown(f"""
                <div style='background:#fff8f0;border-left:3px solid #d97706;
                            padding:7px 12px;border-radius:0 8px 8px 0;
                            font-size:0.83rem;margin-bottom:5px;color:#1a2b3c;'>
                  👁 {sign}
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # ── Immediate Actions + Dressing ──
        imm_col, dress_col = st.columns([1, 1])

        with imm_col:
            st.markdown('<span class="sec-hdr" style="border-bottom-color:#b45309;">Immediate Actions</span>',
                        unsafe_allow_html=True)
            for i, step in enumerate(wd["immediate_actions"], 1):
                st.markdown(
                    f"<div class='action-item' style='background:#fef3c7;border:1px solid #fde68a;'>"
                    f"<span class='action-num' style='color:#b45309;min-width:20px;'>{i}.</span>"
                    f"<span style='color:#1a2b3c;'>{step}</span></div>",
                    unsafe_allow_html=True,
                )

        with dress_col:
            st.markdown('<span class="sec-hdr" style="border-bottom-color:#1d6fa4;">Dressing & SmartGel Protocol</span>',
                        unsafe_allow_html=True)
            st.markdown(f"""
            <div style='background:#e8f4fb;border:1.5px solid #5fa8d3;border-radius:10px;
                        padding:12px 15px;margin-bottom:10px;'>
              <div style='font-size:0.75rem;font-weight:800;color:#1d6fa4;text-transform:uppercase;
                          letter-spacing:0.06em;margin-bottom:5px;'>Recommended Dressing</div>
              <div style='font-size:0.84rem;color:#1a2b3c;'>{wd["recommended_dressing"]}</div>
            </div>
            <div style='background:#e6f6ef;border:1.5px solid #86efac;border-radius:10px;
                        padding:12px 15px;'>
              <div style='font-size:0.75rem;font-weight:800;color:#1b8a5a;text-transform:uppercase;
                          letter-spacing:0.06em;margin-bottom:5px;'>🧪 SmartGel Protocol</div>
              <div style='font-size:0.84rem;color:#1a2b3c;'>{wd["smartgel_protocol"]}</div>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ── Medications + Daily Care ──
        med_col, care_col = st.columns(2)

        with med_col:
            st.markdown('<span class="sec-hdr" style="border-bottom-color:#6d3fc0;">Medications & Treatment</span>',
                        unsafe_allow_html=True)
            for med in wd["medications"]:
                st.markdown(f"""
                <div style='background:#f0ebfb;border-left:3px solid #6d3fc0;
                            padding:7px 12px;border-radius:0 8px 8px 0;
                            font-size:0.82rem;margin-bottom:5px;color:#1a2b3c;'>
                  💊 {med}
                </div>
                """, unsafe_allow_html=True)

        with care_col:
            st.markdown('<span class="sec-hdr" style="border-bottom-color:#1b8a5a;">Daily Care Instructions</span>',
                        unsafe_allow_html=True)
            for i, step in enumerate(wd["daily_care"], 1):
                st.markdown(
                    f"<div class='action-item' style='background:#e6f6ef;border:1px solid #a7dfbe;'>"
                    f"<span class='action-num' style='color:#1b8a5a;min-width:20px;'>{i}.</span>"
                    f"<span style='color:#1a2b3c;'>{step}</span></div>",
                    unsafe_allow_html=True,
                )

        st.divider()

        # ── Nutrition + Warning Signs ──
        nutr_col, warn_col = st.columns(2)

        with nutr_col:
            st.markdown('<span class="sec-hdr" style="border-bottom-color:#0891b2;">Nutrition for Healing</span>',
                        unsafe_allow_html=True)
            for tip in wd["nutrition_tips"]:
                st.markdown(f"""
                <div style='background:#e0f2fe;border-left:3px solid #0891b2;
                            padding:7px 12px;border-radius:0 8px 8px 0;
                            font-size:0.82rem;margin-bottom:5px;color:#1a2b3c;'>
                  🥗 {tip}
                </div>
                """, unsafe_allow_html=True)

        with warn_col:
            st.markdown('<span class="sec-hdr" style="border-bottom-color:#c0392b;">⚠️ Warning Signs — Seek Help If:</span>',
                        unsafe_allow_html=True)
            for sign in wd["warning_signs"]:
                st.markdown(
                    f"<div class='action-item' style='background:#fdecea;border:1px solid #fca5a5;'>"
                    f"<span style='color:#c0392b;flex-shrink:0;font-size:1rem;'>🔴</span>"
                    f"<span style='color:#1a2b3c;'>{sign}</span></div>",
                    unsafe_allow_html=True,
                )

        st.divider()

        # ── Do NOT section ──
        st.markdown('<span class="sec-hdr" style="border-bottom-color:#dc2626;">❌ What NOT To Do</span>',
                    unsafe_allow_html=True)
        donot_cols = st.columns(min(len(wd["do_not"]), 2))
        for i, item in enumerate(wd["do_not"]):
            with donot_cols[i % 2]:
                st.markdown(f"""
                <div style='background:#fdecea;border:1.5px solid #fca5a5;border-radius:10px;
                            padding:9px 13px;margin-bottom:7px;font-size:0.83rem;color:#7f1d1d;
                            font-weight:600;'>
                  ❌ {item}
                </div>
                """, unsafe_allow_html=True)

        st.divider()

        # ── Prognosis ──
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#1b8a5a22 0%,#1b8a5a08 100%);
                    border:1.5px solid #86efac;border-radius:14px;padding:1.2rem 1.6rem;'>
          <div style='font-family:Merriweather Sans,sans-serif;font-weight:800;
                      font-size:0.95rem;color:#1b8a5a;margin-bottom:6px;'>
            📈 Prognosis & Expected Outcome
          </div>
          <div style='font-size:0.88rem;color:#1a2b3c;line-height:1.6;'>
            {wd["prognosis"]}
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ── Export ──
        export_rows = [
            ("Wound Type",           st.session_state.wound_selected),
            ("Category",             wd["category"]),
            ("Severity Level",       wd["severity_level"]),
            ("Severity Score",       str(wd["severity_score"])),
            ("Infection Risk",       wd["infection_risk"]),
            ("Healing Time (days)",  f"{wd['healing_time_min_days']}–{wd['healing_time_max_days']}"),
            ("See Doctor Within",    wd["seek_doctor_within"]),
            ("Seek Emergency",       str(wd["seek_emergency"])),
            ("Recommended Dressing", wd["recommended_dressing"]),
            ("SmartGel Protocol",    wd["smartgel_protocol"]),
            ("Causes",               "; ".join(wd["causes"])),
            ("Visible Signs",        "; ".join(wd["visible_signs"])),
            ("Immediate Actions",    "; ".join(wd["immediate_actions"])),
            ("Medications",          "; ".join(wd["medications"])),
            ("Daily Care",           "; ".join(wd["daily_care"])),
            ("Nutrition Tips",       "; ".join(wd["nutrition_tips"])),
            ("Warning Signs",        "; ".join(wd["warning_signs"])),
            ("Do Not Do",            "; ".join(wd["do_not"])),
            ("Prognosis",            wd["prognosis"]),
            ("Report Generated",     datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]
        df_wound_export = pd.DataFrame(export_rows, columns=["Parameter", "Detail"])

        ex1, ex2 = st.columns(2)
        with ex1:
            st.download_button(
                "📥 Download Wound Diagnosis Report (CSV)",
                df_wound_export.to_csv(index=False),
                f"smartgel_wound_{st.session_state.wound_selected[:30].replace(' ','_')}.csv",
                "text/csv", type="primary", use_container_width=True,
                key="dl_wound",
            )
        with ex2:
            if st.button("🔄 Select a Different Wound Type", use_container_width=True, key="clear_wound"):
                st.session_state.wound_selected = None
                st.rerun()

    elif not st.session_state.wound_category:
        # Show overview summary table of all wound types
        st.markdown('<span class="sec-hdr">All Wound Types — Quick Reference</span>', unsafe_allow_html=True)
        overview_rows = []
        for wname, wdata in WOUND_DATABASE.items():
            overview_rows.append({
                "Wound Type":     f"{wdata['emoji']} {wname}",
                "Category":       wdata["category"],
                "Severity":       wdata["severity_level"],
                "Score /10":      wdata["severity_score"],
                "Infection Risk": wdata["infection_risk"],
                "Healing Days":   f"{wdata['healing_time_min_days']}–{wdata['healing_time_max_days']}",
                "See Doctor":     wdata["seek_doctor_within"],
                "Emergency":      "🚨 YES" if wdata["seek_emergency"] else "No",
            })
        df_overview = pd.DataFrame(overview_rows)
        st.dataframe(df_overview, use_container_width=True, hide_index=True, height=420)
        st.caption(f"📊 {len(WOUND_DATABASE)} wound types in database across {len(WOUND_CATEGORIES)} categories.")
