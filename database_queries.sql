-- =========================================================
-- SMART EVAL AI DATABASE SETUP
-- =========================================================

-- =========================================================
-- 1. CREATE DATABASE
-- =========================================================

CREATE DATABASE IF NOT EXISTS smart_eval_ai;

USE smart_eval_ai;

-- =========================================================
-- 2. USERS TABLE
-- =========================================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL,

    email VARCHAR(100) UNIQUE NOT NULL,

    password_hash VARCHAR(255) NOT NULL,

    role ENUM('student', 'faculty', 'admin') NOT NULL,

    branch VARCHAR(50),

    phone VARCHAR(20),

    id_number VARCHAR(50) UNIQUE,

    profile_image VARCHAR(255),

    is_active BOOLEAN DEFAULT TRUE,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP
);

-- =========================================================
-- 3. ASSIGNMENTS TABLE
-- =========================================================

CREATE TABLE assignments (

    id INT AUTO_INCREMENT PRIMARY KEY,

    faculty_id INT NOT NULL,

    title VARCHAR(255) NOT NULL,

    description TEXT,

    deadline DATETIME,

    difficulty ENUM('Easy', 'Medium', 'Hard'),

    assignment_pdf_url TEXT,

    assignment_s3_key VARCHAR(500),

    total_marks INT DEFAULT 100,

    status ENUM('active', 'closed') DEFAULT 'active',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (faculty_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);

-- =========================================================
-- 4. SUBMISSIONS TABLE
-- =========================================================

CREATE TABLE submissions (

    id INT AUTO_INCREMENT PRIMARY KEY,

    assignment_id INT NOT NULL,

    student_id INT NOT NULL,

    submission_pdf_url TEXT,

    submission_s3_key VARCHAR(500),

    submission_status ENUM(
        'pending',
        'evaluating',
        'completed',
        'failed'
    ) DEFAULT 'pending',

    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (assignment_id)
    REFERENCES assignments(id)
    ON DELETE CASCADE,

    FOREIGN KEY (student_id)
    REFERENCES users(id)
    ON DELETE CASCADE
);

-- =========================================================
-- 5. EVALUATION RESULTS TABLE
-- =========================================================

CREATE TABLE evaluation_results (

    id INT AUTO_INCREMENT PRIMARY KEY,

    submission_id INT NOT NULL,

    ai_model VARCHAR(100),

    score DECIMAL(5,2),

    strengths LONGTEXT,

    weaknesses LONGTEXT,

    missing_points LONGTEXT,

    feedback LONGTEXT,

    plagiarism_score DECIMAL(5,2),

    evaluation_time_seconds FLOAT,

    ai_status ENUM(
        'success',
        'failed',
        'partial'
    ) DEFAULT 'success',

    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (submission_id)
    REFERENCES submissions(id)
    ON DELETE CASCADE
);

-- =========================================================
-- 6. INSERT FACULTY DATA
-- =========================================================

INSERT INTO users (
    name,
    email,
    password_hash,
    role,
    branch,
    phone,
    id_number,
    is_active
)
VALUES
(
    'Dr. Ramesh Kumar',
    'ramesh.kumar@college.edu',
    'scrypt:32768:8:1$qTGoC7eyTCKEwh7J$c56a7f7bf20317a83f4822ec879128c4b5e07179fa878a77c27dc4164b4d5f4615abcd7b2d81b3cd1a06da2e8102d28078c69ec6831d8ddf8e30f0892b936f1c',
    'faculty',
    'CSE',
    '9876543210',
    'FAC001',
    1
);

INSERT INTO users (
    name,
    email,
    password_hash,
    role,
    branch,
    phone,
    id_number,
    is_active
)
VALUES
(
    'Dr. Priya Sharma',
    'priya.sharma@college.edu',
    'scrypt:32768:8:1$Ln7ORKGNSLIDLYll$d6f3b8fef8f45065c15b513cefa5b0657a01849273b9452bc804df1f435dadd1a775a37a6e061b1e0c2ed58a27603c51bfda4d76d2ad125d3c999911f53e635e',
    'faculty',
    'CSE',
    '9876543211',
    'FAC002',
    1
);

INSERT INTO users (
    name,
    email,
    password_hash,
    role,
    branch,
    phone,
    id_number,
    is_active
)
VALUES
(
    'Prof. Anil Verma',
    'anil.verma@college.edu',
    'scrypt:32768:8:1$MwOHspX3cDnqSanZ$4a6e68fd568710fd25a7272055c303b2e86c136ca2821284e7dec87e9af84be7d2d85dacb0d6d33b4b3fe1299a46a4e7a75721869884fc006553a0b70e959828',
    'faculty',
    'ECE',
    '9876543212',
    'FAC003',
    1
);

INSERT INTO users (
    name,
    email,
    password_hash,
    role,
    branch,
    phone,
    id_number,
    is_active
)
VALUES
(
    'Dr. Sunitha Reddy',
    'sunitha.reddy@college.edu',
    'scrypt:32768:8:1$zZlbPzFfkR7nKSpA$36e8ffce2f147a6975d449a76aa0a79cbe39008d05c178c4e6c283b97bf9060be8ae5359b26b66060498a039119ff73bc27b9d89b095645e93e819baeea5a9ab',
    'faculty',
    'MECH',
    '9876543213',
    'FAC004',
    1
);

INSERT INTO users (
    name,
    email,
    password_hash,
    role,
    branch,
    phone,
    id_number,
    is_active
)
VALUES
(
    'Prof. Kiran Babu',
    'kiran.babu@college.edu',
    'scrypt:32768:8:1$YyXPLX3EJiwLDdPS$cff4bf1609c6bb904290444213f941f9d92a606590394067b474f83ebe9d9b9d149b2e334bbeef46b2fb42c2a32b901ec321ff6144f4bdda7dc7560ec7d2dd21',
    'faculty',
    'CSE',
    '9876543214',
    'FAC005',
    1
);

-- =========================================================
-- 7. SAMPLE CHECK QUERIES
-- =========================================================

SHOW TABLES;

DESCRIBE users;

DESCRIBE assignments;

DESCRIBE submissions;

DESCRIBE evaluation_results;

-- =========================================================
-- 8. VERIFY FACULTY DATA
-- =========================================================

SELECT
    id,
    name,
    email,
    role,
    branch
FROM users
WHERE role = 'faculty';

-- =========================================================
-- 9. VIEW TABLE DATA
-- =========================================================

SELECT * FROM assignments;

SELECT * FROM submissions;

SELECT * FROM evaluation_results;
