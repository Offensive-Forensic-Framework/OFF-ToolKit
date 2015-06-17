from uuid import getnode
from Modules.Common import *
import sys
import re
import requests
import json

#Inspired and stolen from Jamie Bull (author).. at http://code.activestate.com/recipes/578637-wigle-wifi-geolocation/


class WigleAgent():
      #These are the options we will set
    def __init__(self, username, password):
        self.agent(username, password)
        self.mac_address()
        # required options
        self.description = "simple WIGLE query"
        self.language = "python"

        # options we require user interaction for- format is {Option : [Value, Description]]}
        self.required_options = {"wigle_user" : ["offtest", "Set WIGLE User-Name"],
                                 "wigle_pass" : ["83128312", "Set WIGLE Password"],
                                 "mac" : ["00:22:55:DF:C8:01", "Set MAC Address"]}    

    def get_lat_lng(self, mac_address=None):
        #Start with Credintial check
        try:
            self.response = send_user_check()
            response = self.check_cred_login()
            if response == 'false':
                print "[*] Unable to validate this user..."
        except:
            #Use this two let user know we had a true login..
            print helpers.color('[*] WIGLE: This user was validated', bold=False)
            pass
        if mac_address == None:
            mac_address = self.mac_address
        if '-' in mac_address:
            mac_address = mac_address.replace('-', ':')
        try:
            self.query_response = self.send_query(mac_address)
            #Need to use Try statment since the "message" Key isnt always prsent when conducting query
            try:
                message = self.check_query_limit()
                if message == "too many queries":
                    print "[*]" + message
            except:
                #Use pass since we dont have an error...
                pass
            response = self.parse_response()
        except IndexError:
            response = 'BSSID (MAC) location not known'
            return response
        print helpers.color('[*] WIGLE: Lat / Long and SSID have been retrived', bold=False)
        return response
        
    def agent(self, username, password):
        self.agent = requests.Session()
        self.agent.post('https://wigle.net/api/v1/jsonLogin',
                   data={'credential_0': username,
                         'credential_1': password,
                         'destination': '/https://wigle.net/'})
        
    def mac_address(self):
        mac = hex(getnode())
        mac_bytes = [mac[x:x+2] for x in xrange(0, len(mac), 2)]
        self.mac_address = ':'.join(mac_bytes[1:6])    
    
    def send_query(self, mac_address):
        response = self.agent.post(url='https://wigle.net/api/v1/jsonLocation', 
                       data={'netid': mac_address,
                             'Query2': 'Query'})
        #Check for and handle JSON Errors, due to blank returns
        try: 
            return response.json()
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print helpers.color('[*] WIGLE: Decoding JSON has failed', bold=False, warning=True)
            print helpers.color('[!] Exiting...', bold=True, warning=True)
            sys.exit()
    
    def send_user_check(self):
        response = self.agent.post()
        return response.json()
    
    def parse_response(self):
        lat = self.get_lat()
        lng = self.get_lng()
        bssid = self.get_ssid()
        string = str(self.query_response)
        return {'lat':lat,'lng':lng, 'bssid':bssid, 'description':string}

    def get_lat(self):
        resp_lat = self.query_response['result'][0]['trilat']
        return float(resp_lat)
    
    def get_lng(self):
        resp_lng = self.query_response['result'][0]['trilong']

        return float(resp_lng)
    #Request the SSID name of the WIFI point
    def get_ssid(self):
        resp_ssid = self.query_response['result'][0]['ssid']
        return str(resp_ssid)
    #Check to see if we reached our limit of 100 querys
    def check_query_limit(self):
        resp_message = self.query_response['message']
        return str(resp_message)
    #Check User loign creds
    def check_cred_login(self):
        resp_message = self.query_response['success']
        return str(resp_message)
