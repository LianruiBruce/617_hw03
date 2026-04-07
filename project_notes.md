# Design Study: State Energy Lifestyle Profiles

## Step 1 — Learning

### Title

**Do U.S. states exhibit different lifestyle profiles through their energy consumption structures?**

### Stakeholder

General public and community advocates who want to understand how everyday energy use differs across U.S. states and how those differences may characterize distinct state lifestyle profiles.

### Background

Looking only at total energy consumption does not reveal how energy is used in everyday life. However, when consumption is broken down by end-use sector — Residential, Commercial, Industrial, and Transportation — different structural patterns may emerge. Some states may show a higher Residential share, suggesting that a larger portion of direct fuel use is tied to household activities such as heating. Others may show stronger Transportation or Industrial shares, indicating more travel dependence or production-oriented energy-use patterns.

This question matters because the public is typically exposed only to aggregate statistics such as "which state consumes the most energy." Those totals are difficult to interpret in terms of daily life. A public-facing visualization tool that highlights structural differences can help users move from comparing totals to understanding profiles, making it easier to discuss how energy-use patterns that may characterize different state lifestyle profiles actually vary across the country.

---

## Step 2 — Winnowing

### Data Source

The primary data source is `energy.csv`, provided via the CORGIS Dataset Project and originally compiled from the U.S. Energy Information Administration (EIA) State Energy Data System (SEDS). The dataset is organized by state and year (1960–2019) and includes sector-level and fuel-type-level energy consumption, expenditure, and price fields. All consumption values are reported in billion BTU.

This project limits the time range to **2010–2019** for manageability and relevance.

### Fields Used and Aggregation Rules

Four end-use sector totals are constructed by summing selected columns. **The `Petroleum` column has different meanings across sectors, requiring careful handling to avoid double-counting:**

| Sector | Formula | Note |
|--------|---------|------|
| **Commercial** | Coal + Petroleum + Natural Gas + Geothermal + Hydropower + Solar + Wind + Wood | Petroleum = "all petroleum products" (includes Distillate Fuel Oil and Kerosene; those sub-columns are NOT added separately) |
| **Industrial** | Coal + Petroleum + Natural Gas + Geothermal + Hydropower + Solar + Wind + Wood | Petroleum = "all petroleum products" (includes Distillate Fuel Oil, Kerosene, Other Petroleum Products) |
| **Transportation** | Coal + Petroleum + Natural Gas | Petroleum = "all petroleum products" (includes Distillate Fuel Oil) |
| **Residential** | Coal + Distillate Fuel Oil + Kerosene + Petroleum + Natural Gas + Geothermal + Wood | Petroleum = "LPG only" — all columns are independent; sum everything |

Sectoral shares (%) are computed as each sector's total divided by the four-sector grand total for that state-year.

### Data Limitations

1. **No end-use electricity**: The dataset does not include electricity consumption by end-use sector (e.g., `Consumption.Residential.Electricity` does not exist). Electricity inputs appear under `Consumption.Electric Power.*`, which represents fuel consumed for power generation, not how that electricity is allocated to end users. Therefore, **this analysis compares direct-fuel consumption profiles, excluding electricity purchased via the grid**.
   - *Implication*: States where residential heating relies primarily on electricity (e.g., Florida, much of the South) will show lower Residential shares than states that burn oil or gas directly for heating (e.g., Maine, Northeast). This is not an error — it is an inherent feature of comparing direct-fuel structures — but it must be acknowledged when interpreting results.
2. **Missing values recorded as 0**: The CORGIS documentation notes that unavailable data or very small values may be recorded as 0. Strong interpretations should not be made for near-zero categories.
3. **"Lifestyle" is interpretive**: Sectoral energy shares approximate, but do not directly measure, lifestyle characteristics. The term "lifestyle profile" is used as a framing device for public communication.

### Why These Fields Are Necessary and Sufficient

- **State** and **Year** identify each unit of analysis.
- The four sector totals define each state's energy profile.
- Normalized shares enable cross-state comparison by removing the effect of state size.

---

## Step 3 — Discover

### Task Generation Process

The target audience is the general public and community advocates. They first need a way to quickly compare structural differences across states (horizontal comparison). However, a single-year snapshot is not enough to understand whether a state's profile is stable or changing, which motivates a temporal exploration task (longitudinal understanding). Together, these two tasks support an overview-to-detail exploration process.

### Task 1 — Cross-State Structural Comparison

- **Action**: Compare
- **Target**: Distribution (sectoral shares across states)
- **Natural language**: Compare how direct-fuel consumption profiles differ across U.S. states in a selected year.
- **Questions it answers**: Which states have higher Residential shares? Which are more Transportation-heavy? Which profiles are more balanced vs. dominated by one sector?

