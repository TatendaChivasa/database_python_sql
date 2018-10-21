insert into members values ('davood@abc.com','Davood Rafiei','780-111-3333','abcd');
insert into members values ('joe@gmail.com','Joe Anderson','780-111-2222','efgh');
insert into members values ('mary@abc.com','Mary Smith','780-222-3333','ijkl');
insert into members values ('paul@a.com','John Paul','780-333-4444','mnop');

insert into cars values (1,'Aston Martin','DB5',1964,1,'davood@abc.com');
insert into cars values (2,'Honda','Civic',2017,4,'joe@gmail.com');
insert into cars values (3,'Nissan','Rogue',2018,4,'mary@abc.com');

insert into locations values ('ab1','Edmonton','Alberta','UofA LRT st');
insert into locations values ('ab2','Edmonton','Alberta','Century LRT st');
insert into locations values ('ab3','Edmonton','Alberta',null);
insert into locations values ('ab4','Calgary','Alberta','111 Edmonton Tr');
insert into locations values ('ab5','Calgary','Alberta','Airport');
insert into locations values ('ab6','Red Deer','Alberta','City Hall');
insert into locations values ('ab7','Red Deer','Alberta','Airport');
insert into locations values ('bc1','Vancouver','British Columbia','Stanley Park');
insert into locations values ('bc2','Vancouver','British Columbia','Airport');

insert into rides values (100, 30, '2018-11-12', 3, 'small bag', 'ab1', 'ab4', 'joe@gmail.com', 2);
insert into rides values (101, 30, '2018-11-13', 3, 'small bag', 'ab1', 'ab4', 'joe@gmail.com', null);

insert into bookings values (10, 'davood@abc.com', 100, null, 1, 'ab2', null);
insert into bookings values (12, 'davood@abc.com', 101, 28, 1, 'ab2', 'ab5');
insert into bookings values (14, 'paul@a.com', 100, null, 1, null, null);

insert into enroute values (100, 'ab6');
insert into enroute values (101, 'ab7');

insert into requests values (1, 'paul@a.com', '2018-12-22', 'ab3', 'bc1', 80);
insert into requests values (2, 'davood@abc.com', '2018-12-24', 'ab1', 'ab7', 30);