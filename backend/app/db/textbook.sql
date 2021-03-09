CREATE TABLE questions (
    ...
);

CREATE TABLE user (
    id CHAR(36) PRIMARY KEY,
    name CHAR(16),
    email CHAR(254) UNIQUE,
    wechat CHAR(16),
    hashed_password CHAR(60) NOT NULL,
    is_active BOOL DEFAULT true,
    is_superuser BOOL DEFAULT false,
    created_time TIMESTAMP DEFAULT (DATETIME('now', 'localtime')),
    first_login TIMESTAMP
);

CREATE TABLE exam_info (
    tag CHAR(10) PRIMARY KEY,
    title CHAR(20) NOT NULL,
    detail CHAR(200),
    type CHAR(10),
    subject CHAR(10),
    created_time TIMESTAMP DEFAULT (datetime('now', 'localtime')),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL
);

CREATE TABLE exam_cache (
    user_id CHAR(36) REFERENCES user(id),
    question_id CHAR(36) REFERENCES questions(id),
    picked CHAR(1),
    exam_tag CHAR(10) REFERENCES exam_info(tag),
    fade_key INTEGER PRIMARY KEY AUTOINCREMENT
);
