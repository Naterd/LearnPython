#!/usr/bin/env python
# pylint: disable=E0611
# Requires Nitro PYTHON API, Download from the download section in the VPX GUI
# Query and print status of all vservers
# Written by Nate Stewart. Date: 08/17/17

import argparse
import urllib3
from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver import lbvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver import csvserver

PARSER = argparse.ArgumentParser(description='Query netscaler for status of VIPS')
PARSER.add_argument('--netscaler', dest='netscaler', type=str, required=True,
                    help='ip or dns entry of netscaler')
PARSER.add_argument('--username', dest='username', type=str, required=True,
                    help='api user')
PARSER.add_argument('--password', dest='password', type=str, required=True,
                    help='password..duh?')
ARGS = PARSER.parse_args()

# Disable warnings about unverified HTTPS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# login to netscaler
NS_SESSION = nitro_service(ARGS.netscaler, 'https')
NS_SESSION.certvalidation = False
NS_SESSION.hostnameverification = False
NS_SESSION.login(ARGS.username, ARGS.password, 3600)

# Find all virtual servers
LBRESULT = lbvserver.get(NS_SESSION)
CSRESULT = csvserver.get(NS_SESSION)
for vserver in LBRESULT:
    print vserver.name, 'is', vserver.curstate

for vserver in CSRESULT:
    print vserver.name, 'is', vserver.curstate

NS_SESSION.logout()
