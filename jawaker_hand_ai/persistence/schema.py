"""SQLite database schema and table definitions for experience and telemetry storage."""

import sqlite3

CREATE_MATCHES_TABLE = """
CREATE TABLE IF NOT EXISTS matches (
    match_id TEXT PRIMARY KEY,
    num_players INTEGER NOT NULL,
    winner_id INTEGER NOT NULL,
    final_scores TEXT NOT NULL,
    total_rounds INTEGER NOT NULL,
    summary TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_ROUNDS_TABLE = """
CREATE TABLE IF NOT EXISTS rounds (
    round_id TEXT PRIMARY KEY,
    match_id TEXT NOT NULL,
    round_number INTEGER NOT NULL,
    dealer_id INTEGER NOT NULL,
    winner_id INTEGER,
    is_hand_finish INTEGER NOT NULL,
    is_normal_finish INTEGER NOT NULL,
    is_stock_exhausted INTEGER NOT NULL,
    round_scores TEXT NOT NULL,
    score_breakdown TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(match_id) REFERENCES matches(match_id)
);
"""

CREATE_TRACES_TABLE = """
CREATE TABLE IF NOT EXISTS decision_traces (
    trace_id TEXT PRIMARY KEY,
    match_id TEXT NOT NULL,
    round_number INTEGER NOT NULL,
    turn_number INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    agent_name TEXT NOT NULL,
    phase TEXT NOT NULL,
    hand_cards TEXT NOT NULL,
    is_opened INTEGER NOT NULL,
    selected_action TEXT NOT NULL,
    candidate_evaluations TEXT NOT NULL,
    opponent_belief_summary TEXT,
    execution_latency_ms REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(match_id) REFERENCES matches(match_id)
);
"""

CREATE_PLAYER_PROFILES_TABLE = """
CREATE TABLE IF NOT EXISTS player_profiles (
    player_name TEXT PRIMARY KEY,
    matches_played INTEGER DEFAULT 0,
    matches_won INTEGER DEFAULT 0,
    rounds_won INTEGER DEFAULT 0,
    hand_finishes INTEGER DEFAULT 0,
    total_points INTEGER DEFAULT 0,
    elo_rating REAL DEFAULT 1500.0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_INDEXES = """
CREATE INDEX IF NOT EXISTS idx_rounds_match ON rounds(match_id);
CREATE INDEX IF NOT EXISTS idx_traces_match ON decision_traces(match_id);
CREATE INDEX IF NOT EXISTS idx_traces_agent ON decision_traces(agent_name);
"""


def create_schema(conn: sqlite3.Connection) -> None:
    with conn:
        conn.execute(CREATE_MATCHES_TABLE)
        conn.execute(CREATE_ROUNDS_TABLE)
        conn.execute(CREATE_TRACES_TABLE)
        conn.execute(CREATE_PLAYER_PROFILES_TABLE)
        conn.executescript(CREATE_INDEXES)
