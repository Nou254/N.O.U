-- N.O.U Digital Systems - Seed Data (MySQL edition)
-- ===================================================
-- The original database/seeds.sql is PostgreSQL-only (uses pgcrypto crypt(),
-- gen_salt() and RANDOM()), so it can never run against the MySQL database
-- this project actually uses (DATABASE_URL=mysql+aiomysql://...).
--
-- This script is the MySQL-compatible replacement. It is idempotent: every
-- insert is guarded by a NOT EXISTS check so it is safe to run repeatedly.
--
-- Demo logins:
--   admin@nou.com    / admin123    (admin)
--   john.doe@example.com / password123 (customer)
--   jane.smith@example.com / password123 (applicant)

-- ---------------------------------------------------------------
-- Users (bcrypt hashes generated with the app's own get_password_hash)
-- ---------------------------------------------------------------
INSERT INTO users (email, password_hash, first_name, last_name, role, is_active)
SELECT 'admin@nou.com', '$2b$12$.q4xin1yuJ4bghLd5ir4Suxb665Ju1EFc7vi/KtuuSQxIgc6vLUZW', 'System', 'Administrator', 'admin', 1
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'admin@nou.com');

INSERT INTO users (email, password_hash, first_name, last_name, role, is_active)
SELECT 'john.doe@example.com', '$2b$12$e.OvIWgrT5f5RVYo8vK.HeBpswlq75DQQK67V27DYDb1yd9wsXKZG', 'John', 'Doe', 'customer', 1
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'john.doe@example.com');

INSERT INTO users (email, password_hash, first_name, last_name, role, is_active)
SELECT 'jane.smith@example.com', '$2b$12$e.OvIWgrT5f5RVYo8vK.HeBpswlq75DQQK67V27DYDb1yd9wsXKZG', 'Jane', 'Smith', 'applicant', 1
WHERE NOT EXISTS (SELECT 1 FROM users WHERE email = 'jane.smith@example.com');

-- ---------------------------------------------------------------
-- Customer profile for the seeded customer
-- ---------------------------------------------------------------
INSERT INTO customers (user_id, company_name, phone, address, city, country)
SELECT u.id, 'Tech Corp Ltd', '+1234567890', '123 Tech Street', 'Nairobi', 'Kenya'
FROM users u
WHERE u.email = 'john.doe@example.com'
  AND NOT EXISTS (SELECT 1 FROM customers c WHERE c.user_id = u.id);

-- ---------------------------------------------------------------
-- Products
-- ---------------------------------------------------------------
INSERT INTO products (name, description, category, version, file_size, download_count, is_active)
SELECT 'N.O.U Office Suite', 'Complete office productivity suite with word processing, spreadsheets, and presentations', 'software', '2.1.0', 157286400, 1250, 1
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'N.O.U Office Suite');

INSERT INTO products (name, description, category, version, file_size, download_count, is_active)
SELECT 'DataGuard Pro', 'Advanced data backup and encryption tool for enterprise environments', 'application', '1.5.2', 52428800, 890, 1
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'DataGuard Pro');

INSERT INTO products (name, description, category, version, file_size, download_count, is_active)
SELECT 'CodeAssist IDE', 'Intelligent code editor with AI-powered suggestions and debugging', 'tool', '3.0.1', 209715200, 2100, 1
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'CodeAssist IDE');

INSERT INTO products (name, description, category, version, file_size, download_count, is_active)
SELECT 'WebOptimizer', 'Website performance analysis and optimization toolkit', 'library', '1.2.0', 10485760, 560, 1
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'WebOptimizer');

INSERT INTO products (name, description, category, version, file_size, download_count, is_active)
SELECT 'CloudSync Manager', 'Multi-cloud file synchronization and management utility', 'application', '2.0.0', 78643200, 720, 1
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'CloudSync Manager');

-- ---------------------------------------------------------------
-- Product versions (so product detail/download pages have versions)
-- ---------------------------------------------------------------
INSERT INTO product_versions (product_id, version_number, release_notes, is_latest)
SELECT p.id, p.version, CONCAT('Latest release of ', p.name), 1
FROM products p
WHERE NOT EXISTS (SELECT 1 FROM product_versions pv WHERE pv.product_id = p.id);

-- ---------------------------------------------------------------
-- Job listings
-- ---------------------------------------------------------------
INSERT INTO job_listings (title, description, department, location, employment_type, requirements, salary_range, status)
SELECT 'Senior Full-Stack Developer', 'We are seeking an experienced full-stack developer to join our core engineering team. You will work on developing and maintaining our flagship web platform.', 'Engineering', 'Nairobi, Kenya', 'full_time', '5+ years experience in React and Python, strong understanding of PostgreSQL, experience with FastAPI or similar frameworks', 'KES 250,000 - 350,000', 'active'
WHERE NOT EXISTS (SELECT 1 FROM job_listings WHERE title = 'Senior Full-Stack Developer');

