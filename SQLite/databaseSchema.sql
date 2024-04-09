
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

create table notification(
    notifyid INTEGER PRIMARY KEY,
    userid Integer,
    attributes varchar(255),
    Foreign Key (userid) References user(userid)
        On Delete Cascade
        On Update Cascade

);

Insert into user(userid, email,adminStatus,password) values(1,'ryanpybus8596@gmail.com',0,'passw');
Insert into notification(userid,attributes) values(1,'magnitude:0-10;area:49.2827,123.1207,10000');

INSERT INTO user (email, adminStatus, password) VALUES ('test@hotmail.com', 1, 'test');
INSERT INTO notification (userid, attributes) VALUES (2, 'magnitude:1-10;area:0,0,50');