from media import MediaObject
from win32api import GetSystemMetrics
import PIL.Image
import PIL.ExifTags
import arrow
import math
import os
import gps_methods


def check_media_path_exists(media_path):
    try:
        os.chdir(media_path)
    except WindowsError:
        return False
    return True


def gui_download_place_names():
    # TODO Write this gui
    return False


def get_photo_list(media_path):

    photo_filename_list = []
    for x in os.listdir(media_path):

        if x.lower()[-4:] == "jpeg" or x.lower()[-3:] == "jpg":
            if x.lower()[:2] != "r-":
                photo_filename_list.insert(len(photo_filename_list), x)

    return photo_filename_list


def get_photo_exif_data(media_path, photo_filename_list, start_time, end_time, tz):

    rejected_photo_filename_list = []
    exif_time_pattern = 'YYYY:MM:DD HH:mm'
    photo_list = []

    for i in range(0, len(photo_filename_list)):
        skip_photo = False

        image_filename = media_path + "\\" + photo_filename_list[i]
        image = PIL.Image.open(image_filename)
        picture_time_raw = ""

        try:
            exif = {
                PIL.ExifTags.TAGS[k]: v
                for k, v in image._getexif().items()
                if k in PIL.ExifTags.TAGS
                }
            picture_time_raw = exif['DateTime']
        except KeyError:
            print ""
            print photo_filename_list[i] + ":"
            print "No exif Data for time taken, either manually select the time created or skip this photo"
            skip_photo = True
        except AttributeError:
            print ""
            print photo_filename_list[i] + ":"
            print "No exif Data, either manually select the time created or skip this photo"
            skip_photo = True

        if skip_photo:
            rejected_photo_filename_list.insert(len(rejected_photo_filename_list), photo_filename_list[i])
        else:

            photo_iso = arrow.get(picture_time_raw, exif_time_pattern).replace(tzinfo=tz)
            photo_epoch = int(photo_iso.timestamp)
            start_time = int(start_time)
            end_time = int(end_time)

            if photo_epoch < start_time or photo_epoch > end_time:
                print ""
                print photo_filename_list[i], "was not taken during the specified chase time"
                rejected_photo_filename_list.insert(len(rejected_photo_filename_list), photo_filename_list[i])

            else:

                photo_list.insert(len(photo_list), MediaObject(photo_epoch, photo_filename_list[i], 0, 0, tz))

    return photo_list, rejected_photo_filename_list


def set_media_location(media_list, gps_track):

    for i in range(0, len(media_list)):
        last_difference = 259200
        first_run = True
        max_difference = 259200

        for j in range(0,len(gps_track)):

            gps_point_time = gps_track[j].get_time()
            difference = int(math.fabs(int(media_list[i].get_epoch()) - int(gps_point_time)))

            if difference > last_difference:

                gps_point = gps_track[j-1].get_location()
                media_list[i].set_location(gps_point[1], gps_point[0])
                last_difference = 259200
                break

            else:

                last_difference = difference

    return media_list


def set_resized_photos(media_path, photo_list):

    for i in range(0, len(photo_list)):
        print ""
        print "(" + str(i + 1) + "/" + str(len(photo_list)) + ") Creating a resized version of " + str(
            photo_list[i].get_filename())

        image = PIL.Image.open(media_path + "\\" + photo_list[i].get_filename())
        image_filename_resized = media_path + "\\r-" + photo_list[i].get_filename()
        image_filename = media_path + "\\" + photo_list[i].get_filename()
        width, height = image.size

        scale1 = float(GetSystemMetrics(0)) / float(width)
        scale2 = float(GetSystemMetrics(1)) / float(height)

        if scale1 < scale2:
            scale = scale1
        else:
            scale = scale2

        if scale < 1:

            os.chdir(media_path)

            if os.path.isfile(image_filename_resized) == False:
                scWidth = scale * width * .95
                scHeight = scale * height * .95

                scHeight = int(round(scHeight))
                scWidth = int(round(scWidth))

                image = image.resize((scWidth, scHeight), PIL.Image.ANTIALIAS)

                image.save(image_filename_resized)
                image_filename = image_filename_resized
            else:
                image_filename = image_filename_resized
                print "Already done"

        photo_list[i].set_filename(image_filename)

    return photo_list


