import requests
import pandas as pd
from datetime import date

pd.set_option("display.max_rows", 200)
pd.set_option("display.width", 200)

BASE = "https://datavardluft.smhi.se/52North/api"
idag = date.today().isoformat()

df = pd.read_csv("tidsserier_malmo.csv")

antal = []
for ts_id in df["tidsserie_id"]:
    print(f"Kollar tidsserie {ts_id}...", flush=True)
    try:
        svar = requests.get(f"{BASE}/timeseries/{ts_id}/getData",
                            params={"timespan": f"P7D/{idag}"},
                            timeout=30).json()
        antal.append(len(svar.get("values", [])))
    except Exception as e:
        print(f"  Fel: {e}")
        antal.append(None)

df["värden_senaste_veckan"] = antal
print(df.sort_values(["plats", "ämne", "procedure"]))
df.to_csv("tidsserier_malmo.csv", index=False)