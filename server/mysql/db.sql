--MySQL config
CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'server'@'localhost' IDENTIFIED BY 'password';
GRANT PRIVILEGE ON db.* TO 'server'@'localhost';



--Users & Rools & Actions
CREATE DATABASE db;
USE db;

CREATE TABLE users (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    UserName VARCHAR NOT NULL,
    Gmail VARCHAR NOT NULL UNIQUE,
    PasswordHash VARCHAR NOT NULL,
    Roles INT NOT NULL,
    FOREIGN KEY (Roles) REFERENCES roles(ID),
    EnabledUser BOOLEAN NOT NULL
);

CREATE TABLE roles (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    RoleName VARCHAR NOT NULL
);

CREATE TABLE actions (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    ActionName VARCHAR NOT NULL,
    ActionDesc VARCHAR
);

CREATE TABLE roles_actions (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    roleID INT NOT NULL,
    FOREIGN KEY (roleID) REFERENCES roles(ID),
    actionID INT NOT NULL,
    FOREIGN KEY (actionID) REFERENCES actions(ID),
);

INSERT INTO users (UserName, Gmail, PasswordHash, Roles, EnabledUser) VALUES
    ('admin', 'admin@gmail.com', SHA2('admin', 256), 1, TRUE); --! PAZI GESLO

INSERT INTO roles (RoleName) VALUES
    ('root'), -- 1
    ('user'); -- 2

INSERT INTO actions (ActionName, ActionDesc) VALUES
    ('EnableAccounts', ''), -- 1
    ('CreateChannel', ''), -- 2
    ('RoleCreate', ''); -- 3

INSERT INTO roles_actions (roleID, actionID) VALUES
    (1, 1),
    (1, 2),
    (1, 3);



--Saved chats
CREATE TABLE msg (
    ID INT NOT NULL AUTO_INCREMENT,
    Edited BOOLEAN NOT NULL,
    User INT NOT NULL,
    FOREIGN KEY (User) REFERENCES user(ID),
    Chat INT NOT NULL,
    FOREIGN KEY (Chat) REFERENCES chat(ID),
    DateInf DATETIME,
    MSG VARCHAR
);

CREATE TABLE chat (
    ID INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    ChatName VARCHAR
);

INSERT INTO chat (ChatName) VALUES
    ('General')

INSERT INTO msg (Edited, User, Chat, DataInf, MSG) VALUES
    (FALSE, 1, 1, now(), "Welcome to server!");