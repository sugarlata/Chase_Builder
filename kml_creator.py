import arrow
import simplekml
import os
from radar_db import RadarDB

# Moethod for creating a trimmed GPS Track
def create_gps_track_kml(gps_track, start_time, end_time, root_path, gps_track_filename, tz):

    # Create a kml object
    kml = simplekml.Kml(name="Chase Track", open=1)

    # Create the kml filename. This will be the original file, with '-trimmed' added onto the end of it.
    trimmed_kml_filename = root_path + "/" + os.path.splitext(os.path.basename(gps_track_filename))[0] + "-trimmed.kml"

    when = []
    coordinates = []
    new_gps_track = []
    start_position = 0
    end_position = 0

    # gps_track[] is the full list. Need to find the trim points. Look through the list and find the start and end point
    for i in range(0, len(gps_track)):
        if gps_track[i].get_time() == start_time:
            start_position = i
        if gps_track[i].get_time() == end_time:
            end_position = i

    # Create new track lists from data between start trim and end trim
    for i in range(start_position, end_position):
        when.append(gps_track[i].get_iso_time())
        coordinates.append(gps_track[i].get_location())
        new_gps_track.append(gps_track[i])


    time_now = arrow.now(tz)

    doc = kml.newdocument(name='Chase Builder', snippet=simplekml.Snippet('Created ' +
                                                                          time_now.format('YYYY-MM-DD HH:mm:ss')))

    fol = doc.newfolder(name='Track')

    schema = kml.newschema()

    trk = fol.newgxtrack(name='Trimmed Track')

    trk.extendeddata.schemadata.schemaurl = schema.id

    trk.newwhen(when)
    trk.newgxcoord(coordinates)
    trk.stylemap.normalstyle.iconstyle.icon.href =\
        'http://earth.google.com/images/kml-icons/track-directional/track-0.png'
    trk.stylemap.normalstyle.linestyle.color = '99ffac59'
    trk.stylemap.normalstyle.linestyle.width = 6

    kml.save(trimmed_kml_filename)
    return trimmed_kml_filename, new_gps_track


def create_radar_kml(frame_db, root_path, radar_path, tb):

    tb.tb_update("")
    tb.tb_update("Creating KML File")
    tb.tb_update("")

    radar_db = RadarDB('IDR023')
    kml = simplekml.Kml()
    kml_folders = []

    # Create a KML file. In the kml file there should be a folder for each radar location and type
    # Inside this folder will be the radar frames.
    # The variable 'ground' will be a list of overlays - the radar frames.
    # The variable 'kml_folders' will be a list of folder objects.
    # Overlay objects are added to the folder object through the method kml_folders.newgroundoverlay
    # These objects are added to the list 'ground'

    # For each IDR subset in frame_db
    # Frame db is a list of lists. The sub lists contains the frame overlay objects.
    # Frame db, is a list of each IDRCode this applies to
    for k in range(0, len(frame_db)):

        # List of ground overlay objects
        ground = []

        # List of radar overlay objects
        frame_list = frame_db[k]

        # Get the IDR Code. Each frame in the sub list will be identical
        idr_code = frame_list[0].get_filename().split('.')[0]
        radar_title = ""
        radar_db.select_radar(idr_code)
        if idr_code[-1:] == "I":
            radar_title = radar_db.get_title(idr_code) + " 128km Doppler Wind (" + idr_code + ")"
        elif idr_code[-1:] == "2":
            radar_title = radar_db.get_title(idr_code) + " 256km Rain (" + idr_code + ")"
        elif idr_code[-1:] == "3":
            radar_title = radar_db.get_title(idr_code) + " 128km Rain (" + idr_code + ")"
        elif idr_code[-1:] == "4":
            radar_title = radar_db.get_title(idr_code) + " 64km Rain (" + idr_code + ")"

        # Want to create a new KML folder for this specific radar IDRCode.
        kml_folders.insert(len(kml_folders), kml.newfolder(name=radar_title))

        # Cycle through each overlay frame in frame_list
        for i in range(0, len(frame_list)):
            filename = frame_list[i].get_filename()

            # Create a new ground overlay in kml_folders, keep this object in the 'ground' list.
            ground.insert(len(ground), kml_folders[k].newgroundoverlay(name=filename.split('.')[2]))

            # Set the details for this ground overlay
            # What image will be over-layed
            ground[i].icon.href = radar_path + "\\" + filename.split('.')[0] + "\\" + filename
            radar_db.select_radar(idr_code)

            # What the position of the image will be
            ground[i].latlonbox.north, ground[i].latlonbox.south, ground[i].latlonbox.east, ground[i].latlonbox.west =\
                radar_db.get_nsew(idr_code)

            # When the over-layed image will be shown and hidden
            ground[i].timespan.begin = arrow.get(int(frame_list[i].get_time()))
            ground[i].timespan.end = arrow.get(int(frame_list[i].get_end_time()))

    # Change the folder to the root path, this is where the kml file will be saved
    os.chdir(root_path)

    # Save the KML file
    kml.save("Radar.kml")

    tb.tb_update("")
    tb.tb_update("Finished Creating the Radar KML File")
    tb.tb_update("")


