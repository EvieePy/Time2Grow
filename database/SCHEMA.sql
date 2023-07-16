CREATE TABLE IF NOT EXISTS stats (
    username TEXT PRIMARY KEY,
    minutes BIGINT DEFAULT 0,
    planted BIGINT DEFAULT 1,
    watered BIGINT DEFAULT 0,
    wilted BIGINT DEFAULT 0,
    killed BIGINT DEFAULT 0,
    epic BIGINT DEFAULT 0,
    sabotaged BIGINT DEFAULT 0,
    victim BIGINT DEFAULT 0,
    disasters BIGINT DEFAULT 0,
    survived BIGINT DEFAULT 0,
    thugged BIGINT DEFAULT 0
);