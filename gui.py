import Tkinter as Tk
import base64
import zlib
import tempfile
import icon_data
import tkFont
from threading import Thread
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
from Tkinter import TOP
from Tkinter import BOTTOM
from Tkinter import SUNKEN
from Tkinter import GROOVE
from Tkinter import RIDGE
from Tkinter import RAISED
from Tkinter import X
from Tkinter import Y
from Tkinter import Listbox
from Tkinter import BOTH
from Tkinter import END
from Tkinter import Text
from Tkinter import DISABLED
from Tkinter import NORMAL
from Tkinter import Scrollbar


class TextScrollBox(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

    def tb_update(self, line):
        self.config(state=NORMAL)
        self.insert(END, line + "\n")
        self.config(state=DISABLED)
        self.see("end")
        self.update()


class MainGUI(Tk.Frame):
    parent = ""
    grandparent=""

    def __init__(self, parent, grandparent):
        Tk.Frame.__init__(Frame(), parent)
        self.grandparent = grandparent
        self.parent = parent
        parent.protocol("WM_DELETE_WINDOW", self.window_close)
        self.parent.wm_title("Chase Builder")

        # Button Methods

        def instructions_button():
            pass

        def set_timezone():
            pass

        def get_root_button():
            root_path = askdirectory(title="Please select the Chase Root Folder", initialdir=r"C:\Users\Nathan\Desktop\Chase Copy")
            if not root_path=="":
                self.grandparent.root_path = root_path
                self.grandparent.radar_path = self.grandparent.root_path + r"\Radar"
                self.grandparent.media_path = self.grandparent.root_path + r"\Media"

                button_open_gps_file.config(state=NORMAL)
                button_get_root.config(state=DISABLED)

                checkbox_correct_blink.config(state=DISABLED)
                checkbox_geocode_parse.config(state=DISABLED)
                checkbox_radar_offline.config(state=DISABLED)

        def open_gps_file():
            file_open_options = dict(defaultextension='.kml', filetypes=[('KML file', '*.kml'), ('All files', '*.*')])
            gps_track_filename = askopenfilename(title="Select the Chase GPS Track", initialdir=self.grandparent.root_path,
                                                 **file_open_options)

            if not gps_track_filename == "":
                self.grandparent.gps_track_filename = gps_track_filename
                self.grandparent.gps_load_track()
                button_open_gps_file.config(state=DISABLED)
                button_trim_gps.config(state=NORMAL)
                button_identify_radars.config(state=NORMAL)

        def trim_gps():
            pass

        def get_near_idrs():
            button_trim_gps.config(state=DISABLED)
            button_identify_radars.config(state=DISABLED)
            self.grandparent.radar_get_local_idr_list()
            button_manually_select_radar.config(state=NORMAL)

            button_process_radar.config(state=NORMAL)

        def get_manual_radars():
            from temp import anything
            anything(text_box_main)

        def process_images():
            button_manually_select_radar.config(state=DISABLED)
            button_process_radar.config(state=DISABLED)
            self.grandparent.process_radar()
            if correct_blink.get() == 1:
                self.grandparent.correct_blink()

            button_create_radar_kml.config(state=NORMAL)

        def create_radar_kml():
            self.grandparent.create_radar_kml_file()
            button_create_media_kml.config(state=DISABLED)

        def find_media():
            pass

        def manual_time_find():
            pass

        def create_media_kml():
            pass

        frame_main = Frame(self.parent)
        frame_main.pack(fill=BOTH, expand=True, pady=5)

        frame_middle = Frame(frame_main)
        frame_middle.pack(fill=BOTH, expand=True, padx=5)

        text_box_main = TextScrollBox(frame_middle, height=5, width=10, state=DISABLED, font=tkFont.Font(family="Courier New", size=8))
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

        label_root_folder = Label(frame_root_folder, text='Root Folder: ')
        label_root_folder.pack()

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

        label_gps_file = Label(frame_gps_file, text='GPS Filename: ')
        label_gps_file.pack()
        label_gps_start = Label(frame_gps_start, text='GPS Start Time: ')
        label_gps_start.pack()
        label_gps_finish = Label(frame_gps_finish, text='GPS Finish Time: ')
        label_gps_finish.pack()

        frame_media_detail = Frame(frame_detail, bd=2, relief=RIDGE)
        frame_media_detail.pack(side=LEFT, padx=5, pady=1, fill=BOTH)

        label_media_detail = Label(frame_media_detail, text='Media Details')
        label_media_detail.pack(padx=5, pady=1)

        frame_media_file = Frame(frame_media_detail)
        frame_media_file.pack(pady=2)
        frame_media_photo = Frame(frame_media_detail)
        frame_media_photo.pack()
        frame_media_video = Frame(frame_media_detail)
        frame_media_video.pack()
        frame_media_time = Frame(frame_media_detail)
        frame_media_time.pack()

        label_media_folder = Label(frame_media_file, text='Media Folder: ')
        label_media_folder.pack()
        label_media_photo = Label(frame_media_photo, text='Photos: ')
        label_media_photo.pack()
        label_media_video = Label(frame_media_video, text='Videos: ')
        label_media_video.pack()
        label_media_time = Label(frame_media_time, text='Time lapse: ')
        label_media_time.pack()

        frame_settings = Frame(frame_action, bd=2, relief=RIDGE)
        frame_settings.pack(side=LEFT, padx=5, pady=1, fill=Y)

        button_help = Button(frame_settings, text="Instructions", command=instructions_button)
        button_help.pack(padx=5, pady=1)
        button_set_tz = Button(frame_settings, text="Set Timezone", command=set_timezone)
        button_set_tz.pack(padx=5, pady=1)
        radar_offline = IntVar()
        correct_blink = IntVar()
        geocode_parse = IntVar()
        checkbox_radar_offline = Checkbutton(frame_settings, text="Use Locally Stored Radar", variable=radar_offline)
        checkbox_radar_offline.pack(padx=5, pady=1)
        checkbox_correct_blink = Checkbutton(frame_settings, text="Correct Blinking Radar Frames", variable=correct_blink)
        checkbox_correct_blink.pack(padx=5, pady=1)
        checkbox_geocode_parse = Checkbutton(frame_settings, text="Get Geocoded Locations)", variable=geocode_parse)
        checkbox_geocode_parse.pack(padx=5, pady=1)

        frame_gps_action = Frame(frame_action, bd=2, relief=RIDGE)
        frame_gps_action.pack(side=LEFT, padx=5, pady=1, fill=Y)

        label_gps_title = Label(frame_gps_action, text="GPS Module")
        label_gps_title.pack(padx=5, pady=1)
        button_get_root = Button(frame_gps_action, text="Select Root Folder", command=get_root_button)
        button_get_root.pack(padx=5, pady=1)
        button_open_gps_file = Button(frame_gps_action, text="Open GPS File", command=open_gps_file, state=DISABLED)
        button_open_gps_file.pack(padx=5, pady=1)
        button_trim_gps = Button(frame_gps_action, text="Trim the GPS Track", command=trim_gps, state=DISABLED)
        button_trim_gps.pack(padx=5, pady=1)

        frame_radar_action = Frame(frame_action, bd=2, relief=RIDGE)
        frame_radar_action.pack(side=LEFT, padx=5, pady=1, fill=Y)

        label_radar_title = Label(frame_radar_action, text="Radar Module")
        label_radar_title.pack(padx=5, pady=1)
        button_identify_radars = Button(frame_radar_action, text="Identify Radars", command=get_near_idrs, state=DISABLED)
        button_identify_radars.pack(padx=5, pady=1)
        button_manually_select_radar = Button(frame_radar_action, text="Select Radars", command=get_manual_radars, state=DISABLED)
        button_manually_select_radar.pack(padx=5, pady=1)
        button_process_radar = Button(frame_radar_action, text="Process Radar Images", command=process_images, state=DISABLED)
        button_process_radar.pack(padx=5, pady=1)
        button_create_radar_kml = Button(frame_radar_action, text="Create the KML file", command=create_radar_kml, state=DISABLED)
        button_create_radar_kml.pack(padx=5, pady=1)

        frame_media_action = Frame(frame_action, bd=2, relief=RIDGE)
        frame_media_action.pack(side=LEFT, padx=5, pady=1, fill=Y)

        label_media_title = Label(frame_media_action, text="Media Module")
        label_media_title.pack(padx=5, pady=1)
        button_find_media = Button(frame_media_action, text="Search for Media", command=find_media, state=DISABLED)
        button_find_media.pack(padx=5, pady=1)
        button_manual_time_media = Button(frame_media_action, text="Manually Set Time", command=manual_time_find, state=DISABLED)
        button_manual_time_media.pack(padx=5, pady=1)
        button_create_media_kml = Button(frame_media_action, text="Create Media KML", command=create_media_kml, state=DISABLED)
        button_create_media_kml.pack(padx=5, pady=1)

        self.parent.update_idletasks()
        self.parent.after_idle(lambda: self.parent.minsize(self.parent.winfo_width(), self.parent.winfo_height()))

        icon = zlib.decompress(base64.b64decode(icon_data.get_icon_data()))

        icon_path = tempfile.mkstemp()[1]
        with open(icon_path, 'wb') as icon_file:
            icon_file.write(icon)

        self.parent.iconbitmap(default=icon_path)

    def window_close(self):
        exit()



class TrimGui(Tk.Frame):
    parent = ""

    def __init__(self, parent):
        Tk.Frame.__init__(Frame(), parent)
        self.parent = parent
        parent.protocol("WM_DELETE_WINDOW", self.window_close)

    def window_close(self):
        self.parent.withdraw()
        self.parent.quit()
