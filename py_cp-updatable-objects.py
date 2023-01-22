# 2023-01 - DME
# Script to fetch available Updatable Objects from Check Point Management and putting them into a csv file.
############################################################################################
from cpapi import APIClient, APIClientArgs
import argparse
import logging
import csv
############################################################################################
# set args 
parser = argparse.ArgumentParser()
parser.add_argument('-H', '--api_server', help='Target Host (CP Management Server)', required=True)
parser.add_argument('-U', '--api_user', help='API User', required=False)
parser.add_argument('-P', '--api_pwd', help='API Users Password // OR API Key (then do not use -U)', required=True)
parser.add_argument('-C', '--api_context', help='If SmartCloud-1 is used, enter context information here (i.e. bhkjnkm-knjhbas-d32424b/web_api) - for On Prem enter \"-C none\"')
parser.add_argument('-v', '--verbose', help='Run Script with logging output - Troubleshooting and so', action='store_true')

subparser = parser.add_subparsers(required=True, dest='cmd', help='Tell what to do (show || set)')

# actions
parser_show = subparser.add_parser('show')
parser_show.add_argument('repositories', type=str, default=None, help='show providers of updatable objects')
parser_show.add_argument('filter', type=str, default='all', help='show providers of updatable objects')

args = parser.parse_args()
try:
    args.api_context
except:
    args.api_context = None


############################################################################################################################################

def fun_getfromapi():
    global output_text
    if args.api_context:
        client_args = APIClientArgs(server=args.api_server, context=args.api_context, unsafe='True')
    else:
        client_args = APIClientArgs(server=args.api_server, unsafe='True')
    with APIClient(client_args) as client:
        # If Error occurs due to fingerprint mismatch
        if client.check_fingerprint() is False:
            #output_text.update({"Message":"Could not get the server's fingerprint - Check connectivity with the server."})
            print("UNKNOWN! Logging into SMS not successful! Please troubleshoot/debug script! "+str(output_text))
            raise SystemExit()
        # login to server:
        if args.api_pwd and not args.api_user:
            login_res = client.login_with_api_key(args.api_pwd)
        elif args.api_pwd and args.api_user:
            login_res = client.login(args.api_user, args.api_pwd)
        else:
            raise SystemExit("check input of User / Password or Key (-U/-P) - see help")
        logging.debug('API Login done: '+str(login_res))
        # when login failed
        list_repos=[]
        if not login_res.success:
            #output_text.update({"Message":"Login failed: "+str(login_res.error_message)})
            print("UNKNOWN! Logging into SMS not successful! Please troubleshoot/debug script! "+str(output_text))
            raise SystemExit()
        else:
            if args.filter == "all":
                # API Call "show all repos (if set to get all)"
                res_repo = client.api_call("show-updatable-objects-repository-content",{"limit":500}).data
                list_repos.append(res_repo['objects'])
                while not res_repo['to'] == res_repo['total']:
                    res_repo = client.api_call("show-updatable-objects-repository-content",{"limit":500,"offset":res_repo['to']}).data
                    list_repos.append(res_repo['objects'])
                #print(res_repo)
            else:
                # Call Repos containing given string"
                res_repo=client.api_call("show-updatable-objects-repository-content",{"limit":500,"filter":{"text":str(args.filter)}}).data
                while not res_repo['to'] == res_repo['total']:
                    res_repo = client.api_call("show-updatable-objects-repository-content",{"limit":500,"offset":res_repo['to'],"filter":{"text":str(args.filter)}}).data
                    list_repos.append(res_repo['objects']) 
            list=[]
            csvdata=[]
            for s in list_repos:
                for e in s:
                    #list.append(e)
                    csvfields=['Name', 'uid in Repo', 'Description', 'info url', 'URI']
                    try:
                        e['name-in-updatable-objects-repository']
                    except:
                        e['name-in-updatable-objects-repository']='n/a'
                    try:
                        e['uid-in-updatable-objects-repository']
                    except:
                        e['uid-in-updatable-objects-repository']='n/a'
                    try:
                        e['additional-properties']
                    except:
                        e['additional-properties']='n/a'
                    try:
                        e['additional-properties']['description']
                    except:
                        e['additional-properties']['description']='n/a'
                    try:
                        e['additional-properties']['info-url']
                    except:
                        e['additional-properties']['info-url']='n/a'
                    try:
                        e['additional-properties']['uri']
                    except:
                        e['additional-properties']['uri']='n/a'
                    list.append([e['name-in-updatable-objects-repository'],e['uid-in-updatable-objects-repository'],e['additional-properties']['description'],e['additional-properties']['info-url'],e['additional-properties']['uri']])
                    csvdata.append(list)
            with open('result.csv','w') as csvres:
                csvwriter = csv.writer(csvres)
                csvwriter.writerow(csvfields)
                csvwriter.writerows(list)
############################################################################################################################################
if __name__ == "__main__":
    fun_getfromapi()
