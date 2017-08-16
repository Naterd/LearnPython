#!/usr/bin/env python
# pylint: disable=E0611
# Requires Nitro PYTHON API
# Download from the download section in the VPX GUI
# Query and print all SSL vserver cipher suite configurations
# Written by Nate Stewart. Date: 07/25/17

import argparse
import urllib3
from nssrc.com.citrix.netscaler.nitro.service.nitro_service import nitro_service
from nssrc.com.citrix.netscaler.nitro.resource.config.lb.lbvserver import lbvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.cs.csvserver import csvserver
from nssrc.com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslciphersuite_binding import sslvserver_sslciphersuite_binding

PARSER = argparse.ArgumentParser(description='Query netscaler for all SSL VIPS')
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
NS_SESSION = nitro_service(ARGS.netscaler, "https")
NS_SESSION.certvalidation = False
NS_SESSION.hostnameverification = False
NS_SESSION.login(ARGS.username, ARGS.password, 3600)


# Find all SSL virtual servers for load balancing and content switching
LBRESULT = lbvserver.get_filtered(NS_SESSION, "servicetype:SSL")
CSRESULT = csvserver.get_filtered(NS_SESSION, "servicetype:SSL")
for vserver in LBRESULT:
    print vserver.name
    # query ciphers for each vserver
    CIPHERS = sslvserver_sslciphersuite_binding.get(NS_SESSION, vserver.name)
    for cipher in CIPHERS:
        print cipher.ciphername
    print
for vserver in CSRESULT:
    print vserver.name
    # query ciphers for each vserver
    CIPHERS = sslvserver_sslciphersuite_binding.get(NS_SESSION, vserver.name)
    for cipher in CIPHERS:
        print cipher.ciphername
    print
NS_SESSION.logout()
