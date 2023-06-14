drop table if exists jobs;

create table jobs (
	-- Use an auto-incrementing integer as the primary key
	id integer primary key autoincrement
	, job_uid text primary key
	, docker_id text primary key
	-- Keep the timestamp when this was created.
	, created timestamp not null default current_timestamp
	-- this is actually a boolean. SQLite does not support boolean
	, killed integer not null default 0
	-- Job information
	, kappa real not null
	, rkappa real not null
	, window real not null
	-- Container information
	, name text 
	-- User information
	, ip text
);
