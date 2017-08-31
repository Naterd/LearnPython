#!/usr/bin/env python
# pylint: disable=E0611,E1101,c0111
# requires pycurl
# to generate rundeck api token, navigate to your user profile in rundeck and click generate new token
# List all GUIDs for rundeck jobs
# Written by Nate Stewart. Date: 08/30/17

import json
import argparse
from StringIO import StringIO
import pycurl

PARSER = argparse.ArgumentParser(
    description='Query rundeck api for the global unique identifier of each job')
PARSER.add_argument('--apitoken', dest='token', type=str, required=True,
                    help='rundeck api token')
ARGS = PARSER.parse_args()

MYTOKEN = ARGS.token

def queryapi(url, token):
    response = StringIO()
    curl = pycurl.Curl()
    curl.setopt(curl.URL, url)
    curl.setopt(curl.HTTPHEADER, [
        "X-Rundeck-Auth-Token: "+ token, 'Accept: application/json'])
    curl.setopt(curl.WRITEDATA, response)
    curl.perform()
    curl.close()

    body = response.getvalue()
    bodyjson = json.loads(body)
    return bodyjson

RUNDECKURL = 'https://switchyard01.xactware.com/rundeck/api/1/projects'
PROJECTS = queryapi(RUNDECKURL, MYTOKEN)

for project in PROJECTS:
    print project['name']
    print '====================='
    JOBS = queryapi(('https://switchyard01.xactware.com/rundeck/api/14/project/{0}/jobs').format(project['name']), MYTOKEN)
    for job in JOBS:
        print 'JOB: {i[name]:55} GUID: {i[id]:36}'.format(i=job)
    print
