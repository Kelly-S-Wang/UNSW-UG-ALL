create or replace function
	append(soFar text, newStr text) returns text
as $$
begin
	if (soFar = '') then
		return newStr;
	else
		return soFar||','||newStr;
	end if;
end;
$$ language plpgsql;

drop aggregate if exists concat(text);

create aggregate concat(text) (
	initcond  = '',
	stype     = text,
	sfunc     = append
);
