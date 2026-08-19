-- N.O.U Digital Systems - Seed Data
-- This script populates the database with sample data for development

-- Insert sample admin user (password: admin123)
INSERT INTO users (email, password_hash, first_name, last_name, role)
VALUES 
    ('admin@nou.com', crypt('admin123', gen_salt('bf')), 'System', 'Administrator', 'admin'),
    ('john.doe@example.com', crypt('password123', gen_salt('bf')), 'John', 'Doe', 'customer'),
    ('jane.smith@example.com', crypt('password123', gen_salt('bf')), 'Jane', 'Smith', 'applicant');

-- Insert sample customers
INSERT INTO customers (user_id, company_name, phone, address, city, country)
SELECT id, 'Tech Corp Ltd', '+1234567890', '123 Tech Street', 'Nairobi', 'Kenya'
FROM users WHERE email = 'john.doe@example.com';

-- Insert sample products
INSERT INTO products (name, description, category, version, file_size, download_count)
VALUES 
    ('N.O.U Office Suite', 'Complete office productivity suite with word processing, spreadsheets, and presentations', 'software', '2.1.0', 157286400, 1250),
    ('DataGuard Pro', 'Advanced data backup and encryption tool for enterprise environments', 'application', '1.5.2', 52428800, 890),
    ('CodeAssist IDE', 'Intelligent code editor with AI-powered suggestions and debugging', 'tool', '3.0.1', 209715200, 2100),
    ('WebOptimizer', 'Website performance analysis and optimization toolkit', 'library', '1.2.0', 10485760, 560),
    ('CloudSync Manager', 'Multi-cloud file synchronization and management utility', 'application', '2.0.0', 78643200, 720);

-- Insert sample job listings
INSERT INTO job_listings (title, description, department, location, employment_type, requirements, salary_range, status)
VALUES 
    ('Senior Full-Stack Developer', 'We are seeking an experienced full-stack developer to join our core engineering team. You will work on developing and maintaining our flagship web platform.', 'Engineering', 'Nairobi, Kenya', 'full_time', '5+ years experience in React and Python, strong understanding of PostgreSQL, experience with FastAPI or similar frameworks', 'KES 250,000 - 350,000', 'active'),
    ('UI/UX Designer', 'Join our design team to create intuitive and beautiful user experiences for our web applications.', 'Design', 'Nairobi, Kenya', 'full_time', '3+ years experience in UI/UX design, proficiency in Figma, understanding of design systems', 'KES 180,000 - 250,000', 'active'),
    ('Database Administrator', 'Manage and optimize our PostgreSQL database infrastructure.', 'Operations', 'Remote', 'contract', '4+ years DBA experience, PostgreSQL expertise, experience with database optimization', 'KES 200,000 - 300,000', 'active'),
    ('Technical Writer', 'Create comprehensive documentation for our software products and APIs.', 'Documentation', 'Remote', 'part_time', '2+ years technical writing experience, familiarity with API documentation, Markdown expertise', 'KES 120,000 - 180,000', 'active');

