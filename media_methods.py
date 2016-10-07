from media import MediaObject
from win32api import GetSystemMetrics
import PIL.Image
import PIL.ExifTags
import arrow
import arrow.parser
import math
import os
import gps_methods


def check_media_path_exists(media_path):
    # Change path to the media path, if error comes up, path doesn't exist. Catch error return false.
    try:
        os.chdir(media_path)
    except WindowsError:
        return False
    return True


def gui_download_place_names():
    # Not sure what this is used for yet.
    return False


def get_photo_list(media_path):
    # Create a list that will contain all the file names of the photos
    photo_filename_list = []
    for x in os.listdir(media_path):

        # Iterate through each file in the media folder. If the extension is jpeg or jpg, add to the file names list.

        # --------------------------------------------------------------------
        # **** For support of more photo extension types, edit code below ****
        # --------------------------------------------------------------------

        if x.lower()[-4:] == "jpeg" or x.lower()[-3:] == "jpg":
            if x.lower()[:2] != "r-":
                photo_filename_list.insert(len(photo_filename_list), x)

    # Return the list of filenames of photos
    return photo_filename_list


def get_photo_exif_data(media_path, photo_filename_list, start_time, end_time, tz, tb):

    # Create two lists, one that will have photo objects, the other is a list of file names that could not be
    # time matched. This list will later be used to manually set the time for them and added as photo objects into the
    # first list if needed.
    # This will happen in a different method however.
    rejected_photo_filename_list = []
    exif_time_pattern = 'YYYY:MM:DD HH:mm'
    photo_list = []

    # Go through the entire list of file names
    for i in range(0, len(photo_filename_list)):
        skip_photo = False

        # Open the image, create an image object.
        image_filename = media_path + "\\" + photo_filename_list[i]
        image = PIL.Image.open(image_filename)
        picture_time_raw = ""

        # Need to firstly try and get the exif data time codes

        # ---------------------------------------------------------
        # To analyse EXIF data for location also, change code below
        # ---------------------------------------------------------
        try:
            exif = {
                # Try and get the time codes from the EXIF Data
                # Depending on the fail, return (print) the particular error.
                PIL.ExifTags.TAGS[k]: v
                for k, v in image._getexif().items()

                if k in PIL.ExifTags.TAGS
                }
            picture_time_raw = exif['DateTime']

        # Catch the different errors possible thrown by parsing EXIF Tags
        except KeyError:
            tb.tb_update("")
            tb.tb_update(photo_filename_list[i] + ":")
            tb.tb_update("No exif Data for time taken, either manually select the time created or skip this photo")
            skip_photo = True
        except AttributeError:
            tb.tb_update("")
            tb.tb_update(photo_filename_list[i] + ":")
            tb.tb_update("No exif Data, either manually select the time created or skip this photo")
            skip_photo = True

        # If there was an error, add the photo to the rejected photo file names list
        if skip_photo:
            rejected_photo_filename_list.insert(len(rejected_photo_filename_list), photo_filename_list[i])
        else:

            # If no error, get the time the photo was taken, as well as the time boundaries for the chase
            photo_iso = arrow.get(picture_time_raw, exif_time_pattern).replace(tzinfo=tz)
            photo_epoch = int(photo_iso.timestamp)
            start_time = int(start_time)
            end_time = int(end_time)

            # Check if the photo was taken outside the chase time boundary
            if photo_epoch < start_time or photo_epoch > end_time:
                tb.tb_update("")
                tb.tb_update(photo_filename_list[i] + " was not taken during the specified chase time")
                # Add photo to the rejected photo file name list. This means it can be manually time coded later if the
                # user desires
                rejected_photo_filename_list.insert(len(rejected_photo_filename_list), photo_filename_list[i])

            else:
                # Otherwise the photo is ready to go, and add the media object into the photo_list
                photo_list.append(MediaObject(photo_epoch, photo_filename_list[i], 0, 0, tz))

    # Return the list of photo objects, and well as the rejected photo file name list
    return photo_list, rejected_photo_filename_list