def set_media_groups(media_list):

    k = 1

    # Cycle through each photo in photo list
    for i in range(0, len(media_list)):
        # If it is the first photo, manually set the group
        if i == 0:
            media_list[i].set_group_number(1)
            k += 1

        else:

            # Cycle through the photos list to see if there's a GPS match
            for j in range(0, i):

                # GPS Match is where distance between points is less than 100m
                lat1 = media_list[i].get_location()[0]
                lon1 = media_list[i].get_location()[1]
                lat2 = media_list[j].get_location()[0]
                lon2 = media_list[j].get_location()[1]

                distance = gps_methods.get_distance_from_coordinates(lat1, lon1, lat2, lon2)

                if distance < 100:
                    media_list[i].set_group_number(media_list[j].get_group_number())
                    break

                if j == i - 1:
                    media_list[i].set_group_number(k)
                    k += 1


def get_video_list(media_path):

    video_filename_list = []
    for x in os.listdir(media_path):

        if x.lower()[-3:] == "mov" or x.lower()[-3:] == "avi" or x.lower()[-3:] == "mpg" or x.lower()[-3:] == "mp4" or x.lower()[-3:] == "mpeg":
            if x.lower()[:2] != "r-":
                video_filename_list.insert(len(video_filename_list), x)

    return video_filename_list


def set_video_time(video_filename_list, pattern_list, tz):

    # Need to match the video to the possible time code
    video_list = []
    rejected_video_filename_list = []
    for i in range(0, len(video_filename_list)):
        # Split the filename on the dot, take the first split
        filename = video_filename_list[i]
        filename = os.path.splitext(filename)[0]
        for j in range(0, len(pattern_list)):
            # Strip string in pattern list
            filename = filename.replace(pattern_list[j][1], '')
            if filename[-10:]=="-timelapse":
                break

            try:
                video_iso = arrow.get(filename, pattern_list[j][0]).replace(tzinfo=tz)
                video_epoch = int(video_iso.timestamp)
                video_list.insert(len(video_list), MediaObject(video_epoch, video_filename_list[i], 0, 0, tz))
                break
            except arrow.parser.ParserError:
                if j==len(pattern_list)-1:
                    print "Could not match time for" , filename
                    rejected_video_filename_list.insert(len(rejected_video_filename_list), video_filename_list[i])

    return video_list, rejected_video_filename_list


def get_time_list(media_path, pattern_list, tz):

    media_paths = [x[0] for x in os.walk(media_path)]
    time_path_list = []
    for i in range(0, len(media_paths)):
        time_path = media_paths[i].split('\\')[-1]

        if time_path=="Media":
            continue

        for j in range(0, len(pattern_list)):
            try:
                time_iso = arrow.get(time_path, pattern_list[j][0]).replace(tzinfo=tz)
                time_path_list.insert(len(time_path_list), time_path)
            except arrow.parser.ParserError:
                if j == len(pattern_list) - 1:
                    print "The time code for folder", time_path, "in Media\ could not be interpreted"

    return time_path_list


def create_time_lapse_video(ffmpeg_location, media_path, time_path_list, frame_rate):

    # Example of command line call
    # "C:\Users\Nathan\Documents\Development\Chaselog\Chaselog\ffmpeg.exe" -f image2 -r 25
    # -start_number 00000001 -i Proj16_img%08d.jpg -s 1920x1080 -vcodec libx264 timelapse.mp4

    for i in range(0, len(time_path_list)):
        if (os.path.isfile(media_path + "\\" + time_path_list[i] + "-timelapse.mp4")) != True:
            os.chdir(media_path + "\\" + time_path_list[i])
            ffmpegCommand = ffmpeg_location
            for f in os.listdir(media_path + "\\" + time_path_list[i]):

                if f[:4] == "Proj" and f[-3:].lower() == "jpg":
                    image_filename = media_path + "\\" + time_path_list[i] + "\\" + f
                    image = PIL.Image.open(image_filename)
                    width, height = image.size
                    base_filename = f[:-12]
                    break

            ffmpegOpts = " -f image2 -r " + str(
                frame_rate) + " -start_number 00000001 -i " + base_filename + "%08d.jpg -s "\
                         + str(width) + "x" + str(height) + " -vcodec libx264 " + time_path_list[i]\
                         + "-timelapse.mp4"
            os.system(ffmpegCommand + ffmpegOpts)
            os.rename(time_path_list[i] + "-timelapse.mp4", media_path + "\\" + time_path_list[i] + "-timelapse.mp4")

        else:
            print time_path_list[i] + ".mp4 already rendered"


