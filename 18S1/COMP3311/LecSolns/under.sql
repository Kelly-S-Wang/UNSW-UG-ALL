-- Find underachievers for a given course

-- Assume we have a table
-- CourseAverages(student,course,mark,grade,stueval,avg)
-- where avg is the average mark for the course

create or replace function
	under(integer) returns setof CourseEnrolments
as $$
select student,course,mark,grade,stueval
from   CourseAverages
where  course = $1 and mark < 0.6*avg
$$
language sql stable;


-- Generate the CourseAverages table using window function

create view CourseAverages as
select student,course,mark,grade,stueval,avg(mark)
over   (partition by course)
from   CourseEnrolments;
