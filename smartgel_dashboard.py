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

DAYS = ["Day " + str(i + 1) for i in range(10)]
SCENARIO_KEYS = list(SCENARIOS.keys())
CHART_COLORS  = ["#d946a8", "#dc2626", "#ea580c"]

# ------------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------------
if "selected"    not in st.session_state:
    st.session_state.selected    = SCENARIO_KEYS[0]
if "sim_running" not in st.session_state:
    st.session_state.sim_running = False
if "log"         not in st.session_state:
    st.session_state.log         = []
if "wound_analysis" not in st.session_state:
    st.session_state.wound_analysis = None

# ------------------------------------------------------------------
# SIDEBAR
# ------------------------------------------------------------------
with st.sidebar:
    st.title("SmartGel IoT Portal")
    st.caption("Biocompatible Nanosensor Monitoring")
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
        if st.button("Start", use_container_width=True, type="primary"):
            st.session_state.sim_running = True
    with col_b:
        if st.button("Stop", use_container_width=True):
            st.session_state.sim_running = False

    if st.button("Clear Log", use_container_width=True):
        st.session_state.log = []
        st.success("Log cleared.")

    st.divider()
    st.subheader("Reapplication Reminder")
    st.warning(
        "Reapply in " + str(sc_side["reapply_hours"]) + " hours\n\n"
        "Treatment: " + sc_side["treatment"]
    )
    st.divider()
    st.subheader("🔑 AI Analysis Key")
    st.caption("Required for Wound Image Analysis tab.")
    sidebar_api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-...",
        help="Enter your Anthropic API key, or set ANTHROPIC_API_KEY in Streamlit secrets.",
    )
    if sidebar_api_key:
        st.session_state["sidebar_api_key"] = sidebar_api_key
    st.divider()
    st.caption("SmartGel IoT Healthcare Portal v3.0")
    st.caption("(c) 2025 SmartGel Medical Systems")

# ------------------------------------------------------------------
# ACTIVE SCENARIO
# ------------------------------------------------------------------
sc    = SCENARIOS[st.session_state.selected]
noise = noise_level

# ------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------
st.title("SmartGel IoT Healthcare Portal")
st.caption(
    "LIVE  |  BLE Uplink Active  |  Biocompatible Nanosensor Monitoring  |  "
    + datetime.now().strftime("%Y-%m-%d  %H:%M:%S")
)
st.divider()

if sc["alert_type"] == "success":
    st.success("STATUS " + sc["status"] + " -- " + sc["alert_msg"])
else:
    st.error("STATUS " + sc["status"] + " -- " + sc["alert_msg"])

st.divider()

# ------------------------------------------------------------------
# TABS
# ------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "  Dashboard  ",
    "  pH Trend Analysis  ",
    "  Sensor Log  ",
    "  Clinical Report  ",
    "  🩹 Wound Image Analysis  ",
])

