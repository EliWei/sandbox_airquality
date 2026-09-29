import requests
import pandas as pd

pd.set_option("display.max_rows", 200)
pd.set_option("display.width", 200)

BASE = "https://datavardluft.smhi.se/52North/api"

stationer = {
    "Dalaplan": [271, 272, 273, 274, 275, 276, 278, 412, 4131, 5750],
    "Rådhuset": [117, 118, 120, 121, 122, 123, 125, 4256, 5513, 5528],
}

rader = []
for plats, ids in stationer.items():
    for station_id in ids:
        print(f"Hämtar {plats} id {station_id}...", flush=True)
        try:
            svar = requests.get(f"{BASE}/stations/{station_id}", timeout=30).json()
        except Exception as e:
            print(f"  Fel: {e}")
            continue
        for ts_id, info in svar["properties"]["timeseries"].items():
            rader.append({
                "plats": plats,
                "station_id": station_id,
                "tidsserie_id": ts_id,
                "ämne": info["phenomenon"]["label"],
                "procedure": info["procedure"]["label"],
            })

df = pd.DataFrame(rader)
print(df.sort_values(["plats", "ämne", "procedure"]))
df.to_csv("tidsserier_malmo.csv", index=False)