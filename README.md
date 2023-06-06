# STAMINA for Servers

This repository contains code to set up the STAMINA REST API through the Spring framework. It is not yet finished. Eventually we will add a Gradle build file.

## Why are we doing this?

FLUENT has recieved some grant funding to use towards some Azure servers. While IBioSym is already running on these servers, we are trying to make STAMINA/STORM able to run on these Azure servers. This is why we have dockerized it and are writing this wrapper program to read REST API calls and start STAMINA.

## REST Query Parameters

This section is a WIP.

STAMINA will take JSON formulated REST queries with the following parameters:

**Status Parameter**: this parameter is used if checking the *status* of an existing job.
- `uid`: If `uid` is provided, all other parameters are ignored. Any log output from STAMINA for job with that UID will be returned immediately.

**Start-job Parameters**: These parameters are required to *start* a job
- `modelFile`: The complete text of the PRISM language model file with which to build the model from
- `propertiesFile`: The complete text of the CSL properties file to check
- `kappa`: The reachability threshold
- `rkappa`: The reduction factor fot the reachability threshold
- `threads`: The number of threads to use (CPU limits will be enforced)
- `method`: The method of truncation to use
- `labels`: Whether or not to print state-labelling information
- `stateLimit`: Enforce a state limit at `n` states
- `transitionFile`: TODO
