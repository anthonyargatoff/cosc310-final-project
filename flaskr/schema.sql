DROP TABLE IF EXISTS earthquake;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS notification;

CREATE TABLE earthquake (
    earthquakeid INTEGER PRIMARY KEY,
    title VARCHAR(50),
    eventTime datetime,
    magnitude decimal (6, 4),
    latitude decimal (9, 6),
    longitude decimal (9, 6),
    depth decimal (10,6),
    url varchar(255)
);

CREATE TABLE user (
    userid INTEGER PRIMARY KEY,
    email Varchar(100) Unique,
    adminStatus Integer,    -- 0 for false 1 for true
    password Varchar(100)
);

create table notification (
    notifyid INTEGER PRIMARY KEY,
    userid Integer,
    minMagnitude decimal(6, 4),
    maxMagnitude decimal(6, 4),
    latitude decimal(9, 6),
    longitude decimal(9, 6),
    location varchar(255),
    radius decimal(10, 6),
    attributes varchar(255),
    Foreign Key (userid) References user(userid)
        On Delete Cascade
        On Update Cascade
);

INSERT INTO user (email, adminStatus, password) VALUES ('test@hotmail.com', 1, 'test');
INSERT INTO notification (userid, minMagnitude, maxMagnitude, latitude, longitude, location, radius, attributes) VALUES (1, 0, 10, 0, 0, 'test', 0, 'test');
INSERT INTO earthquake (title, eventTime, magnitude, latitude, longitude, depth, url) VALUES ('test', '2020-01-01', 0, 0, 0, 0, 'test');