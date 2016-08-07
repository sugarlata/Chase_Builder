from radar_db import RadarDB
from gui import MainGUI
from gui import TrimGui
import kml_creator as kml_creator
import gps_methods as gps_methods
import radar_methods as radar_methods
import radar_download_frames as radar_download_frames
import media_methods as media_methods
import Tkinter as tk
import time


class MainApplication:

    tb=""
    gps_track_filename = ""
    root_path = ""
    radar_path = ""
    media_path = ""
    gps_track, start_time, end_time = "", "", ""
    radar_db = ""
    radar_set = []
    download_radar_module = False
    frames_db=[]
    tz = "Australia/Melbourne"

    def __init__(self):

        # ---------------------------------- Initialisation ----------------------------------

        self.ffmpeg_location = r"C:\Users\Nathan\Documents\Development\Chaselog\Chaselog\ffmpeg.exe"

        self.download_radar_module_enabled = False
        self.correct_radar_blink_tf = True

    def gui_main(self):

        # ---------------------------------- GUI Initialise ----------------------------------

        root = tk.Tk()
        MainGUI(root, self)
        root.mainloop()

        exit()

    def set_tb(self, tb):
        self.tb = tb

    def gps_load_track(self):

        # Open the KML File

        self.gps_track, self.start_time, self.end_time = gps_methods.get_gps_track_list(self.gps_track_filename, self.tz, self.tb)

    def radar_get_local_idr_list(self):

        # Load Radar Database
        self.radar_db = RadarDB('IDR023')

        # Identify local Radars along the track
        self.radar_set = radar_methods.get_near_idr_list(self.gps_track, self.tb)

    def process_radar(self):
        # If public, skip to make radar list from Files
        # If private, check website for frames and that they are downloaded

        if self.download_radar_module:
            self.frames_db = radar_download_frames.get_online_frames(self.radar_set, self.radar_path, self.start_time, self.end_time, self.root_path, self.tb)
        else:
            self.frames_db = radar_methods.get_local_radar_frames_db(self.radar_set, self.radar_path, self.start_time, self.end_time)

    def correct_blink(self):
        # Correct the radar blink. See declaration for more information
        radar_methods.correct_radar_blink(self.frames_db)

    def create_radar_kml_file(self):

        # Create KML File
        kml_creator.create_radar_kml(self.frames_db, self.root_path, self.radar_path)

    def something_else(self):
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

if __name__ == '__main__':

    main_app = MainApplication()
    main_app.gui_main()


# TODO GUI Module

# TODO Create Proper Icon and convert to base64 encoded with zlib and base64
# TODO Create TZ selector, default can be selected (saved in data file)
# TODO Troubleshoot time code for videos

# TODO Edit Radar Frames to look nicer
# TODO Create a GUI for manually selecting IDR Codes
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
