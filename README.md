# Configurator

## Overview
Configurator is implemented in python and can be run either via command line or via pre build template files. This tool uses imperative style of execution and the moment supports minimal set of features

## System Requirements
In order to run configurator, you need the following packages installed on your management host
* Python3+
* Terminal to run the program
* List of remote hosts to configure and their credentials

## How to execute
1. Clone the repo
` git clone git@github.com:ntata/configurator.git`
2. Install python3
`apt-get install python3.6`
3. Create virtual environment
`python -m venv .venv && source .venv/bin/activate`
4. Install requirements
` pip install -r requirements.txt`
5. Set environment variables:
`export CONFIGURATOR_SSH_USER=****`
`export CONFIGURATOR_SSH_USER_PASSWORD=****`
6 run templates
```
$python configurator.py -t run_cmd.yaml

*** Output of 'ls -la' on '54.196.242.68'
total 24
drwx------  3 root root 4096 Feb 21 19:51 .
drwxr-xr-x 22 root root 4096 Jan 13 22:44 ..
-rw-------  1 root root  120 Feb 21 20:24 .bash_history
-rw-r--r--  1 root root 3106 Feb 20  2014 .bashrc
drwx------  2 root root 4096 Jan 15 02:52 .cache
-rw-r--r--  1 root root  140 Feb 20  2014 .profile
-rw-r--r--  1 root root    0 Feb 21 19:51 test_file_1
-rw-r--r--  1 root root    0 Feb 21 19:51 test_file_2

*** Output of 'ls -la' on '34.229.127.246'
total 24
drwx------  3 root root 4096 Feb 21 19:51 .
drwxr-xr-x 22 root root 4096 Jan 13 22:44 ..
-rw-------  1 root root   65 Jan 16 04:29 .bash_history
-rw-r--r--  1 root root 3106 Feb 20  2014 .bashrc
drwx------  2 root root 4096 Jan 15 02:53 .cache
-rw-r--r--  1 root root  140 Feb 20  2014 .profile
-rw-r--r--  1 root root    0 Feb 21 19:51 test_file_1
-rw-r--r--  1 root root    0 Feb 21 19:51 test_file_2
```
