---- Single-table mapping of subclasses ----

-- disjoint, total (i.e. each student belongs to exactly one subclass)

create table Student (
	sid integer primary key,
	name text,
	address text,
	degree text,
	major text,
	thesis text,
	constraint DisjointTotal check
	((degree is not null and major is null and thesis is null)
	 or
	 (degree is null and major is not null and thesis is null)
	 or
	 (degree is null and major is null and thesis is not null))
);

-- disjoint, partial (i.e. each student belongs to zero or one subclasses)

create table Student (
	sid integer primary key,
	name text,
	address text,
	degree text,
	major text,
	thesis text,
	constraint DisjointPartial check
	((degree is not null and major is null and thesis is null)
	 or
	 (degree is null and major is not null and thesis is null)
	 or
	 (degree is null and major is null and thesis is not null)
	 or
	 (degree is null and major is null and thesis is null))
);

-- overlapping, total (i.e. each student belongs to one or more subclasses)

create table Student (
	sid integer primary key,
	name text,
	address text,
	degree text,
	major text,
	thesis text,
	constraint OverlappingTotal check
	(degree is not null or major is not null or thesis is not null)
);

-- overlapping, partial (i.e. each student belongs to zero or more subclasses)

create table Student (
	sid integer primary key,
	name text,
	address text,
	degree text,
	major text,
	thesis text
	-- no constraint needed
);


---- ER mapping of subclasses ----

-- as specified, only properly handles (overlapping, partial) case
-- to make it handle other cases correctly requires triggers

create table Student (
	sid integer primary key,
	name text,
	address text
);

create table Ugrad (
	sid integer references Student(sid),
	degree text,
	primary key (sid)
);

create table Masters (
	sid integer references Student(sid),
	major text,
	primary key (sid)
);

create table Research (
	sid integer references Student(sid),
	thesis text,
	primary key (sid)
);

---- OO mapping of subclasses ----

create table Student (
	sid integer primary key,
	name text,
	address text
);

create table Ugrad (
	sid integer references Student(sid),
	name text,
	address text,
	degree text,
	primary key (sid)
);

create table Masters (
	sid integer references Student(sid),
	name text,
	address text,
	major text,
	primary key (sid)
);

create table Research (
	sid integer references Student(sid),
	name text,
	address text,
	thesis text,
	primary key (sid)
);

---- Extra notes ---

In the ER and single-table cases, you could potentially add an
attribute like the following to suggest a disjoint mapping, but
this doesn't make the above solutions "better" in the sense that
it does not enforce the required constraints

	stype  text not null
		check (stype in ('ugrad','masters','research')),

In the ER and single-table cases, you could potentially add a
boolean attribute for each subclass to suggest overlapping
subclasses, but this doesn't make the above solutions "better"
either

	isUgrad boolean,
	isMasters boolean,
	isResearch boolean,

