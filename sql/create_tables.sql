CREATE TABLE IF NOT EXISTS channels (
    channel_id TEXT PRIMARY KEY,
    channel_name TEXT
);

CREATE TABLE IF NOT EXISTS raw_telegram_messages (
    id BIGINT PRIMARY KEY,
    date TIMESTAMP,
    text TEXT,
    media BOOLEAN,
    media_path TEXT,
    channel_id TEXT REFERENCES channels(channel_id)
);