def set_media_location(media_list, gps_track):

    # Need to get the geographic location for time-coded media objects

    # To start, for each media object in the media_list
    for i in range(0, len(media_list)):

        # To find the position (location), need to find the closest gps_point to when the media was created
        # Need to cycle through all gps_points and find the one closest to the media time.
        # After each gps point iteration, the difference between the media time and gps point should decrease
        # Once this hits a minimum, then the time is selected and the gps location from that time code is used.
        # This is the maximum number of seconds that a chase could foreseeably go for (3 days).
        last_difference = 259200

        for j in range(0, len(gps_track)):

            # Cycle through the GPS points, get the time of that point

            gps_point_time = gps_track[j].get_time()
            # Calculate the difference between the iterated point and media object
            difference = int(math.fabs(int(media_list[i].get_epoch()) - int(gps_point_time)))

            # If the difference is larger than the difference of last iteration, have found a minimum because
            # the list is linear
            if difference > last_difference:

                # Set the GPS location for the media object, reset the difference variable to max possible
                # This corresponds to an estimation of longest chase possible in seconds. (3 Days)
                gps_point = gps_track[j-1].get_location()
                media_list[i].set_location(gps_point[1], gps_point[0])
                break

            else:
                # If the media time hasn't hit a minimum then the time between it and the iterated point becomes
                # the new differences
                last_difference = difference

    # Return the media list, which will have updated location settings
    return media_list


def set_resized_photos(media_path, photo_list, tb):

    # Need to check through all photos and ensure that a photo has a reasonable size.
    # Iterate through the entire media path list
    for i in range(0, len(photo_list)):
        # Update user on current iteration
        tb.tb_update("")
        tb.tb_update("(" + str(i + 1) + "/" + str(len(photo_list)) + ") Attempting to create a resized version of " +
                     str(photo_list[i].get_filename()))

        # Open file to store the size of the photo
        image = PIL.Image.open(media_path + "\\" + photo_list[i].get_filename())
        image_filename_resized = "r-" + photo_list[i].get_filename()
        image_filename = media_path + "\\" + photo_list[i].get_filename()
        width, height = image.size

        # Get size of the screen. If the image is larger than the screen, a resized copy needs to be created.
        scale1 = float(GetSystemMetrics(0)) / float(width)
        scale2 = float(GetSystemMetrics(1)) / float(height)

        # Find the scale to reduce by. (This is whichever ratio is larger (requires a larger reduction in either
        # x or y plane)
        if scale1 < scale2:
            scale = scale1
        else:
            scale = scale2

        # If the picture needs to be resized (shrunk)
        if scale < 1:

            os.chdir(media_path)

            # Check if there is already a resized version, if not resize and save image in a new file with prefix r-
            # Amend file name in the photo_list objects
            if not os.path.isfile(image_filename_resized):
                sc_width = scale * width * .95
                sc_height = scale * height * .95

                sc_height = int(round(sc_height))
                sc_width = int(round(sc_width))

                image = image.resize((sc_width, sc_height), PIL.Image.ANTIALIAS)

                image.save(media_path + "\\" + image_filename_resized)
                image_filename = image_filename_resized
            else:
                # Already resized, but need to amend the file name
                image_filename = image_filename_resized
                tb.tb_update("Already done")

        photo_list[i].set_filename(image_filename)

    return photo_list


def set_media_groups(media_list):

    # Need to cycle through photos, find out and set groups of media taken at the (near) same location
    # (not same, grouped up to a distance of 300m)

    # Variable for iteration
    k = 1

    # Cycle through each photo in photo list
    for i in range(0, len(media_list)):
        # If it is the first photo, manually set the group
        if i == 0:
            media_list[i].set_group_number(1)
            k += 1

        else:

            # Cycle through the photos list that have already been processed to see if there's
            # a GPS match. ie Distance < 300
            # Only need to cycle through images already processed in outer loop. If there is not
            # a group for any, create a new one

            for j in range(0, i):

                # GPS Match is where distance between points is less than 100m
                lat1 = media_list[i].get_location()[0]
                lon1 = media_list[i].get_location()[1]
                lat2 = media_list[j].get_location()[0]
                lon2 = media_list[j].get_location()[1]

                distance = gps_methods.get_distance_from_coordinates(lat1, lon1, lat2, lon2)

                # If distance is close enough, set the group number to the earlier set group number

                # -------------------------------------------------------------------------
                # If you want to group photos closer together than 300m, change value below
                # -------------------------------------------------------------------------

                if distance < 300:
                    media_list[i].set_group_number(media_list[j].get_group_number())
                    break

                # If it gets the the end of the list and there isn't already a group assigned,
                # assign a new group
                if j == i - 1:
                    media_list[i].set_group_number(k)
                    k += 1


