CREATE EXTENSION IF NOT EXISTS vector;
DROP TABLE IF EXISTS jobs;
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL,
    salary TEXT,
    tags TEXT[],
    description TEXT NOT NULL,
    embedding vector(384)
);