# ==================================================================
# TAB 1 -- DASHBOARD
# ==================================================================
with tab1:

    cur_ph   = round(sc["ph_readings"][-1] + random.uniform(-noise, noise), 2)
    cur_temp = round(random.uniform(*sc["temp_range"]), 1)
    cur_mois = round(random.uniform(*sc["moisture_range"]), 1)

    k1, k2, k3, k4 = st.columns(4)

    ph_delta_color = "inverse" if cur_ph > 7.0 else "normal"
    k1.metric(
        label="Current pH",
        value=str(cur_ph),
        delta=str(round(cur_ph - 7.0, 2)) + " vs neutral",
        delta_color=ph_delta_color,
    )
    k2.metric(
        label="Wound Temp (C)",
        value=str(cur_temp) + " C",
        delta=str(round(cur_temp - 37.0, 1)) + " vs normal",
        delta_color="inverse",
    )
    k3.metric(
        label="Moisture Level",
        value=str(cur_mois) + " %",
        delta=str(round(cur_mois - 75.0, 1)) + " vs target",
        delta_color="inverse",
    )
    k4.metric(
        label="Bacterial Load",
        value=sc["bacterial_load"],
    )

    st.divider()

    left_col, right_col = st.columns([1, 2])

    with left_col:
        st.subheader("Hydrogel Physical Status")

        gc = sc["gel_color"]
        r_val = int(gc[1:3], 16)
        g_val = int(gc[3:5], 16)
        b_val = int(gc[5:7], 16)

        fig_orb = go.Figure()
        fig_orb.add_shape(
            type="circle",
            x0=0.25, y0=0.55, x1=0.75, y1=0.95,
            xref="paper", yref="paper",
            fillcolor=gc,
            line_color="rgba(" + str(r_val) + "," + str(g_val) + "," + str(b_val) + ",0.4)",
            line_width=6,
        )
        fig_orb.add_annotation(
            x=0.5, y=0.75,
            xref="paper", yref="paper",
            text="<b>pH " + str(cur_ph) + "</b>",
            showarrow=False,
            font=dict(size=22, color="#ffffff"),
        )
        fig_orb.add_annotation(
            x=0.5, y=0.35,
            xref="paper", yref="paper",
            text="<b>STATUS: " + sc["status"] + "</b>",
            showarrow=False,
            font=dict(size=14, color=gc),
        )
        fig_orb.add_annotation(
            x=0.5, y=0.18,
            xref="paper", yref="paper",
            text=sc["status_detail"],
            showarrow=False,
            font=dict(size=10, color="#475569"),
        )
        fig_orb.update_layout(
            paper_bgcolor="#dbeafe",
            plot_bgcolor="#dbeafe",
            height=220,
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
        st.plotly_chart(fig_orb, use_container_width=True,
                        config={"displayModeBar": False})

        st.info("Treatment: " + sc["treatment"])
        st.info("Healing Stage: " + sc["healing_stage"])
        st.info("Connection: BLE Active | 2.4 GHz | All Nominal")
        st.info("Reapply in: " + str(sc["reapply_hours"]) + " hours")

    with right_col:
        st.subheader("pH Telemetry -- 10-Day Trend")

        ph_vals = [
            round(v + random.uniform(-noise, noise), 2)
            for v in sc["ph_readings"]
        ]

        fig_trend = go.Figure()
        fig_trend.add_hrect(
            y0=7.0, y1=10.5,
            fillcolor="rgba(220,38,38,0.07)",
            line_width=0,
            annotation_text="Alkaline Danger Zone (pH > 7)",
            annotation_position="top left",
            annotation_font_color="#dc2626",
            annotation_font_size=11,
        )
        fig_trend.add_hrect(
            y0=4.0, y1=6.0,
            fillcolor="rgba(22,163,74,0.07)",
            line_width=0,
            annotation_text="Healthy Acidic Range (pH < 6)",
            annotation_position="bottom left",
            annotation_font_color="#16a34a",
            annotation_font_size=11,
        )
        fig_trend.add_trace(go.Scatter(
            x=DAYS,
            y=ph_vals,
            mode="lines+markers",
            name="pH Reading",
            line=dict(color=sc["line_color"], width=3, shape="spline"),
            marker=dict(
                size=10,
                color=ph_vals,
                colorscale=[
                    [0.0,  "#16a34a"],
                    [0.4,  "#0891b2"],
                    [0.7,  "#d97706"],
                    [1.0,  "#dc2626"],
                ],
                cmin=5, cmax=9,
                line=dict(color="#ffffff", width=2),
                showscale=False,
            ),
            fill="tozeroy",
            fillcolor=sc["fill_color"],
            hovertemplate="<b>%{x}</b><br>pH = %{y:.2f}<extra></extra>",
        ))
        fig_trend.add_hline(
            y=7.0,
            line_dash="dash",
            line_color="#dc2626",
            line_width=1,
        )
        fig_trend.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#f0f6fb",
            height=340,
            margin=dict(l=10, r=20, t=20, b=10),
            xaxis=dict(
                showgrid=False,
                tickfont=dict(size=11, color="#475569"),
                color="#475569",
            ),
            yaxis=dict(
                gridcolor="#cbd5e1",
                range=[4, 10.5],
                title="pH Value",
                color="#475569",
                tickfont=dict(size=11),
            ),
            showlegend=False,
        )
        st.plotly_chart(fig_trend, use_container_width=True,
                        config={"displayModeBar": False})

        s1, s2, s3 = st.columns(3)
        s1.metric("Min pH (10-day)", str(min(sc["ph_readings"])))
        s2.metric("Max pH (10-day)", str(max(sc["ph_readings"])))
        s3.metric(
            "Mean pH (10-day)",
            str(round(sum(sc["ph_readings"]) / 10, 2)),
        )

