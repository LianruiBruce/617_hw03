# State Energy Lifestyle Profiles

A mini design study exploring whether U.S. states exhibit different lifestyle profiles through their energy consumption structures.

**Course:** COMP 617 — UNC Chapel Hill  
**Data:** [CORGIS Energy Dataset](https://corgis-edu.github.io/corgis/csv/energy/) / [U.S. EIA SEDS](https://www.eia.gov/state/seds/seds-data-complete.php)

## Live Demo

This project is deployed on Streamlit Community Cloud: **[https://unc617hw03.streamlit.app/](https://unc617hw03.streamlit.app/)**

The hosted app runs on a **free** tier, so the first time you open it (especially after the app has been idle), the service may **cold-start** and take **at least about a minute** to become ready. If the page does not load right away, **wait and then refresh** the browser.

A screen-recording walkthrough is committed in this repository: [`hw03_recording.mp4`](hw03_recording.mp4).

## Quick Start

### 1. Install dependencies

```bash
pip install streamlit pandas plotly
```

### 2. Prepare data

```bash
python clean_data.py
```

This reads `energy.csv` and generates `state_sector_profiles.csv` with sector-level consumption shares for 2010–2019.

### 3. Launch the dashboard

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

## Project Structure

| File | Description |
|------|-------------|
| `energy.csv` | Raw dataset (CORGIS / EIA, 1960–2019, all states) |
| `clean_data.py` | Data cleaning script with sector-specific Petroleum handling |
| `state_sector_profiles.csv` | Cleaned output: 51 states × 10 years, four sector shares |
| `app.py` | Streamlit dashboard with three coordinated views and onboarding guidance |
| `project_notes.md` | Full design study writeup (Steps 1–9) |
| `project_notes.pdf` | PDF version of the writeup |
| `feedback_notes.md` | Documented in-class stakeholder feedback (3/31) |

## Dashboard Features

- **View 1 — U.S. Map:** Choropleth map showing either each state's dominant direct-fuel sector or the share of a selected sector.
- **View 2 — Cross-State Comparison:** 100% stacked bar chart showing Residential, Commercial, Industrial, and Transportation shares for all states in a selected year. Sortable by any sector.
- **View 3 — Single-State Temporal Trend:** Line chart showing how a selected state's profile changes over 2010–2019.
- **View Coordination:** Click a state in the map or bar chart to update the state detail view.
- **Outlier Highlighting:** Optional star markers and table identify the top 5 states with the highest share in a selected sector.
- **Onboarding and Data Explanation:** The app includes a research-question panel, usage guidance, and a plain-language explanation of how raw data is aggregated into sector shares.

## Data Note

The analysis compares **direct-fuel consumption profiles** (coal, gas, petroleum, wood, etc.) and does **not** include electricity purchased via the grid. See `project_notes.md` § Step 2 for full details on aggregation rules and limitations.
