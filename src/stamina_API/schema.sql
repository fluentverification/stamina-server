drop table if exists jobs

create table jobs (
	id integer primary key autoincrement
	, job_uid text primary key
	, docker_id text primary key
	-- this is actually a boolean
	, killed integer not null default 0
	, kappa real not null
	, rkappa real not null
	, window real not null
	, name text 
);
