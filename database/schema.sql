USE towards_version_2_0;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'mentor') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    frequency VARCHAR(50),
    target DECIMAL(10,2),
    unit VARCHAR(50),
    start_date DATE NOT NULL,
    end_date DATE,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium',
    status ENUM('active', 'completed', 'paused') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


CREATE TABLE activity_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    activity_id INT NOT NULL,
    student_id INT NOT NULL,
    log_date DATE NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    actual_value DECIMAL(10,2) DEFAULT 0,
    time_spent INT DEFAULT 0,

    FOREIGN KEY (activity_id)
        REFERENCES activities(id)
        ON DELETE CASCADE,

    FOREIGN KEY (student_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    UNIQUE (activity_id, student_id, log_date)
);


CREATE TABLE mentor_student (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mentor_id INT NOT NULL,
    student_id INT NOT NULL,

    FOREIGN KEY (mentor_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (student_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    UNIQUE (mentor_id, student_id)
);


CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mentor_id INT NOT NULL,
    student_id INT NOT NULL,
    activity_id INT,
    feedback_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (mentor_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (student_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY (activity_id)
        REFERENCES activities(id)
        ON DELETE SET NULL
);


CREATE TABLE achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    achievement_name VARCHAR(150) NOT NULL,
    description TEXT,
    achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    UNIQUE (student_id, achievement_name)
);