### Task 2 — Single-State Temporal Trend

- **Action**: Identify trends
- **Target**: Change over time (sectoral shares of one state across years)
- **Natural language**: Identify how the direct-fuel consumption profile of a selected state changes over the last decade (2010–2019).
- **Questions it answers**: Is a state's profile stable or shifting? Is it becoming more concentrated in one sector or more balanced?

*(Note: Action/Target terminology should be aligned with the specific task framework from Lecture 16.)*

---

## Step 4 — Design (Low-fi Prototype)

### Layout

The dashboard uses two coordinated views:

```
+-------------------------------------------------------+
| Title: State Energy Lifestyle Profiles                 |
| [Year slider: 2010-2019]  [Sort by: sector dropdown]  |
+----------+--------------------------------------------+
| State    |  View 1: Cross-state comparison            |
| selector |  100% stacked bar chart                    |
| (left    |  X: states (sortable)                      |
| sidebar) |  Y: share (0-100%)                         |
|          |  Colors: Res / Com / Ind / Trans            |
|          +--------------------------------------------+
|          |  View 2: Single-state temporal trend        |
| [click   |  Line chart                                |
|  a state |  X: year (2010-2019)                       |
|  to      |  Y: share                                  |
|  update] |  4 lines: Res / Com / Ind / Trans           |
+----------+--------------------------------------------+
```

### Interaction

- Click a state bar in View 1 → View 2 updates to show that state's decade-long trend (view coordination).
- Drag the year slider → View 1 updates to show the selected year.
- Hover over any element to see exact percentages.

### Design Justifications

1. **Normalized shares over raw totals**: Shares are easier for a public audience to interpret when the goal is structural comparison, not scale comparison.
2. **Sortable stacked bar chart**: Allows quick scanning of which states lead or lag in any sector. Sorting by a specific sector places the most relevant states at the top.
3. **Temporal line chart for detail**: Helps users assess whether a selected state's profile is a stable characteristic or a recent shift.
4. **View coordination**: The two views follow Shneiderman's information-seeking mantra (overview first, zoom and filter, details on demand). Selecting a state in the overview triggers the detail view.
5. **Readability over density**: The stakeholder is non-expert, so the design prioritizes clarity over analytical complexity.

### Trade-offs

- A stacked bar chart makes it harder to compare middle segments across states. Sorting and hover tooltips partially mitigate this.
- Showing all 51 states at once can be visually dense. The sortable axis and state selector help users focus.

---

## Step 5 — Implement

### Technology

- **Streamlit** for the interactive web dashboard
- **Plotly** for charts with hover and click interaction
- **Pandas** for data processing

### Implementation Notes

- `clean_data.py` reads `energy.csv`, applies the sector-specific aggregation rules described in Step 2, computes shares, and outputs `state_sector_profiles.csv`.
- `app.py` loads the cleaned data and renders two Plotly charts within a Streamlit layout.
- View coordination is implemented via Plotly's `on_select` callback: clicking a bar in View 1 updates the state selection for View 2.
- The design choices go beyond tool defaults: custom color palette, coordinated views, sortable axis, normalized stacking, and contextual footer noting data limitations.

---

## Step 6 — Deploy

### Demo 1: Cross-State Differences (2019)

Display the stacked bar chart for all states in 2019. Key observations:

- States do **not** share the same direct-fuel consumption profile.
- Northeast states (e.g., Maine, Vermont) show higher Residential shares, reflecting direct fuel use for heating (oil, gas, wood).
- Gulf/industrial states (e.g., Texas, Louisiana) show stronger Industrial and Transportation shares.
- Comparing structural shares reveals lifestyle-relevant patterns that total consumption alone would obscure.

### Demo 2: Single-State Temporal Trend

Select a state (e.g., Texas) and examine its 2010–2019 trend:

- Is this state's profile stable or shifting?
- The tool reveals whether sectoral energy use is becoming more concentrated or more balanced over time.

### Framing

- Conclusions are framed as "supporting pattern discovery and hypothesis generation," not as direct causal or policy claims.
- Representative states are chosen for demonstration; the tool covers all states.

---

## Step 7 — Iterate (In-Class Feedback, 3/31)

### Feedback Questions

1. Does this visualization clearly communicate how state energy profiles differ?
2. Is the relationship between the comparison view and the time view easy to understand?
3. What additional question would you want this tool to support?

### Stakeholder Feedback Summary

The formative feedback was positive about chart clarity once the views were explained, but it surfaced three important problems for a first-time public user:

