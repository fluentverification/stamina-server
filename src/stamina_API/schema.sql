drop table if exists jobs;
drop table if exists deleted_jobs;

-- Jobs still 
create table jobs (
	-- Use an auto-incrementing integer as the primary key
	id integer primary key autoincrement
	, job_uid text key
	, docker_id text key
	-- Keep the timestamp when this was created.
	, created timestamp not null default current_timestamp
	-- this is actually a boolean. SQLite does not support boolean
	, killed integer not null default 0
	-- Job information
	, kappa real not null
	, rkappa real not null
	, window real not null
	-- Container information
	, name text not null
	-- User information
	, ip text not null
);

-- Jobs which have been deleted no longer need information about logs or container information
-- or anything of the sort
create table deleted_jobs (
	id integer primary key autoincrement
	, job_uid text key
	-- timestamps of when they were started vs deleted
	, created timestamp not null
	, deleted timestamp not null default current_timestamp
	-- Container information
	, name text not null
	-- User information
	, ip text not null
);
