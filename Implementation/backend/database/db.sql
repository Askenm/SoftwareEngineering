-- Battle table
CREATE TABLE ckb.battles (
    bid SERIAL PRIMARY KEY,
    battle_name VARCHAR(255) NOT NULL,
    battle_description VARCHAR(3000) NOT NULL,
    tournament_id INT,
    github_repo VARCHAR(255) NOT NULL,
    creator VARCHAR(255),
    create_date DATE DEFAULT CURRENT_DATE,
    end_date DATE
    );

-- Tournament table
CREATE TABLE ckb.tournaments (
    tid SERIAL PRIMARY KEY,
    tournament_name VARCHAR(255) NOT NULL,
    creator VARCHAR(255),
    create_date DATE DEFAULT CURRENT_DATE,
    end_date DATE DEFAULT NULL
    );

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
    notification_type VARCHAR(50),
    tournament_id INT,
    notification_text VARCHAR(500),
    battle_id INT,
    is_sent BOOLEAN DEFAULT FALSE,
    sent_date DATE DEFAULT NULL
);

-- Badge table
CREATE TABLE ckb.badge (
    bid SERIAL PRIMARY KEY,
    badge_name VARCHAR(255),
    badge_description VARCHAR(3000),
    tournament_id INT,
    rank INT,
    num_battles INT,
	create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Badge Holders table
CREATE TABLE ckb.badgeholders (
    bid INT,
    uid INT,
	badge_achieved TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- User table
CREATE TABLE ckb.users (
    uid SERIAL PRIMARY KEY,
    user_name VARCHAR(255),
    create_date DATE DEFAULT CURRENT_DATE,
    user_email VARCHAR(255),
    github_user_name VARCHAR(255),
    is_educator BOOLEAN 
);


-- Submissions table
CREATE TABLE ckb.submissions (
    smid SERIAL PRIMARY KEY,
    gid INT,
    battle_id INT,
    submission_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submission_score DECIMAL,
    notification_registered BOOLEAN DEFAULT FALSE
);

-- Subscriptions table
CREATE TABLE ckb.subscriptions (
    uid INT,
    tid INT,
    subscribe_date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (uid, tid)
);

-- Groups table
CREATE TABLE ckb.groups (
    gid SERIAL PRIMARY KEY,
    group_name VARCHAR(255),
    bid INT,
    uid INT,
    group_create_date DATE DEFAULT CURRENT_DATE
);
