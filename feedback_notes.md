# Feedback Notes — In-Class Session (3/31)

## Questions Asked

1. Does this visualization clearly communicate how state energy profiles differ?
2. Is the relationship between the comparison view and the time view easy to understand?
3. What additional question would you want this tool to support?

## Raw Feedback

| # | Source | Comment |
|---|--------|---------|
| 1 | Classmate stakeholder | The charts looked clear, but I was not sure what exact question the project was answering at first. |
| 2 | Classmate stakeholder | I did not immediately understand what "structure" meant in the chart. |
| 3 | Classmate stakeholder | It was not obvious how this energy structure connects to people's daily life or "lifestyle." |
| 4 | Classmate stakeholder | A U.S. map would make the patterns more intuitive than only using the bar chart. |
| 5 | Classmate stakeholder | I wanted to know how the original data was processed: did you add columns together, and then normalize them? |
| 6 | Classmate stakeholder | The interface was clear after explanation, but I wanted more guidance on how to use it the first time. |
| 7 | Classmate stakeholder | Some controls did not obviously look clickable at first. |

## Summary of Improvement Directions

- Make the project question explicit in the interface.
- Explain that "structure" refers to the percentage split across the four sectors.
- Clarify that "lifestyle profile" is an interpretive framing rather than a direct measurement.
- Add a U.S. map to provide a more intuitive overview of national patterns.
- Explain the data-processing pipeline from raw columns to sector totals to normalized shares.
- Add clearer onboarding text so first-time users know what to click and what interactions are available.
- Highlight unusual or extreme states to support faster discovery.

## Confirmed Third Task

- **Task 3**: Identify states with unusual energy-use profiles and see where they appear geographically.
- Action: Identify
- Target: Spatial outliers and extreme values
- Natural language description: Find states that are especially Residential-heavy, Industrial-heavy, or Transportation-heavy, and understand those outliers in a national context.
- Planned implementation change: Add a U.S. choropleth map, provide a dominant-sector view for each state, and highlight top outlier states for a selected sector in the comparison chart.
