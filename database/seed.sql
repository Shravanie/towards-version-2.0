USE towards_version_2_0;


-- =========================================================
-- DEMO USERS
-- Password for all demo accounts: Demo@123
-- =========================================================

INSERT INTO users
(name, email, password_hash, role)
VALUES
(
    'Aarav Mentor',
    'aarav.mentor@example.com',
    'pbkdf2:sha256:600000$z0htAkzFl10UDk3L$092cf16e014229752900c47ab7bb3a4fd6d154d533cbfa77013f59754fd18e8e',
    'mentor'
),
(
    'Priya Mentor',
    'priya.mentor@example.com',
    'pbkdf2:sha256:600000$z0htAkzFl10UDk3L$092cf16e014229752900c47ab7bb3a4fd6d154d533cbfa77013f59754fd18e8e',
    'mentor'
),
(
    'Riya Sharma',
    'riya.student@example.com',
    'pbkdf2:sha256:600000$z0htAkzFl10UDk3L$092cf16e014229752900c47ab7bb3a4fd6d154d533cbfa77013f59754fd18e8e',
    'student'
),
(
    'Kabir Mehta',
    'kabir.student@example.com',
    'pbkdf2:sha256:600000$z0htAkzFl10UDk3L$092cf16e014229752900c47ab7bb3a4fd6d154d533cbfa77013f59754fd18e8e',
    'student'
),
(
    'Ananya Patel',
    'ananya.student@example.com',
    'pbkdf2:sha256:600000$z0htAkzFl10UDk3L$092cf16e014229752900c47ab7bb3a4fd6d154d533cbfa77013f59754fd18e8e',
    'student'
),
(
    'Vivaan Shah',
    'vivaan.student@example.com',
    'pbkdf2:sha256:600000$z0htAkzFl10UDk3L$092cf16e014229752900c47ab7bb3a4fd6d154d533cbfa77013f59754fd18e8e',
    'student'
),
(
    'Ishita Rao',
    'ishita.student@example.com',
    'pbkdf2:sha256:600000$z0htAkzFl10UDk3L$092cf16e014229752900c47ab7bb3a4fd6d154d533cbfa77013f59754fd18e8e',
    'student'
),
(
    'Arjun Joshi',
    'arjun.student@example.com',
    'pbkdf2:sha256:600000$z0htAkzFl10UDk3L$092cf16e014229752900c47ab7bb3a4fd6d154d533cbfa77013f59754fd18e8e',
    'student'
);


-- =========================================================
-- MENTOR-STUDENT ASSIGNMENTS
-- =========================================================

INSERT INTO mentor_student
(mentor_id, student_id)

SELECT
    mentors.id,
    students.id

FROM users AS mentors
JOIN users AS students

WHERE mentors.email = 'aarav.mentor@example.com'
AND students.email IN (
    'riya.student@example.com',
    'kabir.student@example.com',
    'ananya.student@example.com'
);


INSERT INTO mentor_student
(mentor_id, student_id)

SELECT
    mentors.id,
    students.id

FROM users AS mentors
JOIN users AS students

WHERE mentors.email = 'priya.mentor@example.com'
AND students.email IN (
    'vivaan.student@example.com',
    'ishita.student@example.com',
    'arjun.student@example.com'
);


-- =========================================================
-- ACTIVITIES
-- =========================================================

INSERT INTO activities
(
    student_id,
    title,
    description,
    category,
    frequency,
    target,
    unit,
    start_date,
    end_date,
    priority,
    status
)

SELECT
    id,
    'Python Practice',
    'Practice Python programming concepts and solve coding problems.',
    'Academic',
    'Daily',
    60,
    'minutes',
    DATE_SUB(CURDATE(), INTERVAL 30 DAY),
    DATE_ADD(CURDATE(), INTERVAL 30 DAY),
    'high',
    'active'
FROM users
WHERE email = 'riya.student@example.com';


INSERT INTO activities
(
    student_id,
    title,
    description,
    category,
    frequency,
    target,
    unit,
    start_date,
    end_date,
    priority,
    status
)

