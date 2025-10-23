# StockMarketDataScraper

A lightweight scraper for daily price data of BIST100 stocks with export support to CSV/XLSX.

Key files
- `src/main.py` — CLI entry point and workflow.
- `src/scraper/scraper.py` — HTTP requests and raw JSON retrieval (`Scraper`).
- `src/models/stock_data_model.py` — data model `StockDataModel`.
- `src/utils/export.py` — CSV/XLSX export helpers using pandas (`Export`).
- `src/utils/parser.py` — command-line arguments parsing.
- `src/utils/get_user_agent.py` — helper for selecting a random user-agent.

Features
- Fetch historical daily price data for a given stock within a date range.
- Model the data and provide JSON / pretty-printed output.
- Export results easily to CSV or Excel (.xlsx).

Requirements
- Python 3.9+
- Dependencies: requests, pandas, openpyxl (see requirements.txt)

Installation (macOS)
1. Create and activate a virtual environment:
   - python3 -m venv .venv
   - source .venv/bin/activate
2. Install dependencies:
   - pip install -r requirements.txt

Usage examples
- Basic:
  - python src/main.py --stock-name KOZAL --start 21-10-2025
- With end date:
  - python src/main.py --stock-name KOZAL --start 01-01-2025 --end 22-10-2025
- Pretty output:
  - python src/main.py --stock-name KOZAL --start 21-10-2025 --prettify
- Export to CSV or Excel:
  - python src/main.py --stock-name KOZAL --start 21-10-2025 --export-to-csv ./out.csv
  - python src/main.py --stock-name KOZAL --start 21-10-2025 --export-to-excel ./out.xlsx

Notes & tips
- Command-line arguments are defined in `src/utils/parser.py`.
- Request headers and user-agent are configured in `src/scraper/scraper.py`.
- Export routines expect dates in day-month-year format; numeric formatting is optional.

Contributing
- Please open an issue or submit a pull request for bugs or improvements.