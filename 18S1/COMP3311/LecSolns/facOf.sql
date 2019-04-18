drop type if exists AncestorTuple cascade;
create type AncestorTuple as (id integer, typ text);

-- generate all ancestors of a given OrgUnit

create or replace function 
	ancOf(integer) returns setof AncestorTuple
as $$
with recursive Ancestors(id,typ) as (
	(select u.id, t.name
	 from   Orgunits u
	         join OrgUnitTypes t on (u.utype = t.id)
	 where  u.id = $1)
	union
	(select u.id, t.name
	 from   OrgUnits u
	         join OrgUnitTypes t on (u.utype = t.id)
	         join UnitGroups g on (g.owner = u.id)
	         join Ancestors a on (a.id = g.member)
    )
)
select * from Ancestors
$$
language sql;


-- select the ancestor of an OrgUnit which is a faculty

create or replace function
	facOf(integer) returns integer
as $$
select id from ancOf($1) where typ = 'Faculty';
$$
language sql;
