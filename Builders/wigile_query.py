from uuid import getnode
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
        if mac_address == None:
            mac_address = self.mac_address
        if '-' in mac_address:
            mac_address = mac_address.replace('-', ':')
        try:
            self.query_response = self.send_query(mac_address)
            response = self.parse_response()
        except IndexError:
            response = 'MAC location not known'
        return response
        
    def agent(self, username, password):
        proxies = {"http": "http://127.0.0.1:8080"}
        self.agent = requests.Session()
        r = self.agent.get('https://wigle.net/api/v1/jsonLogin', proxies=proxies)
        print r
        self.agent.post('https://wigle.net/api/v1/jsonLogin',
                   data={'credential_0': username,
                         'credential_1': password,
                         'destination': '/https://wigle.net/'}, proxies=proxies)
        
    def mac_address(self):
        mac = hex(getnode())
        mac_bytes = [mac[x:x+2] for x in xrange(0, len(mac), 2)]
        self.mac_address = ':'.join(mac_bytes[1:6])    
    
    def send_query(self, mac_address):
        proxies = {"http": "http://127.0.0.1:8080"}
        response = self.agent.post(url='https://wigle.net/api/v1/jsonLocation', 
                       data={'netid': mac_address,
                             'Query2': 'Query'}, proxies=proxies,)
        print response.json()
        print "\n"
        return response.json()
    
    def parse_response(self):
        lat = self.get_lat()
        lng = self.get_lng()
        bssid = self.get_ssid()
        return lat, lng, bssid
    
    def get_lat(self):
        resp_lat = self.query_response['result'][0]['locationData'][0]['latitude']
        return float(resp_lat)
    
    def get_lng(self):
        resp_lng = self.query_response['result'][0]['locationData'][0]['longitude']
        return float(resp_lng)

    def get_ssid(self):
        resp_ssid = self.query_response['result'][0]['locationData'][0]['ssid']
        return str(resp_ssid)

if __name__ == "__main__":

    wa = WigleAgent('offtest', '83128312')
    final = str(wa.get_lat_lng('00:22:55:DF:C8:01'))
    print "Our Cords are: " + final
