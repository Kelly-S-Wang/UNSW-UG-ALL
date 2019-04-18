create or replace view tables("table",ntuples)
as
select t.relname,t.reltuples
from   pg_class t
	join pg_namespace n on (t.relnamespace = n.oid)
where  t.relkind = 'r' and n.nspname = 'public'
order  by t.relname
;
