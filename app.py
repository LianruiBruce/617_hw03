"""
State Energy Lifestyle Profiles — Streamlit Dashboard

Three coordinated views:
  View 1: U.S. map of dominant sector or sector share
  View 2: Cross-state comparison (100% stacked bar, sortable)
  View 3: Single-state temporal trend (line chart, 2010-2019)
"""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="State Energy Lifestyle Profiles", layout="wide")

SECTORS = ["Residential", "Commercial", "Industrial", "Transportation"]
COLORS = {
    "Residential": "#4C78A8",
    "Commercial": "#F58518",
    "Industrial": "#E45756",
    "Transportation": "#72B7B2",
}
STATE_ABBR = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}
DOMINANT_CODE = {sector: idx for idx, sector in enumerate(SECTORS)}


@st.cache_data
def load_data():
    df = pd.read_csv("state_sector_profiles.csv")
    df["abbr"] = df["State"].map(STATE_ABBR)
    df["Dominant sector"] = df[[f"{sector}_share" for sector in SECTORS]].idxmax(axis=1)
    df["Dominant sector"] = df["Dominant sector"].str.replace("_share", "", regex=False)
    df["Dominant share"] = df[[f"{sector}_share" for sector in SECTORS]].max(axis=1)
    df["Dominant code"] = df["Dominant sector"].map(DOMINANT_CODE)
    return df


def build_outlier_table(year_df, focus_sector):
    outliers = (
        year_df[["State", f"{focus_sector}_share"]]
        .sort_values(f"{focus_sector}_share", ascending=False)
        .head(5)
        .rename(columns={f"{focus_sector}_share": "Share (%)"})
    )
    outliers["Share (%)"] = outliers["Share (%)"].round(2)
    return outliers


def sector_shade_scale(sector):
    return [[0.0, "#F4F4F4"], [1.0, COLORS[sector]]]


df = load_data()

# Sidebar
st.sidebar.title("Controls")
year = st.sidebar.slider("Year", 2010, 2019, 2019)
sort_by = st.sidebar.selectbox("Sort states by", ["State name"] + SECTORS)
selected_state = st.sidebar.selectbox(
    "State for detail view", sorted(df["State"].unique()), index=4
)
map_mode = st.sidebar.selectbox(
    "Map coloring",
    ["Dominant sector"] + [f"{sector} share" for sector in SECTORS],
    help="Use the map to see which sector dominates a state, or switch to a single sector share.",
)
highlight_sector = st.sidebar.selectbox(
    "Highlight outliers for",
    [sector for sector in SECTORS if sector != "Commercial"] + ["Commercial"],
)
show_outliers = st.sidebar.checkbox("Highlight top 5 outlier states", value=True)

# Title and framing
st.title("State Energy Lifestyle Profiles")
st.markdown(
    "This tool helps the general public compare how states differ in **direct-fuel energy use structure** "
    "and explore whether those structures stay stable over time."
)

st.info(
    "How to use this dashboard: 1) Choose a year. 2) Read the map for a quick national overview. "
    "3) Compare states in the stacked bar chart. 4) Click a state in the map or bar chart to update the time trend."
)

with st.expander("What question does this project answer?"):
    st.write(
        "The dashboard asks whether U.S. states show different energy-use profiles when we compare the "
        "share of direct-fuel consumption in Residential, Commercial, Industrial, and Transportation sectors. "
        "For a public audience, these profiles provide a more intuitive description than total energy consumption alone."
    )
    st.write(
        "Here, 'structure' means the percentage split across those four sectors in one state and one year. "
        "A state with a much larger Transportation share, for example, looks different from a state with a much larger Residential share."
    )

with st.expander("How was the raw data processed?"):
    st.write(
        "The raw CORGIS / EIA data reports many fuel-specific columns. We first summed relevant fuel columns into "
        "four sector totals: Residential, Commercial, Industrial, and Transportation."
    )
    st.write(
        "After that, we computed each sector's share as: sector total / (Residential + Commercial + Industrial + Transportation). "
        "The result is a 100% profile for each state-year."
    )
    st.write(
        "Important limitation: these shares describe direct-fuel use only and do not include electricity purchased through the grid."
    )

year_df = df[df["Year"] == year].copy()
if sort_by == "State name":
    year_df = year_df.sort_values("State")
else:
    year_df = year_df.sort_values(f"{sort_by}_share", ascending=False)

