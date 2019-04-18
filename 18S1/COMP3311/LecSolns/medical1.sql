-- Mapping of ER diagram with Prescription as relationship

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

create table Prescribes (
	drug        integer references Drug(dno),
	doctor      integer not null references Doctor(tfn),
	patient     integer references Patient(pid),
	quantity    integer not null,
	"date"      date,
	primary key ("date",patient,drug)
	-- allows a patient to be prescribed 
	-- a given drug only once on a given day 
);

-- think about the implications of alternative primary keys
-- primary key(patient)
-- primary key(drug)
-- primary key("date")
-- primary key(patient,"date")
-- primary key(patient,"date",drug,doctor)

