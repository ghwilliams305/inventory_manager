CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    quantity INTEGER NOT NULL,
    unit TEXT DEFAULT 'unit',
    building TEXT DEFAULT 'home',
    room TEXT DEFAULT 'unknown',
    placement TEXT DEFAULT 'unknown'
);