# Presentation Script

Target: ~10 minutes total. Simple sentences for non-native speakers.

---

## Title Slide (~15 sec)

Hi everyone. My name is Lianrui, and my teammate is Shengkai. Today we will present our mini design study: State Energy Lifestyle Profiles.

---

## Slide 1 — Outline (~15 sec)

Here is our outline. We will go through three parts: the precondition phase, the core design phase, and the analysis phase. Let's get started.

---

## Slide 2 — Step 1: Learning (~50 sec)

Our research question is: Do U.S. states have different lifestyle profiles based on how they use energy?

Most people only see total energy rankings. But totals don't tell you how energy is actually used. If we break it down into four sectors — Residential, Commercial, Industrial, and Transportation — we can see very different patterns across states.

Our stakeholder is the general public. They want a simple and intuitive way to compare states, not just by how much energy they use, but by how they use it.

---

## Slide 3 — Step 2: Winnowing (~50 sec)

Our data comes from the CORGIS dataset, which is based on the U.S. Energy Information Administration. It covers all 51 states from 2010 to 2019.

For each state and year, we summed fuel-specific columns — like coal, natural gas, petroleum, and wood — into four sector totals. Then we normalized them into percentage shares.

These four shares are both necessary and sufficient. State and Year identify each row. The four shares define the profile. And using percentages removes the effect of state size, so we can compare fairly.

One important limitation: we only look at direct fuel use. We do not include electricity from the grid. So states that heat with electricity may look lower in the Residential sector.

---

## Slide 4 — Step 3: Discover (~50 sec)

Next, we defined our tasks. Our stakeholder wants two things: first, compare states side by side; second, check if a state's profile is stable over time. So we got two core tasks.

Task 1 is cross-state comparison. The action is Compare, and the target is Distribution. We want to compare sector share profiles across all states in one year.

Task 2 is temporal trend. The action is Identify Trends, and the target is Change Over Time. We want to see how one state's profile changes from 2010 to 2019.

Task 3 was added later after feedback. The action is Identify, and the target is Spatial Outliers. We want to find states with extreme shares and see where they are on a map.

---

## Slide 5 — Step 4: Design (~45 sec)

Here is our low-fidelity sketch. On the left is a sidebar with controls for year and state. The top area shows a stacked bar chart for cross-state comparison, which supports Task 1. The bottom area shows a line chart for the temporal trend, which supports Task 2.

The key interaction is: click a bar, and the detail view updates. This follows the overview-to-detail pattern.

We chose percentage shares instead of raw totals because our audience is the general public — shares are easier to understand.

One trade-off: in a stacked bar chart, the middle segments are hard to compare. We mitigate this with sorting and tooltips.

---

## Slide 6 — Step 5: Implement (Map) (~30 sec)

This is our final dashboard. We built it with Streamlit and Plotly. The first view is a U.S. choropleth map, which was added to support Task 3. Each state is colored by its dominant direct-fuel sector. Users can also switch to see a single sector's share across the country.

---

## Slide 7 — Step 5: Implement (Bar & Line) (~30 sec)

On the left is View 2 — the stacked bar chart for Task 1. The star markers highlight the top five outlier states for a selected sector. On the right is View 3 — the line chart for Task 2, showing California's profile over the decade.

All three views are coordinated. Clicking a state on the map or bar chart automatically updates the line chart.

---

## Slide 8 — Steps 6 & 7: Deploy & Iterate (~60 sec)

When our stakeholder explored the tool, they noticed some interesting patterns. Northeast states like Maine and Vermont show a higher Residential share — because people there burn oil and gas directly for heating. Gulf states like Texas and Louisiana show stronger Industrial and Transportation shares. And most states have relatively stable profiles over the decade.

During in-class feedback on March 31st, we got two main suggestions. First, the research question was not clear enough at first glance. Second, our stakeholder wanted a U.S. map so they could see spatial patterns right away.

In response, we added the choropleth map, onboarding text to explain the question, and outlier highlighting. This is how Task 3 was born.

---

## Slide 9 — Step 8: Reflect Part 1 (~50 sec)

For our summative evaluation on April 7th, we used a think-aloud method. We asked classmates to explore the dashboard and tell us what they were thinking.

The key insight from our tool is that states differ not just in how much energy they use, but in how they use it. Regional patterns show up clearly that you cannot see from totals alone.

What worked well: the map made the dashboard immediately intuitive, and the coordinated views supported a natural workflow from overview to detail.

What could improve: the original version assumed users already understood the research question. Also, some controls did not look obviously clickable.

If we had more time, we would add annotation callouts and overlays that connect energy patterns to things like climate or infrastructure.

---

## Slide 10 — Step 9: Reflect Part 2 (~45 sec)

Finally, here are our four lessons about the visualization design process.

First, framing is part of the design. Even good charts fail if users don't know what question they are answering.

Second, coordinated views really help when the domain is unfamiliar. The map, bar chart, and line chart each support a different stage of reasoning.

Third, you have to signpost all interactions. Users should never have to guess what is clickable.

Fourth, stakeholder feedback can reshape your entire design. Our project shifted from an analytical focus to a more interpretable, guided experience — and that was a big improvement.

---

## Slide 11 — Thanks (~5 sec)

Thanks for listening!
