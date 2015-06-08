import wigile_query
import kml_builder



if __name__ == "__main__":
  wa = wigile_query.WigleAgent('offtest', '83128312')
  final = wa.get_lat_lng('00:22:55:DF:C8:01')
  print final
  kml = kml_builder.kml()
  kml.build(final["lat"], final["lng"], final["bssid"]) #Pass SSID name of network
  print "[*] Check output"
    

