# TecTimeTravel
A project to gather flight data.

## Getting Started
### Required login
An OpenSky account is required. Timestamps are used to let the retrieval catch up when it has stopped for a short time or if an error occurred. This functionality is only supported with an OpenSky account. It can be created for free on https://opensky-network.org/. 
The account details need to be provided in the file *config/logins.yml*. You can use the template *config/logins_template.yml* for the right format.

### How to run
For now, provide the required login and run load/opensky/schedule.py to save OpenSky data to disk.