USING main;

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

IF NOT EXISTS main.user CREATE TABLE user (
    userid INTEGER PRIMARY KEY,
    email Varchar(100) Unique,
    adminStatus Integer,    -- 0 for false 1 for true
    password Varchar(100)
);

IF NOT EXISTS main.notification create table notification(
    notifyid INTEGER PRIMARY KEY,
    userid Integer,
    attributes varchar(255),
    Foreign Key (userid) References user(userid)
        On Delete Cascade
        On Update Cascade
);