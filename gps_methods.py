import arrow
from xml.etree import ElementTree as et
from gps_points import GPSPoint

def getGPSKML(gpsKMLfn, tz):  # Function to get the GPS KML Filename

    f = open(gpsKMLfn, 'r')
    fr = f.read()
    kmlTree = et.fromstring(fr)

    track = kmlTree.find(".//{http://www.google.com/kml/ext/2.2}Track")

    gpsPointsList = []
    when = []
    locations = []

    for i in range(0, len(track)):

        if track[i].tag[-4:] == "when":
            when.insert(len(when), arrow.get(str(track[i].text).split(' ')[0]).format('X'))
        elif track[i].tag[-5:] == "coord":
            lat, lon, height = float(str(track[i].text).split(' ')[0]), float(
                str(track[i].text).split(' ')[1]), float(
                str(track[i].text).split(' ')[2])

            locations.insert(len(locations), (lat, lon, height))

    print "Completed"

    if len(when) != len(locations):
        print "There was an error in your KML file"
        print "Please start again with another KML file"
        exit()

    for i in range(0, len(when)):
        gpsP = GPSPoint(when[i], locations[i][0], locations[i][1], locations[i][2], tz)
        gpsPointsList.insert(len(gpsPointsList), gpsP)

    print str(len(gpsPointsList)) + " points were successfully imported"
    f.close()
    print "------------------------------------------------------------"

    print ""
    startTime = gpsPointsList[0].getLocalTime()
    endTime = gpsPointsList[len(gpsPointsList) - 1].getLocalTime()
    print "The track starts from ", arrow.get(startTime)
    print "and finishes at       ", arrow.get(endTime)
    print ""
    return gpsPointsList
