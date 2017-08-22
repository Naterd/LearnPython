#!/usr/bin/env python
# pylint: disable=E0611
# Requires Nitro PYTHON API, Download from the download section in the VPX GUI
# Query and print high availability status for sdx appliances
# Written by Nate Stewart. Date: 08/22/17

import argparse
import urllib3
from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service
from nssrc.com.citrix.netscaler.nitro.resource.config.ha.hanode import hanode

PARSER = argparse.ArgumentParser(
    description='Query high availability status of netscaler sdx appliances')
PARSER.add_argument('--username', dest='username', type=str, required=True,
                    help='api user')
PARSER.add_argument('--password', dest='password', type=str, required=True,
                    help='password..duh?')
ARGS = PARSER.parse_args()

# Disable warnings about unverified HTTPS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SDX01IPS = '####IP ADDRESSES####'
SDX02IPS = '####IP ADDRESSES####'

# login to each netscaler
print 'Lehi SDX 01 High Availability Status'
print
for ip in SDX01IPS:
    NS_SESSION = nitro_service(ip, 'https')
    NS_SESSION.certvalidation = False
    NS_SESSION.hostnameverification = False
    NS_SESSION.login(ARGS.username, ARGS.password, 3600)
    HASTATUS = hanode.get_filtered(NS_SESSION, 'id:0')
    info = {'name': HASTATUS[0].name, 'ip': HASTATUS[0].ipaddress, 'status':
            HASTATUS[0].hastatus, 'state': HASTATUS[0].state}
    print '{i[name]:20} IP: {i[ip]:15} STATUS: {i[status]:14} STATE: {i[state]}'.format(i=info)

    NS_SESSION.logout()

print
print 'Lehi SDX 02 High Availability Status'
print
for ip in SDX02IPS:
    NS_SESSION = nitro_service(ip, 'https')
    NS_SESSION.certvalidation = False
    NS_SESSION.hostnameverification = False
    NS_SESSION.login(ARGS.username, ARGS.password, 3600)
    HASTATUS = hanode.get_filtered(NS_SESSION, 'id:0')
    info = {'name': HASTATUS[0].name, 'ip': HASTATUS[0].ipaddress, 'status':
            HASTATUS[0].hastatus, 'state': HASTATUS[0].state}
    print '{i[name]:20} IP: {i[ip]:15} STATUS: {i[status]:14} STATE: {i[state]}'.format(i=info)

    NS_SESSION.logout()
