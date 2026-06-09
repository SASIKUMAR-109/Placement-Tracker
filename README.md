# College Placement Tracker

## What This Project Does
A full-stack web application that tracks and visualises
college placement data across India from 2017 to 2025,
sourced from NIRF government rankings data.

## Tech Stack
- Python — data pipeline and Flask REST API
- SQLite — relational database for time-series data
- HTML, CSS, JavaScript — interactive frontend dashboard
- Chart.js — data visualisation

## Features
- Search any college by name or abbreviation (IIT, NIT, BITS)
- Year-wise placement trend shown as a line chart
- Stat cards showing total students, placed, percentage
- Detailed data table with year and branch breakdown
- 3991 records across 221 colleges from 2017 to 2025
- Data sourced from NIRF Ministry of Education rankings

## How To Run
1. Install dependencies: pip install -r requirements.txt
2. Run the scraper: python scraper/scraper.py
3. Start the API: python api/app.py
4. Open frontend/index.html in your browser
5. Or visit http://127.0.0.1:5000/dashboard after starting API

## Project Structure
placement_tracker/
├── scraper/scraper.py     ← CSV parser and data pipeline
├── database/placement.db  ← SQLite database
├── api/app.py             ← Flask REST API
├── frontend/              ← HTML CSS JS dashboard
└── requirements.txt       ← Python dependencies