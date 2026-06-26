CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_url TEXT NOT NULL UNIQUE,
    job_title TEXT NOT NULL,
    location TEXT,
    job_description TEXT,
    source_url TEXT,
    ats_platform TEXT,
    salary TEXT,
    date_posted TEXT,
    status TEXT DEFAULT 'open',
    first_seen TEXT,
    last_seen TEXT,
    is_active INTEGER DEFAULT 1
);