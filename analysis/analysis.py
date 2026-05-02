import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

_data = Path(__file__).resolve().parent.parent / "data" / "movies_upgraded1.csv"
df = pd.read_csv(_data)

# CSV column is `runtime` (seconds); keep minutes/hours for reporting
df["runtime_minutes"] = df["runtime"] / 60
df['runtime_hours'] = df['runtime_minutes'] / 60

print(df.isnull().sum())

top_movies = df.sort_values(by='rating', ascending=False)
print(top_movies[["title", "rating", "runtime_hours"]].head())

yearly = df.groupby("year")["rating"].mean().sort_values(ascending=False)
print(yearly.head(10))

df["genres"] = df["genres"].str.split(", ")

df_exploded = df.explode("genres")

top10 = df.sort_values(by="rating", ascending=False).head(10)

plt.figure()
plt.barh(top10["title"], top10["rating"])
plt.xlabel("Rating")
plt.title("Top 10 Movies")
plt.gca().invert_yaxis()
plt.tight_layout()
_chart = Path(__file__).resolve().parent / "top10_movies.png"
plt.savefig(_chart, dpi=150, bbox_inches="tight")
plt.close()
print(f"Saved chart: {_chart}")

new_file = Path(__file__).resolve().parent.parent / "data" / "movies_cleaned.csv"

df.to_csv(new_file, index=False)