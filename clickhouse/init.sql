CREATE DATABASE IF NOT EXISTS reports;
CREATE TABLE IF NOT EXISTS reports.user_reports (
                                                    user_id String,
                                                    report_date Date,
                                                    total_actions UInt32,
                                                    avg_latency_ms Float32
) ENGINE = MergeTree() ORDER BY (user_id, report_date);
INSERT INTO reports.user_reports VALUES ('ВАШ_USER_ID', '2025-12-26', 150, 82.7);