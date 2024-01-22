-- Notifications table
CREATE TABLE ckb.notifications (
    nid SERIAL PRIMARY KEY,
    notification_name VARCHAR(255),
    notification_logic TEXT,
    create_date DATE DEFAULT CURRENT_DATE
);

-- Message Board table
CREATE TABLE ckb.message_board (
    nid SERIAL PRIMARY KEY,
    uid INT,
    battle_id INT,
    sent_date DATE DEFAULT CURRENT_DATE
);

-- Badge table
CREATE TABLE ckb.badge (
    bid SERIAL PRIMARY KEY,
    badge_name VARCHAR(255),
    tournament_id INT,
    badge_logic TEXT,
	create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User table
CREATE TABLE ckb.users (
    uid SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    create_date DATE DEFAULT CURRENT_DATE,
    user_email VARCHAR(255),
    github_user_name VARCHAR(255)
);

-- Submissions table
CREATE TABLE ckb.submissions (
    smid SERIAL PRIMARY KEY,
    gid INT,
    battle_id INT,
    submission_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submission_score DECIMAL
);

-- Subscriptions table
CREATE TABLE ckb.subscriptions (
    uid INT,
    tid INT,
    subscribe_date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (uid, tid)
);

-- Participations table
CREATE TABLE ckb.participations (
    tournament_id INT,
    group_id INT,
    participate_id SERIAL PRIMARY KEY
);

-- Groups table
CREATE TABLE ckb.groups (
    gid SERIAL PRIMARY KEY,
    participant_id INT,
    tournament_id INT,
    group_create_date DATE DEFAULT CURRENT_DATE
);
