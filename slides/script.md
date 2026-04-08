# Presentation Script

Target: ~10 minutes. Short sentences for non-native speakers.

---

## Title Slide (~15 sec)

Hi everyone. I'm Lianrui, and my teammate is Shengkai. Today we present our mini design study: State Energy Lifestyle Profiles.

---

## Slide 1 — Outline (~10 sec)

Here is our outline. We have three parts: Precondition, Core, and Analysis. Let's start.

---

## Slide 2 — Step 1: Learning (~40 sec)

Our question is: Do U.S. states have different lifestyle profiles based on how they use energy?

Most people only see total energy rankings. But totals hide how energy is actually used. When we break it into four sectors — Residential, Commercial, Industrial, and Transportation — different patterns appear.

Our stakeholder is the general public. They want a simple way to compare states.

---

## Slide 3 — Step 2: Winnowing (Data) (~40 sec)

Our data comes from the CORGIS dataset, based on the U.S. EIA. It covers 51 states from 2010 to 2019.

For each state and year, we sum fuel columns — like coal, natural gas, petroleum, and wood — into four sector totals. Then we normalize them into percentage shares.

State and Year identify each row. The four shares define the profile. Percentages remove the effect of state size, so we can compare fairly.

---

## Slide 4 — Step 2: Winnowing (Limitations) (~25 sec)

One important limitation: we only look at direct fuel use. Grid electricity is excluded. So states that heat with electricity, like Florida, show a lower Residential share.

Also, missing values are recorded as zero in the source data.

---

## Slide 5 — Step 3: Discover (~40 sec)

Our stakeholder wants two things: compare states side by side, and check if profiles are stable over time. That gives us two tasks.

Task 1 is cross-state comparison. Action: Compare. Target: Distribution.

Task 2 is temporal trend. Action: Identify trends. Target: Change over time.

Task 3 was added after feedback. Action: Identify. Target: Outliers. We want to find extreme states on a map.

---

## Slide 6 — Step 4: Design (~35 sec)

Here is our low-fi sketch. On the left is a sidebar with year and state controls. The main area has a stacked bar chart for Task 1 and a line chart for Task 2.

The key interaction: click a bar to update the detail view. We use percentage shares instead of raw totals because our audience is the general public.

One trade-off: middle segments in stacked bars are hard to compare. Sorting and tooltips help.

---

## Slide 7 — Step 5: Implement (Map) (~20 sec)

This is our final dashboard built with Streamlit and Plotly. The first view is a U.S. map. Each state is colored by its dominant sector. This supports Task 3.

---

## Slide 8 — Step 5: Implement (Bar & Line) (~25 sec)

On the left is the stacked bar chart for Task 1, with star markers for outlier states. On the right is the line chart for Task 2.

All three views are coordinated. Click a state on the map or bar chart, and the line chart updates.

---

## Slide 9 — Step 6: Deploy (~30 sec)

When our stakeholder explored the tool, they noticed clear patterns. Northeast states like Maine and Vermont have higher Residential shares — people there burn fuel directly for heating. Gulf states like Texas and Louisiana have stronger Industrial and Transportation shares. Most profiles are stable over the decade.

---

## Slide 10 — Step 7: Iterate (~35 sec)

During in-class feedback on March 31st, we got two main points. First, the research question was not clear at first glance. Second, stakeholders wanted a U.S. map for spatial context.

In response, we added a choropleth map, onboarding text, and outlier highlights. This is how Task 3 was created.

---

## Slide 11 — Step 8: Reflect Part 1 (~40 sec)

For our evaluation on April 7th, we used think-aloud with classmate stakeholders.

What worked: the map was immediately intuitive, and coordinated views supported a natural overview-to-detail workflow.

What could improve: the original version assumed too much prior knowledge, and some controls were not obviously clickable.

The key insight: states differ in how they use energy, not just how much.

Given more time, we would add richer tooltips and overlays linking patterns to climate data.

---

## Slide 12 — Step 9: Reflect Part 2 (~30 sec)

Four design lessons.

First, framing is part of the design. Charts fail if users don't know the question.

Second, coordinated views help when the domain is unfamiliar.

Third, signpost all interactions. Users should never guess what is clickable.

Fourth, stakeholder feedback can reshape your entire design — and that's a good thing.

---

## Slide 13 — Thanks (~5 sec)

Thanks for listening!