1. **The central question was not obvious enough.** Viewers asked what exact question the project was trying to answer.
2. **The meaning of "structure" was unclear.** Stakeholders wanted a more direct explanation that the visualization shows the percentage split across Residential, Commercial, Industrial, and Transportation sectors for each state-year.
3. **The "lifestyle" interpretation needed stronger scaffolding.** Stakeholders were unsure how a sectoral split could relate to everyday life, and they wanted the interface to make the interpretation more concrete.

The strongest design suggestion was to add a **U.S. map** so users could see national patterns more intuitively. They also wanted clearer explanation of how the raw data was processed, including whether values were summed and then normalized.

### Confirmed Third Task

- **Task 3**
- **Action**: Identify
- **Target**: Spatial outliers and extreme values
- **Natural language**: Identify which states stand out as unusually Residential-heavy, Industrial-heavy, or Transportation-heavy, and see where those states appear geographically.

### Iteration Changes

To address that new task and reduce first-use confusion, the revised dashboard adds:

1. **A choropleth map of the United States** showing either each state's dominant sector or the share of a selected sector. This gives a more intuitive national overview than the stacked bar chart alone.
2. **Explicit onboarding text** explaining what question the dashboard answers and how to interact with it.
3. **A data-processing explainer** describing that raw fuel columns were first summed into four sector totals and then converted into shares.
4. **Outlier highlighting** for the top states in a selected sector, making it easier for non-expert users to spot extreme profiles.

These changes make the tool better aligned with the public-facing stakeholder. The dashboard now supports both comparison and explanation, rather than assuming users already understand the data model.

---

## Step 8 — Reflect, Pt 1

### Method for Gathering Feedback

During the in-class summative evaluation on 4/7, I presented the revised dashboard to classmates acting as public stakeholders and asked them to perform short exploration tasks. I also observed where they hesitated, what they clicked first, and which parts required verbal explanation. This lightweight think-aloud style evaluation was useful because the intended audience was not domain-expert; first impressions and moments of confusion mattered as much as formal task completion.

### What the Solution Tells Stakeholders

The revised solution helps classmates see that states differ not only in total energy use, but also in **how that use is distributed across sectors**. The map makes broad regional differences easier to notice, while the stacked bars and temporal trend chart support follow-up questions. For example, users can observe that some Northeast states have comparatively higher Residential shares, while states such as Texas or Louisiana tend to show stronger Industrial or Transportation components. The tool therefore supports pattern discovery and comparison in a way that is more accessible to the public than raw tables or total-consumption rankings.

### What Worked

- The overall visual design was considered clear once users were oriented.
- The addition of the map made the dashboard feel much more intuitive and immediately interpretable.
- The coordinated views supported an effective overview-to-detail workflow.
- The written guidance reduced uncertainty about whether charts and controls were interactive.

### What Did Not Work as Well

- The original version assumed too much prior understanding of the research question.
- Terms such as "structure" and "lifestyle profile" were not self-explanatory to first-time viewers.
- Some controls were not obviously clickable before labels and instructions were added.

### What I Would Keep the Same

I would keep the normalized-share framing, because it makes state-to-state comparison much easier for a public audience than raw totals. I would also keep the coordinated overview-and-detail design, since it matches the two core analytical tasks well.

### Given More Time

Given more time, I would add short annotation callouts for representative states, stronger tooltips that interpret the pattern in plain language, and optional contextual overlays connecting observed patterns to climate, transportation infrastructure, or industrial composition. That would help move the dashboard further from pattern discovery toward actionable public communication.

---

## Step 9 — Reflect, Pt 2

This design study showed that designing visualizations for a public audience requires more than choosing appropriate charts. Even when the charts themselves are readable, users may still be unsure what question the visualization answers, what the visual encoding represents, and how to begin interacting with it. In this project, the biggest lesson was that explanatory framing is part of the visualization design, not an optional extra.

I also learned that coordinated views are especially valuable when the domain is unfamiliar. The map offered an approachable entry point, the stacked bars enabled comparison, and the temporal chart provided detail. Together, these views supported different stages of reasoning. However, the study also reinforced that interaction must be signposted clearly; users should not have to guess which marks or controls are clickable.

More broadly, the process highlighted how strongly stakeholder feedback shapes design. My initial solution emphasized analytical comparison, but the stakeholder pushed the project toward interpretability, guidance, and geographic context. That shift improved the design substantially. For this target problem, the most effective visualization process was not simply to encode the data accurately, but to iteratively build an interface that helps non-expert viewers understand what they are looking at and why it matters.
