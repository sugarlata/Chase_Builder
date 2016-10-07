import arrow
from xml.etree import ElementTree as Et
from gps_points import GPSPoint


def get_gps_track_list(gps_kml_filename, tz, tb):  # Function to get the GPS KML Filename

    tb.tb_update("Opening Track KML and reading locations")

    # Open the KML file
    # Read the KML with lxml and put data into variable 'track'

    f = open(gps_kml_filename, 'r')
    fr = f.read()

    try:
        kml_tree = Et.fromstring(fr)
    except Et.ParseError:
        raise ImportError("There was an error importing the track kml file")

    track = kml_tree.find(".//{http://www.google.com/kml/ext/2.2}Track")

    gps_points_list = []
    when = []
    locations = []

    # In KML file, there are "When" tags and "Coord" tags.
    # Read line, if 'when tag' put in 'when' list. If 'coord' put in 'coord' list

    # mid calculates how many updates to send to the user. 42 is suggested here, being the meaning of life.

    mid = (len(track))/42

    for i in range(0, len(track)):

        # Update user on what percentage of the file has bee read, at selected intervals.
        try:
            if round(float(i)/float(mid), 0) == float(i)/float(mid):
                tb.tb_update(str(round(100*float(i)/float(len(track)), 2)) + "%")
        except ZeroDivisionError:
            tb.tb_update("")

        if track[i].tag[-4:] == "when":
            when.insert(len(when), arrow.get(str(track[i].text).split(' ')[0]).format('X'))
        elif track[i].tag[-5:] == "coord":
            lat, lon, height = float(str(track[i].text).split(' ')[0]), float(
                str(track[i].text).split(' ')[1]), float(
                str(track[i].text).split(' ')[2])

            locations.insert(len(locations), (lat, lon, height))

    # Update the User
    tb.tb_update("")
    tb.tb_update("Completed")
    tb.tb_update("")

    # If length of when list is different to coords list, then throw an error

    if len(when) != len(locations):
        tb.tb_update("There was an error in your KML file")
        tb.tb_update("Please start again with another KML file")
        exit()

    # Create a GPSPoint object for each point in 'when' and 'coord'. Put this point in a list of points

    tb.tb_update("")
    tb.tb_update("Processing Points")
    tb.tb_update("Please Wait")
    tb.tb_update("")

    for i in range(0, len(when)):
        # Create GPSPoint Object based on time, location (lat, lon, height) and put in the timezone
        gps_p = GPSPoint(when[i], locations[i][0], locations[i][1], locations[i][2], tz)

        # Put the created object in a list
        gps_points_list.insert(len(gps_points_list), gps_p)

    # Update the User
    tb.tb_update(str(len(gps_points_list)) + " points were successfully imported")

    # If too few points loaded, throw error
    if len(gps_points_list) < 3:
        raise ValueError("Too few points in file")

    # Close the file
    f.close()
    tb.tb_update("------------------------------------------------------------")
    tb.tb_update("")

    # Calculate the first and last time in the points list.
    # Assuming that the KML file is created in Chronological order, this is the first and last entry.
    # TODO Introduce code that sorts the epochs and finds the first and last to remove this assumption.

    # First GPS Point
    start_time = gps_points_list[0].get_time()

    # Last GPS Point
    end_time = gps_points_list[len(gps_points_list) - 1].get_time()

    # Update User
    tb.tb_update("The track starts from " + arrow.get(start_time).to(tz).format('YYYY-MM-DD HH:mm:ss'))
    tb.tb_update("and finishes at       " + arrow.get(end_time).to(tz).format('YYYY-MM-DD HH:mm:ss'))
    tb.tb_update("")
    tb.tb_update("------------------------------------------------------------")

    # Return the gps points list, as well as the start time and end time
    return gps_points_list, start_time, end_time


def set_gps_kml():
    pass


def get_distance_from_coordinates(lat1, lon1, lat2, lon2):
    import math

    # Calculate the distance between two gps points
    # This uses the "haversine formula"
    # Taken from the internet
    # Calculates the distance using the big circle equation

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
