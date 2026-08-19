-- N.O.U migration: OTP auth + module-based assessments
-- Adds module tracking, results-email tracking, and updates assessment
-- duration/total questions to the new product rules.

ALTER TABLE assessment_session_questions ADD COLUMN module VARCHAR(100) NULL;

ALTER TABLE assessment_sessions ADD COLUMN modules TEXT NULL;
ALTER TABLE assessment_sessions ADD COLUMN results_emailed_at DATETIME NULL;

-- Every assessment now runs 3 hours 30 minutes with 8 modules x 20 questions.
UPDATE assessments SET duration_minutes = 210 WHERE duration_minutes <> 210;
UPDATE assessments SET total_questions = 160 WHERE total_questions <> 160;

-- Backfill module on existing session questions where possible (category
-- often mirrors the module name for AI-generated sessions).
UPDATE assessment_session_questions
SET module = category
WHERE module IS NULL AND category IS NOT NULL AND category <> '';

-- Backfill modules list on completed sessions from their questions.
UPDATE assessment_sessions s
SET modules = (
    SELECT CONCAT('[', GROUP_CONCAT(CONCAT('"', REPLACE(q.module, '"', '\\"'), '"')), ']')
    FROM (SELECT DISTINCT module FROM assessment_session_questions WHERE session_id = s.id) q
    WHERE q.module IS NOT NULL
)
WHERE s.modules IS NULL
  AND EXISTS (SELECT 1 FROM assessment_session_questions WHERE session_id = s.id AND module IS NOT NULL);
