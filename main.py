import gps_methods as gps

mediaPath = r"C:\Users\Nathan\Desktop\16-01-03 Chase log\Media"
gpsTrackFN = r"C:\Users\Nathan\Desktop\16-01-03 Chase log\16-01-03 Echuca Area-trimmed.kml"
tz = "Australia/Melbourne"

gpsTrack = gps.getGPSKML(gpsTrackFN,tz)

print gpsTrack[0].getLocation()



##TODO
##TODO RADAR Module (Public)
##TODO RADAR Module (Private)
##TODO Media Module
##TODO GUI Module