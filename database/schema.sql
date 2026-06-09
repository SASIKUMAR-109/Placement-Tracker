PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS placement_summary;
DROP TABLE IF EXISTS colleges;

CREATE TABLE colleges (
    college_id INTEGER PRIMARY KEY,
    college_name TEXT NOT NULL,
    city TEXT,
    state TEXT,
    college_type TEXT,
    institute_id TEXT,
    scraped_at DATETIME
);

CREATE TABLE placement_summary (
    summary_id INTEGER PRIMARY KEY,
    college_id INTEGER NOT NULL,
    year INTEGER,
    branch TEXT,
    total_students INTEGER,
    students_placed INTEGER,
    placement_pct REAL,
    median_package_lpa REAL,
    scraped_at DATETIME,
    FOREIGN KEY(college_id) REFERENCES colleges(college_id)
);
