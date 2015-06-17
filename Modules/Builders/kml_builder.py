import simplekml 
from Modules.Common import *


class kml():

  def __init__(self):
    print helpers.color("[*] Started KML", bold=False)

  def build(self, geo_lat, geo_long, ssid, desc_data=""): #Pass SSID name
    #Build the instance
    kml = simplekml.Kml()
    #start the Point data.
    pnt = kml.newpoint(name=ssid, coords=[(geo_lat, geo_long)])  # lon, lat, optional height
    #If you pass description data, place it into the point.
    if desc_data != "":
        pnt.description = desc_data
    kml.save("output2.kml")




    


