import requests
import pandas as pd

pd.set_option("display.max_rows", 200)
pd.set_option("display.width", 200)

url = "https://datavardluft.smhi.se/52North/api/stations"
stations = requests.get(url).json()

df = pd.DataFrame([{
    "id": s["id"],
    "namn": s["properties"]["label"],
    "typ": s["properties"].get("classification"),
    "lon": s["geometry"]["coordinates"][0],
    "lat": s["geometry"]["coordinates"][1],
} for s in stations])

print(len(df), "stationer")
print(df["typ"].value_counts())

# Bara stationer vars namn börjar med "Malmö"
malmo = df[df["namn"].str.startswith("Malmö")]

print("\nAntal id-nummer per plats i Malmö:")
print(malmo.groupby(["namn", "typ"]).size().sort_values(ascending=False))

print("\nDalaplan och Rådhuset:")
print(malmo[malmo["namn"].str.contains("Dalaplan|Rådhus", case=False)])