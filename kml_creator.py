import arrow
import simplekml
import os
from radar_db import RadarDB


def create_radar_kml(frame_db, root_path, radar_path, tz):

    radar_db = RadarDB('IDR023')
    kml = simplekml.Kml()
    kml_folders = []

    # Create a KML file. In the kml file there should be a folder for each radar location and type
    # Inside this folder will be the radar frames.
    # The variable 'ground' will be a list of overlays - the radar frames.
    # The variable 'kml_folders' will be a list of folder objects.
    # Overlay objects are added to the folder object through the method kml_folders.newgroundoverlay
    # These objects are added to the list 'ground'
    for k in range(0, len(frame_db)):
        ground = []
        frame_list = frame_db[k]
        idr_code = frame_list[0].get_filename().split('.')[0]

        print idr_code
        radar_db.select_radar(idr_code)
        radar_title = radar_db.get_title(idr_code)
        kml_folders.insert(len(kml_folders), kml.newfolder(name=radar_title))
        for i in range(0,len(frame_list)):
            filename = frame_list[i].get_filename()
            ground.insert(len(ground),kml_folders[k].newgroundoverlay(name=filename.split('.')[2]))
            ground[i].icon.href = radar_path + "\\" + filename.split('.')[0] + "\\" + filename
            radar_db.select_radar(idr_code)
            ground[i].latlonbox.north, ground[i].latlonbox.south, ground[i].latlonbox.east, ground[i].latlonbox.west = radar_db.get_nsew(idr_code)
            ground[i].timespan.begin = arrow.get(int(frame_list[i].get_time()))
            ground[i].timespan.end = arrow.get(int(frame_list[i].get_time()) + (60*6))

    os.chdir(root_path)
    kml.save("Radar - Updated.kml")


def create_media_kml(root_path, photo_list, video_list, time_list, dwell_time, tz):
    # Create HTML Blocks for Photos and Videos:

    photo_html_block = r"""<![CDATA[<font size = "18">
$NAME$</font>
<img src="$FILENAME$"/><font size = 18><br><br></font>]]>"""

    # Create the media kml. Firstly need to create the photo objects
    # Test that photo_list isn't empty
    # Firstly, create a kml object that will have folders added to it
    # Also create a list for the folders to go in

    kml = simplekml.Kml()
    kml_folders = []

    if len(photo_list) == 0:
        print "There are no photos"
    else:
        # There are photos to process
        # Need to create a kml folder for photos, then create the objects in this folder.
        # Create a list for photo objects to go into

        # folder = kml.newfolder(name='Hi')
        # point1 = folder.newpoint(name='Hi there')
        # point1.coords = [(145, -37)]
        # os.chdir(r'C:\Users\Nathan\Desktop')
        # kml.save('Test.kml')

        photo_items = []
        kml_folders.insert(len(kml_folders), kml.newfolder(name='Photos'))
        k=0
        for i in range(0, len(photo_list)):

            if i == 0:
                photo_items.append(kml_folders[0].newpoint(name=str(photo_list[i].get_group_number())))
                lat, lon = photo_list[i].get_location()
                photo_items[i - k].coords = [(lon, lat)]
                photo_items[i - k].style.iconstyle.icon.href = \
                    'http://maps.google.com/mapfiles/kml/paddle/grn-circle.png'
                photo_items[i - k].timespan.begin = photo_list[i].get_iso()
                photo_items[i - k].timespan.end = arrow.get(photo_list[i].get_epoch() + int(dwell_time) * 60)
                name = photo_list[i].get_local()
                filename = photo_list[i].get_filename()
                filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()
                photo_items[i - k].description = photo_html_block.replace('$NAME$', name).replace('$FILENAME$', filename)
                continue

            for j in range(0, i):

                if photo_list[i].get_group_number() == photo_list[j].get_group_number():
                    # Add HTML Code to current place mark

                    for l in range(0, len(photo_items)):
                        if photo_items[l].name == str(photo_list[j].get_group_number()):
                            name = photo_list[i].get_local()
                            filename = photo_list[i].get_filename()
                            filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()
                            photo_items[l].description = photo_items[l].description + photo_html_block.replace('$NAME$', name).replace('$FILENAME$', filename)
                            break


                    k += 1
                    break

                elif j==i-1:
                    # Create a point
                    photo_items.append(kml_folders[0].newpoint(name=str(photo_list[i].get_group_number())))
                    lat, lon = photo_list[i].get_location()
                    photo_items[i-k].coords = [(lon, lat)]
                    photo_items[i-k].style.iconstyle.icon.href =\
                        'http://maps.google.com/mapfiles/kml/paddle/grn-circle.png'
                    photo_items[i-k].timespan.begin = photo_list[i].get_iso()
                    photo_items[i-k].timespan.end = arrow.get(photo_list[i].get_epoch()+int(dwell_time)*60)
                    name = photo_list[i].get_local()
                    filename = photo_list[i].get_filename()
                    filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()
                    photo_items[i - k].description = photo_html_block.replace('$NAME$', name).replace('$FILENAME$', filename)

        os.chdir(r'C:\Users\Nathan\Desktop')
        kml.save('Test.kml')







