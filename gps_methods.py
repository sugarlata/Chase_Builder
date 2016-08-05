import arrow
from xml.etree import ElementTree as Et
from gps_points import GPSPoint


def get_gps_track_list(gps_kml_filename, tz):  # Function to get the GPS KML Filename

    print "Opening Track KML and reading locations"

    # Open the KML file
    # Read the KML with lxml and put data into variable 'track'

    f = open(gps_kml_filename, 'r')
    fr = f.read()
    kml_tree = Et.fromstring(fr)

    track = kml_tree.find(".//{http://www.google.com/kml/ext/2.2}Track")

    gps_points_list = []
    when = []
    locations = []

    # In KML file, there are "When" tags and "Coord" tags.
    # Read line, if 'when tag' put in 'when' list. If 'coord' put in 'coord' list

    for i in range(0, len(track)):

        if track[i].tag[-4:] == "when":
            when.insert(len(when), arrow.get(str(track[i].text).split(' ')[0]).format('X'))
        elif track[i].tag[-5:] == "coord":
            lat, lon, height = float(str(track[i].text).split(' ')[0]), float(
                str(track[i].text).split(' ')[1]), float(
                str(track[i].text).split(' ')[2])

            locations.insert(len(locations), (lat, lon, height))

    print "Completed"

    # If length of when list is different to coords list, then throw an error

    if len(when) != len(locations):
        print "There was an error in your KML file"
        print "Please start again with another KML file"
        exit()

    # Create a GPSPoint object for each point in 'when' and 'coord'. Put this point in a list of points

    for i in range(0, len(when)):
        gps_p = GPSPoint(when[i], locations[i][0], locations[i][1], locations[i][2], tz)
        gps_points_list.insert(len(gps_points_list), gps_p)

    print str(len(gps_points_list)) + " points were successfully imported"
    f.close()
    print "------------------------------------------------------------"

    print ""

    # Calculate the first and last time in the points list.
    # Assuming that the KML file is created in Chronological order, this is the first and last entry.
    # TODO Introduce code that sorts the epochs and finds the first and last to remove this assumption.

    start_time = gps_points_list[0].get_time()
    end_time = gps_points_list[len(gps_points_list) - 1].get_time()
    print "The track starts from ", arrow.get(start_time).to(tz).format('YYYY-MM-DD HH:mm:ss')
    print "and finishes at       ", arrow.get(end_time).to(tz).format('YYYY-MM-DD HH:mm:ss')
    print ""
    print "------------------------------------------------------------"

    # Return the gps points list, as well as the start time and end time

    return gps_points_list, start_time, end_time


def set_gps_kml():
    print ""


def get_distance_from_coordinates(lat1, lon1, lat2, lon2):
    import math

    # Calculate the distance between two gps points
    # This uses the "haversine formula"
    # Taken from the internet
    # Calculates the distance using the big circle

    # Radius of the Earth, in meters
    r = int(6371e3)

    lat1rad = math.radians(lat1)
    lat2rad = math.radians(lat2)

    lat_d_rad = math.radians(lat2 - lat1)
    lon_d_rad = math.radians(lon2 - lon1)

    a = math.sin(lat_d_rad / 2) * math.sin(lat_d_rad / 2) + math.cos(lat1rad) * math.cos(lat2rad) * math.sin(
        lon_d_rad / 2) * math.sin(lon_d_rad / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = round(r * c, 0)

    # Returns the length rounded to 0 decimal places in meters.
    return int(d)