-- Insert sample questions for technical assessment
INSERT INTO questions (category, question_text, options, correct_answer, explanation, difficulty_level, points)
VALUES 
    -- Programming questions
    ('programming', 'What is the time complexity of binary search?', 
     '[{"id": "A", "text": "O(n)"}, {"id": "B", "text": "O(log n)"}, {"id": "C", "text": "O(n^2)"}, {"id": "D", "text": "O(1)"}]', 
     'B', 'Binary search divides the search space in half with each comparison, resulting in logarithmic time complexity.', 2, 2),
    
    ('programming', 'Which of the following is NOT a valid Python variable name?', 
     '[{"id": "A", "text": "my_var"}, {"id": "B", "text": "_private"}, {"id": "C", "text": "2nd_value"}, {"id": "D", "text": "camelCase"}]', 
     'C', 'Variable names cannot start with a number in Python (or most programming languages).', 1, 1),
    
    ('programming', 'What does REST stand for in RESTful APIs?', 
     '[{"id": "A", "text": "Remote Execution State Transfer"}, {"id": "B", "text": "Representational State Transfer"}, {"id": "C", "text": "Resource Entity State Transfer"}, {"id": "D", "text": "Reliable Endpoint State Transfer"}]', 
     'B', 'REST stands for Representational State Transfer, an architectural style for designing networked applications.', 2, 2),
    
    -- Database questions
    ('database', 'Which SQL command is used to retrieve data from a database?', 
     '[{"id": "A", "text": "GET"}, {"id": "B", "text": "FETCH"}, {"id": "C", "text": "SELECT"}, {"id": "D", "text": "RETRIEVE"}]', 
     'C', 'SELECT is the standard SQL command used to query and retrieve data from database tables.', 1, 1),
    
    ('database', 'What is a primary key in a database?', 
     '[{"id": "A", "text": "A key used for encryption"}, {"id": "B", "text": "A unique identifier for each record"}, {"id": "C", "text": "The first column in a table"}, {"id": "D", "text": "A password for database access"}]', 
     'B', 'A primary key is a unique identifier that uniquely identifies each record in a database table.', 2, 2),
    
    -- Mathematics questions
    ('mathematics', 'What is the derivative of x^2 with respect to x?', 
     '[{"id": "A", "text": "x"}, {"id": "B", "text": "2x"}, {"id": "C", "text": "2"}, {"id": "D", "text": "x^2"}]', 
     'B', 'Using the power rule, the derivative of x^n is n*x^(n-1). So for x^2, it is 2x.', 2, 2),
    
    ('mathematics', 'What is the value of log base 10 of 1000?', 
     '[{"id": "A", "text": "10"}, {"id": "B", "text": "100"}, {"id": "C", "text": "3"}, {"id": "D", "text": "1000"}]', 
     'C', 'log base 10 of 1000 equals 3 because 10^3 = 1000.', 1, 1),
    
    -- Logical Reasoning
    ('logical_reasoning', 'If all roses are flowers, and some flowers fade quickly, which statement must be true?', 
     '[{"id": "A", "text": "All roses fade quickly"}, {"id": "B", "text": "Some roses may fade quickly"}, {"id": "C", "text": "No roses fade quickly"}, {"id": "D", "text": "All flowers are roses"}]', 
     'B', 'Since some flowers fade quickly and roses are flowers, some roses may fade quickly, but we cannot definitively say all do.', 3, 3),
    
    -- Software Engineering
    ('software_engineering', 'What is the main purpose of version control systems like Git?', 
     '[{"id": "A", "text": "To compile code"}, {"id": "B", "text": "To track changes in code over time"}, {"id": "C", "text": "To run tests"}, {"id": "D", "text": "To design user interfaces"}]', 
     'B', 'Version control systems track changes to code, allowing developers to collaborate and maintain history of modifications.', 1, 1),
    
    ('software_engineering', 'What does SOLID stand for in object-oriented design?', 
     '[{"id": "A", "text": "Simple, Organized, Logical, Integrated, Direct"}, {"id": "B", "text": "Single responsibility, Open-closed, Liskov substitution, Interface segregation, Dependency inversion"}, {"id": "C", "text": "Secure, Optimized, Lightweight, Independent, Dynamic"}, {"id": "D", "text": "Standard, Original, Linear, Incremental, Documented"}]', 
     'B', 'SOLID is an acronym for five object-oriented design principles that help developers write maintainable and flexible code.', 3, 3);

-- Insert sample assessments
INSERT INTO assessments (title, description, duration_minutes, total_questions, passing_score)
VALUES 
    ('General Technical Assessment', 'Comprehensive assessment covering programming, databases, mathematics, and software engineering fundamentals.', 60, 50, 60),
    ('Programming Fundamentals', 'Focused assessment on programming concepts, data structures, and algorithms.', 45, 30, 70),
    ('Database Knowledge Test', 'Assessment covering SQL, database design, and optimization concepts.', 30, 20, 65);

-- Link questions to assessments
INSERT INTO assessment_questions (assessment_id, question_id, order_number, points)
SELECT 
    (SELECT id FROM assessments WHERE title = 'General Technical Assessment'),
    id,
    ROW_NUMBER() OVER (ORDER BY RANDOM()),
    points
FROM questions
WHERE is_active = TRUE;

-- Insert sample announcements
INSERT INTO announcements (title, content, target_audience, is_published, published_at, created_by)
VALUES 
    ('Welcome to N.O.U Digital Systems', 'We are excited to launch our new centralized platform for customer interaction, software distribution, and technical recruitment. Explore our products and services today!', 'all', TRUE, CURRENT_TIMESTAMP, (SELECT id FROM users WHERE email = 'admin@nou.com')),
    ('New Software Release: N.O.U Office Suite 2.1', 'We are pleased to announce the release of N.O.U Office Suite version 2.1 with improved performance and new features. Visit our products page to download.', 'customers', TRUE, CURRENT_TIMESTAMP, (SELECT id FROM users WHERE email = 'admin@nou.com')),
    ('Technical Assessment Now Available', 'Applicants can now take our comprehensive technical assessment as part of the recruitment process. Complete your profile and start the assessment today.', 'applicants', TRUE, CURRENT_TIMESTAMP, (SELECT id FROM users WHERE email = 'admin@nou.com'));