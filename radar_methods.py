import gps_methods as gps_methods
from radar_db import RadarDB


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


