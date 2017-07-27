from os import path
import json
import ast
from urllib import quote_plus 

import httplib
import base64
import json
import logging as logger
import os
import sys
import StringIO
import requests
from requests.auth import HTTPBasicAuth
from urllib3 import PoolManager



"""
--------------------------------------------------------------------------
Makes a requesto to SDN API to send threats.
--------------------------------------------------------------------------
"""
def perform_action(action, ip):
    print "perform_action"
    pusher = StaticFlowPusher('34.213.70.37')

    flow1 = {
        'switch':"00:00:00:00:00:00:00:11",
        "name":"Blocking Flow1",
        "cookie":"0",
        "priority":"1",
        "in_port":"1",
        "active":"true"
        }
    flow2 = {
        'switch':"00:00:00:00:00:00:00:11",
        "name":"Blocking Flow2",
        "cookie":"0",
        "priority":"1",
        "eth_src":"00:00:00:00:00:00:00:01",
        "active":"true"
        }
    flow3 = {
        'switch':"00:00:00:00:00:00:00:11",
        "name":"Blocking Flow3",
        "cookie":"0",
        "priority":"1",
        "ipv4_src":"10.0.0.1",
        "active":"true"
        }

    investigate1 = {
        'switch':"00:00:00:00:00:00:00:21",
        "name":"Rewrite IP to Honeynet",
        "cookie":"0",
        "priority":"1",
        "in_port":"1",
        "active":"true",
        "eth_type":"0x0800",
        "eth_src":"00:00:00:00:00:02",    #<MAC_OF_10.0.0.2>
        "eth_dst":"00:00:00:00:00:06",    #<MAC_OF_10.0.0.6>
        "ipv4_src":"10.0.0.2",
        "ipv4_dst":"10.0.0.6",
        "actions":"set_field=eth_dst->00:00:00:00:00:04,set_field=ipv4_dst->10.0.0.4,output=2"
    }

    investigate2 = {
        'switch':"00:00:00:00:00:00:00:01",
        "name":"S1 Redirect",
        "cookie":"0",
        "priority":"1",
        "in_port":"2",
        "active":"true",
        "actions":"output=4"
    }

    investigate3 = {
        'switch':"00:00:00:00:00:00:00:01",
        "name":"S1 Redirect 2",
        "cookie":"0",
        "priority":"1",
        "in_port":"4",
        "active":"true",
        "actions":"output=2"
    }
    
    if action=='ToHoneynet':
        result = pusher.set(investigate1)
        result = pusher.set(investigate2)
        result = pusher.set(investigate3)
    elif action =="BlockPort":
        result = pusher.set(flow1)
    elif action =="BlockMac":
        result = pusher.set(flow2)
    elif action == "BlockIp":
        result = pusher.set(flow3)

    print result
 
'''
--------------------------------------------------------------------------------------
When the service is excecuted plugin's action_schema will take some values from the api
--------------------------------------------------------------------------------------
'''
def populateWidget():
    try:
        file_name = "{}/plugin.json".format(path.dirname(path.dirname(__file__)))
        with open(file_name) as json_file:
            data = json.load(json_file)
            data['action_schema']['schema']['properties']['action']['enum'] = []
            data['action_schema']['schema']['properties']['action']['enumNames'] = []

            for values in security_groups():
                data['action_schema']['schema']['properties']['action']['enum'].append(int(values['key']))
                data['action_schema']['schema']['properties']['action']['enumNames'].append(values['value'])
            rewrite_json(file_name, data)
            populateValuesSetupSchema()
            #After populate select input we need to check if there is data stored on MongoDB's plugins collection
    except:
        return "Unable to read the file"


 
class StaticFlowPusher(object):

    def __init__(self, server):
        self.server = server

    def get(self, data):
        ret = self.rest_call({}, 'GET')
        return json.loads(ret[2])

    def set(self, data):
        ret = self.rest_call(data, 'POST')
        return ret[0] == 200

    def remove(self, objtype, data):
        ret = self.rest_call(data, 'DELETE')
        return ret[0] == 200

    def rest_call(self, data, action):
        path = '/wm/staticflowpusher/json'
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json',
            }
        body = json.dumps(data)
        conn = httplib.HTTPConnection(self.server, 8080)
        conn.request(action, path, body, headers)
        response = conn.getresponse()
        ret = (response.status, response.reason, response.read())
        print ret
        conn.close()
        return ret 
 