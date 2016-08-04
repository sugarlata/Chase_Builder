import arrow


class RadarFrameOnline:

    __filename__ = str()
    __time__ = int()
    __end_time__ = int()

    def __init__(self, time, filename):
        self.__filename__ = filename
        self.__time__ = int(time)
        self.__end_time__ = int(time) + (6 * 60)

    def get_filename(self):
        return self.__filename__

    def get_time(self):
        return self.__time__


class RadarFrameOffline:

    __filename__ = str()
    __time__ = int()
    __end_time__ = int()

    def __init__(self, filename):
        self.__filename__ = filename

        # Need to convert the filename into a time stamp. Here is an example of the filename:
        # IDR02I.T.201510302101.png
        pattern = "YYYYMMDDHHmm"
        time = arrow.get(filename.split('.')[2], pattern)
        self.__time__ = int(time.timestamp)
        self.__end_time__ = int(time.timestamp) + (6 * 60)

    def get_filename(self):
        return self.__filename__

    def get_time(self):
        return self.__time__

    def set_end_time(self, time):
        self.__end_time__ = time

    def get_end_time(self):
        return self.__end_time__