def set_time_time(time_path_list, pattern_list, tz):
    time_list=[]
    for i in range(0, len(time_path_list)):
        time_path = time_path_list[i]
        for j in range(0, len(pattern_list)):
            try:
                time_iso = arrow.get(time_path, pattern_list[j][0]).replace(tzinfo=tz)
                time_epoch = int(time_iso.timestamp)
                time_path_list.insert(len(time_path_list), MediaObject(time_epoch, time_path + ".mp4", 0, 0, tz))
            except arrow.parser.ParserError:
                if j == len(pattern_list) - 1:
                    print "There was an error matching the time for video", time_path + ".mp4"

    return time_list

def process_media(root_path, media_path, ffmpeg_location, gps_track, start_time, end_time, tz):

    # List of patterns for matching time codes. Second item in list is string for removal
    pattern_list = [('YYYY:MM:DD HH:mm:ss', ''), ('YYYYMMDD_HHmmss','VID_'),
                    ('YYYY-MM-DD HH.mm.ss', ''), ('YYYY.MM.DD_HH.mm.ss', '')]

    # Set the Frame Rate
    frame_rate = 25

    # GUI Ask about downloading place names
    dl_place_names = gui_download_place_names()

    # # ---------------------------------- Photo ----------------------------------
    #
    # # Get Photo List
    # photo_filename_list = get_photo_list(media_path)

    # # Check if the list is empty
    #
    # # TODO Code module here for user to manually select what pictures they want in and out.
    # # TODO Need to edit photo_filename_list (along with above)
    #
    # # Get Photo Exif Data (time taken)
    # photo_list, rejected_photos_filename_list = get_photo_exif_data(media_path, photo_filename_list, start_time,
    #                                                                 end_time, tz)
    # # Set the time for leftover photos manually
    # # TODO Write code for this gui
    # if len(rejected_photos_filename_list)!=0:
    #     print ""
    #
    # # Set the location for each picture
    # photo_list = set_media_location(photo_list, gps_track)
    #
    # # Resize photos as necessary
    # set_resized_photos(media_path, photo_list)
    #
    # # Group Photos together
    # set_media_groups(photo_list)

    # # ---------------------------------- Video ----------------------------------
    #
    # # Get video list
    # video_filename_list = get_video_list(media_path)
    #
    # # Check if the list is empty
    #
    # # Get time from filename
    # video_list, rejected_video_filename_list = set_video_time(video_filename_list, pattern_list, tz)
    #
    # # Set the time for leftover videos
    # # TODO Write code for this gui
    #
    # # Set the location for each video
    # video_list = set_media_location(video_list, gps_track)
    #
    # # Group Videos as necessary
    # set_media_groups(video_list)

    # ---------------------------------- Time Lapse ----------------------------------

    # Get Time lapse List
    time_path_list = get_time_list(media_path, pattern_list, tz)

    # Create the video
    create_time_lapse_video(ffmpeg_location, media_path, time_path_list, frame_rate)

    # Create db of videos and the time they were taken
    time_list = set_time_time(time_path_list, pattern_list, tz)

    # Set the time for leftover videos
    # TODO Write code for this gui

    # Set the location for each video
    time_list = set_media_location(time_list, gps_track)

    # Group videos as necessary
    set_media_groups(time_list)

    # ---------------------------------- KML ----------------------------------

    # Create the Media KML
