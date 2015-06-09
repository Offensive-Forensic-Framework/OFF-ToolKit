from Builders import wigile_query
from Builders import kml_builder


class ClassName():
      #These are the options we will set
    def __init__(self):
      # required options
      self.name = "Registry Network info corelation"
      self.description = "WIGLE Query your known BSSID"
      self.language = "python"
      self.extension = "py"
      self.rating = "Excellent"    
        
      # options we require user interaction for- format is {Option : [Value, Description]]}
      self.required_options = {"bssid" : ['00:22:55:DF:C8:01', "Set BSSID or MAC of AP"],
                               "user" : ['offtest', "Set Username to WIGLE"],
                               "pass" : ['83128312', "Set Password to WIGLE"]}

    def startx(self):
      wa = wigile_query.WigleAgent(self.required_options["user"][0], self.required_options["pass"][0])
      final = wa.get_lat_lng(self.required_options["bssid"][0])
      print final
      kml = kml_builder.kml()
      kml.build(final["lat"], final["lng"], final["bssid"]) #Pass SSID name of network
      print "[*] Check output"