def get_video_list(media_path):

    # Return a list of video file names.
    # Currently the list of valid video formats is avi, mpg, mp4, mpeg, mov
    video_filename_list = []
    for x in os.listdir(media_path):

        # ---------------------------------------------------
        # To support more video files, change filetypes below
        # ---------------------------------------------------

        if x.lower()[-3:] == "mov" or x.lower()[-3:] == "avi" or x.lower()[-3:] == "mpg" or x.lower()[-3:] == "mp4" or \
                        x.lower()[-3:] == "mpeg":
            if x.lower()[:2] != "r-":
                # Ignore anything with r- in it, although this shouldn't be a problem for video media
                video_filename_list.insert(len(video_filename_list), x)

    return video_filename_list


def set_video_time(video_filename_list, pattern_list, start_time, end_time, tz, tb):

    # Need to match the video to the possible time code
    # Similar to the photo code.
    # Difference here is that there is no library or standard metadata format to save this
    # information compared to the photo time
    # Try and work out the time from the filename, using different patterns of time determines by the pattern_list
    # If this works, add a media object into video_list

    video_list = []
    rejected_video_filename_list = []
    start_time = int(start_time)
    end_time = int(end_time)

    # Iterate through each filename in the list
    for i in range(0, len(video_filename_list)):
        # Split the filename on the dot, take the first split, ie. 10497435.avi becomes 10497435
        filename = video_filename_list[i]
        filename = os.path.splitext(filename)[0]
        for j in range(0, len(pattern_list)):
            # Strip string in pattern list

            # ---------------------------------------------
            # Pattern list is declared at the start of main
            # ---------------------------------------------
            filename = filename.replace(pattern_list[j][1], '')

            # If the file has the ending designation -timelapse, it is not classed as a video, but as a time lapse
            if filename[-10:] == "-timelapse":
                break

            try:
                # Try to convert the time according to the pattern_list
                video_iso = arrow.get(filename, pattern_list[j][0]).replace(tzinfo=tz)
                video_epoch = int(video_iso.timestamp)

                # Check to see whether the video was taken during the time or not
                if video_epoch < start_time or video_epoch > end_time:
                    tb.tb_update("")
                    tb.tb_update(video_filename_list[i] + " was not taken during the specified chase time")
                    # Add video to the rejected video file name list. This means it can be manually time coded later
                    # if the user desires
                    rejected_video_filename_list.insert(len(rejected_video_filename_list), video_filename_list[i])
                    break

                else:
                    # Insert the video into the database
                    video_list.insert(len(video_list), MediaObject(video_epoch, video_filename_list[i], 0, 0, tz))
                    # If successful up to this point then match is successful for this video, break loop
                    break

            except arrow.parser.ParserError:
                # If it fails, it will continue to the next iteration in the pattern list
                if j == len(pattern_list)-1:
                    # If it fails and can't find a time, add it to a rejected list for user to determine manually.
                    tb.tb_update("")
                    tb.tb_update("Could not match time for video " + filename)
                    rejected_video_filename_list.insert(len(rejected_video_filename_list), video_filename_list[i])

    return video_list, rejected_video_filename_list


