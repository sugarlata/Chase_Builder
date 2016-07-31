import arrow
import simplekml
import os
from radar_db import RadarDB


def create_radar_kml(frame_db, root_path, radar_path, tz):

    radar_db = RadarDB('IDR023')
    kml = simplekml.Kml()
    kml_folders = []

    for k in range(0, len(frame_db)):
        ground = []
        frame_list = frame_db[k]
        idr_code = frame_list[0].get_filename().split('.')[0]
        print idr_code
        radar_db.select_radar(idr_code)
        kml_folders.insert(len(kml_folders), kml.newfolder(name=idr_code))
        for i in range(0,len(frame_list)):
            filename = frame_list[i].get_filename()
            ground.insert(len(ground),kml_folders[k].newgroundoverlay(name=filename.split('.')[2]))
            ground[i].icon.href = radar_path + "\\" + filename.split('.')[0] + "\\" + filename
            radar_db.select_radar(idr_code)
            ground[i].latlonbox.north, ground[i].latlonbox.south, ground[i].latlonbox.east, ground[i].latlonbox.west = radar_db.get_nsew(idr_code)
            ground[i].timespan.begin = arrow.get(int(frame_list[i].get_time()))
            ground[i].timespan.end = arrow.get(int(frame_list[i].get_time()) + (60*6))

    os.chdir(root_path)
    kml.save("Radar - test.kml")

