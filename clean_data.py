"""
Generate state_sector_profiles.csv from energy.csv.

Aggregation rules per sector (avoids Petroleum double-counting):
  Commercial   = Coal + Petroleum(all) + NatGas + Geothermal + Hydro + Solar + Wind + Wood
  Industrial   = Coal + Petroleum(all) + NatGas + Geothermal + Hydro + Solar + Wind + Wood
  Transportation = Coal + Petroleum(all) + NatGas
  Residential  = Coal + DistillateFuelOil + Kerosene + Petroleum(LPG) + NatGas + Geothermal + Wood
"""

import pandas as pd

df = pd.read_csv("energy.csv")

# --- sector totals (billion BTU) ---

df["Commercial"] = (
    df["Consumption.Commercial.Coal"]
    + df["Consumption.Commercial.Petroleum"]       # all petroleum products
    + df["Consumption.Commercial.Natural Gas"]
    + df["Consumption.Commercial.Geothermal"]
    + df["Consumption.Commercial.Hydropower"]
    + df["Consumption.Commercial.Solar"]
    + df["Consumption.Commercial.Wind"]
    + df["Consumption.Commercial.Wood"]
)

df["Industrial"] = (
    df["Consumption.Industrial.Coal"]
    + df["Consumption.Industrial.Petroleum"]        # all petroleum products
    + df["Consumption.Industrial.Natural Gas"]
    + df["Consumption.Industrial.Geothermal"]
    + df["Consumption.Industrial.Hydropower"]
    + df["Consumption.Industrial.Solar"]
    + df["Consumption.Industrial.Wind"]
    + df["Consumption.Industrial.Wood"]
)

df["Transportation"] = (
    df["Consumption.Transportation.Coal"]
    + df["Consumption.Transportation.Petroleum"]    # all petroleum products
    + df["Consumption.Transportation.Natural Gas"]
)

df["Residential"] = (
    df["Consumption.Residential.Coal"]
    + df["Consumption.Residential.Distillate Fuel Oil"]
    + df["Consumption.Residential.Kerosene"]
    + df["Consumption.Residential.Petroleum"]       # LPG only
    + df["Consumption.Residential.Natural Gas"]
    + df["Consumption.Residential.Geothermal"]
    + df["Consumption.Residential.Wood"]
)

# --- keep 2010-2019 ---
out = df.loc[
    df["Year"].between(2010, 2019),
    ["State", "Year", "Residential", "Commercial", "Industrial", "Transportation"],
].copy()

# --- compute shares ---
out["Total"] = out[["Residential", "Commercial", "Industrial", "Transportation"]].sum(axis=1)
for sector in ["Residential", "Commercial", "Industrial", "Transportation"]:
    out[f"{sector}_share"] = (out[sector] / out["Total"] * 100).round(2)

out.to_csv("state_sector_profiles.csv", index=False)
print(f"Wrote {len(out)} rows to state_sector_profiles.csv")
print(out.head(10).to_string(index=False))