SELECT
    id,
    'Reading',
    'Read books or educational material for personal development.',
    'Personal Growth',
    'Daily',
    30,
    'minutes',
    DATE_SUB(CURDATE(), INTERVAL 30 DAY),
    DATE_ADD(CURDATE(), INTERVAL 30 DAY),
    'medium',
    'active'
FROM users
WHERE email = 'riya.student@example.com';


INSERT INTO activities
(
    student_id,
    title,
    description,
    category,
    frequency,
    target,
    unit,
    start_date,
    end_date,
    priority,
    status
)

SELECT
    id,
    'Exercise',
    'Daily physical activity and exercise.',
    'Health',
    'Daily',
    45,
    'minutes',
    DATE_SUB(CURDATE(), INTERVAL 30 DAY),
    DATE_ADD(CURDATE(), INTERVAL 30 DAY),
    'medium',
    'active'
FROM users
WHERE email = 'riya.student@example.com';


INSERT INTO activities
(
    student_id,
    title,
    description,
    category,
    frequency,
    target,
    unit,
    start_date,
    end_date,
    priority,
    status
)

SELECT
    id,
    'Data Structures',
    'Practice arrays, stacks, queues and linked lists.',
    'Academic',
    'Daily',
    60,
    'minutes',
    DATE_SUB(CURDATE(), INTERVAL 30 DAY),
    DATE_ADD(CURDATE(), INTERVAL 30 DAY),
    'high',
    'active'
FROM users
WHERE email = 'kabir.student@example.com';


INSERT INTO activities
(
    student_id,
    title,
    description,
    category,
    frequency,
    target,
    unit,
    start_date,
    end_date,
    priority,
    status
)

SELECT
    id,
    'Communication Practice',
    'Improve communication and presentation skills.',
    'Personal Growth',
    'Weekly',
    3,
    'sessions',
    DATE_SUB(CURDATE(), INTERVAL 30 DAY),
    DATE_ADD(CURDATE(), INTERVAL 30 DAY),
    'medium',
    'active'
FROM users
WHERE email = 'kabir.student@example.com';


INSERT INTO activities
(
    student_id,
    title,
    description,
    category,
    frequency,
    target,
    unit,
    start_date,
    end_date,
    priority,
    status
)

SELECT
    id,
    'SQL Practice',
    'Practice SQL queries and database concepts.',
    'Academic',
    'Daily',
    45,
    'minutes',
    DATE_SUB(CURDATE(), INTERVAL 30 DAY),
    DATE_ADD(CURDATE(), INTERVAL 30 DAY),
    'high',
    'active'
FROM users
WHERE email = 'ananya.student@example.com';


INSERT INTO activities
(
    student_id,
    title,
    description,
    category,
    frequency,
    target,
    unit,
    start_date,
    end_date,
    priority,
    status
)

SELECT
    id,
    'Project Work',
    'Work on college project development.',
    'Academic',
    'Daily',
    90,
    'minutes',
    DATE_SUB(CURDATE(), INTERVAL 30 DAY),
    DATE_ADD(CURDATE(), INTERVAL 30 DAY),
    'high',
    'active'
FROM users
WHERE email = 'ananya.student@example.com';


INSERT INTO activities
(
    student_id,
    title,
    description,
    category,
    frequency,
    target,
    unit,
    start_date,
    end_date,
    priority,
    status
)

SELECT
    id,
    'Workout',
    'Regular workout and physical activity.',
    'Health',
    'Daily',
    45,
    'minutes',
    DATE_SUB(CURDATE(), INTERVAL 30 DAY),
    DATE_ADD(CURDATE(), INTERVAL 30 DAY),
    'medium',
    'active'
FROM users
WHERE email = 'vivaan.student@example.com';


INSERT INTO activities
(
    student_id,
    title,
    description,
    category,
    frequency,
    target,
    unit,
    start_date,
    end_date,
    priority,
    status
)

SELECT
    id,
    'JavaScript Practice',
    'Practice JavaScript programming.',
    'Academic',
    'Daily',
    60,
    'minutes',
    DATE_SUB(CURDATE(), INTERVAL 30 DAY),
    DATE_ADD(CURDATE(), INTERVAL 30 DAY),
    'high',
    'active'
