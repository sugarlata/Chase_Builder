import gps_methods as gps
from radar_db import RadarDB
import radar_methods as radar_methods

# ---------------------------------- Initialisation ----------------------------------

# media_path = r"C:\Users\Nathan\Desktop\16-01-03 Chase log\Media"

# gps_track_filename = r"C:\Users\Nathan\Desktop\16-01-03 Chase log\16-01-03 Echuca Area-trimmed.kml"
gps_track_filename = r"C:\Users\Nathan\Desktop\Chase 16-04-30\Track-trimmed.kml"
root_path = r"C:\Users\Nathan\Desktop\Chase 16-04-30"

radar_path = root_path + r"\Radar"

tz = "Australia/Melbourne"

download_radar_module_enabled = True

# ---------------------------------- GPS ----------------------------------

# Open the KML File
gps_track, start_time, end_time = gps.get_gps_track_list(gps_track_filename,tz)

# Show GUI to get start time and end time

# Create the trimmed KML, update gpsTrack

# ---------------------------------- Radar ----------------------------------

# Load Radar Database
radar_db = RadarDB('IDR023')

# Identify local Radars along the track
radar_set = radar_methods.get_near_idr_list(gps_track, tz)

# If public, skip to make radar list from Files
# If private, check website for frames and that they are downloaded

if download_radar_module_enabled:
    radar_methods.get_online_frames(radar_set, radar_path,start_time,end_time,root_path,tz)

# Create KML File


# ---------------------------------- Media ----------------------------------

# Check that the media path exists

# GUI Ask about downloading place names

# If it doesn't exit()?

# Get Photo List

# Get Photo Exif Data (time taken)

# Create db of pictures and the time taken

# Set the time for leftover photos manually

# Set the location for each picture

# Resize photos as necessary

# Group Photos together


# Get video list

# Get time from filename

# Create db of video and the time taken

# Set the time for leftover videos

# Set the location for each video

# Group Videos as necessary


# Get Timelapse List

# Get time from Timelapse

# Create the video

# Create db of videos and the time they were taken

# Set the time for leftover videos

# Set the location for each video

# Group videos as necessary

# Create the Media KML



##TODO
##TODO RADAR Module (Public)
##TODO RADAR Module (Private)
##TODO Media Module
##TODO GUI Module