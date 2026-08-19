-- ============================================================
-- N.O.U - AI Assessment migration (Groq-powered assessments)
-- Run once against an existing MySQL database.
-- Fresh installs get the same schema automatically via
-- SQLAlchemy create_all (models already include these columns).
-- ============================================================

-- 1) Widen user_answer for open-ended written answers (was VARCHAR(10))
ALTER TABLE assessment_answers MODIFY COLUMN user_answer TEXT NULL;

-- 2) Answers may now reference AI session questions instead of the bank
ALTER TABLE assessment_answers MODIFY COLUMN question_id INT NULL;
ALTER TABLE assessment_answers ADD COLUMN session_question_id INT NULL AFTER question_id;

-- 3) Store per-answer AI feedback
ALTER TABLE assessment_answers ADD COLUMN ai_feedback TEXT NULL;

-- 4) Store the AI overall summary + hiring recommendation on the session
ALTER TABLE assessment_sessions ADD COLUMN ai_summary TEXT NULL;
ALTER TABLE assessment_sessions ADD COLUMN ai_recommendation VARCHAR(50) NULL;

-- 5) Per-session AI-generated question snapshots (randomized per candidate)
CREATE TABLE IF NOT EXISTS assessment_session_questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    category VARCHAR(100) NOT NULL,
    question_text TEXT NOT NULL,
    order_number INT NOT NULL,
    points INT DEFAULT 10,
    grading_notes TEXT,
    CONSTRAINT fk_assessment_session_questions_session
        FOREIGN KEY (session_id) REFERENCES assessment_sessions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
