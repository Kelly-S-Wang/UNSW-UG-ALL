create or replace function
	iotar(integer, integer, integer) returns setof integer
as $$
with recursive terms(n) as (
	select $1
	union all
	select n+$3 from terms where n+$3 <= $2
)
select n from terms
$$ language sql;
