from radar_db import RadarDB
import kml_creator as kml_creator
import gps_methods as gps
import radar_methods as radar_methods
import radar_download_frames as radar_download_frames
import media_methods as media_methods


# ---------------------------------- Initialisation ----------------------------------

#gps_track_filename = r"C:\Users\Nathan\Desktop\16-01-03 Chase log\16-01-03 Echuca Area-trimmed.kml"
#root_path = r"C:\Users\Nathan\Desktop\16-01-03 Chase log"

gps_track_filename = r"C:\Users\Nathan\Desktop\15-10-31 Chase Log\15-10-31 Chase Track-trimmed.kml"
root_path = r"C:\Users\Nathan\Desktop\15-10-31 Chase Log"

#gps_track_filename = r"C:\Users\Nathan\Desktop\Chase 16-04-30\Track-trimmed.kml"
#root_path = r"C:\Users\Nathan\Desktop\Chase 16-04-30"

radar_path = root_path + r"\Radar"
media_path = root_path + r"\Media"

tz = "Australia/Melbourne"

ffmpeg_location = r"C:\Users\Nathan\Documents\Development\Chaselog\Chaselog\ffmpeg.exe"

download_radar_module_enabled = True

# ---------------------------------- GPS ----------------------------------

# Open the KML File
gps_track, start_time, end_time = gps.get_gps_track_list(gps_track_filename,tz)

# Show GUI to get start time and end time

# Create the trimmed KML, update gpsTrack

# ---------------------------------- Radar ----------------------------------

# # Load Radar Database
# radar_db = RadarDB('IDR023')
#
# # Identify local Radars along the track
# radar_set = radar_methods.get_near_idr_list(gps_track, tz)
#
# # If public, skip to make radar list from Files
# # If private, check website for frames and that they are downloaded
#
# if download_radar_module_enabled:
#     frames_db = radar_download_frames.get_online_frames(radar_set, radar_path,start_time,end_time,root_path,tz)
#
# # Create KML File
# kml_creator.create_radar_kml(frames_db, root_path, radar_path,tz)

# ---------------------------------- Media ----------------------------------

# Check that the media path exists
if media_methods.check_media_path_exists(media_path):
    media_methods.process_media(root_path, media_path, ffmpeg_location, gps_track, start_time, end_time, tz)
else:
    print "------------------------------------------------------------"
    print ""
    print "No Media found for this chase"
    print ""
    print "------------------------------------------------------------"


# TODO Troubleshoot why Radar location isn't centered on locations properly
# TODO Photos and Video, and Timelapse, instead of using filenames use address
# TODO RADAR Module (Public)
# TODO GUI Module
# TODO Change names in KML file for Radar to common names

# TODO Create TZ selector, default can be selected (saved in data file)
# TODO Troubleshoot time code for videos

# TODO Create a GUI for dwell time
# TODO Change pictures for car (troubleshooting, different kml)
# TODO Build GUI to house everything
# TODO Find a module to put stdout in a scrollbox in GUI
# TODO Implement shortlister for pictures
# TODO Implement GUI to select ffmpeg. Include error handling
# TODO Create an EXE using nuitka

# TODO Implement error handling if no track file is selected
# TODO Write code for selecting IDRCodes
# TODO Write code for WorkingOffline
# TODO Implement a version of the code for online use that manually downloads radar

# TODO Implement gpx support
# TODO Create module to dissect a location history KML downloaded from Google
