import simplekml 
from Modules.Common import *


class kml():

  def __init__(self):
    print "[*] Started KML"

  def build(self, geo_lat, geo_long, ssid, desc_data=""): #Pass SSID name
    #Build the instance
    kml = simplekml.Kml()
    #start the Point data.
    pnt = kml.newpoint(name=ssid, coords=[(geo_lat, geo_long)])  # lon, lat, optional height
    #If you pass description data, place it into the point.
    if desc_data != "":
        pnt.description = desc_data
    #Change the defult icon and make 2x larger
    pnt.style.iconstyle.scale = 2  
    pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/pal3/icon40.png'

    #Save KML
    kml.save("output2.kml")


    


