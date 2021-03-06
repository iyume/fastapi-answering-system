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