# ==================================================================
# TAB 2 -- pH TREND ANALYSIS
# ==================================================================
with tab2:
    st.subheader("Advanced pH Trend Analysis")

    ph_vals2 = [
        round(v + random.uniform(-noise_level, noise_level), 2)
        for v in sc["ph_readings"]
    ]

    col_bar, col_gauge = st.columns(2)

    with col_bar:
        st.markdown("**Daily pH Bar Chart**")
        bar_colors = [
            "#16a34a" if v < 6.0 else ("#d97706" if v < 7.0 else "#dc2626")
            for v in ph_vals2
        ]
        fig_bar = go.Figure(go.Bar(
            x=DAYS,
            y=ph_vals2,
            marker_color=bar_colors,
            marker_line_color="#ffffff",
            marker_line_width=2,
            text=["pH " + str(v) for v in ph_vals2],
            textposition="outside",
            textfont=dict(size=10, color="#334155"),
        ))
        fig_bar.add_hline(
            y=7.0,
            line_dash="dash",
            line_color="#dc2626",
            line_width=2,
            annotation_text="pH 7.0 -- Danger Threshold",
            annotation_font_color="#dc2626",
            annotation_font_size=11,
        )
        fig_bar.add_hline(
            y=6.0,
            line_dash="dot",
            line_color="#d97706",
            line_width=1,
            annotation_text="pH 6.0 -- Warning",
            annotation_font_color="#d97706",
            annotation_font_size=10,
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#f0f6fb",
            height=360,
            margin=dict(l=10, r=10, t=20, b=10),
            xaxis=dict(
                showgrid=False,
                color="#475569",
                tickfont=dict(size=10),
            ),
            yaxis=dict(
                gridcolor="#cbd5e1",
                range=[4, 11.5],
                color="#475569",
            ),
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True,
                        config={"displayModeBar": False})

    with col_gauge:
        st.markdown("**Live pH Gauge**")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=ph_vals2[-1],
            delta={
                "reference": 7.0,
                "valueformat": ".2f",
                "increasing": {"color": "#dc2626"},
                "decreasing": {"color": "#16a34a"},
            },
            number={
                "font": {"color": "#0f172a", "size": 56},
                "valueformat": ".2f",
            },
            gauge={
                "axis": {
                    "range": [4, 10],
                    "tickwidth": 1,
                    "tickcolor": "#64748b",
                    "tickfont": {"color": "#64748b", "size": 11},
                    "nticks": 7,
                },
                "bar":     {"color": sc["gel_color"], "thickness": 0.3},
                "bgcolor": "#f0f6fb",
                "borderwidth": 1,
                "bordercolor": "#cbd5e1",
                "steps": [
                    {"range": [4.0, 6.0], "color": "#dcfce7"},
                    {"range": [6.0, 7.0], "color": "#fef9c3"},
                    {"range": [7.0, 10.0], "color": "#fee2e2"},
                ],
                "threshold": {
                    "line": {"color": "#dc2626", "width": 4},
                    "thickness": 0.8,
                    "value": 7.4,
                },
            },
            title={
                "text": "Current pH Reading<br><span style='font-size:12px;color:#64748b'>"
                        "Green = Healthy | Yellow = Warning | Red = Danger</span>",
                "font": {"color": "#334155", "size": 14},
            },
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            height=360,
            margin=dict(l=20, r=20, t=50, b=20),
        )
        st.plotly_chart(fig_gauge, use_container_width=True,
                        config={"displayModeBar": False})

    st.divider()
    st.subheader("All-Scenario Comparison")

    fig_comp = go.Figure()
    for i, (sname, sval) in enumerate(SCENARIOS.items()):
        fig_comp.add_trace(go.Scatter(
            x=DAYS,
            y=sval["ph_readings"],
            mode="lines+markers",
            name=sname,
            line=dict(width=2.5, shape="spline", color=CHART_COLORS[i]),
            marker=dict(size=8, color=CHART_COLORS[i],
                        line=dict(color="#ffffff", width=1)),
            hovertemplate="<b>" + sname + "</b><br>%{x}: pH %{y}<extra></extra>",
        ))
    fig_comp.add_hline(
        y=7.0,
        line_dash="dot",
        line_color="#94a3b8",
        line_width=2,
        annotation_text="Neutral pH 7.0",
        annotation_font_color="#64748b",
        annotation_font_size=11,
    )
    fig_comp.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#f0f6fb",
        height=320,
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(showgrid=False, color="#475569",
                   tickfont=dict(size=10)),
        yaxis=dict(gridcolor="#cbd5e1", range=[4, 10],
                   title="pH Value", color="#475569"),
        legend=dict(
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="#cbd5e1",
            borderwidth=1,
            font=dict(size=12, color="#334155"),
        ),
    )
    st.plotly_chart(fig_comp, use_container_width=True,
                    config={"displayModeBar": False})