if map_mode == "Dominant sector":
    map_title = f"View 1: Dominant Direct-Fuel Sector by State ({year})"
    map_fig = go.Figure()
    for sector in SECTORS:
        sector_df = year_df[year_df["Dominant sector"] == sector]
        if sector_df.empty:
            continue
        hover_text = [
            (
                f"{row['State']}<br>Dominant sector: {sector}<br>"
                f"Dominant share: {row['Dominant share']:.1f}%<br>"
                + "<br>".join(f"{s}: {row[f'{s}_share']:.1f}%" for s in SECTORS)
            )
            for _, row in sector_df.iterrows()
        ]
        map_fig.add_trace(
            go.Choropleth(
                locations=sector_df["abbr"],
                z=sector_df["Dominant share"],
                locationmode="USA-states",
                colorscale=sector_shade_scale(sector),
                zmin=25,
                zmax=80,
                marker_line_color="white",
                marker_line_width=0.8,
                text=hover_text,
                hovertemplate="%{text}<extra></extra>",
                name=sector,
                showscale=False,
                showlegend=True,
            )
        )
else:
    focus_sector = map_mode.replace(" share", "")
    map_title = f"View 1: {focus_sector} Share by State ({year})"
    z_values = year_df[f"{focus_sector}_share"]
    colorbar = dict(title="Share (%)", len=0.75)
    hover_text = [
        (
            f"{state}<br>{focus_sector}: {row[f'{focus_sector}_share']:.1f}%<br>"
            + f"Dominant sector: {row['Dominant sector']}"
        )
        for state, (_, row) in zip(year_df["State"], year_df.iterrows())
    ]
    colorscale = "Blues"
    map_fig = go.Figure(
        go.Choropleth(
            locations=year_df["abbr"],
            z=z_values,
            locationmode="USA-states",
            colorscale=colorscale,
            marker_line_color="white",
            marker_line_width=0.8,
            text=hover_text,
            hovertemplate="%{text}<extra></extra>",
            colorbar=colorbar,
        )
    )
map_fig.update_layout(
    title=map_title,
    geo_scope="usa",
    clickmode="event+select",
    height=420,
    margin=dict(t=60, b=20, l=0, r=0),
)
if map_mode == "Dominant sector":
    map_fig.update_layout(
        legend=dict(
            title="Dominant sector",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        )
    )

map_event = st.plotly_chart(
    map_fig,
    use_container_width=True,
    on_select="rerun",
    key="map",
    config={"scrollZoom": False, "displayModeBar": False, "staticPlot": False},
)
if map_event and map_event.selection and map_event.selection.points:
    clicked_abbr = map_event.selection.points[0].get("location")
    for state_name, abbr in STATE_ABBR.items():
        if abbr == clicked_abbr:
            selected_state = state_name
            break

# View 2: Cross-state comparison
st.subheader(f"View 2: Cross-State Comparison ({year})")

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

if show_outliers:
    outlier_states = build_outlier_table(year_df, highlight_sector)
    fig1.add_trace(
        go.Scatter(
            x=outlier_states["State"],
            y=[101] * len(outlier_states),
            mode="markers+text",
            text=["Outlier"] * len(outlier_states),
            textposition="top center",
            marker=dict(symbol="star", size=10, color="#222222"),
            name=f"Top {highlight_sector} outliers",
            hovertemplate=highlight_sector + ": %{x}<extra></extra>",
        )
    )

fig1.update_layout(
    barmode="stack",
    title=f"Sector Shares Across States — {year}",
    clickmode="event+select",
    xaxis_title="State",
    yaxis_title="Share of Direct-Fuel Consumption (%)",
    yaxis=dict(range=[0, 106]),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    height=450,
    margin=dict(t=60, b=80),
)
fig1.update_xaxes(tickangle=-45, tickfont_size=9)

bar_event = st.plotly_chart(fig1, use_container_width=True, on_select="rerun", key="bar")
if bar_event and bar_event.selection and bar_event.selection.points:
    clicked = bar_event.selection.points[0].get("x")
    if clicked and clicked in df["State"].values:
        selected_state = clicked

if show_outliers:
    st.caption(
        f"Star markers identify the top 5 states with the highest {highlight_sector.lower()} share in {year}."
    )
    st.dataframe(build_outlier_table(year_df, highlight_sector), hide_index=True, use_container_width=True)

# View 3: Single-state temporal trend
st.subheader(f"View 3: Energy Profile Over Time — {selected_state}")

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

latest_row = state_df[state_df["Year"] == year].iloc[0]
st.markdown(
    f"**Current reading for {selected_state} in {year}:** "
    f"Residential {latest_row['Residential_share']:.1f}%, "
    f"Commercial {latest_row['Commercial_share']:.1f}%, "
    f"Industrial {latest_row['Industrial_share']:.1f}%, "
    f"Transportation {latest_row['Transportation_share']:.1f}%. "
    f"The dominant sector is **{latest_row['Dominant sector']}**."
)

st.caption(
    "Data: CORGIS / U.S. EIA State Energy Data System (1960-2019). "
    "Shares reflect direct-fuel consumption only and exclude electricity purchased via the grid. "
    "Missing or negligible values may be recorded as 0 in the source data."
)
