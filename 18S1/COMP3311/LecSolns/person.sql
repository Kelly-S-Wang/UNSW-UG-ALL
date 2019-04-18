create table Person (
	ssn         char(20),
	familyName  varchar(50),
	givenName   varchar(50),
	weight      float,
	birthDate   date,
	primary key (ssn)
);

create table PersonHobbies (
	person    char(20) references Person(ssn),
	hobby       varchar(30),
	primary key (person,hobby)
);
