# Salvadoran Restaurant Finder 🥟

A Python scraper that finds Salvadoran restaurants in LA using Google Places API. Part of an ETL pipeline that will scrape, transform, and visualize restaurant data on Tableau Public maps.

⚠️ **Cost Warning**: This uses Google Places API which charges per request. Monitor your usage!

## 🚀 Setup

1. Get API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Places API
3. Create `.env`: `GOOGLE_PLACES_API_KEY=your_key_here`
4. Install: `pip install -r requirements.txt`

## 📖 Usage

```bash
python scrapper.py
```

## 🔮 Future Plans

This is **Phase 1** of a complete ETL pipeline:
- **Extract** → Scrape restaurant data via Places API ✅
- **Transform** → Clean and enrich data (coming soon)
- **Load** → Visualize on Tableau Public interactive maps (coming soon)

## 📊 Output

Generates `salvadoran_restaurants.csv` with restaurant names, ratings, locations, and addresses for Tableau visualization.