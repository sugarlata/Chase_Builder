import arrow


class GPSPoint:

    # Declare all variables for each GPS point
    __timePoint__ = int()
    __lat__ = float()
    __lon__ = float()
    __height__ = float()
    __timeISO__ = str()
    __timeLocal__ = str()

    # Upon creation, will need the epoch, location, height and timezone
    def __init__(self,epoch,lat,lon, height,tz):
        self.__timePoint__ = epoch
        self.__lat__ = lat
        self.__lon__ = lon
        self.__height__ = height
        # ISO time and Local time can be derived from the epoch.
        self.__timeISO__ = arrow.get(epoch)
        self.__timeLocal__ = self.__timeISO__.to(tz).format('YYYY-MM-DD HH:mm:ss')

    def get_time(self):
        return self.__timePoint__

    def get_full_location(self):
        return self.__lat__, self.__lon__, self.__height__

    def get_location(self):
        return self.__lat__, self.__lon__

    def get_height(self):
        return self.__height__

    def get_local_time(self):
        return self.__timeLocal__

    def get_iso_time(self):
        return self.__timeISO__
