# IMDb Movie Scraper with Pandas

A beginner-friendly Python project structure to scrape movie data from IMDb and analyze it using Pandas.

## Folder structure

```
imdb-scraper/
├── scraper/
│   └── imdb_scraper.py
├── analysis/
│   └── analysis.py
├── data/
│   └── movies.csv
├── requirements.txt
└── README.md
```

## What each folder is for

- **`scraper/`**: code to scrape movie data from IMDb and save it to `data/movies.csv`
- **`analysis/`**: code to read `data/movies.csv` and analyze it with Pandas (and optionally plot with Matplotlib)
- **`data/`**: CSV files produced by the scraper (starts with an empty `movies.csv`)

## Setup

From the `imdb-scraper/` folder, install dependencies:

```bash
pip install -r requirements.txt
```

## Run the scraper

From the `imdb-scraper/` folder:

```bash
python scraper/imdb_scraper.py
```

## Run the analysis

From the `imdb-scraper/` folder:

```bash
python analysis/analysis.py
```