# ==================================================================
# TAB 3 -- SENSOR LOG
# ==================================================================
with tab3:
    st.subheader("Live Sensor Event Log")

    btn1, btn2, btn3 = st.columns([1, 1, 2])

    with btn1:
        if st.button("Add Reading", use_container_width=True, type="primary"):
            ph_new   = round(sc["ph_readings"][-1] + random.uniform(-0.35, 0.35), 2)
            temp_new = round(random.uniform(*sc["temp_range"]), 1)
            mois_new = round(random.uniform(*sc["moisture_range"]), 1)
            status_new = "CRITICAL" if ph_new > 7.0 else "OK"
            st.session_state.log.append({
                "Timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Scenario":     st.session_state.selected[:32],
                "pH":           ph_new,
                "Temp (C)":     temp_new,
                "Moisture (%)": mois_new,
                "Status":       status_new,
            })
            st.success("Reading logged -- pH " + str(ph_new) + " | Status: " + status_new)

    with btn2:
        if st.session_state.log:
            df_export = pd.DataFrame(st.session_state.log)
            st.download_button(
                "Export CSV",
                df_export.to_csv(index=False),
                "smartgel_sensor_log.csv",
                "text/csv",
                use_container_width=True,
            )

    st.divider()

    if st.session_state.log:
        df_log = pd.DataFrame(st.session_state.log)

        total   = len(df_log)
        ok_cnt  = len(df_log[df_log["Status"] == "OK"])
        crit_cnt = total - ok_cnt

        lm1, lm2, lm3 = st.columns(3)
        lm1.metric("Total Readings", total)
        lm2.metric("OK Readings",    ok_cnt)
        lm3.metric("Critical Readings", crit_cnt,
                   delta=str(crit_cnt) + " need attention",
                   delta_color="inverse" if crit_cnt > 0 else "normal")

        st.divider()
        st.dataframe(df_log, use_container_width=True, height=420)

        if len(df_log) > 1:
            st.markdown("**pH Over Time (from log)**")
            fig_log = go.Figure(go.Scatter(
                x=df_log["Timestamp"],
                y=df_log["pH"],
                mode="lines+markers",
                line=dict(color="#0891b2", width=2),
                marker=dict(
                    size=8,
                    color=df_log["pH"],
                    colorscale=[
                        [0.0, "#16a34a"],
                        [0.5, "#d97706"],
                        [1.0, "#dc2626"],
                    ],
                    cmin=5, cmax=9,
                    line=dict(color="#ffffff", width=1),
                    showscale=True,
                    colorbar=dict(title="pH", thickness=12),
                ),
                hovertemplate="<b>%{x}</b><br>pH = %{y:.2f}<extra></extra>",
            ))
            fig_log.add_hline(
                y=7.0,
                line_dash="dash",
                line_color="#dc2626",
                annotation_text="Danger Threshold",
                annotation_font_color="#dc2626",
            )
            fig_log.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="#f0f6fb",
                height=280,
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=False, color="#475569",
                           tickfont=dict(size=9)),
                yaxis=dict(gridcolor="#cbd5e1", range=[4, 10],
                           title="pH", color="#475569"),
                showlegend=False,
            )
            st.plotly_chart(fig_log, use_container_width=True,
                            config={"displayModeBar": False})
    else:
        st.info(
            "No readings logged yet. "
            "Click 'Add Reading' above or start the live simulation."
        )

    if st.session_state.sim_running:
        with st.spinner("Live simulation active -- auto-logging readings..."):
            time.sleep(sim_interval)
        ph_sim   = round(sc["ph_readings"][-1] + random.uniform(-0.35, 0.35), 2)
        temp_sim = round(random.uniform(*sc["temp_range"]), 1)
        mois_sim = round(random.uniform(*sc["moisture_range"]), 1)
        st.session_state.log.append({
            "Timestamp":    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Scenario":     st.session_state.selected[:32],
            "pH":           ph_sim,
            "Temp (C)":     temp_sim,
            "Moisture (%)": mois_sim,
            "Status":       "CRITICAL" if ph_sim > 7.0 else "OK",
        })
        st.rerun()

