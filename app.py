"""
AI-Based Smart Parking System
A beginner-friendly Streamlit web application for college mini project / academic demonstration.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time

# ─────────────────────────────────────────────
# PAGE CONFIG & CUSTOM CSS
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartPark AI",
    page_icon="🅿️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    color: #e8e8f0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1f 0%, #1a1a35 100%);
    border-right: 1px solid rgba(100, 200, 255, 0.15);
}
[data-testid="stSidebar"] * { color: #ccd6f6 !important; }
[data-testid="stSidebar"] .stRadio label {
    padding: 8px 14px;
    border-radius: 8px;
    transition: background 0.2s;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(100, 200, 255, 0.1);
}

/* ── Metric Cards ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(100, 200, 255, 0.15);
    border-radius: 16px;
    padding: 20px !important;
    backdrop-filter: blur(10px);
    transition: transform 0.2s, border-color 0.2s;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-3px);
    border-color: rgba(100, 200, 255, 0.4);
}
[data-testid="metric-container"] label { color: #8892b0 !important; font-size: 13px !important; }
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #64ffda !important;
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem !important;
    font-weight: 700;
}

/* ── Section Headers ── */
.section-header {
    font-size: 1.6rem;
    font-weight: 700;
    color: #ccd6f6;
    margin-bottom: 6px;
    letter-spacing: -0.3px;
}
.section-sub {
    color: #8892b0;
    font-size: 0.92rem;
    margin-bottom: 24px;
}

/* ── Slot Cards ── */
.slot-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; }
.slot-card {
    width: 90px; height: 80px;
    border-radius: 12px;
    display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700; font-size: 15px;
    cursor: default;
    transition: transform 0.2s, box-shadow 0.2s;
    border: 2px solid transparent;
}
.slot-card:hover { transform: scale(1.07); }
.slot-available {
    background: rgba(100, 255, 218, 0.12);
    border-color: #64ffda;
    color: #64ffda;
    box-shadow: 0 0 14px rgba(100,255,218,0.2);
}
.slot-occupied {
    background: rgba(255, 90, 120, 0.12);
    border-color: #ff5a78;
    color: #ff5a78;
    box-shadow: 0 0 14px rgba(255,90,120,0.2);
}
.slot-reserved {
    background: rgba(255, 190, 50, 0.12);
    border-color: #ffbe32;
    color: #ffbe32;
    box-shadow: 0 0 14px rgba(255,190,50,0.2);
}
.slot-icon { font-size: 20px; margin-bottom: 2px; }

/* ── Info Boxes ── */
.info-box {
    background: rgba(100, 255, 218, 0.06);
    border: 1px solid rgba(100,255,218,0.25);
    border-radius: 12px;
    padding: 18px 22px;
    margin-bottom: 14px;
    color: #ccd6f6;
}
.info-box strong { color: #64ffda; }

/* ── AI Suggestion Box ── */
.ai-box {
    background: linear-gradient(135deg, rgba(100,255,218,0.08), rgba(100,120,255,0.08));
    border: 1px solid rgba(100,255,218,0.3);
    border-radius: 16px;
    padding: 24px 28px;
    margin: 16px 0;
}
.ai-title { font-size: 1.1rem; font-weight: 700; color: #64ffda; margin-bottom: 8px; }
.ai-slot { font-family: 'JetBrains Mono', monospace; font-size: 2rem; font-weight: 700; color: #fff; }
.ai-reason { color: #8892b0; font-size: 0.9rem; margin-top: 6px; }

/* ── Prediction Cards ── */
.pred-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 18px;
    text-align: center;
}
.pred-label { color: #8892b0; font-size: 0.82rem; margin-bottom: 4px; }
.pred-value { font-size: 1.3rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }
.traffic-low    { color: #64ffda; }
.traffic-medium { color: #ffbe32; }
.traffic-high   { color: #ff8c42; }
.traffic-very-high { color: #ff5a78; }

/* ── Admin Table ── */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* ── Form Styling ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(100,200,255,0.2) !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
}
.stTextInput > div > div > input:focus {
    border-color: #64ffda !important;
    box-shadow: 0 0 0 2px rgba(100,255,218,0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #64ffda, #48b2ff) !important;
    color: #0d0d1f !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    letter-spacing: 0.3px;
    transition: opacity 0.2s, transform 0.2s !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-2px) !important;
}

/* ── Progress Bar ── */
.stProgress > div > div { background: linear-gradient(90deg, #64ffda, #48b2ff) !important; border-radius: 4px; }

/* ── Success / Warning / Error ── */
.stSuccess { background: rgba(100,255,218,0.1) !important; border-color: #64ffda !important; }
.stWarning { background: rgba(255,190,50,0.1) !important; }
.stError   { background: rgba(255,90,120,0.1) !important; }

/* ── Legend Chip ── */
.legend-chip {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.83rem;
    font-weight: 600;
    margin-right: 8px;
}
.chip-green { background: rgba(100,255,218,0.12); color: #64ffda; border: 1px solid #64ffda44; }
.chip-red   { background: rgba(255,90,120,0.12); color: #ff5a78; border: 1px solid #ff5a7844; }
.chip-yellow{ background: rgba(255,190,50,0.12); color: #ffbe32; border: 1px solid #ffbe3244; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ─────────────────────────────────────────────
def init_session_state():
    """Initialise all session-state variables on first run."""
    if "slots" not in st.session_state:
        # Create 30 parking slots across 3 rows: A, B, C
        slots = []
        for row in ["A", "B", "C"]:
            for num in range(1, 11):
                slot_id = f"{row}{num}"
                # Randomly pre-populate some as occupied/reserved for demo
                rand = random.random()
                if rand < 0.30:
                    status = "Occupied"
                elif rand < 0.40:
                    status = "Reserved"
                else:
                    status = "Available"
                slots.append({
                    "Slot ID": slot_id,
                    "Row": row,
                    "Number": num,
                    "Status": status,
                    "Distance from Entrance": num  # slot 1 = nearest
                })
        st.session_state.slots = pd.DataFrame(slots)

    if "bookings" not in st.session_state:
        st.session_state.bookings = pd.DataFrame(columns=[
            "Booking ID", "Name", "Vehicle No", "Vehicle Type",
            "Slot ID", "Arrival Time", "Duration (hrs)", "Booked At"
        ])

    if "booking_counter" not in st.session_state:
        st.session_state.booking_counter = 1


# ─────────────────────────────────────────────
# HELPER UTILITIES
# ─────────────────────────────────────────────
def get_counts():
    """Return a dict with total / available / occupied / reserved counts."""
    df = st.session_state.slots
    return {
        "total":     len(df),
        "available": int((df["Status"] == "Available").sum()),
        "occupied":  int((df["Status"] == "Occupied").sum()),
        "reserved":  int((df["Status"] == "Reserved").sum()),
    }


def slot_html(slot_id, status):
    """Return an HTML card for a single parking slot."""
    icons = {"Available": "🟢", "Occupied": "🔴", "Reserved": "🟡"}
    css_class = {
        "Available": "slot-available",
        "Occupied":  "slot-occupied",
        "Reserved":  "slot-reserved"
    }
    return (
        f'<div class="slot-card {css_class[status]}">'
        f'<span class="slot-icon">{icons[status]}</span>'
        f'{slot_id}'
        f'</div>'
    )


def ai_suggest():
    """
    Simple rule-based AI suggestion:
    1. Pick available slots
    2. Sort by distance from entrance
    3. Return the nearest one with a reason
    """
    df = st.session_state.slots
    available = df[df["Status"] == "Available"].sort_values("Distance from Entrance")
    if available.empty:
        return None, "No slots available right now."
    best = available.iloc[0]
    reasons = [
        f"it is the closest available slot to the entrance (distance rank #{best['Distance from Entrance']})",
        f"this zone has the least congestion and best access route",
        f"it is in Row {best['Row']} which currently has fewer vehicles",
    ]
    return best["Slot ID"], random.choice(reasons)


# ─────────────────────────────────────────────
# PAGE: HOME / DASHBOARD
# ─────────────────────────────────────────────
def page_home():
    st.markdown('<div class="section-header">🅿️ SmartPark AI — Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Real-time overview of your parking facility</div>', unsafe_allow_html=True)

    counts = get_counts()
    occupancy_pct = round((counts["occupied"] + counts["reserved"]) / counts["total"] * 100, 1)

    # ── Metric row ──
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("🏢 Total Slots",     counts["total"])
    c2.metric("✅ Available",        counts["available"])
    c3.metric("🔴 Occupied",         counts["occupied"])
    c4.metric("🟡 Reserved",         counts["reserved"])
    c5.metric("📊 Occupancy",        f"{occupancy_pct}%")

    st.markdown("---")

    # ── Occupancy gauge ──
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown("#### Occupancy Level")
        st.progress(occupancy_pct / 100)
        st.markdown(f"**{occupancy_pct}%** of total capacity is in use.")

        # Status colour badge
        if occupancy_pct < 50:
            st.success("🟢 Low Traffic — Plenty of space available!")
        elif occupancy_pct < 75:
            st.warning("🟡 Moderate Traffic — Some slots filling up.")
        else:
            st.error("🔴 High Traffic — Very few slots remaining!")

        # Quick AI tip
        slot_id, reason = ai_suggest()
        if slot_id:
            st.markdown(
                f'<div class="info-box">🤖 <strong>AI Quick Tip:</strong> '
                f'Best slot right now is <strong>{slot_id}</strong> — {reason}.</div>',
                unsafe_allow_html=True
            )

    with col_right:
        # Donut chart
        fig = go.Figure(go.Pie(
            labels=["Available", "Occupied", "Reserved"],
            values=[counts["available"], counts["occupied"], counts["reserved"]],
            hole=0.62,
            marker_colors=["#64ffda", "#ff5a78", "#ffbe32"],
            textinfo="label+percent",
            textfont_color="#ccd6f6",
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ccd6f6",
            showlegend=False,
            margin=dict(t=20, b=20, l=20, r=20),
            height=280,
        )
        fig.add_annotation(
            text=f"<b>{counts['total']}</b><br>Slots",
            x=0.5, y=0.5, font_size=18, showarrow=False,
            font_color="#ccd6f6"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📅 Today's Booking Summary")

    booking_df = st.session_state.bookings
    if booking_df.empty:
        st.info("No bookings made yet. Head to **Book Slot** to get started.")
    else:
        st.dataframe(
            booking_df[["Booking ID", "Name", "Vehicle No", "Slot ID", "Arrival Time"]].tail(5),
            use_container_width=True, hide_index=True
        )


# ─────────────────────────────────────────────
# PAGE: VIEW SLOTS
# ─────────────────────────────────────────────
def page_view_slots():
    st.markdown('<div class="section-header">🗺️ Parking Slot Map</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Visual overview of all parking slots and their current status</div>', unsafe_allow_html=True)

    # Legend
    st.markdown(
        '<span class="legend-chip chip-green">🟢 Available</span>'
        '<span class="legend-chip chip-red">🔴 Occupied</span>'
        '<span class="legend-chip chip-yellow">🟡 Reserved</span>',
        unsafe_allow_html=True
    )
    st.markdown("<br>", unsafe_allow_html=True)

    df = st.session_state.slots

    # Filter
    filter_col, _ = st.columns([2, 3])
    with filter_col:
        status_filter = st.selectbox("Filter by Status", ["All", "Available", "Occupied", "Reserved"])

    for row_label in ["A", "B", "C"]:
        st.markdown(f"#### Row {row_label}")
        row_df = df[df["Row"] == row_label]
        if status_filter != "All":
            row_df = row_df[row_df["Status"] == status_filter]

        cards_html = '<div class="slot-grid">'
        for _, r in row_df.iterrows():
            cards_html += slot_html(r["Slot ID"], r["Status"])
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    # Slot detail table
    with st.expander("📋 View Full Slot Details Table"):
        show_df = df.copy()
        if status_filter != "All":
            show_df = show_df[show_df["Status"] == status_filter]
        st.dataframe(show_df.drop(columns=["Row", "Number"]), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
# PAGE: BOOK SLOT
# ─────────────────────────────────────────────
def page_book_slot():
    st.markdown('<div class="section-header">📝 Book a Parking Slot</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Fill in your details and the system will assign you the best available slot</div>', unsafe_allow_html=True)

    counts = get_counts()
    if counts["available"] == 0:
        st.error("❌ Sorry! No parking slots are currently available. Please check back later.")
        return

    st.info(f"ℹ️ **{counts['available']} slots** are currently available for booking.")

    with st.form("booking_form"):
        st.markdown("#### 👤 Personal Details")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="e.g. Rahul Sharma")
        with col2:
            vehicle_no = st.text_input("Vehicle Number", placeholder="e.g. TS09AB1234")

        col3, col4 = st.columns(2)
        with col3:
            vehicle_type = st.selectbox("Vehicle Type", ["Car", "Bike", "SUV", "Truck", "Electric Vehicle"])
        with col4:
            duration = st.number_input("Duration (hours)", min_value=1, max_value=24, value=2)

        arrival_time = st.time_input("Arrival Time", value=datetime.now().time())

        # Preference
        st.markdown("#### 🎯 Slot Preference")
        preference = st.radio(
            "Preferred Zone",
            ["Any (AI will decide)", "Row A (Near Entrance)", "Row B (Middle)", "Row C (Far End)"],
            horizontal=True
        )

        submitted = st.form_submit_button("🚗 Confirm Booking")

    if submitted:
        # Validate inputs
        if not name.strip():
            st.error("Please enter your name.")
            return
        if not vehicle_no.strip():
            st.error("Please enter your vehicle number.")
            return

        df = st.session_state.slots
        avail = df[df["Status"] == "Available"]

        # Apply row preference
        if "Row A" in preference:
            avail = avail[avail["Row"] == "A"] if not avail[avail["Row"] == "A"].empty else avail
        elif "Row B" in preference:
            avail = avail[avail["Row"] == "B"] if not avail[avail["Row"] == "B"].empty else avail
        elif "Row C" in preference:
            avail = avail[avail["Row"] == "C"] if not avail[avail["Row"] == "C"].empty else avail

        # Assign nearest available slot
        assigned = avail.sort_values("Distance from Entrance").iloc[0]
        slot_id = assigned["Slot ID"]

        # Update slot status
        st.session_state.slots.loc[
            st.session_state.slots["Slot ID"] == slot_id, "Status"
        ] = "Reserved"

        # Add booking record
        booking_id = f"BK{str(st.session_state.booking_counter).zfill(4)}"
        st.session_state.booking_counter += 1

        new_booking = pd.DataFrame([{
            "Booking ID":    booking_id,
            "Name":          name.strip(),
            "Vehicle No":    vehicle_no.upper().strip(),
            "Vehicle Type":  vehicle_type,
            "Slot ID":       slot_id,
            "Arrival Time":  str(arrival_time),
            "Duration (hrs)": duration,
            "Booked At":     datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        st.session_state.bookings = pd.concat(
            [st.session_state.bookings, new_booking], ignore_index=True
        )

        # Success message
        st.success(f"✅ Booking Confirmed! Slot **{slot_id}** has been reserved for **{name}**.")
        st.markdown(
            f'<div class="ai-box">'
            f'<div class="ai-title">🎫 Booking Receipt</div>'
            f'<div class="ai-slot">{slot_id}</div>'
            f'<div class="ai-reason">'
            f'<b>Booking ID:</b> {booking_id} &nbsp;|&nbsp; '
            f'<b>Vehicle:</b> {vehicle_no.upper()} ({vehicle_type}) &nbsp;|&nbsp; '
            f'<b>Arrival:</b> {arrival_time} &nbsp;|&nbsp; '
            f'<b>Duration:</b> {duration} hrs'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )


# ─────────────────────────────────────────────
# PAGE: AI SUGGESTION
# ─────────────────────────────────────────────
def page_ai_suggestion():
    st.markdown('<div class="section-header">🤖 AI Smart Parking Suggestion</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Our AI engine analyses slot availability, distance, and zone congestion to find your ideal spot</div>', unsafe_allow_html=True)

    # How it works
    with st.expander("ℹ️ How does the AI work?"):
        st.markdown("""
        The AI uses a **rule-based scoring algorithm** that considers:
        - 📍 **Distance from Entrance** — slots closer to the entrance rank higher
        - 🏷️ **Zone Congestion** — rows with fewer occupied slots are preferred
        - 🚗 **Vehicle Type Compatibility** — larger vehicles are assigned wider slots
        - ⚡ **EV Priority** — Electric Vehicles are directed to charging-enabled spots (Row A)

        _This simulates real-world AI parking systems that use sensor data and machine learning._
        """)

    vehicle_type = st.selectbox("Select your Vehicle Type", ["Car", "Bike", "SUV", "Truck", "Electric Vehicle"])

    if st.button("🔍 Get AI Suggestion"):
        with st.spinner("AI analysing parking slots..."):
            time.sleep(1.2)  # Simulate processing

        df = st.session_state.slots
        avail = df[df["Status"] == "Available"].copy()

        if avail.empty:
            st.error("❌ No available slots at the moment!")
            return

        # EV preference
        if vehicle_type == "Electric Vehicle":
            ev_avail = avail[avail["Row"] == "A"]
            if not ev_avail.empty:
                avail = ev_avail

        # Score: lower distance = better score
        avail["Score"] = avail["Distance from Entrance"]
        # Add zone bonus: fewer occupied in zone = lower penalty
        for row in avail["Row"].unique():
            occupied_in_row = int((df[(df["Row"] == row) & (df["Status"] == "Occupied")].shape[0]))
            avail.loc[avail["Row"] == row, "Score"] += occupied_in_row * 0.5

        best = avail.sort_values("Score").iloc[0]
        slot_id = best["Slot ID"]
        zone_occupied = int(df[(df["Row"] == best["Row"]) & (df["Status"] == "Occupied")].shape[0])

        reason = (
            f"Slot <b>{slot_id}</b> is the optimal choice — "
            f"it is <b>rank #{best['Distance from Entrance']}</b> from the entrance "
            f"and Row {best['Row']} currently has only <b>{zone_occupied} occupied slots</b>."
        )
        if vehicle_type == "Electric Vehicle":
            reason += " EV charging points are available in Row A. ⚡"

        st.markdown(
            f'<div class="ai-box">'
            f'<div class="ai-title">✨ AI Recommended Slot</div>'
            f'<div class="ai-slot">{slot_id}</div>'
            f'<div class="ai-reason">{reason}</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        # Show top 3 alternatives
        st.markdown("#### 🔄 Top 3 Alternatives")
        top3 = avail.sort_values("Score").head(3)
        cols = st.columns(3)
        for i, (_, row) in enumerate(top3.iterrows()):
            with cols[i]:
                st.markdown(
                    f'<div class="pred-card">'
                    f'<div class="pred-label">Option {i+1}</div>'
                    f'<div class="pred-value">{row["Slot ID"]}</div>'
                    f'<div style="color:#8892b0;font-size:0.8rem;">Row {row["Row"]} | Distance #{row["Distance from Entrance"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )


# ─────────────────────────────────────────────
# PAGE: PREDICTION
# ─────────────────────────────────────────────
def page_prediction():
    st.markdown('<div class="section-header">📈 Parking Demand Prediction</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">AI-simulated prediction of parking demand throughout the day</div>', unsafe_allow_html=True)

    # Hourly demand data (simulated)
    hours = list(range(0, 24))
    demand = [
        5,  5,  3,  2,  3,  8,   # 0–5 (night → early morning)
        20, 40, 65, 72, 78, 85,  # 6–11 (morning rush)
        90, 95, 88, 82, 85, 92,  # 12–17 (afternoon)
        88, 75, 60, 40, 25, 10   # 18–23 (evening → night)
    ]
    hour_labels = [f"{h:02d}:00" for h in hours]

    df_pred = pd.DataFrame({"Hour": hour_labels, "Occupancy (%)": demand})

    # Current hour highlight
    current_hour = datetime.now().hour
    current_demand = demand[current_hour]

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown('<div class="pred-card"><div class="pred-label">Current Hour</div>'
                    f'<div class="pred-value">{current_hour:02d}:00</div></div>', unsafe_allow_html=True)
    with col_b:
        traffic_class = (
            "traffic-low" if current_demand < 40 else
            "traffic-medium" if current_demand < 65 else
            "traffic-high" if current_demand < 85 else
            "traffic-very-high"
        )
        label = (
            "Low" if current_demand < 40 else
            "Medium" if current_demand < 65 else
            "High" if current_demand < 85 else
            "Very High"
        )
        st.markdown(f'<div class="pred-card"><div class="pred-label">Predicted Traffic</div>'
                    f'<div class="pred-value {traffic_class}">{label}</div></div>', unsafe_allow_html=True)
    with col_c:
        avail_pred = int(30 * (1 - current_demand / 100))
        st.markdown(f'<div class="pred-card"><div class="pred-label">Predicted Available</div>'
                    f'<div class="pred-value">{avail_pred} slots</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hour_labels, y=demand,
        mode="lines+markers",
        line=dict(color="#64ffda", width=3),
        marker=dict(size=6, color="#64ffda"),
        fill="tozeroy",
        fillcolor="rgba(100,255,218,0.06)",
        name="Predicted Occupancy"
    ))
    # Highlight current hour
    fig.add_vline(
        x=hour_labels[current_hour],
        line_width=2, line_dash="dash", line_color="#ffbe32",
        annotation_text="Now", annotation_font_color="#ffbe32"
    )
    fig.update_layout(
        title="24-Hour Parking Demand Forecast",
        xaxis_title="Hour",
        yaxis_title="Estimated Occupancy (%)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ccd6f6",
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", range=[0, 105]),
        height=380,
    )
    st.plotly_chart(fig, use_container_width=True)

    # Time-of-day insights
    st.markdown("#### 🕐 Time-of-Day Traffic Insights")
    insights = [
        ("🌙 Night (00–06)", "Low", "traffic-low",       "Parking almost empty. Ideal for late arrivals."),
        ("🌅 Morning (06–11)", "High", "traffic-high",   "Rush hour! Book early to secure a slot."),
        ("☀️ Afternoon (11–17)", "Very High", "traffic-very-high", "Peak time. Very limited availability."),
        ("🌆 Evening (17–21)", "High", "traffic-high",   "Post-work traffic. Arrive early if possible."),
        ("🌃 Late Night (21–24)", "Medium", "traffic-medium", "Gradually decreasing. Slots become available."),
    ]
    for period, level, css, tip in insights:
        st.markdown(
            f'<div class="info-box">'
            f'<b>{period}</b> — Traffic: <span class="{css}"><b>{level}</b></span><br>'
            f'<span style="color:#8892b0;">{tip}</span>'
            f'</div>',
            unsafe_allow_html=True
        )


# ─────────────────────────────────────────────
# PAGE: ADMIN PANEL
# ─────────────────────────────────────────────
def page_admin():
    st.markdown('<div class="section-header">🔧 Admin Panel</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Manage bookings, slots, and system settings</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📋 All Bookings", "🔄 Manage Slots", "⚙️ System Actions"])

    # ── Tab 1: All Bookings ──
    with tab1:
        bookings = st.session_state.bookings
        if bookings.empty:
            st.info("No bookings recorded yet.")
        else:
            st.markdown(f"**Total Bookings:** {len(bookings)}")
            st.dataframe(bookings, use_container_width=True, hide_index=True)

            st.markdown("#### ❌ Cancel a Booking")
            booking_ids = bookings["Booking ID"].tolist()
            selected_id = st.selectbox("Select Booking ID to Cancel", booking_ids)
            if st.button("Cancel Booking"):
                # Find the slot associated with this booking and free it
                row = bookings[bookings["Booking ID"] == selected_id].iloc[0]
                slot_id = row["Slot ID"]
                st.session_state.slots.loc[
                    st.session_state.slots["Slot ID"] == slot_id, "Status"
                ] = "Available"
                # Remove booking
                st.session_state.bookings = bookings[bookings["Booking ID"] != selected_id].reset_index(drop=True)
                st.success(f"✅ Booking {selected_id} cancelled. Slot {slot_id} is now Available.")
                st.rerun()

    # ── Tab 2: Manage Slots ──
    with tab2:
        st.markdown("#### ✏️ Update a Slot Status Manually")
        col1, col2, col3 = st.columns(3)
        with col1:
            all_slots = st.session_state.slots["Slot ID"].tolist()
            slot_to_update = st.selectbox("Select Slot", all_slots)
        with col2:
            new_status = st.selectbox("New Status", ["Available", "Occupied", "Reserved"])
        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Update Slot"):
                st.session_state.slots.loc[
                    st.session_state.slots["Slot ID"] == slot_to_update, "Status"
                ] = new_status
                st.success(f"✅ Slot {slot_to_update} updated to **{new_status}**.")
                st.rerun()

        st.markdown("#### 📊 Current Slot Status Table")
        st.dataframe(
            st.session_state.slots[["Slot ID", "Status", "Distance from Entrance"]],
            use_container_width=True, hide_index=True
        )

    # ── Tab 3: System Actions ──
    with tab3:
        st.markdown("#### 🔁 Reset All Slots to Available")
        st.warning("⚠️ This will mark ALL slots as Available and clear all bookings!")
        if st.button("Reset All Parking Slots"):
            st.session_state.slots["Status"] = "Available"
            st.session_state.bookings = pd.DataFrame(columns=[
                "Booking ID", "Name", "Vehicle No", "Vehicle Type",
                "Slot ID", "Arrival Time", "Duration (hrs)", "Booked At"
            ])
            st.session_state.booking_counter = 1
            st.success("✅ All slots reset to Available. All bookings cleared.")
            st.rerun()

        st.markdown("---")
        st.markdown("#### 🎲 Randomise Demo Data")
        st.info("Re-randomise slot statuses for demonstration purposes.")
        if st.button("Randomise Slots"):
            def random_status():
                r = random.random()
                return "Occupied" if r < 0.3 else "Reserved" if r < 0.4 else "Available"
            st.session_state.slots["Status"] = st.session_state.slots["Slot ID"].apply(lambda _: random_status())
            st.success("✅ Slot statuses randomised!")
            st.rerun()


# ─────────────────────────────────────────────
# PAGE: REPORTS / ANALYTICS
# ─────────────────────────────────────────────
def page_reports():
    st.markdown('<div class="section-header">📊 Reports & Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Visual insights into parking usage and booking trends</div>', unsafe_allow_html=True)

    counts = get_counts()
    df = st.session_state.slots
    bookings = st.session_state.bookings

    # ── Row 1: Occupancy bar by row ──
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Slot Status by Row")
        row_data = df.groupby(["Row", "Status"]).size().reset_index(name="Count")
        fig = px.bar(
            row_data, x="Row", y="Count", color="Status",
            color_discrete_map={"Available": "#64ffda", "Occupied": "#ff5a78", "Reserved": "#ffbe32"},
            barmode="stack",
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ccd6f6", height=300, margin=dict(t=20, b=20, l=0, r=0),
            legend=dict(orientation="h", y=-0.3),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Overall Slot Distribution")
        fig2 = px.pie(
            names=["Available", "Occupied", "Reserved"],
            values=[counts["available"], counts["occupied"], counts["reserved"]],
            color_discrete_sequence=["#64ffda", "#ff5a78", "#ffbe32"],
            hole=0.4,
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", font_color="#ccd6f6",
            height=300, margin=dict(t=20, b=20, l=0, r=0),
        )
        st.plotly_chart(fig2, use_container_width=True)

    # ── Row 2: Booking analytics ──
    if not bookings.empty:
        col3, col4 = st.columns(2)

        with col3:
            st.markdown("#### Bookings by Vehicle Type")
            vtype_counts = bookings["Vehicle Type"].value_counts().reset_index()
            vtype_counts.columns = ["Vehicle Type", "Count"]
            fig3 = px.bar(
                vtype_counts, x="Vehicle Type", y="Count",
                color="Vehicle Type",
                color_discrete_sequence=["#64ffda", "#48b2ff", "#ffbe32", "#ff5a78", "#b8a9ff"],
            )
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#ccd6f6", showlegend=False, height=300,
                margin=dict(t=20, b=20, l=0, r=0),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            )
            st.plotly_chart(fig3, use_container_width=True)

        with col4:
            st.markdown("#### Bookings by Row")
            bookings["Row"] = bookings["Slot ID"].str[0]
            row_counts = bookings["Row"].value_counts().reset_index()
            row_counts.columns = ["Row", "Bookings"]
            fig4 = px.bar(
                row_counts, x="Row", y="Bookings",
                color_discrete_sequence=["#48b2ff"],
            )
            fig4.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font_color="#ccd6f6", showlegend=False, height=300,
                margin=dict(t=20, b=20, l=0, r=0),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
            )
            st.plotly_chart(fig4, use_container_width=True)

        # Summary metrics
        st.markdown("#### 📌 Key Statistics")
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Total Bookings",   len(bookings))
        s2.metric("Most Used Row",    bookings["Row"].mode()[0] if not bookings.empty else "—")
        s3.metric("Avg Duration",     f"{bookings['Duration (hrs)'].mean():.1f} hrs")
        s4.metric("Most Common Vehicle", bookings["Vehicle Type"].mode()[0])
    else:
        st.info("No booking data yet. Make some bookings to see analytics!")


# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
def sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center; padding: 20px 0 10px;">
            <div style="font-size:2.5rem;">🅿️</div>
            <div style="font-size:1.2rem; font-weight:700; color:#64ffda; letter-spacing:1px;">SmartPark AI</div>
            <div style="font-size:0.75rem; color:#8892b0; margin-top:4px;">AI-Based Smart Parking System</div>
        </div>
        <hr style="border-color:rgba(100,200,255,0.15); margin:10px 0 20px;">
        """, unsafe_allow_html=True)

        page = st.radio(
            "Navigation",
            ["🏠  Home", "🗺️  View Slots", "📝  Book Slot",
             "🤖  AI Suggestion", "📈  Prediction",
             "🔧  Admin Panel", "📊  Reports"],
            label_visibility="collapsed"
        )

        st.markdown("""
        <hr style="border-color:rgba(100,200,255,0.1); margin:20px 0 14px;">
        <div style="font-size:0.76rem; color:#8892b0; text-align:center; line-height:1.7;">
            Built with ❤️ using Python & Streamlit<br>
            <span style="color:#64ffda;">Academic Mini Project</span>
        </div>
        """, unsafe_allow_html=True)

    return page


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────
def main():
    init_session_state()
    page = sidebar()

    if "Home"        in page: page_home()
    elif "View"      in page: page_view_slots()
    elif "Book"      in page: page_book_slot()
    elif "AI"        in page: page_ai_suggestion()
    elif "Prediction"in page: page_prediction()
    elif "Admin"     in page: page_admin()
    elif "Reports"   in page: page_reports()


if __name__ == "__main__":
    main()
