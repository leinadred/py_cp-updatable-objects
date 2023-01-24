![license](https://img.shields.io/github/license/leinadred/py_cp-updatable-objects)
![language](https://img.shields.io/github/languages/top/leinadred/py_cp-updatable-objects)
# py_cp-updatable-objects
Script to fetch available Updatable Objects from Check Point Management and putting them into a csv file.

Modules used:
 - cpapi (https://github.com/CheckPointSW/cp_mgmt_api_python_sdk)
 - argparse (should be there by default)
 - csv (should be there by default)

possible use cases:

 - providing this to rule change requester to request the correct source / destinations
 - just having an eye of what is possible to import
 - (coming later) - having an eye of what is imported
 - (coming later) - having an eye of last update occured to specific objects


# usage
  
python py_cp-updatable-objects.py -H <Host IP/Name> (-U/--user <user>) -P/--password <auth credential> (if API key, use only "-P", else password for "--user") show repositories (-f <string to filter for, i.e. "Azure">)

example:

python py_cp-updatable-objects.py -H 1.2.3.4  -P s3cr3tk3Y show repositories -f Azure




