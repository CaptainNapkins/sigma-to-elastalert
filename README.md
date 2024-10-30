# sigma-to-elastalert
### Janky Script to Convert Sigma Rules to Elastalert Rules 

# Exposition
Ran into a slight problem with a school project... Needed to convert Sigma rules to Elastic Search rules. Surely it can't be that bad. 

However, there are few massive issues.

1. `sigmac` the, converter for sigma rules to various other rule formats (splunk, elastalert, etc), has been deprecated as of 8/3/2024.
2. `sigmac` does work and can convert sigma rules to elastalert rules, but the elastic search queries it generates are out of date. I am not sure as to exactly how much, but they do not work for my elastic instance which is on 8.10 So that is out. It also doesn't support some specific backend configurations that I need. 
3. `pySigma`, the replacement for `sigmac`, does not support direct conversion from Sigma rules to elastalert rules. However, it does support conversion from Sigma rules to elastic search *queries*. This will come in handy later. Additionally it should be noted that it notably only supports the following pipelines for elastic search...
	- `ecs_windows` (elastic schema for windows logs from version 7) 
	- `ecs_zeek_beats` for zeek logs that use filebeat version >= 7.6.1
	- It also supports older windows logs schma, zeek mappings from corelight, and kubernetes mappings.
	- But, notably, no pipelines for linux Sigma rules. 

So, this approach uses `sigma-cli`, based on `pySigma`, to convert Sigma rules to elastic search queries, and then manually build an appropriate elastalert config file. 

# Getting Started

## Install sigma-cli Tool
1. Make sure you have `sigma-cli` installed and that the resultant program is added to your path
- Install from here https://github.com/SigmaHQ/sigma-cli
2. Install the `elasticsearch` plugin with `sigma plugin install elasticsearch`

##  Grab Some Sigma Rules
1. Found here https://github.com/SigmaHQ/sigma 

## Replace Default Values
Inside the script there are currently two default values at the top. An `alert_type` and `ms_webhook`. My usecase was sending these alerts to an Microsoft Teams channel. So, I had set `alert_type` to `ms_teams` and `ms_webhook` to my MS teams channel connector webhook. Feel free to go crazy and set more/different values. They are best changed in `edit_fields()` where you can see that the `final_rule` dictionary is being set up in the proper elastalert yaml structrure. 

Additionally, the `gen_syntax()` function generates some syntax so that the alerts look halfway decent in teams. Feel free to replace/edit this to your hearts content. 

## Best of luck, soldier 

# Example Usage
Convert some Windows builtin security Sigma rules to elastalert rules
```bash
python3 converter.py --sigma_rule_dir /home/user/sigma/rules/windows/builtin/security --out_dir output
```

# But wait, there's more! 
A `docker-compose` file for `elastalert2` is included for funzies. Run `docker compose up` to start the elastalert2 instance. 

Also included is the config file. You will have to make a `rules` directory to store your shiny new elastalert rules. **ENSURE** that your rules directory and elastalert global config are in the cwd of the docker compose file. You can adjust the locations of these items in the compose file itself if you would like. Additionally, change the default values in the `elastalert.yaml` file. 

# Disclaimer 
This was done for a school project and is uploaded for the help of fellow classmates. The code is quite jank and is by no means a finished product. This was only tested on Ubuntu 22.04 and is ~~definitely~~ probably prone to breaking. There are also quite a few optimizations/changes to be done regarding filtering by log levels, realert times, etc. This is mostly a POC. GGs
