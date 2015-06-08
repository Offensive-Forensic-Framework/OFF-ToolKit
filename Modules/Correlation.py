from Builders import wigile_query
from Builders import kml_builder


class ClassName():
      #These are the options we will set
    def __init__(self):
      print """
      ---------------------------------------
      Starting Your first dynamic module ever
      ---------------------------------------
      """

    def startx(self):
      wa = wigile_query.WigleAgent('offtest', '83128312')
      final = wa.get_lat_lng('00:22:55:DF:C8:01')
      print final
      kml = kml_builder.kml()
      kml.build(final["lat"], final["lng"], final["bssid"]) #Pass SSID name of network
      print "[*] Check output"
