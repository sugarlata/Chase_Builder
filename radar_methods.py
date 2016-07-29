import gps_methods as gps_methods
from radar_db import RadarDB
from radar_overlays import RadarFrame
import urllib2
import arrow
import os


# Function to return nearest IDRs according to gps_track
def get_near_idr_list(gps_track, tz):

        # Create list of IDR Codes to match up and see how far away they are.

        radar_working_list = ['IDR773', 'IDR093', 'IDR633', 'IDR783', 'IDR423', 'IDR073', 'IDR413', 'IDR363', 'IDR193', 'IDR173',
                    'IDR393', 'IDR733', 'IDR243', 'IDR163', 'IDR153', 'IDR753', 'IDR223', 'IDR293', 'IDR563', 'IDR723',
                    'IDR253', 'IDR233', 'IDR053', 'IDR443', 'IDR083', 'IDR673', 'IDR503', 'IDR663', 'IDR063', 'IDR623',
                    'IDR533', 'IDR283', 'IDR483', 'IDR693', 'IDR273', 'IDR333', 'IDR703', 'IDR043', 'IDR713', 'IDR323',
                    'IDR303', 'IDR033', 'IDR643', 'IDR313', 'IDR553', 'IDR463', 'IDR403', 'IDR493', 'IDR143', 'IDR023',
                    'IDR683', 'IDR523', 'IDR763']

        # Create lists for suggestions of Radars
        radar64suggests = []
        radar128suggests = []
        radar256suggests = []

        # Cycle through the list of points, calculate the distance from the point to the radar
        # If more that 2500kms get rid of the Radar (unlikely to be close to an point by the end of the day)
        # If it's less than 256kms, add the IDRCode to the 256km suggestions and remove it from
        # the radar working list

        # Create RadarDB object to put in codes and return locations
        radar_db = RadarDB('IDR023')

        for i in range(0,len(gps_track)):
            # Iterate through GPS Points
            lat1 = gps_track[i].get_location()[1]
            lon1 = gps_track[i].get_location()[0]
            k = 0

            for j in range(0, len(radar_working_list)):
                # Iterate through IDRs
                lat2 = radar_db.get_location(radar_working_list[j-k])[0]
                lon2 = radar_db.get_location(radar_working_list[j-k])[1]

                distance = int(gps_methods.get_distance_from_coordinates(lat1,lon1,lat2,lon2))/1000

                if distance < 362:  # sqrt(2)*max distance which is 256kms. This allows for corners of the radar
                    radar256suggests.insert(len(radar256suggests), radar_working_list[j - k])
                    radar_working_list.remove(radar_working_list[j - k])
                    k += 1
                elif distance > 2500:
                
                    radar_working_list.remove(radar_working_list[j - k])
                    k += 1

        # Working list is now the 256 suggests. If there is a positive 256km radar,
        # it will also be positive for 256km

        radar_working_list = list(radar256suggests)

        # Iterate through working list for 128km suggestions

        for i in range(0, len(gps_track)):
            # Iterate through GPS Points
            lat1 = gps_track[i].get_location()[1]
            lon1 = gps_track[i].get_location()[0]
            k = 0

            for j in range(0, len(radar_working_list)):
                # Iterate through IDRs
                lat2 = radar_db.get_location(radar_working_list[j - k])[0]
                lon2 = radar_db.get_location(radar_working_list[j - k])[1]

                distance = int(gps_methods.get_distance_from_coordinates(lat1, lon1, lat2, lon2)) / 1000

                if distance < 181:  # sqrt(2)*max distance which is 256kms. This allows for corners of the radar
                    radar128suggests.insert(len(radar128suggests), radar_working_list[j - k])
                    radar_working_list.remove(radar_working_list[j - k])
                    k += 1

        # Same again, iterate for 64kms

        radar_working_list = list(radar128suggests)

        for i in range(0, len(gps_track)):
            # Iterate through GPS Points
            lat1 = gps_track[i].get_location()[1]
            lon1 = gps_track[i].get_location()[0]
            k = 0

            for j in range(0, len(radar_working_list)):
                # Iterate through IDRs
                lat2 = radar_db.get_location(radar_working_list[j - k])[0]
                lon2 = radar_db.get_location(radar_working_list[j - k])[1]

                distance = int(gps_methods.get_distance_from_coordinates(lat1, lon1, lat2, lon2)) / 1000

                if distance < 91:  # sqrt(2)*max distance which is 256kms. This allows for corners of the radar
                    radar64suggests.insert(len(radar64suggests), radar_working_list[j - k])
                    radar_working_list.remove(radar_working_list[j - k])
                    k += 1

        radar_set = []

        # Check to make sure that the radars exist (64km)
        if len(radar64suggests) != 0:

            for i in range(0, len(radar64suggests)):
                if radar_db.get_64(radar64suggests[i]):
                    radar_rh = radar64suggests[i][:-1] + "4"
                    radar_set.insert(len(radar_set), radar_rh)

        # Same for 128km (both rain rate and doppler wind)
        if len(radar128suggests) != 0:
            for i in range(0, len(radar128suggests)):
                if radar_db.get_128(radar128suggests[i]):
                    radar_rh = radar128suggests[i][:-1] + "3"
                    radar_set.insert(len(radar_set), radar_rh)
                if radar_db.get_doppler(radar128suggests[i]):
                    radar_rh = radar128suggests[i][:-1] + "I"
                    radar_set.insert(len(radar_set), radar_rh)

        # Same for 256km
        if len(radar256suggests) != 0:
            for i in range(0, len(radar256suggests)):
                if radar_db.get_256(radar256suggests[i]):
                    radar_rh = radar256suggests[i][:-1] + "2"
                    radar_set.insert(len(radar_set), radar_rh)

        return radar_set


