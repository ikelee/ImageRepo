DROP DATABASE IF EXISTS IMAGE_REPO;
CREATE DATABASE IMAGE_REPO;
USE IMAGE_REPO;

DROP TABLE IF EXISTS `user_credential`;
CREATE TABLE IF NOT EXISTS `user_credential` (
    id INT(16) AUTO_INCREMENT,
    username VARCHAR(20) UNIQUE,
    password_hash VARCHAR(75),
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX user_credential_username ON `user_credential` (username);

DROP TABLE IF EXISTS `user_info`;
CREATE TABLE IF NOT EXISTS `user_info` (
    id INT(16) UNIQUE,
    `name` VARCHAR(20),
    age INT(15),
    birthday DATE,
    business_id VARCHAR(50),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES `user_credential`(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `folder`;
CREATE TABLE IF NOT EXISTS `folder` (
    id INT(16) AUTO_INCREMENT,
    user_id INT(16),
    `name` VARCHAR(30),
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES `user_credential`(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
CREATE INDEX folder_user_id ON `folder` (user_id);

DROP TABLE IF EXISTS `image`;
CREATE TABLE IF NOT EXISTS `image` (
    id INT(16) AUTO_INCREMENT,
    user_id INT(16),
    `name` VARCHAR(30),
    folder_id INT(16),
    deleted BOOLEAN DEFAULT 0,
    public BOOLEAN DEFAULT 0,
    PRIMARY KEY (id),
    FOREIGN KEY (folder_id) REFERENCES `folder`(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;