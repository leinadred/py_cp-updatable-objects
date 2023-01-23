![license](https://img.shields.io/github/license/leinadred/py_cp-updatable-objects)
![language](https://img.shields.io/github/languages/top/leinadred/py_cp-updatable-objects)
# py_cp-updatable-objects
Script to fetch available Updatable Objects from Check Point Management and putting them into a csv file.

Modules used:
 - cpapi (https://github.com/CheckPointSW/cp_mgmt_api_python_sdk)
 - argparse (should be there by default)
 - csv (should be there by default)

# usage

python py_cp-updatable-objects.py -H <Check Point Management Server> (-U/--user <api user name>) -P/--password <if API key, use only "-P", else password for "--user"> show repositories (-f Azure)
  
  