def create_media_kml(root_path, media_path, photo_list, video_list, time_list, dwell_time, tb):
    # Create HTML Blocks for Photos and Videos:

    photo_html_block = r"""<![CDATA[<font size = "18">
$NAME$</font>
<img src="$FILENAME$"/><font size = 18><br><br></font>]]>"""

    video_html_block = r"""<![CDATA[<font size = "18">$NAME$</font><OBJECT ID="MediaPlayer" width="720" height="576"
    CLASSID="CLSID:22D6F312-B0F6-11D0-94AB-0080C74C7E95" CODEBASE="http://activex.microsoft.com/activex/controls/
    mplayer/en/nsmp2inf.cab#Version=5,1,52,701" STANDBY="Loading Windows Media Player components..." TYPE="application/
    x-oleobject">
<param name="fileName" value="$FILENAME$">
<param name="autoStart" value="False">
<param name="showControls" value="True">
<param name="ShowStatusBar" value="True">
<param name="ShowDisplay" VALUE="True">
<embed type="application/x-mplayer2" src="$FILENAME$" name="MediaPlayer" width="720" height="576" ShowControls="1"
ShowStatusBar="1" ShowDisplay="1" autostart="0"> </embed>
</object>
<font size = 18><br><br></font>]]>"""

    # Create the media kml. Firstly need to create the photo objects
    # Test that photo_list isn't empty
    # Firstly, create a kml object that will have folders added to it
    # Also create a list for the folders to go in

    kml = simplekml.Kml()
    kml_folders = []

    if len(photo_list) == 0:
        tb.tb_update("There are no photos")
    else:
        # There are photos to process
        # Need to create a kml folder for photos, then create the objects in this folder.
        # Create a list for photo objects to go into

        photo_items = []

        # Create the Photo folder inside the kml, keep this in the kml_folders list.
        kml_folders.insert(len(kml_folders), kml.newfolder(name='Photos'))
        k = 0

        # This is the iteration for photos i.e. kml_folders[0]
        for i in range(0, len(photo_list)):

            if i == 0:

                # If this is the first iteration, i.e. first photo in a group

                # Create a new point in the kml folder. Keep this point in the photo_items list.
                # Currently set the name of the group to the group number. After creating the groups, will change this
                # to the location of the group (using geocode info returned from Google)
                photo_items.append(kml_folders[len(kml_folders)-1].newpoint(name=str(photo_list[i].get_group_number())))
                lat, lon = photo_list[i].get_location()
                photo_items[i - k].coords = [(lon, lat)]

                # Photo icons will be the green circle
                photo_items[i - k].style.iconstyle.icon.href = \
                    'http://maps.google.com/mapfiles/kml/paddle/ltblu-stars.png'

                # Set the begin and end time
                photo_items[i - k].timespan.begin = photo_list[i].get_iso()
                photo_items[i - k].timespan.end = arrow.get(photo_list[i].get_epoch() + int(dwell_time) * 60)
                name = photo_list[i].get_local()
                filename = media_path + "\\" + photo_list[i].get_filename()
                filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()

                # Add the html block into the description, changing the $NAME$ tag and $FILENAME$ Tag
                # Currently defaulting to using the local time as the name of the photo, or at least what to put in
                # that field
                photo_items[i - k].description = photo_html_block.replace('$NAME$', name).replace('$FILENAME$',
                                                                                                  filename)
                continue

            for j in range(0, i):

                # Need to check through each previous photo in the list and see whether it has an identical group number
                # If it does, then most of the information is set and all that has to be done is add in the html code.
                # If it cycles through all photos in the list and there isn't a matching group number then have to
                # create a new one with html description of the photo

                if photo_list[i].get_group_number() == photo_list[j].get_group_number():
                    # Add HTML Code to current place mark

                    # Have identified that there is a matching group number, need to find where in the list this is
                    # though.

                    # Cycle through the list and find the right photo item that has matching group number
                    for l in range(0, len(photo_items)):
                        if photo_items[l].name == str(photo_list[j].get_group_number()):
                            name = photo_list[i].get_local()
                            filename = media_path + "\\" + photo_list[i].get_filename()
                            filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()

                            # Add in the html block
                            photo_items[l].description += photo_html_block.replace('$NAME$', name).replace('$FILENAME$',
                                                                                                           filename)
                            break

                    k += 1
                    break

                elif j == i-1:

                    # If a group number can't be matched then have to create a new point
                    # Exactly the same as on the first iteration
                    photo_items.append(kml_folders[0].newpoint(name=str(photo_list[i].get_group_number())))
                    lat, lon = photo_list[i].get_location()
                    photo_items[i-k].coords = [(lon, lat)]
                    photo_items[i-k].style.iconstyle.icon.href =\
                        'http://maps.google.com/mapfiles/kml/paddle/ltblu-stars.png'
                    photo_items[i-k].timespan.begin = photo_list[i].get_iso()
                    photo_items[i-k].timespan.end = arrow.get(photo_list[i].get_epoch()+int(dwell_time)*60)
                    name = photo_list[i].get_local()
                    filename = media_path + "\\" + photo_list[i].get_filename()
                    filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()
                    photo_items[i - k].description = photo_html_block.replace('$NAME$', name).replace('$FILENAME$',
                                                                                                      filename)

    # Next is to add in the videos

    # Code is identical, except deals with the video side of things
    if len(video_list) == 0:
        tb.tb_update("There are no videos")
    else:
        # There are videos to process
        # Need to create a kml folder for videos, then create the objects in this folder.
        # Create a list for video objects to go into

        video_items = []

        # Create the Video folder inside the kml, keep this in the kml_folders list.
        kml_folders.insert(len(kml_folders), kml.newfolder(name='Videos'))
        k = 0

        # This is the iteration for videos i.e. kml_folders[1]
        for i in range(0, len(video_list)):

            if i == 0:
                # If this is the first iteration, i.e. first video in a group

                # Create a new point in the kml folder. Keep this point in the video_items list.
                # Currently set the name of the group to the group number. After creating the groups, will change this
                # to the location of the group (using geocode info returned from Google)
                print video_list[i].get_group_number()
                print len(kml_folders)

                video_items.append(kml_folders[len(kml_folders)-1].newpoint(name=str(video_list[i].get_group_number())))
                lat, lon = video_list[i].get_location()
                video_items[i - k].coords = [(lon, lat)]

                # Video icons will be the green circle
                video_items[i - k].style.iconstyle.icon.href = \
                    'http://maps.google.com/mapfiles/kml/paddle/go.png'

                # Set the begin and end time
                video_items[i - k].timespan.begin = video_list[i].get_iso()
                video_items[i - k].timespan.end = arrow.get(video_list[i].get_epoch() + int(dwell_time) * 60)
                name = video_list[i].get_local()
                filename = media_path + "\\" + video_list[i].get_filename()
                filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()

                # Add the html block into the description, changing the $NAME$ tag and $FILENAME$ Tag
                # Currently defaulting to using the local time as the name of the video, or at least what to put in
                # that field
                video_items[i - k].description = video_html_block.replace('$NAME$', name).replace('$FILENAME$',
                                                                                                  filename)
                continue

            for j in range(0, i):

                # Need to check through each previous video in the list and see whether it has an identical group number
                # If it does, then most of the information is set and all that has to be done is add in the html code.
                # If it cycles through all videos in the list and there isn't a matching group number then have to
                # create a new one with html description of the video

                if video_list[i].get_group_number() == video_list[j].get_group_number():
                    # Add HTML Code to current place mark

                    # Have identified that there is a matching group number, need to find where in the list this is
                    # though.

                    # Cycle through the list and find the right video item that has matching group number
                    for l in range(0, len(video_items)):
                        if video_items[l].name == str(video_list[j].get_group_number()):
                            name = video_list[i].get_local()
                            filename = media_path + "\\" + video_list[i].get_filename()
                            filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()

                            # Add in the html block
                            video_items[l].description += video_html_block.replace('$NAME$', name).replace('$FILENAME$',
                                                                                                           filename)
                            break

                    k += 1
                    break

                elif j == i - 1:

                    # If a group number can't be matched then have to create a new point
                    # Exactly the same as on the first iteration
                    video_items.append(kml_folders[0].newpoint(name=str(video_list[i].get_group_number())))
                    lat, lon = video_list[i].get_location()
                    video_items[i - k].coords = [(lon, lat)]
                    video_items[i - k].style.iconstyle.icon.href = \
                        'http://maps.google.com/mapfiles/kml/paddle/go.png'
                    video_items[i - k].timespan.begin = video_list[i].get_iso()
                    video_items[i - k].timespan.end = arrow.get(video_list[i].get_epoch() + int(dwell_time) * 60)
                    name = video_list[i].get_local()
                    filename = media_path + "\\" + video_list[i].get_filename()
                    filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()
                    video_items[i - k].description = video_html_block.replace('$NAME$', name).replace('$FILENAME$',
                                                                                                      filename)\


    # Last is to add in the time lapse

    # Code is identical, except deals with the time lapse side of things
    if len(time_list) == 0:
        tb.tb_update("There are no time lapse videos")
    else:
        # There are time lapse videos to process
        # Need to create a kml folder for time lapse videos, then create the objects in this folder.
        # Create a list for time lapse video objects to go into

        time_items = []

        # Create the Photo folder inside the kml, keep this in the kml_folders list.
        kml_folders.insert(len(kml_folders), kml.newfolder(name='Videos'))
        k = 0

        # This is the iteration for time lapse videos i.e. kml_folders[1]
        for i in range(0, len(time_list)):

            if i == 0:
                # If this is the first iteration, i.e. first time lapse video in a group

                # Create a new point in the kml folder. Keep this point in the video_items list.
                # Currently set the name of the group to the group number. After creating the groups, will change this
                # to the location of the group (using geocode info returned from Google)
                time_items.append(kml_folders[len(kml_folders)-1].newpoint(name=str(time_list[i].get_group_number())))
                lat, lon = time_list[i].get_location()
                time_items[i - k].coords = [(lon, lat)]

                # Video icons will be the green circle
                time_items[i - k].style.iconstyle.icon.href = \
                    'http://maps.google.com/mapfiles/kml/paddle/wht-diamond.png'

                # Set the begin and end time
                time_items[i - k].timespan.begin = time_list[i].get_iso()
                time_items[i - k].timespan.end = arrow.get(time_list[i].get_epoch() + int(dwell_time) * 60)
                name = time_list[i].get_local()
                filename = media_path + "\\" + time_list[i].get_filename()
                filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()

                # Add the html block into the description, changing the $NAME$ tag and $FILENAME$ Tag
                # Currently defaulting to using the local time as the name of the time lapse video, or at least
                # what to put in that field
                time_items[i - k].description = video_html_block.replace('$NAME$', name).replace('$FILENAME$',
                                                                                                 filename)
                continue

            for j in range(0, i):

                # Need to check through each previous video in the list and see whether it has an identical group number
                # If it does, then most of the information is set and all that has to be done is add in the html code.
                # If it cycles through all videos in the list and there isn't a matching group number then have to
                # create a new one with html description of the video

                if time_list[i].get_group_number() == time_list[j].get_group_number():
                    # Add HTML Code to current place mark

                    # Have identified that there is a matching group number, need to find where in the list this is
                    # though.

                    # Cycle through the list and find the right time lapse video item that has matching group number
                    for l in range(0, len(time_items)):
                        if time_items[l].name == str(time_list[j].get_group_number()):
                            name = time_list[i].get_local()
                            filename = media_path + "\\" + time_list[i].get_filename()
                            filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()

                            # Add in the html block
                            time_items[l].description += video_html_block.replace('$NAME$', name).replace('$FILENAME$',
                                                                                                          filename)
                            break

                    k += 1
                    break

                elif j == i - 1:

                    # If a group number can't be matched then have to create a new point
                    # Exactly the same as on the first iteration
                    time_items.append(kml_folders[0].newpoint(name=str(time_list[i].get_group_number())))
                    lat, lon = time_list[i].get_location()
                    time_items[i - k].coords = [(lon, lat)]
                    time_items[i - k].style.iconstyle.icon.href = \
                        'http://maps.google.com/mapfiles/kml/paddle/wht-diamond.png'
                    time_items[i - k].timespan.begin = time_list[i].get_iso()
                    time_items[i - k].timespan.end = arrow.get(time_list[i].get_epoch() + int(dwell_time) * 60)
                    name = time_list[i].get_local()
                    filename = media_path + "\\" + time_list[i].get_filename()
                    filename = "file:///" + filename.replace("\\", "/").replace(" ", "%20").lower()
                    time_items[i - k].description = video_html_block.replace('$NAME$', name).replace('$FILENAME$',
                                                                                                     filename)

    if len(kml_folders) == 0:
        tb.tb_update("There was no media found")
    else:
        os.chdir(root_path)
        kml.save('Media.kml')
