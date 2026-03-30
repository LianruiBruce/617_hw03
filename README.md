# State Energy Lifestyle Profiles

A mini design study exploring whether U.S. states exhibit different lifestyle profiles through their energy consumption structures.

**Course:** COMP 617 — UNC Chapel Hill  
**Data:** [CORGIS Energy Dataset](https://corgis-edu.github.io/corgis/csv/energy/) / [U.S. EIA SEDS](https://www.eia.gov/state/seds/seds-data-complete.php)

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
| `app.py` | Streamlit dashboard with two coordinated views |
| `project_notes.md` | Full design study writeup (Steps 1–7) |
| `project_notes.pdf` | PDF version of the writeup |
| `feedback_notes.md` | Template for in-class feedback (3/31) |

## Dashboard Features

- **View 1 — Cross-State Comparison:** 100% stacked bar chart showing Residential, Commercial, Industrial, and Transportation shares for all states in a selected year. Sortable by any sector.
- **View 2 — Single-State Temporal Trend:** Line chart showing how a selected state's profile changes over 2010–2019.
- **View Coordination:** Click a state bar in View 1 to update View 2.

## Data Note

The analysis compares **direct-fuel consumption profiles** (coal, gas, petroleum, wood, etc.) and does **not** include electricity purchased via the grid. See `project_notes.md` § Step 2 for full details on aggregation rules and limitations.
