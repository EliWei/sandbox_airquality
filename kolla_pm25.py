"""Visar PM2.5 och väder i Malmö de senaste 24 timmarna.

Körs med: python kolla_pm25.py
"""

from datetime import datetime, timezone

import pandas as pd
import requests

LUFT_API = "https://datavardluft.smhi.se/52North/api"
VADER_API = "https://opendata-download-metobs.smhi.se/api/version/1.0"

PM25 = {"PM2.5 Dalaplan": 6247, "PM2.5 Rådhuset": 6161}
VADER = {"Temp (°C)": 1, "Vind (m/s)": 4, "Fukt (%)": 6}  # parametrar för Malmö A
MALMO_A = 52350


def hamta_pm25(tidsserie_id):
    slut = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    svar = requests.get(f"{LUFT_API}/timeseries/{tidsserie_id}/getData",
                        params={"timespan": f"PT24H/{slut}"}, timeout=60)
    svar.raise_for_status()
    df = pd.DataFrame(svar.json()["values"])
    tid = pd.to_datetime(df["timestamp"], unit="ms", utc=True).dt.tz_convert("Europe/Stockholm")
    return pd.Series(df["value"].values, index=tid)


def hamta_vader(parameter):
    url = f"{VADER_API}/parameter/{parameter}/station/{MALMO_A}/period/latest-day/data.json"
    svar = requests.get(url, timeout=60)
    svar.raise_for_status()
    df = pd.DataFrame(svar.json()["value"])
    tid = pd.to_datetime(df["date"], unit="ms", utc=True).dt.tz_convert("Europe/Stockholm")
    return pd.Series(pd.to_numeric(df["value"], errors="coerce").values, index=tid)


kolumner = {}
for namn, ts_id in PM25.items():
    try:
        kolumner[namn] = hamta_pm25(ts_id)
    except Exception as e:
        print(f"Kunde inte hämta {namn}: {e}")

for namn, parameter in VADER.items():
    try:
        kolumner[namn] = hamta_vader(parameter)
    except Exception as e:
        print(f"Kunde inte hämta {namn}: {e}")

tabell = pd.DataFrame(kolumner).sort_index()
tabell.index = tabell.index.strftime("%a %H:%M")

print(f"\nMalmö, senaste 24 timmarna (hämtat {datetime.now():%Y-%m-%d %H:%M})\n")
print(tabell.round(1).to_string())