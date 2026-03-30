"""
State Energy Lifestyle Profiles — Streamlit Dashboard

Two coordinated views:
  View 1: Cross-state comparison (100% stacked bar, sortable)
  View 2: Single-state temporal trend (line chart, 2010-2019)
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="State Energy Lifestyle Profiles", layout="wide")

SECTORS = ["Residential", "Commercial", "Industrial", "Transportation"]
COLORS = {
    "Residential": "#4C78A8",
    "Commercial": "#F58518",
    "Industrial": "#E45756",
    "Transportation": "#72B7B2",
}


@st.cache_data
def load_data():
    return pd.read_csv("state_sector_profiles.csv")


df = load_data()

# ── Sidebar ──────────────────────────────────────────────────────────────────
st.sidebar.title("Controls")
year = st.sidebar.slider("Year", 2010, 2019, 2019)
sort_by = st.sidebar.selectbox("Sort states by", ["State name"] + SECTORS)
selected_state = st.sidebar.selectbox("State for temporal view", sorted(df["State"].unique()), index=4)

# ── Title ────────────────────────────────────────────────────────────────────
st.title("State Energy Lifestyle Profiles")
st.markdown(
    "Direct-fuel consumption shares by sector across U.S. states. "
    "Click a bar in the top chart or use the sidebar to select a state for the temporal view."
)

# ── View 1: Cross-state comparison ──────────────────────────────────────────
year_df = df[df["Year"] == year].copy()

if sort_by == "State name":
    year_df = year_df.sort_values("State")
else:
    year_df = year_df.sort_values(f"{sort_by}_share", ascending=False)

fig1 = go.Figure()
for sector in SECTORS:
    fig1.add_trace(
        go.Bar(
            x=year_df["State"],
            y=year_df[f"{sector}_share"],
            name=sector,
            marker_color=COLORS[sector],
            hovertemplate="%{x}<br>" + sector + ": %{y:.1f}%<extra></extra>",
        )
    )

fig1.update_layout(
    barmode="stack",
    title=f"Cross-State Energy Profiles — {year}",
    xaxis_title="State",
    yaxis_title="Share of Direct-Fuel Consumption (%)",
    yaxis=dict(range=[0, 100]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    height=420,
    margin=dict(t=60, b=80),
)
fig1.update_xaxes(tickangle=-45, tickfont_size=9)

event = st.plotly_chart(fig1, use_container_width=True, on_select="rerun", key="bar")

if event and event.selection and event.selection.points:
    clicked = event.selection.points[0].get("x")
    if clicked and clicked in df["State"].values:
        selected_state = clicked

# ── View 2: Single-state temporal trend ─────────────────────────────────────
st.subheader(f"Energy Profile Over Time — {selected_state}")

state_df = df[df["State"] == selected_state].sort_values("Year")

fig2 = go.Figure()
for sector in SECTORS:
    fig2.add_trace(
        go.Scatter(
            x=state_df["Year"],
            y=state_df[f"{sector}_share"],
            mode="lines+markers",
            name=sector,
            line=dict(color=COLORS[sector], width=2),
            hovertemplate="%{x}<br>" + sector + ": %{y:.1f}%<extra></extra>",
        )
    )

fig2.update_layout(
    xaxis_title="Year",
    yaxis_title="Share of Direct-Fuel Consumption (%)",
    yaxis=dict(range=[0, 100]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    height=380,
    margin=dict(t=40, b=40),
)
fig2.update_xaxes(dtick=1)

st.plotly_chart(fig2, use_container_width=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.caption(
    "Data: CORGIS / U.S. EIA State Energy Data System (1960-2019). "
    "Shares reflect direct-fuel consumption only (excludes electricity purchased via the grid). "
    "Missing or negligible values may be recorded as 0 in the source data."
)
