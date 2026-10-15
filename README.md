# College Placement Tracker

**Live demo:** [placement-tracker-in.vercel.app](https://placement-tracker-in.vercel.app/)

## What This Project Does
A full-stack web application that tracks and visualises college placement
data across India from 2017 to 2025, using NIRF (Ministry of Education)
rankings data. Search a college to see how its placement percentage,
student counts, and packages changed over the years.

## Features
- Search any college by name or abbreviation (IIT, NIT, BITS)
- Year-wise placement trend shown as a line chart
- Stat cards showing total students, placed, and placement percentage
- Detailed data table with year and branch breakdown
- 3,991 records across 221 colleges from 2017 to 2025
- Colleges classified as Government / Private / Unknown

## Tech Stack
- **Python**: data pipeline and Flask REST API
- **SQLite**: relational database (colleges, placement_summary)
- **HTML, CSS, JavaScript**: interactive frontend dashboard
- **Chart.js**: data visualisation
- **Deployment**: backend on Render, frontend on Vercel

## How It Works
```
NIRF CSV  →  pipeline/pipeline.py  →  SQLite (placement.db)  →  Flask API  →  Chart.js dashboard
```
The pipeline reads the raw CSV row by row, skips rows with no placement data,
cleans and converts values (for example, package amounts in rupees to LPA),
and upserts into the database. Re-running it updates existing rows instead of
creating duplicates.

## API Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/api/colleges` | List all colleges (id, name, city, state, type) |
| GET | `/api/college?name=<text>` | Search by name (partial match, first match returned) with its year-wise placement data. Returns 400 if `name` is missing and 404 if not found. |

## Database Schema
Full definition in `database/schema.sql`.

| Table | Columns |
|-------|---------|
| `colleges` | college_id, college_name, city, state, college_type, institute_id, scraped_at |
| `placement_summary` | summary_id, college_id, year, branch, total_students, students_placed, placement_pct, median_package_lpa, scraped_at |

`placement_summary.college_id` references `colleges.college_id`.

## Data Notes
The source CSV uses a different column layout for 2017 than for 2018 onwards,
so the pipeline has a separate parsing branch for each:
- **2017:** placement % = placed ÷ (placed + higher studies)
- **2018–2025:** placement % = placed ÷ total graduating students

Because the formulas differ, compare 2017 values with later years with care.

## How To Run
`placement.db` is already included in the repo, so you can skip the optional
steps and go straight to starting the API.

1. Install dependencies: `pip install -r requirements.txt`
2. *(Optional, to rebuild the database)* Create the tables from `database/schema.sql`
3. *(Optional)* Load the data: `python pipeline/pipeline.py`
4. Start the API: `python api/app.py`
5. Open http://127.0.0.1:5000/ in your browser

## Project Structure
```
Placement-Tracker/
├── pipeline/pipeline.py                  ← CSV parser and data pipeline
├── database/
│   ├── nirf_full_dataset_2017_2025.csv   ← source data
│   ├── schema.sql                        ← table definitions
│   └── placement.db                      ← SQLite database
├── api/app.py                            ← Flask REST API
├── frontend/                             ← HTML, CSS, JS dashboard
├── procfile
└── requirements.txt                      ← Python dependencies
```

## Future Scope
- Company-level placement data (from NIRF PDFs)

## Author
Built by Sasi Kumar.