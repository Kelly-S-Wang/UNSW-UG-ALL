-- A very small database to demonstrate different joins

create table R (
	x  integer primary key,
	y  text
);

insert into R values (1,'abc');
insert into R values (2,'def');
insert into R values (3,'ghi');

create table S (
	z  char(1) primary key,
	x  integer references R(x)
);

insert into S values ('a',1);
insert into S values ('b',3);
insert into S values ('c',1);
insert into S values ('d',null);

-- compare the differences in the results of the following:

-- select * from R natural join S;
x	y	z
1	abc	a
1	abc	c
3	ghi	b

-- select * from R join S on (R.x = S.x);  -- join means inner join (inner is optional and is the default)
x	y	z	x
1	abc	a	1
1	abc	c	1
3	ghi	b	3

-- select * from R, S where R.x = S.x;
x	y	z	x
1	abc	a	1
1	abc	c	1
3	ghi	b	3

-- select * from R left outer join S on (R.x = S.x);  -- outer not compulsory when left, right, and full are used
x	y	z	x
1	abc	a	1
1	abc	c	1
2	def	
3	ghi	b	3

-- select * from R right outer join S on (R.x = S.x);
x	y	z	x
1	abc	a	1
1	abc	c	1
3	ghi	b	3
		d	

-- select * from R full outer join S on (R.x = S.x);
x	y	z	x
1	abc	a	1
1	abc	c	1
2	def	
3	ghi	b	3
		d