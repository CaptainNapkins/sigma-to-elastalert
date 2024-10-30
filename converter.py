"""
Project: Convert Sigma Rules to Elastalert Rules
Date: 10/30/2024
Author: Gabe Samide
Version: 1
Description: Creates Elastalert Rule Files from Sigma Rules using the new pySigma ecs_windows pipeline
"""

# converter, i hardly know her
import os
import subprocess
import argparse
import yaml

# ONLY SUPPORTS THE ECS_WINDOWS PIPELINE

# Change your alert type
alert_type = "ms_teams"

# Input your ms teams webhook
ms_webhook = ""

# Generates some syntax such that the alert does not look like complete garbage in 
# ms teams
def gen_syntax():
    alert_syntax = """
    alert_subject: |
      Alert: {{ host.name if host.name else "Unknown Host" }} - {{ event.action if event.action else "Unknown Action" }}

    alert_text: |
      Alert Triggered  
      Machine Name: {{ host.name if host.name else "N/A" }}
      IP Address: {{ host.ip[0] if host.ip and host.ip[0] else "N/A" }}
      Timestamp: {{ timestamp if timestamp else "N/A" }}
      Status: {{ event.outcome if event.outcome else "N/A" }}
      Log Level: {{ log.level if log.level else "N/A" }}
      Message: {{ message if message else "N/A" }}

    alert_text_type: alert_text_jinja
    alert_text_kw: 
      machine_name: "host.name"
      host: "host"
      timestamp: "timestamp"
      status: "event.outcome"
      log_level: "log.level"
      message: "message"
    """
    alert_syntax = yaml.safe_load(alert_syntax)
    return alert_syntax

# Gets all necessary fields of the sigma rule file, such as title, description, and ID
# such that we can start constructing an elastalert rule
def grab_fields(rule_file):
    needed_fields = {'title': None, 'description': None}
    with open(rule_file, "r") as file:
        data = yaml.safe_load(file)

    needed_fields['title'] = data['title'] 
    needed_fields['description'] = data['description']
    needed_fields["id"] = data["id"]
    return needed_fields

# Construct the elastalert rule
# Start with a base dictionary and then we add fields
# Can also change any of these fields if your index is different 
def edit_fields(query, rule_file, mins):
    final_rule = {}
    final_rule["name"] = rule_file["title"]
    final_rule["type"] = "any"
    final_rule["index"] = "logs-*"
    final_rule["alert"] = [alert_type]
    final_rule["ms_teams_webhook_url"] = ms_webhook
    final_rule["filter"] = [{"query": {"query_string": {"query": str(query.strip("\n"))}}}]
    # some modular arithmatic shenenigans so that we change the realert time for each rule
    # so that each rule does not continusoly query the elastic instance
    op = mins % 10
    if op == 0:
        final_rule["realert"] = {"minutes": op}
    elif op == 1:
        final_rule["realert"] = {"minutes": op}
    elif op == 2:
        final_rule["realert"] = {"minutes": op}
    elif op == 3:
        final_rule["realert"] = {"minutes": op}
    elif op == 4:
        final_rule["realert"] = {"minutes": op}
    elif op == 5:
        final_rule["realert"] = {"minutes": op}
    elif op == 6:
        final_rule["realert"] = {"minutes": op}
    elif op == 6:
        final_rule["realert"] = {"minutes": op}
    elif op == 7:
        final_rule["realert"] = {"minutes": op}
    elif op == 8:
        final_rule["realert"] = {"minutes": op}
    elif op == 9:
        final_rule["realert"] = {"minutes": op}
    else:
        final_rule["realert"] = {"minutes": op}
    return final_rule

# Takes in name of the rule, the final elastalert rule from edit_fields, 
# the alert_syntax, and the output directory to create the yaml file
def write_final(name, final_rule, alert_syntax, out_dir):
    final_name = name + ".yaml"
    out_path = os.path.join(out_dir, final_name)
    final_rule.update(alert_syntax) 
    with open(out_path, "w") as file:
        yaml.dump(final_rule, file)
        
def main():
    mins = 1

    # add arg parser stuff
    parser = argparse.ArgumentParser(description="Modify alert fields in a YAML file.")
    parser.add_argument("--sigma_rule_dir", help="Sigma Rules you'd like to convert", required=True)
    parser.add_argument("--out_dir", help="Output directory for elastalert rules", required=True)
    args = parser.parse_args()
    # generate syntax fluff
    alert_syntax =  gen_syntax()
    
    # Iterate thru all rule files in a given directory
    for file in os.listdir(args.sigma_rule_dir):
        sigma_rule_file = os.path.join(args.sigma_rule_dir, file)
        command = f"sigma convert -t eql -p ecs_windows {sigma_rule_file}".split(' ')
        # Each rule is processed seperately so this script takes a long time on some directories
        # with a lot of rules. This is because sigma-cli does not seem to process the rules in 
        # alphabetical order. So, rather than trying to tie each rule to something in one big
        # file they are evaluted one by one. This should probably be changed but the assignment
        # is due tomorrow so....
        query = subprocess.run(command, capture_output=True, text=True)
        query = query.stdout
        if os.path.isdir(sigma_rule_file):
            continue
        # Get fields from sigma rules
        data = grab_fields(sigma_rule_file)
        # Coonstruct elastic alert rule
        final_rule = edit_fields(query, data, mins)

        # Write final elastalert rule to output dir
        write_final(data["id"], final_rule, alert_syntax, args.out_dir)
        mins += 1

if __name__ == "__main__":
    main()