def get_time_list(media_path, pattern_list, tz, tb):

    # Read through the media folder for directories, if there are directories that can be time coded
    # successfully, assume that they are time lapse folders, add to the time_path_list
    # Otherwise, print out warning that the folder could not be time coded
    media_paths = [x[0] for x in os.walk(media_path)]
    time_path_list = []

    # Iterate through the directory names
    for i in range(0, len(media_paths)):
        # Get the directory name
        time_path = media_paths[i].split('\\')[-1]

        # In this list, if will start with "Media" at the top, this has to be skipped
        if time_path == "Media":
            continue

        # Attempt to match time according to pattern list
        for j in range(0, len(pattern_list)):
            try:
                arrow.get(time_path, pattern_list[j][0]).replace(tzinfo=tz)
                time_path_list.insert(len(time_path_list), time_path)
                break
                # Again, if successful, can break here without need to try and match time again.

            # If can't match time
            except arrow.parser.ParserError:
                if j == len(pattern_list) - 1:
                    tb.tb_update("The time code for folder " + time_path + " in Media\ could not be interpreted")

    return time_path_list


def create_time_lapse_video(ffmpeg_location, media_path, time_path_list, frame_rate, tb):

    # Example of command line call
    # "C:\Users\Nathan\Documents\Development\Chaselog\Chaselog\ffmpeg.exe" -f image2 -r 25
    # -start_number 00000001 -i Proj16_img%08d.jpg -s 1920x1080 -vcodec libx264 timelapse.mp4

    # Go through each time coded folder
    for i in range(0, len(time_path_list)):
        # Check if there's already a time lapse file created, if not then:
        if not os.path.isfile(media_path + "\\" + time_path_list[i] + "-timelapse.mp4"):

            # Need to create an ffmpeg command call in two parts
            # First part will hold the ffmpeg executable
            # Second part has the options for rendering the video

            os.chdir(media_path + "\\" + time_path_list[i])
            ffmpeg_command = ffmpeg_location

            # Need to figure out the name of the files to pass into the ffmpeg options
            # An example format:
            # Proj17_img00000014.jpg
            # Need to find the first file that matches this pattern, and create the pattern getting the project number
            # As well as the size to render in the correct size

            base_filename = ""
            width = 0
            height = 0

            for f in os.listdir(media_path + "\\" + time_path_list[i]):

                if f[:4] == "Proj" and f[-3:].lower() == "jpg":
                    image_filename = media_path + "\\" + time_path_list[i] + "\\" + f
                    image = PIL.Image.open(image_filename)
                    width, height = image.size
                    base_filename = f[:-12]
                    break

            # Options argument to pass to ffmpeg
            ffmpeg_opts = " -f image2 -r " + str(
                frame_rate) + " -start_number 00000001 -i " + base_filename + "%08d.jpg -s "\
                + str(width) + "x" + str(height) + " -vcodec libx264 " + time_path_list[i]\
                + "-timelapse.mp4"

            # Call the ffmpeg command with options
            os.system(ffmpeg_command + ffmpeg_opts)

            # Rename the created file and put it in the media folder
            os.rename(time_path_list[i] + "-timelapse.mp4", media_path + "\\" + time_path_list[i] + "-timelapse.mp4")

        else:
            tb.tb_update(time_path_list[i] + ".mp4 already rendered")


def set_time_time(time_path_list, pattern_list, tz, tb):

    # Method to interpret the time code of time lapse folders
    # Each folder will be in the format:
    # 2016.01.03_14.34.42
    # Will make use of the pattern list an add in an entry for this pattern (already done in pattern_list initiation)

    time_list = []
    # Iterate through each timelapse folder, create object for timelapse and set time
    for i in range(0, len(time_path_list)):
        time_path = time_path_list[i]

        # Work through the pattern list trying to match the string to a pattern in the list
        for j in range(0, len(pattern_list)):
            try:
                time_iso = arrow.get(time_path, pattern_list[j][0]).replace(tzinfo=tz)
                time_epoch = int(time_iso.timestamp)
                time_list.insert(len(time_path_list), MediaObject(time_epoch, time_path + "-timelapse.mp4", 0, 0, tz))
                break
            except arrow.parser.ParserError:
                if j == len(pattern_list) - 1:
                    tb.tb_update("There was an error matching the time for video " + time_path + ".mp4")

    return time_list
