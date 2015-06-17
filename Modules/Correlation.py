from Builders import wigile_query
from Builders import kml_builder
from xml.dom import minidom


class ClassName():
      #These are the options we will set
    def __init__(self):
      # Descriptions that are required!!!
      self.name = "Registry Network info corelation"
      self.description = "WIGLE Query your known BSSID"
      self.language = "python"
      self.extension = "py"
      self.rating = "Excellent"    
        
      # options we require user interaction for- format is {Option : [Value, Description]]}
      self.required_options = {"data" : ['xm1.xml', "File to import SSID and BSSID"],
                               "user" : ['offtest', "Set Username to WIGLE"],
                               "pass" : ['83128312', "Set Password to WIGLE"]}

    def startx(self): 
      xmldoc = minidom.parse('/root/Desktop/Tools/OFF-ToolKit/Modules/xm1.xml')
      itemlist = xmldoc.getElementsByTagName('id') 
      #print "Len : ", len(itemlist)
      #print "Attribute Name : ", itemlist[0].attributes['name'].value
      #print "Text : ", itemlist[0].firstChild.nodeValue
      for s in itemlist :
        try:
          attr = s.attributes['name'].value
          val = s.firstChild.nodeValue
          if attr == "FirstNetwork":
            ssid = val
          if attr == "DefaultGatewayMac":
            bssid = val
        except:
          pass
    
      wa = wigile_query.WigleAgent(self.required_options["user"][0], self.required_options["pass"][0])
      final = wa.get_lat_lng(bssid) #self.required_options["bssid"][0]
      kml = kml_builder.kml()
      point_data = kml.build(final["lat"], final["lng"], final["bssid"], final["description"]) #Pass SSID name of network
      print "[*] Check output"

      