INSERT INTO job_listings (title, description, department, location, employment_type, requirements, salary_range, status)
SELECT 'UI/UX Designer', 'Join our design team to create intuitive and beautiful user experiences for our web applications.', 'Design', 'Nairobi, Kenya', 'full_time', '3+ years experience in UI/UX design, proficiency in Figma, understanding of design systems', 'KES 180,000 - 250,000', 'active'
WHERE NOT EXISTS (SELECT 1 FROM job_listings WHERE title = 'UI/UX Designer');

INSERT INTO job_listings (title, description, department, location, employment_type, requirements, salary_range, status)
SELECT 'Database Administrator', 'Manage and optimize our PostgreSQL database infrastructure.', 'Operations', 'Remote', 'contract', '4+ years DBA experience, PostgreSQL expertise, experience with database optimization', 'KES 200,000 - 300,000', 'active'
WHERE NOT EXISTS (SELECT 1 FROM job_listings WHERE title = 'Database Administrator');

INSERT INTO job_listings (title, description, department, location, employment_type, requirements, salary_range, status)
SELECT 'Technical Writer', 'Create comprehensive documentation for our software products and APIs.', 'Documentation', 'Remote', 'part_time', '2+ years technical writing experience, familiarity with API documentation, Markdown expertise', 'KES 120,000 - 180,000', 'active'
WHERE NOT EXISTS (SELECT 1 FROM job_listings WHERE title = 'Technical Writer');

-- ---------------------------------------------------------------
-- Questions (options stored as JSON, as required by the ORM JSON column)
-- ---------------------------------------------------------------
INSERT INTO questions (category, question_text, options, correct_answer, explanation, difficulty_level, points, is_active)
SELECT 'programming', 'What is the time complexity of binary search?',
       '[{"id": "A", "text": "O(n)"}, {"id": "B", "text": "O(log n)"}, {"id": "C", "text": "O(n^2)"}, {"id": "D", "text": "O(1)"}]',
       'B', 'Binary search divides the search space in half with each comparison, resulting in logarithmic time complexity.', 2, 2, 1
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question_text = 'What is the time complexity of binary search?');

INSERT INTO questions (category, question_text, options, correct_answer, explanation, difficulty_level, points, is_active)
SELECT 'programming', 'Which of the following is NOT a valid Python variable name?',
       '[{"id": "A", "text": "my_var"}, {"id": "B", "text": "_private"}, {"id": "C", "text": "2nd_value"}, {"id": "D", "text": "camelCase"}]',
       'C', 'Variable names cannot start with a number in Python (or most programming languages).', 1, 1, 1
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question_text = 'Which of the following is NOT a valid Python variable name?');

INSERT INTO questions (category, question_text, options, correct_answer, explanation, difficulty_level, points, is_active)
SELECT 'programming', 'What does REST stand for in RESTful APIs?',
       '[{"id": "A", "text": "Remote Execution State Transfer"}, {"id": "B", "text": "Representational State Transfer"}, {"id": "C", "text": "Resource Entity State Transfer"}, {"id": "D", "text": "Reliable Endpoint State Transfer"}]',
       'B', 'REST stands for Representational State Transfer, an architectural style for designing networked applications.', 2, 2, 1
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question_text = 'What does REST stand for in RESTful APIs?');

INSERT INTO questions (category, question_text, options, correct_answer, explanation, difficulty_level, points, is_active)
SELECT 'database', 'Which SQL command is used to retrieve data from a database?',
       '[{"id": "A", "text": "GET"}, {"id": "B", "text": "FETCH"}, {"id": "C", "text": "SELECT"}, {"id": "D", "text": "RETRIEVE"}]',
       'C', 'SELECT is the standard SQL command used to query and retrieve data from database tables.', 1, 1, 1
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question_text = 'Which SQL command is used to retrieve data from a database?');

INSERT INTO questions (category, question_text, options, correct_answer, explanation, difficulty_level, points, is_active)
SELECT 'database', 'What is a primary key in a database?',
       '[{"id": "A", "text": "A key used for encryption"}, {"id": "B", "text": "A unique identifier for each record"}, {"id": "C", "text": "The first column in a table"}, {"id": "D", "text": "A password for database access"}]',
       'B', 'A primary key is a unique identifier that uniquely identifies each record in a database table.', 2, 2, 1
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question_text = 'What is a primary key in a database?');

INSERT INTO questions (category, question_text, options, correct_answer, explanation, difficulty_level, points, is_active)
SELECT 'mathematics', 'What is the derivative of x^2 with respect to x?',
       '[{"id": "A", "text": "x"}, {"id": "B", "text": "2x"}, {"id": "C", "text": "2"}, {"id": "D", "text": "x^2"}]',
       'B', 'Using the power rule, the derivative of x^n is n*x^(n-1). So for x^2, it is 2x.', 2, 2, 1
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question_text = 'What is the derivative of x^2 with respect to x?');

INSERT INTO questions (category, question_text, options, correct_answer, explanation, difficulty_level, points, is_active)
SELECT 'mathematics', 'What is the value of log base 10 of 1000?',
       '[{"id": "A", "text": "10"}, {"id": "B", "text": "100"}, {"id": "C", "text": "3"}, {"id": "D", "text": "1000"}]',
       'C', 'log base 10 of 1000 equals 3 because 10^3 = 1000.', 1, 1, 1
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question_text = 'What is the value of log base 10 of 1000?');

