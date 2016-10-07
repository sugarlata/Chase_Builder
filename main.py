from radar_db import RadarDB
from gui import MainGUI
import kml_creator as kml_creator
import gps_methods as gps_methods
import radar_methods as radar_methods
import radar_download_frames as radar_download_frames
import media_methods as media_methods
import Tkinter as Tk
import sys


class MainApplication:

    # Initial variables
    tb = ""
    gps_track_filename = ""
    root_path = ""
    radar_path = ""
    media_path = ""
    gps_track, start_time, end_time = "", "", ""
    radar_db = ""
    radar_set = []
    download_radar_module = False
    frames_db = []
    tz = "Australia/Melbourne"
    dl_place_names = False
    photo_len = ""
    video_len = ""
    time_len = ""
    photo_filename_list = []
    video_filename_list = []
    time_filename_list = []
    photo_list = []
    rejected_photos_filename_list = []
    rejected_video_filename_list = []
    video_list = []
    time_path_list = []
    time_list = []

    # Different Hard Coded Options

    # List of patterns for matching time codes. Second item in list is string for removal
    pattern_list = [('YYYY:MM:DD HH:mm:ss', ''), ('YYYYMMDD_HHmmss', 'VID_'),
                    ('YYYY-MM-DD HH.mm.ss', ''), ('YYYY.MM.DD_HH.mm.ss', '')]

    # Set the Frame Rate for rendering time lapse videos
    frame_rate = 25

    # Set the time for media objects to dwell in google earth before disappearing (in minutes)
    dwell_time = 45

    def __init__(self):

        # ---------------------------------- Initialisation ----------------------------------

        # Hard code in location of FFMPEG for the moment
        self.ffmpeg_location = r"C:\Users\Nathan\Documents\Development\Chaselog\Chaselog\ffmpeg.exe"

        # Automatic Download of Radar is enabled or disabled
        self.download_radar_module_enabled = False

        # Correct radar blink (gets changed according to check box by gui.py
        self.correct_radar_blink_tf = True

        self.root = ""

    def gui_main(self):

        # ---------------------------------- GUI Initialise ----------------------------------

        # Create root object
        self.root = Tk.Tk()
        MainGUI(self.root, self)
        self.root.mainloop()

        # Once finished the main loop, exit.
        sys.exit(1)

    def set_tb(self, tb):
        # Pass the text updater box to self referenced object, then can pass to different lines of code as needed,
        # passing self.tb
        self.tb = tb

    def gps_load_track(self):

        # Open the KML File
        self.gps_track, self.start_time, self.end_time = gps_methods.get_gps_track_list(self.gps_track_filename,
                                                                                        self.tz, self.tb)

    def radar_get_local_idr_list(self):

        # Load Radar Database
        self.radar_db = RadarDB('IDR023')

        # Identify local Radars along the track
        self.radar_set = radar_methods.get_near_idr_list(self.gps_track, self.tb)

    def process_radar(self):
        # If app is publicly released, skip to make radar list from files, need to check the self.download_radar_module
        # If app is private, check website for frames and that they are downloaded
        if self.download_radar_module:
            # Method to download radar frames from external module "radar_download_frames"
            # This method also catalogues the radars into the self.frames_db
            self.frames_db = radar_download_frames.get_online_frames(self.radar_set, self.radar_path, self.start_time,
                                                                     self.end_time, self.root_path, self.tb)
        else:
            # Method to search local filesystem according to convention and catalogue the files into self.frames_db
            self.frames_db = radar_methods.get_local_radar_frames_db(self.radar_set, self.radar_path, self.start_time,
                                                                     self.end_time, self.tb)

    def correct_blink(self):
        # Correct the radar blink. See declaration for more information
        radar_methods.correct_radar_blink(self.frames_db, self.tb)

    def create_radar_kml_file(self):
        # Create KML File
        kml_creator.create_radar_kml(self.frames_db, self.root_path, self.radar_path, self.tb)

    def find_media(self, str_photos, str_videos, str_time, tb):
        # ---------------------------------- Media ----------------------------------

        # Check that the media path exists
        if media_methods.check_media_path_exists(self.media_path):

            # Get Photo List
            self.photo_filename_list = media_methods.get_photo_list(self.media_path)
            self.photo_len = len(self.photo_filename_list)
            str_photos.set(self.photo_len)

            # Get Photo Exif Data (time taken)
            self.photo_list, self.rejected_photos_filename_list =\
                media_methods.get_photo_exif_data(self.media_path, self.photo_filename_list, self.start_time,
                                                  self.end_time, self.tz, self.tb)

            # Get video list
            self.video_filename_list = media_methods.get_video_list(self.media_path)

            # Get time from filename
            self.video_list, self.rejected_video_filename_list =\
                media_methods.set_video_time(self.video_filename_list, self.pattern_list, self.start_time,
                                             self.end_time, self.tz, self.tb)
            self.video_len = len(self.video_filename_list)
            str_videos.set(self.video_len)

            # Get Time lapse List
            self.time_path_list = media_methods.get_time_list(self.media_path, self.pattern_list, self.tz, self.tb)

            # Create the video
            media_methods.create_time_lapse_video(self.ffmpeg_location, self.media_path, self.time_path_list,
                                                  self.frame_rate, self.tb)

            # Create db of videos and the time they were taken
            self.time_list = media_methods.set_time_time(self.time_path_list, self.pattern_list, self.tz, self.tb)
            self.time_len = len(self.time_list)
            str_time.set(self.time_len)

        else:
            # If there is no media found at all.
            tb.tb_update("------------------------------------------------------------")
            tb.tb_update("")
            tb.tb_update("No Media found for this chase")
            tb.tb_update("")
            tb.tb_update("------------------------------------------------------------")

    def create_media_kml(self):

        # Set the location for each picture
        self.photo_list = media_methods.set_media_location(self.photo_list, self.gps_track)

        # Resize photos as necessary
        media_methods.set_resized_photos(self.media_path, self.photo_list, self.tb)

        # Group Photos together
        media_methods.set_media_groups(self.photo_list)

        # Set the location for each video
        self.video_list = media_methods.set_media_location(self.video_list, self.gps_track)

        # Group Videos as necessary
        media_methods.set_media_groups(self.video_list)

        # Set the location for each video
        self.time_list = media_methods.set_media_location(self.time_list, self.gps_track)

        # Group videos as necessary
        media_methods.set_media_groups(self.time_list)

        # Create the Media KML
        kml_creator.create_media_kml(self.root_path, self.media_path, self.photo_list, self.video_list, self.time_list,
                                     self.dwell_time, self.tb)


if __name__ == '__main__':
    main_app = MainApplication()
    main_app.gui_main()
