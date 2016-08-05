import Tkinter as Tk
import base64
import zlib
import tempfile
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

    def update_text_box(self, line):
        self.config(state=NORMAL)
        self.insert(END, line + "\n")
        self.config(state=DISABLED)
        self.see("end")

class MainGUI(Tk.Frame):

    parent = ""

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        parent.protocol("WM_DELETE_WINDOW", self.window_close)
        self.parent.wm_title("Chase Builder")

        # Button Methods

        def help_button():
            pass

        def set_timezone():
            pass

        def get_root_button():
            pass

        def get_near_idrs():
            pass

        def get_manual_radars():
            from temp import anything
            anything(main_text_box)

        def process_images():
            update_textbox("Hello")

        def create_kml_file():
            for i in range(0,9999):
                update_textbox(str(i))

        def create_media_kml():
            self.parent.update()

        def update_textbox():
            pass

        def exit_cb():
            exit()

        main_frame = Frame(self.parent)
        main_frame.pack(fill=BOTH, expand=True)
        middle_frame = Frame(main_frame)
        middle_frame.pack(fill=BOTH, expand=True)

        main_text_box = TextScrollBox(middle_frame, height=5, width=10, state=DISABLED)
        main_text_box.pack(fill=BOTH, expand=True, padx=5, pady=5)

        bottom_frame = Frame(main_frame)
        bottom_frame.pack(expand=False)

        settings_frame = Frame(bottom_frame, bd=2, relief=RIDGE)
        settings_frame.pack(side=LEFT, padx=5, pady=5, fill=Y)

        button_help = Button(settings_frame, text="Help", command=help_button).pack(padx=5, pady=5)
        button_set_tz = Button(settings_frame, text="Set Timezone", command=set_timezone).pack( padx=5, pady=5)
        radar_offline = Checkbutton(settings_frame, text="Use Locally Stored Radar").pack(padx=5, pady=5)
        correct_blink = Checkbutton(settings_frame, text="Correct Blinking Radar Frames").pack(padx=5, pady=5)
        geocode_parse = Checkbutton(settings_frame, text="Match Media Locations to Geocoded Location (needs internet"
                                                         " connection)").pack(padx=5, pady=5)

        gps_frame = Frame(bottom_frame, bd=2, relief=RIDGE)
        gps_frame.pack(side=LEFT, padx=5, pady=5, fill=Y)

        label_gps_title = Label(gps_frame, text="GPS Module").pack(padx=5, pady=5)
        button_get_root = Button(gps_frame, text="Select Root Folder", command=get_root_button).pack(padx=5, pady=5)
        button_open_gps_file = Button(gps_frame, text="Open GPS File", command=get_root_button).pack(padx=5, pady=5)
        label_gps_details = Label(gps_frame, text="GPS Details go here").pack(padx=5, pady=5)
        button_trim_gps = Button(gps_frame, text="Trim the GPS Track", command=get_root_button).pack()

        radar_frame = Frame(bottom_frame, bd=2, relief=RIDGE)
        radar_frame.pack(side=LEFT, padx=5, pady=5, fill=Y)

        label_radar_title = Label(radar_frame, text="Radar Module").pack(padx=5, pady=5)
        button_identify_radars = Button(radar_frame, text="Identify Radars", command=get_near_idrs).pack(padx=5, pady=5)
        button_manually_select_radar = Button(radar_frame, text="Select Radars", command=get_manual_radars).pack(padx=5, pady=5)
        button_process_radar = Button(radar_frame, text="Process Radar Images", command=process_images).pack(padx=5, pady=5)
        button_create_radar_kml = Button(radar_frame, text="Create the KML file", command=create_kml_file).pack(padx=5, pady=5)

        media_frame = Frame(bottom_frame, bd=2, relief=RIDGE)
        media_frame.pack(side=LEFT, padx=5, pady=5, fill=Y)

        label_media_title = Label(media_frame, text="Media Module").pack(padx=5, pady=5)
        label_media_location = Label(media_frame, text="Media Location: Whatever").pack(padx=5, pady=5)
        button_create_media_kml = Button(media_frame, text="Create Media KML", command=create_media_kml).pack(padx=5, pady=5)

        button_exit = Button(main_frame, text="Exit", command=exit_cb, width=10)
        button_exit.pack(pady=5, padx=5)

        self.parent.update_idletasks()
        self.parent.after_idle(lambda: self.parent.minsize(self.parent.winfo_width(), self.parent.winfo_height()))

        # icon = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
        #                                         'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

        icon = zlib.decompress(base64.b64decode('eJyFU8tuGkEQnFUixdx8ipRbLqD8mFG+YM85IOdfOCMZCYJ5Pw0IWFgEfkAQAmSDeJmV7RWdqrHWMpFlNyp2d6Zruru6RykDv+Njhf/v6udnpb4qpX4AWMLK87o27HW+PeN/i8ViKp1KGYVCwZ9MJk0gen5+bhOJRCIKmPF43B8Oh41IJHLArVarKpvN+gaDwUmv1+ukUikX31KpVKTRaEir1ZJms+niu5PP508ymYwvl8tpbrlcJveo3W6HJpOJs9lsZDabCZ9PT0/iuq48Pj6K4zh6vdvtOpZlhXDWEeOKiML5QcTdcZ/+xHK5lOFwKPAV+AniSLFY1MD7DvGDyFeh3oBt21a/35ebmxuNer0uyFFQ+wGgyWtYWAugVhNnujyfNXPvDd8DpNNpQVxytM7v+b4Gc4eOgnypA9/Jtd/jMBfmdXV1JdvtVm5vbwVaMz7zsD/i1+s1WSwWQnt4eNCxUbNXo/1W/tyjfpeXl5pDu7+/17PAffJLpZKgB1HUZOLpvtaN/WKe+/1ec9frtVQvLl72qcH19bWLvpvoVQA9tmq1mhCj0eglJm21Wuk59HrIs+kDPSxyOT+gB9H/3Xg81nnSGPvu7k7n6XGpGX2AHfQPksv5xUwfIZcQtHE4c9PpVDCPWnePy/ng+nw+d5B7iDNfw/zS0AeFunx48m608XSpETVkfJ4FDVzcifZo9PcEa75Ws3lwB3E31dnZmYF76i8WCqbd6USRi40a7O1mE8V9MDHb/t+np8Yf+Ho2+KJU8pNSv4xnfGSeHznk/gM54Ryx'))

        icon_path = tempfile.mkstemp()[1]
        with open(icon_path, 'wb') as icon_file:
            icon_file.write(icon)

        #icon_path = r"C:\Users\Nathan\Downloads\favico.ico"

        #f = open(icon_path, 'r')
        #icon = f.read()
        #print icon
        #print base64.b64encode(zlib.compress(icon))
        #f.close()
        self.parent.iconbitmap(default=icon_path)

    def window_close(self):
        self.parent.quit()
        self.parent.withdraw()


class TrimGui(Tk.Frame):

    parent = ""

    def __init__(self, parent):
        Tk.Frame.__init__(self, parent)
        self.parent = parent
        parent.protocol("WM_DELETE_WINDOW", self.window_close)

    def window_close(self):
        self.parent.withdraw()
        self.parent.quit()