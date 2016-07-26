import arrow

class GPSPoint:

    __timePoint__ = int()
    __lat__ = float()
    __lon__ = float()
    __height__ = float()
    __timeISO__ = str()
    __timeLocal__ = str()


    def __init__(self,epoch,lat,lon, height,tz):
        self.__timePoint__ = epoch
        self.__lat__ = lat
        self.__lon__ = lon
        self.__height__ = height
        self.__timeISO__ = arrow.get(epoch)
        self.__timeLocal__ = self.__timeISO__.to(tz).format('YYYY-MM-DD HH:mm:ss')

    def getTime(self):
        return self.__timePoint__

    def getFull(self):
        return self.__lat__, self.__lon__, self.__height__

    def getLocation(self):
        return self.__lat__, self.__lon__

    def getHeight(self):
        return self.__height__

    def getLocalTime(self):
        return self.__timeLocal__

    def getISOTime(self):
        return self.__timeISO__
