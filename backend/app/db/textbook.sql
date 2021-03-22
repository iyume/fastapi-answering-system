CREATE TABLE questions (
    ...
);

CREATE TABLE user (
    id CHAR(36) PRIMARY KEY,
    name CHAR(16) UNIQUE,
    email CHAR(254) UNIQUE,
    wechat CHAR(16),
    hashed_password CHAR(60) NOT NULL,
    is_active BOOL DEFAULT true,
    is_superuser BOOL DEFAULT false,
    created_time TIMESTAMP DEFAULT (DATETIME('now', 'localtime')),
    first_login TIMESTAMP
);

CREATE TABLE exam_info (
    tag CHAR(20) PRIMARY KEY,
    title CHAR(20) NOT NULL,
    detail CHAR(200),
    type CHAR(10),
    subject CHAR(10),
    created_time TIMESTAMP DEFAULT (datetime('now', 'localtime')),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL
);

CREATE TABLE exam_cache (
    username CHAR(36),
    question_id CHAR(36) REFERENCES questions(id),
    picked CHAR(1),
    exam_tag CHAR(20) REFERENCES exam_info(tag),
    question_order INT,
    fade_key INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE exam_status (
    username CHAR(36),
    exam_tag CHAR(20) REFERENCES exam_info(tag),
    status INT DEFAULT 0,
    fade_key INTEGER PRIMARY KEY AUTOINCREMENT
);

CREATE TABLE answer_cache (
    username CHAR(16) NOT NULL,
    question_id CHAR(36) NOT NULL REFERENCES questions(id),
    picked CHAR(1) NOT NULL,
    refreshed BOOL DEFAULT false,
    fade_key INTEGER PRIMARY KEY AUTOINCREMENT
);
