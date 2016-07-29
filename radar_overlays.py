

class RadarFrame:

    __filename__ = str()
    __time__ = int()

    def __init__(self, time, filename):
        # TODO Need to write code to interpret the time based on the filename
        self.__filename__=filename
        self.__time__=time

    def get_filename(self):
        return self.__filename__

    def get_time(self):
        return self.__time__