FROM users
WHERE email = 'ishita.student@example.com';


INSERT INTO activities
(
    student_id,
    title,
    description,
    category,
    frequency,
    target,
    unit,
    start_date,
    end_date,
    priority,
    status
)

SELECT
    id,
    'Portfolio Building',
    'Improve portfolio and professional projects.',
    'Career',
    'Weekly',
    2,
    'sessions',
    DATE_SUB(CURDATE(), INTERVAL 30 DAY),
    DATE_ADD(CURDATE(), INTERVAL 30 DAY),
    'high',
    'active'
FROM users
WHERE email = 'arjun.student@example.com';


-- =========================================================
-- ACTIVITY LOGS
-- =========================================================

-- Riya - strong consistent progress

INSERT INTO activity_logs
(
    activity_id,
    student_id,
    log_date,
    completed,
    actual_value,
    time_spent
)

SELECT
    a.id,
    a.student_id,
    DATE_SUB(CURDATE(), INTERVAL d.day_offset DAY),
    TRUE,
    60,
    60
FROM activities a
JOIN (
    SELECT 6 AS day_offset
    UNION SELECT 5
    UNION SELECT 4
    UNION SELECT 3
    UNION SELECT 2
    UNION SELECT 1
    UNION SELECT 0
) d
WHERE a.title = 'Python Practice'
AND a.student_id = (
    SELECT id
    FROM users
    WHERE email = 'riya.student@example.com'
);


INSERT INTO activity_logs
(
    activity_id,
    student_id,
    log_date,
    completed,
    actual_value,
    time_spent
)

SELECT
    a.id,
    a.student_id,
    DATE_SUB(CURDATE(), INTERVAL d.day_offset DAY),
    TRUE,
    30,
    30
FROM activities a
JOIN (
    SELECT 6 AS day_offset
    UNION SELECT 4
    UNION SELECT 2
    UNION SELECT 0
) d
WHERE a.title = 'Reading'
AND a.student_id = (
    SELECT id
    FROM users
    WHERE email = 'riya.student@example.com'
);


-- Kabir - moderate progress

INSERT INTO activity_logs
(
    activity_id,
    student_id,
    log_date,
    completed,
    actual_value,
    time_spent
)

SELECT
    a.id,
    a.student_id,
    DATE_SUB(CURDATE(), INTERVAL d.day_offset DAY),
    CASE
        WHEN d.day_offset IN (0, 2, 4, 6) THEN TRUE
        ELSE FALSE
    END,
    CASE
        WHEN d.day_offset IN (0, 2, 4, 6) THEN 60
        ELSE 20
    END,
    CASE
        WHEN d.day_offset IN (0, 2, 4, 6) THEN 60
        ELSE 20
    END
FROM activities a
JOIN (
    SELECT 6 AS day_offset
    UNION SELECT 5
    UNION SELECT 4
    UNION SELECT 3
    UNION SELECT 2
    UNION SELECT 1
    UNION SELECT 0
) d
WHERE a.title = 'Data Structures'
AND a.student_id = (
    SELECT id
    FROM users
    WHERE email = 'kabir.student@example.com'
);


-- Ananya - high project involvement

INSERT INTO activity_logs
(
    activity_id,
    student_id,
    log_date,
    completed,
    actual_value,
    time_spent
)

SELECT
    a.id,
    a.student_id,
    DATE_SUB(CURDATE(), INTERVAL d.day_offset DAY),
    TRUE,
    90,
    90
FROM activities a
JOIN (
    SELECT 6 AS day_offset
    UNION SELECT 5
    UNION SELECT 4
    UNION SELECT 2
    UNION SELECT 1
    UNION SELECT 0
) d
WHERE a.title = 'Project Work'
AND a.student_id = (
    SELECT id
    FROM users
    WHERE email = 'ananya.student@example.com'
);


-- Vivaan - lower progress

INSERT INTO activity_logs
(
    activity_id,
    student_id,
    log_date,
    completed,
    actual_value,
    time_spent
)

