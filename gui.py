import Tkinter as Tk
import base64
import zlib
import tempfile
import icon_data
import tkFont
import arrow
import timezones
import tkMessageBox
import tkSimpleDialog
import kml_creator
import sys
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from Tkinter import IntVar
from Tkinter import StringVar
from Tkinter import Label
from Tkinter import Scale
from Tkinter import CENTER
from Tkinter import HORIZONTAL
from Tkinter import Frame
from Tkinter import Button
from Tkinter import Checkbutton
from Tkinter import LEFT
from Tkinter import RIGHT
from Tkinter import RIDGE
from Tkinter import Y
from Tkinter import Listbox
from Tkinter import BOTH
from Tkinter import END
from Tkinter import Text
from Tkinter import DISABLED
from Tkinter import NORMAL
from Tkinter import Scrollbar
from Tkinter import W
from Tkinter import Toplevel


# Implement the Scrolling Text Box Class. This is an extended class to include a custom method 'tb_update'
# This object can be thrown to different classes, with the tb_update method used to update the user within the text box
class TextScrollBox(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

    def tb_update(self, line):
        # Text box is created to be non-editable. To write, first need to make it editable, write the line to the end,
        # make it non-editable again and update the gui.
        self.config(state=NORMAL)
        self.insert(END, line + "\n")
        self.config(state=DISABLED)
        self.see("end")
        self.update()


# GUI for Timezone Selection
class TimezoneSelector(Toplevel):

    # Declare Variables. Selecting Timezones is two stage. Selecting a broad region, then selecting a location
    region = []
    region_shorter = []
    locations = []
    location_shorter = []
    current_region = ""
    grandfather = ""

    def __init__(self, grandfather):
        Toplevel.__init__(self)

        # Create the Timezone GUI
        self.grandfather = grandfather
        self.protocol("WM_DELETE_WINDOW", self.window_close)
        self.wm_title("Time Zone Selector")

        # Load lists from Timezones object into local lists
        self.region, self.locations = timezones.get_options()

        # main_frame is the base frame for the window
        main_frame = Frame(self)
        main_frame.pack(padx=5, pady=1, fill=BOTH, expand=True)

        # Window split into top brame and bottom frame
        frame_top = Frame(main_frame)
        frame_top.pack(pady=2, expand=True, fill=BOTH)

        # Inside top frame are two frames containing region options and location options
        frame_region = Frame(frame_top)
        frame_region.pack(side=LEFT, padx=3, expand=True, fill=BOTH)
        frame_location = Frame(frame_top)
        frame_location.pack(side=LEFT, padx=3, expand=True, fill=BOTH)

        # Region frame contains listbox of options to select
        self.listbox_region = Listbox(frame_region)
        self.listbox_region.pack(side=LEFT, padx=2, pady=2, fill=BOTH, expand=True)
        # Scrollbar for  region listbox
        scrollbar_region = Scrollbar(frame_region)
        scrollbar_region.pack(side=LEFT, fill=Y)
        self.listbox_region.config(yscrollcommand=scrollbar_region.set)
        scrollbar_region.config(command=self.listbox_region.yview)
        # Listbox doesn't have a feature to call method on change value. Need to set this manually:
        self.listbox_region.bind('<<ListboxSelect>>', self.on_select)

        # Populate the Region Listbox according to local region list
        k = 0
        last_region = ""
        for i in range(0, len(self.region)):
            if self.region[i] == last_region:
                k += 1
            else:
                self.listbox_region.insert(i-k, self.region[i])
                last_region = self.region[i]
                self.region_shorter.append(self.region[i])

        # Create the Locations Listbox
        self.listbox_location = Listbox(frame_location)
        self.listbox_location.pack(side=LEFT, padx=2, pady=2, fill=BOTH, expand=True)
        scrollbar_location = Scrollbar(frame_location)
        scrollbar_location.pack(side=LEFT, fill=Y)
        self.listbox_location.config(yscrollcommand=scrollbar_location.set)
        scrollbar_location.config(command=self.listbox_location.yview)
        # No need to have a manual call on listselect, want user to click ok after selecting location.

        # Also have a bottom frame
        frame_bottom = Frame(main_frame)
        frame_bottom.pack(pady=2)

        # Two buttons in bottom frame, OK and Cancel
        button_ok = Button(frame_bottom, text='OK', command=self.ok_button)
        button_ok.pack(padx=3, side=LEFT)
        button_cancel = Button(frame_bottom, text='Cancel', command=self.cancel_button)
        button_cancel.pack(padx=3, side=LEFT)

    # Method to populate locations list when region list value is changed
    def on_select(self):
        k = 0

        # Delete everything in the location listbox
        self.listbox_location.delete(0, END)

        # Create custom list with only locations from a particular region
        self.location_shorter = []

        # Declare current region
        self.current_region = self.region_shorter[self.listbox_region.curselection()[0]]

        # Cycle through locations list, populate locations listbox if regions match.
        for i in range(0, len(self.locations)):
            if self.region[i] == self.region_shorter[self.listbox_region.curselection()[0]]:
                self.listbox_location.insert(i - k, self.locations[i])
                self.location_shorter.append(self.locations[i])
            else:
                k += 1

    # If OK selected
    def ok_button(self):
        # Note current Timezone, return this in format usable by Arrow Module.
        tz = self.current_region + "/" + self.location_shorter[self.listbox_location.curselection()[0]]
        self.grandfather.tz = tz.replace(' - ', '/')
        print self.grandfather.tz
        # Close window
        self.withdraw()

    # If cancel pressed, close window, do nothing
    def cancel_button(self):
        self.window_close()

    # If window is closed, do nothing
    def window_close(self):
        self.withdraw()


# GUI for Radar Selection
class RadarSelector(Toplevel):

    # Define variables
    idr_check_list = []
    radar_checkbox_list = []

    def __init__(self, grandparent):

        # Define button methods to start with
        def ok_button():
            # radar_set is list of IDRCodes to download / look for locally
            self.grandparent.radar_set = []

            # Cycle through checklist, for each once selected, add into radar_set
            for l in range(0, len(self.idr_code_list)):
                if self.idr_check_list[l].get() == 1:
                    self.grandparent.radar_set.append(self.idr_code_list[l])

            # Close window
            self.withdraw()

        def cancel_button():
            # Same as close window
            radar_window_close()

        def radar_window_close():
            # Close window, do nothing
            self.withdraw()

        Toplevel.__init__(self)

        # Title, as well as defining "main" object.
        self.title("Radar Selector")
        self.grandparent = grandparent
        self.protocol("WM_DELETE_WINDOW", radar_window_close)

        # Main Frame in which everything will go
        frame_main = Frame(self)
        frame_main.pack(padx=3, pady=3)
        # Selections frame, where check boxes will go
        frame_selections = Frame(frame_main)
        frame_selections.pack(fill=BOTH, expand=True)
        # Bottom frame for buttons
        frame_bottom = Frame(frame_main)
        frame_bottom.pack(fill=BOTH, pady=3)

        self.idr_code_list = []

        # Add everything in the radar set, into the local list for showing
        for i in range(0, len(self.grandparent.radar_set)):
            self.idr_code_list.append(self.grandparent.radar_set[i])

        self.idr_code_list.sort()

        # For each IDR Code
        for i in range(0, len(self.idr_code_list)):

            # Create an IntVar
            self.idr_check_list.insert(i, IntVar())

            # Take note of the code and name
            idr_code = self.idr_code_list[i]
            idr_name = self.grandparent.radar_db.get_title(idr_code)

            radar_type = ""

            # Interpret Radar type from IDR Code (last character gives type)
            if idr_code[-1] == "2":
                radar_type = "256km"
            elif idr_code[-1] == "I":
                radar_type = "128km Wind"
            elif idr_code[-1] == "1":
                radar_type = "512km"
            elif idr_code[-1] == "3":
                radar_type = "128km"
            elif idr_code[-1] == "4":
                radar_type = "64km"

            # Create checkbox list. Checkbox value goes to IntVar list. Name is according to name and type of radar.
            self.radar_checkbox_list.insert(i, Checkbutton(frame_selections, text=idr_code + " - " + idr_name + " " +
                                                           radar_type, variable=self.idr_check_list[i]))

            # Some code to ensure they are all selected to start with.
            self.radar_checkbox_list[i].select()
            self.radar_checkbox_list[i].grid(row=i, sticky=W)

        # Create the ok button and cancel button
        button_ok = Button(frame_bottom, text='OK', command=ok_button)
        button_ok.pack(padx=3, side=LEFT)
        button_cancel = Button(frame_bottom, text='Cancel', command=cancel_button)
        button_cancel.pack(padx=3, side=LEFT)


# GUI for Trimming the GPS Track
class TrimGPS(Toplevel):

    def __init__(self, parent, grandparent, tb):
        # tb is textbox object used to update user.
        self.tb = tb
        self.parent = parent

        def trim_window_close():
            # Want to grab release (so that you can use the main window and close this window.
            self.grab_release()
            self.withdraw()

        def start_change_value(arg):
            # Change the IntVar will change the scrollbar
            var_local_time_start.set(self.grandparent.gps_track[int(arg)].get_local_time())

        def end_change_value(arg):
            # Change the IntVar will change the scroll bar
            var_local_time_end.set(self.grandparent.gps_track[int(arg)].get_local_time())

        def set_start():

            # Prompt user for the start time.
            start_response = tkSimpleDialog.askinteger("Set Start",
                                                       "Please select the value you would like to start from")
            # If response is blank, throw back to Trim GUI with grab set
            if start_response == "":
                self.grab_set()
            else:
                # If not empty, set the response accordingly then throw to Trim GUI.
                scale_start.set(start_response)
                self.grab_set()

        def set_end():

            # Prompt user for the end time.
            end_response = tkSimpleDialog.askinteger("Set End", "Please select the value you would like to end from")

            # If response is blank, throw back to Trim GUI with grab set
            if end_response == "":
                self.grab_set()
            else:
                # If not empty, set the response accordingly then throw to Trim GUI.
                scale_end.set(end_response)
                self.grab_set()

        def set_start_left():
            # Move start scrollbar left one value
            if scale_start.get() != 0:
                scale_start.set(scale_start.get() - 1)

        def set_start_right():
            # Move start scrollbar right one value
            if scale_start.get() != (len(self.gps_track) - 1):
                scale_start.set(scale_start.get() + 1)

        def set_end_left():
            # Move end scrollbar left one value
            if scale_end.get() != 0:
                scale_end.set(scale_end.get() - 1)

        def set_end_right():
            # Move end scrollbar right one value
            if scale_end.get() != (len(self.gps_track) - 1):
                scale_end.set(scale_end.get() + 1)

        def ok():
            # First need to check that the start time is before the finish point
            if int(var_end.get()) < int(var_start.get()):
                tkMessageBox.showwarning("Trim Error", "The end time is before the start point")

            # Next make sure that the start and end time are not the same
            elif int(var_end.get()) == int(var_start.get()):
                tkMessageBox.showwarning("Trim Error", "The end time cannot be the same as the start point")

            # Set the correct trim
            else:
                self.grab_release()

                # Update User
                tb.tb_update("")
                tb.tb_update("GPS Time Range has been updated")
                tb.tb_update("")

                # Update start and end time in main module
                self.grandparent.start_time = self.grandparent.gps_track[int(var_start.get())].get_time()
                self.grandparent.end_time = self.grandparent.gps_track[int(var_end.get())].get_time()

                # Use the kml creator to create the trimmed track. This returns an updated gps track and gps track file,
                # kept in the main module
                self.grandparent.gps_track_filename, self.grandparent.gps_track =\
                    kml_creator.create_gps_track_kml(self.grandparent.gps_track, self.grandparent.start_time,
                                                     self.grandparent.end_time, self.grandparent.root_path,
                                                     self.grandparent.gps_track_filename, self.grandparent.tz)
                # Update the User
                tb.tb_update("")
                tb.tb_update("Updated KML has been created:")
                tb.tb_update(self.grandparent.gps_track_filename)
                tb.tb_update("")

                # Disable Trim Track Button and destroy window
                self.parent.button_trim_gps.config(state=DISABLED)
                self.destroy()

        Toplevel.__init__(self)

        # Create window details
        self.grab_set()
        self.title("Trim Chase Start and End")
        self.grandparent = grandparent
        self.protocol("WM_DELETE_WINDOW", trim_window_close)

        self.gps_track = self.grandparent.gps_track

        # Define trim start and end
        self.trim_start = 0
        self.trim_end = len(self.gps_track)

        # Create Int Variables for scrollbars
        var_start = IntVar()
        var_end = IntVar()

        # String variable to be updated for local time display (as well as point number)
        var_local_time_start = StringVar()
        var_local_time_end = StringVar()

        # Base Frame
        frame_main = Frame(self)
        frame_main.pack()

        # Start Section
        label_start = Label(frame_main, textvariable=var_local_time_start)
        label_start.pack(anchor=CENTER)

        scale_start = Scale(frame_main, from_=0, to=self.trim_end - 1, variable=var_start, length=500,
                            orient=HORIZONTAL,
                            command=start_change_value)
        scale_start.pack(anchor=CENTER)

        # Bottom Frame
        frame_bottom = Frame(frame_main)
        frame_bottom.pack(anchor=CENTER)

        button_set_start = Button(frame_bottom, text="Set Start Time", command=set_start)
        button_set_start.grid(row=2, column=2)
        button_set_start_left = Button(frame_bottom, text="Left", command=set_start_left)
        button_set_start_left.grid(row=2, column=1)
        button_set_start_right = Button(frame_bottom, text="Right", command=set_start_right)
        button_set_start_right.grid(row=2, column=3)

        label_space = Label(frame_main, text="")
        label_space.pack(anchor=CENTER)

        # End Section
        label_end = Label(frame_main, textvariable=var_local_time_end)
        label_end.pack(anchor=CENTER)

        scale_end = Scale(frame_main, from_=0, to=len(self.gps_track) - 1, variable=var_end, length=500,
                          orient=HORIZONTAL,
                          command=end_change_value)
        scale_end.pack(anchor=CENTER)
        scale_end.set(len(self.gps_track))

        end_frame = Frame(frame_main)
        end_frame.pack(anchor=CENTER)

        button_set_end = Button(end_frame, text="Set Start Time", command=set_end)
        button_set_end.grid(row=2, column=2)
        button_set_end_left = Button(end_frame, text="Left", command=set_end_left)
        button_set_end_left.grid(row=2, column=1)
        button_set_end_right = Button(end_frame, text="Right", command=set_end_right)
        button_set_end_right.grid(row=2, column=3)

        # OK Button at Bottom
        button_ok = Button(frame_main, text="OK", command=ok)
        button_ok.pack(anchor=CENTER)


class MainGUI(Tk.Frame):
    parent = ""
    grandparent = ""
    tz = ""

    def __init__(self, parent, grandparent):
        Tk.Frame.__init__(Frame(), parent)
        self.grandparent = grandparent
        self.parent = parent
        parent.protocol("WM_DELETE_WINDOW", window_close)
        self.parent.wm_title("Chase Builder")

        # Button Methods

        def instructions_button():
            pass

        def set_timezone():
            TimezoneSelector(self.grandparent)

        def get_root_button():
            root_path = askdirectory(title="Please select the Chase Root Folder",
                                     initialdir=r"C:\Users\Nathan\Desktop\Chase Copy")
            if not root_path == "":
                self.str_root_folder.set(root_path.replace('/', "\\"))
                self.grandparent.root_path = root_path
                self.grandparent.radar_path = self.grandparent.root_path + r"\Radar"
                self.grandparent.media_path = self.grandparent.root_path + r"\Media"

                button_open_gps_file.config(state=NORMAL)
                button_get_root.config(state=DISABLED)
                button_set_tz.config(state=DISABLED)

                checkbox_correct_blink.config(state=DISABLED)
                checkbox_geocode_parse.config(state=DISABLED)
                checkbox_radar_offline.config(state=DISABLED)

        def open_gps_file():
            file_open_options = dict(defaultextension='.kml', filetypes=[('KML file', '*.kml'), ('All files', '*.*')])
            gps_track_filename = askopenfilename(title="Select the Chase GPS Track",
                                                 initialdir=self.grandparent.root_path, **file_open_options)

            if not gps_track_filename == "":
                self.str_gps_file.set(gps_track_filename.split('/')[-1])
                self.grandparent.gps_track_filename = gps_track_filename
                self.grandparent.gps_load_track()
                start_time = arrow.get(self.grandparent.start_time)
                end_time = arrow.get(self.grandparent.end_time)
                tz = self.grandparent.tz
                self.str_gps_start.set(start_time.to(tz).format('DD-MM-YYYY HH:mm:ss'))
                self.str_gps_end.set(end_time.to(tz).format('DD-MM-YYYY HH:mm:ss'))
                button_open_gps_file.config(state=DISABLED)
                self.button_trim_gps.config(state=NORMAL)
                button_identify_radars.config(state=NORMAL)
                button_find_media.config(state=NORMAL)

        def trim_gps():
            TrimGPS(self, self.grandparent, text_box_main)

        def get_near_idrs():
            self.button_trim_gps.config(state=DISABLED)
            button_identify_radars.config(state=DISABLED)
            self.grandparent.radar_get_local_idr_list()
            button_manually_select_radar.config(state=NORMAL)

            button_process_radar.config(state=NORMAL)

        def get_manual_radars():
            RadarSelector(self.grandparent)

        def process_images():
            button_manually_select_radar.config(state=DISABLED)
            button_process_radar.config(state=DISABLED)
            if self.radar_offline.get() == 0:
                self.grandparent.download_radar_module = True
            else:
                self.grandparent.download_radar_module = False

            self.grandparent.process_radar()

            if self.correct_blink.get() == 1:
                self.grandparent.correct_blink()

            button_create_radar_kml.config(state=NORMAL)

        def create_radar_kml():
            self.grandparent.create_radar_kml_file()
            button_create_radar_kml.config(state=DISABLED)

        def find_media():
            self.grandparent.find_media(self.str_photos, self.str_videos, self.str_time)
            button_create_media_kml.config(state=NORMAL)
            button_find_media.config(state=DISABLED)

        def manual_time_find():
            pass

        def create_media_kml():
            self.grandparent.create_media_kml()
            button_create_media_kml.config(state=DISABLED)

        self.str_root_folder = StringVar()
        self.str_gps_file = StringVar()
        self.str_gps_start = StringVar()
        self.str_gps_end = StringVar()

        self.str_photos = StringVar()
        self.str_videos = StringVar()
        self.str_time = StringVar()

        self.radar_offline = IntVar()
        self.correct_blink = IntVar()
        self.geocode_parse = IntVar()

        frame_main = Frame(self.parent)
        frame_main.pack(fill=BOTH, expand=True, pady=5)

        frame_middle = Frame(frame_main)
        frame_middle.pack(fill=BOTH, expand=True, padx=5)

        text_box_main = TextScrollBox(frame_middle, height=5, width=10, state=DISABLED,
                                      font=tkFont.Font(family="Courier New", size=8))
        text_box_main.pack(side=LEFT, fill=BOTH, expand=True, pady=1)
        self.grandparent.set_tb(text_box_main)

        scrollbar_main = Scrollbar(frame_middle)
        scrollbar_main.pack(side=RIGHT, fill=Y, pady=1, padx=1)

        text_box_main.config(yscrollcommand=scrollbar_main.set)
        scrollbar_main.config(command=text_box_main.yview)

        frame_action = Frame(frame_main)
        frame_action.pack(expand=False)

        frame_detail = Frame(frame_main)
        frame_detail.pack(expand=False)

        frame_general_detail = Frame(frame_detail, bd=2, relief=RIDGE)
        frame_general_detail.pack(side=LEFT, padx=5, pady=1, fill=BOTH)

        label_general_detail = Label(frame_general_detail, text='General Details')
        label_general_detail.pack(padx=5, pady=1)

        frame_root_folder = Frame(frame_general_detail)
        frame_root_folder.pack()

        label_root_folder = Label(frame_root_folder, textvariable=self.str_root_folder)
        label_root_folder.pack(side=LEFT)

        frame_gps_detail = Frame(frame_detail, bd=2, relief=RIDGE)
        frame_gps_detail.pack(side=LEFT, padx=5, pady=1, fill=BOTH)

        label_gps_detail = Label(frame_gps_detail, text='GPS Details')
        label_gps_detail.pack(padx=5, pady=1)

        frame_gps_file = Frame(frame_gps_detail)
        frame_gps_file.pack()
        frame_gps_start = Frame(frame_gps_detail)
        frame_gps_start.pack()
        frame_gps_finish = Frame(frame_gps_detail)
        frame_gps_finish.pack()

        label_gps_file = Label(frame_gps_file, textvariable=self.str_gps_file)
        label_gps_file.pack(side=LEFT)

        label_gps_start_title = Label(frame_gps_start, text='GPS Start Time: ')
        label_gps_start_title.pack(side=LEFT)
        label_gps_start = Label(frame_gps_start, textvariable=self.str_gps_start)
        label_gps_start.pack(side=LEFT)

        label_gps_finish_title = Label(frame_gps_finish, text='GPS Finish Time: ')
        label_gps_finish_title.pack(side=LEFT)
        label_gps_finish = Label(frame_gps_finish, textvariable=self.str_gps_end)
        label_gps_finish.pack(side=LEFT)

        frame_media_detail = Frame(frame_detail, bd=2, relief=RIDGE)
        frame_media_detail.pack(side=LEFT, padx=5, pady=1, fill=BOTH)

        label_media_detail = Label(frame_media_detail, text='Media Details')
        label_media_detail.pack(padx=5, pady=1)

        frame_media_photo = Frame(frame_media_detail)
        frame_media_photo.pack()
        frame_media_video = Frame(frame_media_detail)
        frame_media_video.pack()
        frame_media_time = Frame(frame_media_detail)
        frame_media_time.pack()

        label_media_photo_title = Label(frame_media_photo, text='Photos: ')
        label_media_photo_title.pack(side=LEFT)
        label_media_video_title = Label(frame_media_video, text='Videos: ')
        label_media_video_title.pack(side=LEFT)
        label_media_time_title = Label(frame_media_time, text='Time lapse: ')
        label_media_time_title.pack(side=LEFT)

        label_media_photo = Label(frame_media_photo, textvariable=self.str_photos)
        label_media_photo.pack(side=LEFT)
        label_media_video = Label(frame_media_video, textvariable=self.str_videos)
        label_media_video.pack(side=LEFT)
        label_media_time = Label(frame_media_time, textvariable=self.str_time)
        label_media_time.pack(side=LEFT)

        frame_settings = Frame(frame_action, bd=2, relief=RIDGE)
        frame_settings.pack(side=LEFT, padx=5, pady=1, fill=Y)

        button_help = Button(frame_settings, text="Instructions", command=instructions_button)
        button_help.pack(padx=5, pady=1)
        button_set_tz = Button(frame_settings, text="Set Timezone", command=set_timezone)
        button_set_tz.pack(padx=5, pady=1)
        checkbox_radar_offline = Checkbutton(frame_settings, text="Use Locally Stored Radar",
                                             variable=self.radar_offline)
        self.radar_offline.set(1)
        checkbox_radar_offline.config(state=DISABLED)
        checkbox_radar_offline.pack(padx=5, pady=1)
        checkbox_correct_blink = Checkbutton(frame_settings, text="Correct Blinking Radar Frames",
                                             variable=self.correct_blink)
        checkbox_correct_blink.pack(padx=5, pady=1)
        checkbox_geocode_parse = Checkbutton(frame_settings, text="Get Geo-coded Locations",
                                             variable=self.geocode_parse)
        checkbox_geocode_parse.pack(padx=5, pady=1)

        frame_gps_action = Frame(frame_action, bd=2, relief=RIDGE)
        frame_gps_action.pack(side=LEFT, padx=5, pady=1, fill=Y)

        label_gps_title = Label(frame_gps_action, text="GPS Module")
        label_gps_title.pack(padx=5, pady=1)
        button_get_root = Button(frame_gps_action, text="Select Root Folder", command=get_root_button)
        button_get_root.pack(padx=5, pady=1)
        button_open_gps_file = Button(frame_gps_action, text="Open GPS File", command=open_gps_file, state=DISABLED)
        button_open_gps_file.pack(padx=5, pady=1)
        self.button_trim_gps = Button(frame_gps_action, text="Trim the GPS Track", command=trim_gps, state=DISABLED)
        self.button_trim_gps.pack(padx=5, pady=1)

        frame_radar_action = Frame(frame_action, bd=2, relief=RIDGE)
        frame_radar_action.pack(side=LEFT, padx=5, pady=1, fill=Y)

        label_radar_title = Label(frame_radar_action, text="Radar Module")
        label_radar_title.pack(padx=5, pady=1)
        button_identify_radars = Button(frame_radar_action, text="Identify Radars", command=get_near_idrs,
                                        state=DISABLED)
        button_identify_radars.pack(padx=5, pady=1)
        button_manually_select_radar = Button(frame_radar_action, text="Select Radars", command=get_manual_radars,
                                              state=DISABLED)
        button_manually_select_radar.pack(padx=5, pady=1)
        button_process_radar = Button(frame_radar_action, text="Process Radar Images", command=process_images,
                                      state=DISABLED)
        button_process_radar.pack(padx=5, pady=1)
        button_create_radar_kml = Button(frame_radar_action, text="Create the KML file", command=create_radar_kml,
                                         state=DISABLED)
        button_create_radar_kml.pack(padx=5, pady=1)

        frame_media_action = Frame(frame_action, bd=2, relief=RIDGE)
        frame_media_action.pack(side=LEFT, padx=5, pady=1, fill=Y)

        label_media_title = Label(frame_media_action, text="Media Module")
        label_media_title.pack(padx=5, pady=1)
        button_find_media = Button(frame_media_action, text="Search for Media", command=find_media, state=DISABLED)
        button_find_media.pack(padx=5, pady=1)
        button_manual_time_media = Button(frame_media_action, text="Manually Set Time", command=manual_time_find,
                                          state=DISABLED)
        button_manual_time_media.pack(padx=5, pady=1)
        button_create_media_kml = Button(frame_media_action, text="Create Media KML", command=create_media_kml,
                                         state=DISABLED)
        button_create_media_kml.pack(padx=5, pady=1)

        self.parent.update_idletasks()
        self.parent.after_idle(lambda: self.parent.minsize(self.parent.winfo_width(), self.parent.winfo_height()))

        icon = zlib.decompress(base64.b64decode(icon_data.get_icon_data()))

        icon_path = tempfile.mkstemp()[1]
        with open(icon_path, 'wb') as icon_file:
            icon_file.write(icon)

        self.parent.iconbitmap(default=icon_path)


def window_close():
    sys.exit(1)
