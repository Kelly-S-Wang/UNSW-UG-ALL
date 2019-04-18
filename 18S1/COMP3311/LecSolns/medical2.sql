-- Mapping of ER diagram with Prescription as an Entity

create domain NameValue as varchar(100) not null;
--  character varying (100)

create table Drug (
	dno         integer, -- unique not null because PK
	name        NameValue unique, -- not null from domain
	formula     text,    -- can be null
	primary key (dno)
);

create table Patient (
	pid         integer,  -- unique not null because PK
	name        NameValue, -- not null from domain
	address     text not null,
	primary key (pid)
);

create table Doctor (
	tfn         integer, -- unique not null because PK
	name        NameValue, -- not null from domain
	specialty   text not null,
	primary key (tfn)
);

create table Prescription (
	prNum       integer,
	"date"      date not null,
	doctor      integer not null references Doctor(tfn), -- n:1 relationship
	patient     integer not null references Patient(pid), -- n:1 relationship
	primary key (prNum)
);

create table PrescriptionItem (
	prescription integer references Prescription(prNum),
	drug         integer references Drug(dno),
	quantity     integer check (quantity > 0),
	primary key  (prescription,drug)
);
