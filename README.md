# STAMINA for Servers

This repository contains code to allow STAMINA to be run via a REST API.

## Why are we doing this?

FLUENT has recieved some grant funding to use towards some Azure servers. While IBioSym is already running on these servers, we are trying to make STAMINA/STORM able to run on these Azure servers. This is why we have dockerized it and are writing this wrapper program to read REST API calls and start STAMINA.

## Overview

Each job is assigned a `id`, sometimes called a `jid` or `uid` for job ID or unique ID. These are stored in a hashed set and associated with an IP address. You can access the details of a job with its ID from any IP address (maybe should change this).

Jobs are pruned every so often and time out every few minutes.

## Endpoints

- `/jobs`:
	+ `POST`: Creates a job, which is a run of STAMINA with a specific model and properties file. Accepts `application/json` and `multipart/form-data`, and returns `application/json`.
	+ `GET`: Gets the list of all jobs. Currently just errors because I haven't figured out a good way to authenticate yet.
	+ `DELETE` (not yet implemented): Deletes a job with a specific ID.
- `/myjobs`:
	+ `GET`: Gets a list of all jobs associated with the current IP address.
	+ `DELETE`: Deletes all active jobs associated with the current IP Address.
- `/rename`:
	+ `POST`: Renames a job with a certain ID.
- `/about`:
	+ `GET`: Gets some information about STAMINA
- `/checkjob`
	+ `POST`: Gets just the log information about a Job, given its UID in HTTP `POST`.
- `/kill`
	+ `POST`: Kills, but does not delete, a job. Job logs can still be viewed after it is killed, but not after it is deleted.
<!--
- `/egg` (easter egg):
	+ `GET`: An easter egg ;)
- `/qapla` (easter egg):
	+ `GET`: Another easter egg 
-->