def get_online_frames(idr_codes, radar_path, start_gps_time, end_gps_time,root_path,tz):  # Function to Download radar frames according to Selected IDRs

    user_agent = "chase-builder/1.0"

    url_list = []

    radar_set = idr_codes
    radar_db = RadarDB('IDR023')

    print ""
    print ""
    print "------------------------------------------------------------"
    print "Checking radar frames from the following addresses:"
    print ""

    # Iterate through the Radar set (of nearest radar locations) and create a URL
    # for the timeframe required. Put in url_list

    if len(radar_set) != 0:
        radar_set.sort()

        # Get the start time and end time, put in the format that will be used for the url
        a = arrow.get(start_gps_time)
        url_start_time = str(a.year) + "-" + str(a.month) + "-" + str(a.day) + "-" + str(a.hour)
        # Add an extra hour to the finish time, make sure that it download frames to the end of that hour.
        # The below code concatenates the minute and uses the hour
        z = arrow.get(int(end_gps_time) + 60*60)
        url_end_time = str(z.year) + "-" + str(z.month) + "-" + str(z.day) + "-" + str(z.hour)

        for i in range(0, len(radar_set)):

            url_idr = radar_set[i]

            if url_idr[-1:] == "I":
                code = "128km Wind"
            elif url_idr[-1:] == "2":
                code = "256km"
            elif url_idr[-1:] == "3":
                code = "128km"
            elif url_idr[-1:] == "4":
                code = "64km"

            # Create the URL Address
            url_address = url_idr, r"http://www.theweatherchaser.com/radar-loop/" + str(url_idr) + r"/" + str(
                url_start_time) + r"/" + url_end_time, radar_db.get_title(url_idr[:-1] + "3"), code

            # Print the addresses for the radar to view on the website if desired
            print url_address[0], url_address[1], url_address[2], url_address[3]
            url_list.insert(len(url_list), url_address)

        print ""
        print "------------------------------------------------------------"

    else:

        print "There were no radar images that covered your track"


    # Now to check whether there is a folder for each of the IDR Codes. If not create one
    # Open the folder, load the web page source and create a file list
    # Check the file list for files required
    # Download any needed files

    full_frame_db = []
    frame_db = []

    # Iterate through all url addresses in url_list
    for i in range(0, len(url_list)):

        root_radar = root_path + r"\Radar"

        # Check if the Radar folder exists
        if os.path.isdir(root_radar) == False:
            os.chdir(root_path)
            os.mkdir("radar")

        radar_path = root_radar + "\\" + url_list[i][0]

        # Check if the IDR Code folder exists inside the Radar Folder
        if os.path.isdir(radar_path) == False:
            os.chdir(root_radar)
            os.mkdir(url_list[i][0])

        # Print which IDR is being downloaded
        print "Downloading " + url_list[i][2] + " " + url_list[i][3] + " Frames (" + str(i + 1) + "/" + str(
            len(url_list)) + ")"

        # Now need to get the list of frames for that IDR and timeframe

        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', user_agent)]
        response = opener.open(url_list[i][1])
        page_line = response.readline()
        radar_frames = []

        # Get the list of frames and create list with frame objects in it

        while True:
            if "var image_data = " in page_line:
                frame = page_line.lstrip().rstrip()[19:-2].split(',')[0], page_line.lstrip().rstrip()[19:-2].split(',')[
                                                                         1].lstrip()[1:-1]
                temp_weather_frame = RadarFrame(frame[0],frame[1])
                radar_frames.insert(len(radar_frames), temp_weather_frame)
                break

            page_line = response.readline()

        while True:

            page_line = response.readline()
            if """;""" in page_line:
                break
            else:
                frame = page_line.lstrip().rstrip()[1:-1].split(',')[0], page_line.lstrip().rstrip()[1:-1].split(',')[1].lstrip()[1:-1]
                temp_weather_frame = RadarFrame(frame[0], frame[1])
                radar_frames.insert(len(radar_frames), temp_weather_frame)

        frame
        os.chdir(radar_path)

        temp_frame = []
        for j in range(0, len(radar_frames)):
            print str(round(100 * j / float(len(radar_frames)), 1)) + "%"
            frame_filename = radar_frames[j].get_filename().split('/')[-1]
            frame_full_filename = radar_path + "\\" + frame_filename
            if os.path.isfile(frame_full_filename) == False:

                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', user_agent)]
                f = opener.open(radar_frames[j].get_filename())
                data = f.read()
                with open(frame_filename, "wb") as code:
                    code.write(data)

            temp_frame.insert(len(temp_frame), frame_filename)
            if j == len(radar_frames) - 1:
                full_frame_db.insert(len(full_frame_db), temp_frame)

        print "Completed"
        print ""

    print "------------------------------------------------------------"
    print full_frame_db
    return full_frame_db