INSERT INTO questions (category, question_text, options, correct_answer, explanation, difficulty_level, points, is_active)
SELECT 'logical_reasoning', 'If all roses are flowers, and some flowers fade quickly, which statement must be true?',
       '[{"id": "A", "text": "All roses fade quickly"}, {"id": "B", "text": "Some roses may fade quickly"}, {"id": "C", "text": "No roses fade quickly"}, {"id": "D", "text": "All flowers are roses"}]',
       'B', 'Since some flowers fade quickly and roses are flowers, some roses may fade quickly, but we cannot definitively say all do.', 3, 3, 1
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question_text = 'If all roses are flowers, and some flowers fade quickly, which statement must be true?');

INSERT INTO questions (category, question_text, options, correct_answer, explanation, difficulty_level, points, is_active)
SELECT 'software_engineering', 'What is the main purpose of version control systems like Git?',
       '[{"id": "A", "text": "To compile code"}, {"id": "B", "text": "To track changes in code over time"}, {"id": "C", "text": "To run tests"}, {"id": "D", "text": "To design user interfaces"}]',
       'B', 'Version control systems track changes to code, allowing developers to collaborate and maintain history of modifications.', 1, 1, 1
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question_text = 'What is the main purpose of version control systems like Git?');

INSERT INTO questions (category, question_text, options, correct_answer, explanation, difficulty_level, points, is_active)
SELECT 'software_engineering', 'What does SOLID stand for in object-oriented design?',
       '[{"id": "A", "text": "Simple, Organized, Logical, Integrated, Direct"}, {"id": "B", "text": "Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion"}, {"id": "C", "text": "Secure, Optimized, Lightweight, Independent, Dynamic"}, {"id": "D", "text": "Standard, Original, Linear, Incremental, Documented"}]',
       'B', 'SOLID is an acronym for five object-oriented design principles that help developers write maintainable and flexible code.', 3, 3, 1
WHERE NOT EXISTS (SELECT 1 FROM questions WHERE question_text = 'What does SOLID stand for in object-oriented design?');

-- ---------------------------------------------------------------
-- Assessments
-- ---------------------------------------------------------------
INSERT INTO assessments (title, description, duration_minutes, total_questions, passing_score, is_active)
SELECT 'General Technical Assessment', 'Comprehensive assessment covering programming, databases, mathematics, and software engineering fundamentals.', 60, 50, 60, 1
WHERE NOT EXISTS (SELECT 1 FROM assessments WHERE title = 'General Technical Assessment');

INSERT INTO assessments (title, description, duration_minutes, total_questions, passing_score, is_active)
SELECT 'Programming Fundamentals', 'Focused assessment on programming concepts, data structures, and algorithms.', 45, 30, 70, 1
WHERE NOT EXISTS (SELECT 1 FROM assessments WHERE title = 'Programming Fundamentals');

INSERT INTO assessments (title, description, duration_minutes, total_questions, passing_score, is_active)
SELECT 'Database Knowledge Test', 'Assessment covering SQL, database design, and optimization concepts.', 30, 20, 65, 1
WHERE NOT EXISTS (SELECT 1 FROM assessments WHERE title = 'Database Knowledge Test');

-- ---------------------------------------------------------------
-- Link all questions to each assessment
-- ---------------------------------------------------------------
INSERT INTO assessment_questions (assessment_id, question_id, order_number, points)
SELECT a.id, q.id, q.id, q.points
FROM assessments a
JOIN questions q ON q.is_active = 1
WHERE a.title = 'General Technical Assessment'
  AND NOT EXISTS (
      SELECT 1 FROM assessment_questions aq
      JOIN assessments a2 ON aq.assessment_id = a2.id
      WHERE a2.title = 'General Technical Assessment' AND aq.question_id = q.id
  );

INSERT INTO assessment_questions (assessment_id, question_id, order_number, points)
SELECT a.id, q.id, q.id, q.points
FROM assessments a
JOIN questions q ON q.is_active = 1
WHERE a.title = 'Programming Fundamentals'
  AND NOT EXISTS (
      SELECT 1 FROM assessment_questions aq
      JOIN assessments a2 ON aq.assessment_id = a2.id
      WHERE a2.title = 'Programming Fundamentals' AND aq.question_id = q.id
  );

INSERT INTO assessment_questions (assessment_id, question_id, order_number, points)
SELECT a.id, q.id, q.id, q.points
FROM assessments a
JOIN questions q ON q.is_active = 1
WHERE a.title = 'Database Knowledge Test'
  AND NOT EXISTS (
      SELECT 1 FROM assessment_questions aq
      JOIN assessments a2 ON aq.assessment_id = a2.id
      WHERE a2.title = 'Database Knowledge Test' AND aq.question_id = q.id
  );

-- ---------------------------------------------------------------
-- NOTE: The original seeds.sql also inserted "announcements". That table does
-- NOT exist in the ORM models (see backend/app/models/), so it was omitted.
-- ---------------------------------------------------------------
