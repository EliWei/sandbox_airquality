"""Hämtar SMHI:s väderprognos för Malmö A och sparar de första 24 timmarna.

Körs en gång i timmen av GitHub Actions. Varje körning läggs till i en fil per dygn.
"""

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

LAT, LON = 55.5715, 13.0708  # Malmö A, samma station som våra väderobservationer
URL = ("https://opendata-download-metfcst.smhi.se/api/category/snow1g/version/1/"
       f"geotype/point/lon/{LON}/lat/{LAT}/data.json")
MAPP = Path(__file__).resolve().parent / "prognoser"
TIMMAR = 24  # hur långt fram vi sparar


def main():
    svar = requests.get(URL, timeout=60)
    svar.raise_for_status()
    data = svar.json()

    df = pd.json_normalize(data["timeSeries"])
    df.columns = [c.replace("data.", "") for c in df.columns]
    df["time"] = pd.to_datetime(df["time"], utc=True)

    # Spara bara de närmaste 24 timmarna
    referens = pd.to_datetime(data["referenceTime"], utc=True)
    df = df[df["time"] <= referens + pd.Timedelta(hours=TIMMAR)].copy()

    # Information om vilken prognos raden kommer från
    df.insert(0, "referenceTime", data["referenceTime"])
    df.insert(1, "hamtad_utc", datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    df.insert(2, "timmar_fram", ((df["time"] - referens).dt.total_seconds() / 3600).round(2))

    # Lägg till i dagens fil
    MAPP.mkdir(exist_ok=True)
    fil = MAPP / f"prognos_{datetime.now(timezone.utc):%Y-%m-%d}.csv"
    if fil.exists():
        df = pd.concat([pd.read_csv(fil), df], ignore_index=True)
    df.to_csv(fil, index=False)

    print(f"Sparade prognos med referenceTime {data['referenceTime']} i {fil.name}")


if __name__ == "__main__":
    main()