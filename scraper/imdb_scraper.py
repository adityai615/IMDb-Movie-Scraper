import requests
import pandas as pd
from pathlib import Path
from datetime import datetime

url = "https://graphql.imdb.com/"

query = """
{
  chartTitles(chart: { chartType: TOP_RATED_MOVIES }, first: 50) {
    edges {
      node {
        titleText {
          text
        }
        releaseYear {
          year
        }
        runtime {
          seconds
        }
        genres{
          genres{
            text
          }
        }
        primaryImage {
          url
        }
        ratingsSummary {
          aggregateRating
        }
      }
    }
  }
}
"""

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

response = requests.post(url, json={"query": query}, headers=headers)

data = response.json()

movies = data["data"]["chartTitles"]["edges"]

movie_list = []

for i, movie in enumerate(movies, start=1):
    node = movie["node"]
    print(node)
    title = node["titleText"]["text"]
    rating = node["ratingsSummary"]["aggregateRating"]
    year = node["releaseYear"]["year"] if node["releaseYear"] else None
    runtime = node["runtime"]["seconds"] if node["runtime"] else None
    genre_items = (node.get("genres") or {}).get("genres") or []
    genres = ", ".join([g.get("text") for g in genre_items if isinstance(g, dict) and g.get("text")]) or None
    image = node["primaryImage"]["url"] if node["primaryImage"] else None
    
    movie_list.append({
        "title": title,
        "rating": rating,
        "year": year,
        "runtime": runtime,
        "genres": genres,
        "image": image
    })

df = pd.DataFrame(movie_list)

df = df.drop_duplicates()

# Top 10
print(df.head(10))

# Save CSV
repo_root = Path(__file__).resolve().parents[1]
data_dir = repo_root / "data"
data_dir.mkdir(parents=True, exist_ok=True)
out_path = data_dir / "movies_upgraded1.csv"
tmp_path = data_dir / "movies.tmp.csv"

try:
    # Write to a temp file first to reduce partial-write risk
    df.to_csv(tmp_path, index=False, encoding="utf-8-sig")
    tmp_path.replace(out_path)
except PermissionError:
    # Common on Windows/OneDrive if the CSV is open in Excel or being synced.
    fallback = data_dir / f"movies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(fallback, index=False, encoding="utf-8-sig")
    print(f"Could not overwrite {out_path} (file locked). Saved to: {fallback}")