# ==================================================================
# TAB 4 -- CLINICAL REPORT
# ==================================================================
with tab4:
    st.subheader("Auto-Generated Clinical Summary")

    ph_mean_val = round(sum(sc["ph_readings"]) / 10, 2)
    ph_max_val  = max(sc["ph_readings"])
    ph_min_val  = min(sc["ph_readings"])
    ph_trend    = (
        "Alkaline Drift Detected (worsening)"
        if sc["ph_readings"][-1] > sc["ph_readings"][0]
        else "Stable or Improving"
    )
    recommendation = (
        "Continue current protocol. Wound environment is stable. "
        "Healing progresses normally. Weekly monitoring recommended."
        if sc["bacterial_load"] == "LOW"
        else (
            "IMMEDIATE clinical evaluation required. "
            "Alkaline pH shift confirms active bacterial colonisation. "
            "Consider systemic antibiotics and advanced wound debridement. "
            "Do not delay treatment."
        )
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
            ("Sensor Connection",   "BLE Active -- All sensors nominal"),
            ("Report Generated",    datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]
        df_report = pd.DataFrame(rows, columns=["Parameter", "Value"])
        st.dataframe(
            df_report,
            use_container_width=True,
            hide_index=True,
            height=410,
        )

        st.divider()

        if sc["bacterial_load"] == "LOW":
            st.success("RECOMMENDATION: " + recommendation)
        else:
            st.error("RECOMMENDATION: " + recommendation)

        st.divider()
        st.download_button(
            "Download Clinical Report (CSV)",
            df_report.to_csv(index=False),
            "smartgel_clinical_report.csv",
            "text/csv",
            type="primary",
            use_container_width=True,
        )

    with radar_col:
        st.markdown("**Wound Health Radar**")

        categories = [
            "pH Safety",
            "Temperature",
            "Moisture Control",
            "Bacterial Defence",
            "Healing Rate",
            "Gel Integrity",
        ]
        scores = sc["radar_scores"]
        gc2    = sc["gel_color"]
        r2     = int(gc2[1:3], 16)
        g2     = int(gc2[3:5], 16)
        b2     = int(gc2[5:7], 16)
        fill2  = "rgba(" + str(r2) + "," + str(g2) + "," + str(b2) + ",0.22)"

        fig_radar = go.Figure(go.Scatterpolar(
            r=scores + [scores[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor=fill2,
            line=dict(color=gc2, width=2.5),
            marker=dict(
                size=9,
                color=gc2,
                line=dict(color="#ffffff", width=1),
            ),
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="#f0f6fb",
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    gridcolor="#cbd5e1",
                    tickfont=dict(size=9, color="#64748b"),
                    tickvals=[0, 25, 50, 75, 100],
                ),
                angularaxis=dict(
                    gridcolor="#cbd5e1",
                    tickfont=dict(size=11, color="#334155"),
                ),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            height=430,
            margin=dict(l=50, r=50, t=30, b=30),
            showlegend=False,
        )
        st.plotly_chart(fig_radar, use_container_width=True,
                        config={"displayModeBar": False})

        radar_df = pd.DataFrame({
            "Category": categories,
            "Score / 100": scores,
            "Rating": [
                "Excellent" if s >= 80 else ("Good" if s >= 60 else
                ("Fair" if s >= 40 else "Poor"))
                for s in scores
            ],
        })
        st.dataframe(radar_df, use_container_width=True,
                     hide_index=True, height=245)


# ==================================================================
# TAB 5 -- WOUND IMAGE ANALYSIS (AI-Powered)
# ==================================================================
with tab5:
    st.subheader("🩹 AI-Powered Wound Image Analysis")
    st.caption(
        "Upload a photo of your wound, cut, burn, or skin injury. "
        "Our AI will assess severity, estimate healing time, and provide care recommendations."
    )

    st.warning(
        "⚠️ **Medical Disclaimer**: This AI analysis is for informational purposes only and does "
        "NOT replace professional medical advice. Always consult a qualified healthcare provider "
        "for diagnosis and treatment, especially for serious wounds."
    )

    st.divider()

    # --- Upload section ---
    upload_col, preview_col = st.columns([1, 1])

    with upload_col:
        st.markdown("**Step 1: Upload Wound Image**")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["jpg", "jpeg", "png", "webp", "bmp"],
            help="Supported formats: JPG, PNG, WEBP, BMP. Max size: 10 MB.",
        )

        st.markdown("**Step 2: Provide Context (Optional)**")
        wound_age = st.selectbox(
            "How old is this wound?",
            ["Just occurred (< 1 hour)", "Few hours old (1–12 hours)",
             "1 day old", "2–3 days old", "4–7 days old",
             "More than 1 week old", "Chronic / Unknown"],
        )
        patient_context = st.text_area(
            "Additional context (optional)",
            placeholder="E.g.: diabetic patient, animal bite, burn from hot water, "
                        "not cleaned yet, on blood thinners...",
            height=100,
        )

        analyze_btn = st.button(
            "🔬 Analyse Wound with AI",
            type="primary",
            use_container_width=True,
            disabled=(uploaded_file is None),
        )

    with preview_col:
        if uploaded_file:
            st.markdown("**Image Preview**")
            st.image(uploaded_file, caption="Uploaded wound image", use_column_width=True)
        else:
            st.markdown("**Image Preview**")
            st.info("Upload an image on the left to see a preview here.")

    st.divider()

    # --- AI Analysis ---
    if analyze_btn and uploaded_file:
        # Encode image to base64
        image_bytes = uploaded_file.read()
        b64_image   = base64.standard_b64encode(image_bytes).decode("utf-8")

        # Determine MIME type
        fname = uploaded_file.name.lower()
        if fname.endswith(".png"):
            mime_type = "image/png"
        elif fname.endswith(".webp"):
            mime_type = "image/webp"
        elif fname.endswith(".bmp"):
            mime_type = "image/bmp"
        else:
            mime_type = "image/jpeg"

        # Build context string
        context_str = ""
        if patient_context.strip():
            context_str = "\n\nAdditional context provided by the user: " + patient_context.strip()

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

        with st.spinner("🔬 Analysing wound image with AI... Please wait."):
            try:
                import urllib.request
                import urllib.error

                # Resolve API key: secrets file → sidebar input
                api_key = st.secrets.get("ANTHROPIC_API_KEY", "") or st.session_state.get("sidebar_api_key", "")
                if not api_key:
                    st.error(
                        "**API Key Missing.** Provide it via one of these methods:\n\n"
                        "**Option A – Streamlit Cloud Secrets** (recommended for deployed apps):\n"
                        "App Settings → Secrets → add `ANTHROPIC_API_KEY = \"sk-ant-...\"`\n\n"
                        "**Option B – Local secrets file**: create `.streamlit/secrets.toml` "
                        "and add `ANTHROPIC_API_KEY = \"sk-ant-...\"`\n\n"
                        "**Option C – Sidebar**: paste your key directly into the "
                        "🔑 AI Analysis Key field in the left sidebar."
                    )
                    st.stop()

                payload = json.dumps({
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": 1500,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": mime_type,
                                        "data": b64_image,
                                    },
                                },
                                {"type": "text", "text": prompt},
                            ],
                        }
                    ],
                }).encode("utf-8")

                req = urllib.request.Request(
                    "https://api.anthropic.com/v1/messages",
                    data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": api_key,
                        "anthropic-version": "2023-06-01",
                    },
                    method="POST",
                )

                with urllib.request.urlopen(req) as resp:
                    raw = json.loads(resp.read().decode("utf-8"))

                # Extract text content
                full_text = ""
                for block in raw.get("content", []):
                    if block.get("type") == "text":
                        full_text += block["text"]

                # Strip any stray markdown fences and parse
                clean = re.sub(r"```(?:json)?", "", full_text).strip().rstrip("`").strip()
                result = json.loads(clean)
                st.session_state.wound_analysis = result

            except Exception as e:
                st.error("Analysis failed: " + str(e))
                st.session_state.wound_analysis = None

    # --- Display Results ---
    if st.session_state.wound_analysis:
        r = st.session_state.wound_analysis

        st.subheader("📋 AI Wound Assessment Results")

        # Severity colour mapping
        sev = r.get("severity_level", "MODERATE")
        sev_color_map = {
            "MILD":     ("#16a34a", "#dcfce7"),
            "MODERATE": ("#d97706", "#fef9c3"),
            "SEVERE":   ("#dc2626", "#fee2e2"),
            "CRITICAL": ("#7c3aed", "#ede9fe"),
        }
        sev_color, sev_bg = sev_color_map.get(sev, ("#475569", "#f1f5f9"))

        # Top summary banner
        score = r.get("severity_score", 5)
        if r.get("seek_emergency"):
            st.error(
                "🚨 **EMERGENCY**: This wound requires IMMEDIATE emergency medical attention. "
                "Call emergency services or go to the nearest emergency room NOW."
            )

        # KPI row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Wound Type",      r.get("wound_type", "Unknown"))
        m2.metric("Severity Score",  str(score) + " / 10")
        m3.metric("Infection Risk",  r.get("infection_risk", "Unknown"))
        m4.metric(
            "Est. Healing Time",
            str(r.get("healing_time_min_days", "?")) + "–" +
            str(r.get("healing_time_max_days", "?")) + " days",
        )

        st.divider()

        detail_col, action_col = st.columns([1, 1])

        with detail_col:
            st.markdown("#### 🔍 Clinical Details")

            details_rows = [
                ("Severity Level",      r.get("severity_level", "—")),
                ("Severity Score",      str(r.get("severity_score", "—")) + " / 10"),
                ("Wound Type",          r.get("wound_type", "—")),
                ("Affected Area",       r.get("affected_area", "—")),
                ("Healing Phase",       r.get("healing_phase", "—")),
                ("Infection Risk",      r.get("infection_risk", "—")),
                ("Healing Time (Est.)", str(r.get("healing_time_min_days", "?")) +
                                        "–" + str(r.get("healing_time_max_days", "?")) + " days"),
                ("See Doctor Within",   r.get("seek_doctor_within", "—")),
                ("SmartGel Protocol",   r.get("smartgel_recommendation", "—")),
                ("Recommended Tx",      r.get("recommended_treatment", "—")),
            ]
            df_details = pd.DataFrame(details_rows, columns=["Parameter", "Value"])
            st.dataframe(df_details, use_container_width=True, hide_index=True, height=380)

            # Visible signs
            signs = r.get("visible_signs", [])
            if signs:
                st.markdown("**🩺 Visible Clinical Signs Detected:**")
                for s in signs:
                    st.markdown("- " + str(s))

        with action_col:
            st.markdown("#### ⚡ Immediate Actions Required")
            for i, step in enumerate(r.get("immediate_actions", []), 1):
                st.markdown(str(i) + ". " + str(step))

            st.divider()
            st.markdown("#### 🏥 Daily Care Instructions")
            for i, step in enumerate(r.get("care_instructions", []), 1):
                st.markdown(str(i) + ". " + str(step))

            st.divider()
            st.markdown("#### ⚠️ Warning Signs to Watch For")
            for sign in r.get("warning_signs", []):
                st.markdown("🔴 " + str(sign))

        st.divider()

        # Severity visual gauge
        st.markdown("#### 📊 Severity Visualisation")
        gauge_col, note_col = st.columns([2, 1])

        with gauge_col:
            score_val = r.get("severity_score", 5)
            fig_sev = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score_val,
                number={"font": {"size": 52, "color": sev_color}, "suffix": "/10"},
                gauge={
                    "axis": {
                        "range": [0, 10],
                        "tickwidth": 1,
                        "tickcolor": "#64748b",
                        "tickfont": {"size": 11},
                        "nticks": 11,
                    },
                    "bar": {"color": sev_color, "thickness": 0.28},
                    "bgcolor": "#f0f6fb",
                    "borderwidth": 1,
                    "bordercolor": "#cbd5e1",
                    "steps": [
                        {"range": [0,   3.5], "color": "#dcfce7"},
                        {"range": [3.5, 6.0], "color": "#fef9c3"},
                        {"range": [6.0, 8.5], "color": "#fee2e2"},
                        {"range": [8.5, 10],  "color": "#ede9fe"},
                    ],
                },
                title={
                    "text": "Wound Severity Score<br>"
                            "<span style='font-size:12px;color:#64748b'>"
                            "1–3 Mild | 4–6 Moderate | 7–8 Severe | 9–10 Critical</span>",
                    "font": {"size": 14, "color": "#334155"},
                },
            ))
            fig_sev.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                height=300,
                margin=dict(l=20, r=20, t=60, b=10),
            )
            st.plotly_chart(fig_sev, use_container_width=True,
                            config={"displayModeBar": False})

        with note_col:
            st.markdown("#### 📝 Confidence Note")
            st.info(r.get("confidence_note", "No note available."))

            heal_min = r.get("healing_time_min_days", 0)
            heal_max = r.get("healing_time_max_days", 0)
            st.markdown("#### ⏱️ Healing Timeline")
            st.success(
                "Estimated healing: **" + str(heal_min) + " – " + str(heal_max) + " days**\n\n"
                "Phase: " + r.get("healing_phase", "Unknown")
            )

        st.divider()

        # Export report
        export_rows = [
            ("Wound Type",          r.get("wound_type", "")),
            ("Severity Level",      r.get("severity_level", "")),
            ("Severity Score",      str(r.get("severity_score", ""))),
            ("Affected Area",       r.get("affected_area", "")),
            ("Infection Risk",      r.get("infection_risk", "")),
            ("Healing Time (days)", str(r.get("healing_time_min_days", "")) +
                                    "–" + str(r.get("healing_time_max_days", ""))),
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
            ("Analysis Time",       datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        ]
        df_export_report = pd.DataFrame(export_rows, columns=["Parameter", "Value"])
        st.download_button(
            "📥 Download AI Wound Analysis Report (CSV)",
            df_export_report.to_csv(index=False),
            "smartgel_wound_analysis.csv",
            "text/csv",
            type="primary",
            use_container_width=True,
        )

        if st.button("🔄 Clear Analysis & Upload New Image", use_container_width=True):
            st.session_state.wound_analysis = None
            st.rerun()
