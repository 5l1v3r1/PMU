![alt text](http://leonvoerman.nl/coding/pmu.png)
![alt text](http://leonvoerman.nl/coding/pmuv1.png)

# PMU (Beta test)
**P**ackage **M**anager **U**nlimited is a RAT for Linux coded with Python.

---

# Remote Package Manager for Linux (Python)

	Name: Package Manager Unlimited (PMU)
	Files: server.py, shell.py, rat.py
  
	Installation: Put the rat.py in start-up as Root.
  
	Theory Craft:
	Client creates a key to connect with a remote server that sends command and data to controll the client.
  	This is a reverse connection.
	
# Remote server 

**Output:**

| Status        | Key    | Hostname| User   |  Ip address| Package Status       |
| -------------  |:------| ------- |:-------| -----------|:---------------------|
| [Online]       | FHT3Z | example | Dennis | 10.0.0.223 | 4 updates, 2 upgrades|
| [Online]       | RTF56 | Kees    | Klaus  | 10.0.0.217 | 1 updates, 7 upgrades|
| [Offline]      | PTOV2 | Piet    | None   | 10.0.0.215 | ? updates, ? upgrades|

								


# Commands

| Command        | Execution     |
| ------------- |:-------------|
| /genkey      | Generate Key voor client |
| /del <key>      | Delete client key|
| /update example  | client.send('apt-get update && apt-get upgrade -y')|
| /update all  | all.send('apt-get update && apt-get upgrade -y')|
| /save list csv  | save output in .csv|
| /save list txt  | save output in .txt|
| /connect 10.0.0.223  | Connect to client (reverse shell >> drop /bin/bash)|
| /c <command>  | send and execute custom command on remote client|
| /shutdown all  | Shutdown all remote clients|
| /shutdown {key}  | Shutdown all remote clients|
| /reboot all | Reboot all remote client|
| /reboot {key}  | Reboot remote client|
| /show list  | Show all clients|
| /show offline | Show offline only|
| /show online  | show online only|
| /shutdown  | Shutdown remote server|


# Client installation:
	Server IP \> 10.0.0.1
	Port \> 3435
	Authentication Key \> PTOV2
	
	*Do magic*

	s.send(KEY$PTOV2)
	
	Add to list on remote server
	
	Startup >> Connect >> Send Key >> Authenticate >> Allow or deny socket
	
	Put the rat.py in start-up as Root

# Security
	Future versions will have authentication.
	
	>> Sofar, 'rm' commands are blocked by the RAT.
	>> Commands are encrypted
	
## Pentest
	Now encrypted. Pentest ahead.