SELECT
    a.id,
    a.student_id,
    DATE_SUB(CURDATE(), INTERVAL d.day_offset DAY),
    CASE
        WHEN d.day_offset IN (1, 4) THEN TRUE
        ELSE FALSE
    END,
    CASE
        WHEN d.day_offset IN (1, 4) THEN 45
        ELSE 10
    END,
    CASE
        WHEN d.day_offset IN (1, 4) THEN 45
        ELSE 10
    END
FROM activities a
JOIN (
    SELECT 6 AS day_offset
    UNION SELECT 5
    UNION SELECT 4
    UNION SELECT 3
    UNION SELECT 2
    UNION SELECT 1
    UNION SELECT 0
) d
WHERE a.title = 'Workout'
AND a.student_id = (
    SELECT id
    FROM users
    WHERE email = 'vivaan.student@example.com'
);


-- Ishita - consistent coding

INSERT INTO activity_logs
(
    activity_id,
    student_id,
    log_date,
    completed,
    actual_value,
    time_spent
)

SELECT
    a.id,
    a.student_id,
    DATE_SUB(CURDATE(), INTERVAL d.day_offset DAY),
    TRUE,
    60,
    60
FROM activities a
JOIN (
    SELECT 4 AS day_offset
    UNION SELECT 3
    UNION SELECT 2
    UNION SELECT 1
    UNION SELECT 0
) d
WHERE a.title = 'JavaScript Practice'
AND a.student_id = (
    SELECT id
    FROM users
    WHERE email = 'ishita.student@example.com'
);


-- Arjun - career-focused progress

INSERT INTO activity_logs
(
    activity_id,
    student_id,
    log_date,
    completed,
    actual_value,
    time_spent
)

SELECT
    a.id,
    a.student_id,
    DATE_SUB(CURDATE(), INTERVAL d.day_offset DAY),
    TRUE,
    90,
    90
FROM activities a
JOIN (
    SELECT 6 AS day_offset
    UNION SELECT 3
    UNION SELECT 0
) d
WHERE a.title = 'Portfolio Building'
AND a.student_id = (
    SELECT id
    FROM users
    WHERE email = 'arjun.student@example.com'
);


-- =========================================================
-- DEMO FEEDBACK
-- =========================================================

INSERT INTO feedback
(
    mentor_id,
    student_id,
    activity_id,
    feedback_text
)

SELECT
    m.id,
    s.id,
    a.id,
    'Excellent consistency with your Python practice. Keep maintaining this routine.'
FROM users m
JOIN users s
    ON s.email = 'riya.student@example.com'
JOIN activities a
    ON a.student_id = s.id
    AND a.title = 'Python Practice'
WHERE m.email = 'aarav.mentor@example.com';


INSERT INTO feedback
(
    mentor_id,
    student_id,
    activity_id,
    feedback_text
)

SELECT
    m.id,
    s.id,
    a.id,
    'Your progress is improving. Try to maintain a more regular study schedule.'
FROM users m
JOIN users s
    ON s.email = 'kabir.student@example.com'
JOIN activities a
    ON a.student_id = s.id
    AND a.title = 'Data Structures'
WHERE m.email = 'aarav.mentor@example.com';


INSERT INTO feedback
(
    mentor_id,
    student_id,
    activity_id,
    feedback_text
)

SELECT
    m.id,
    s.id,
    a.id,
    'Good work on the project. Continue investing consistent time in development.'
FROM users m
JOIN users s
    ON s.email = 'ananya.student@example.com'
JOIN activities a
    ON a.student_id = s.id
    AND a.title = 'Project Work'
WHERE m.email = 'aarav.mentor@example.com';


INSERT INTO feedback
(
    mentor_id,
    student_id,
    activity_id,
    feedback_text
)

SELECT
    m.id,
    s.id,
    a.id,
    'Try to be more consistent with your workouts. Small improvements every day matter.'
FROM users m
JOIN users s
    ON s.email = 'vivaan.student@example.com'
JOIN activities a
    ON a.student_id = s.id
    AND a.title = 'Workout'
WHERE m.email = 'priya.mentor@example.com';