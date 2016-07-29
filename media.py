import arrow

class Photo:

    __epoch__ = int()
    __localtime__ = str()
    __ISO__ = str()
    __lat__ = float()
    __lon__ = float()
    __fn__ = str()
    __groupnumber__ = int()
    __tz__ = str()

    def __init__(self, epoch, fn, lat, lon, tz):
        self.__epoch__ = epoch
        self.__fn__ = fn
        self.__lat__=lat
        self.__lon__=lon
        self.__ISO__=arrow.get(epoch)
        self.__localtime__ = self.__ISO__.to(tz).format('YYYY-MM-DD HH:mm:ss')

    def getEpoch(self):
        return self.__epoch__

    def getLocal(self):
        return self.__localtime__

    def getISO(self):
        return self.__ISO__

    def getLocation(self):
        return self.__lat__, self.__lon__

    def getFilename(self):
        return self.__fn__

    def setFilename(self,fn):
        self.__fn__ = fn

    def getGroupNumber(self):
        return self.__group__

    def setGroupNumber(self, gn):
        self.__group__ = gn

    def getTZ(self):
        return self.__tz__


class Video:
    __epoch__ = int()
    __localtime__ = str()
    __ISO__ = str()
    __lat__ = float()
    __lon__ = float()
    __fn__ = str()
    __groupnumber__ = int()
    __tz__ = str()

    def __init__(self, epoch, fn, lat, lon, tz):

        self.__epoch__ = epoch
        self.__fn__ = fn
        self.__lat__ = lat
        self.__lon__ = lon
        self.__ISO__ = arrow.get(epoch)
        self.__localtime__ = self.__ISO__.to(tz).format('YYYY-MM-DD HH:mm:ss')

    def getEpoch(self):
        return self.__epoch__

    def getLocal(self):
        return self.__localtime__

    def getISO(self):
        return self.__ISO__

    def getLocation(self):
        return self.__lat__, self.__lon__

    def getFilename(self):
        return self.__fn__

    def setFilename(self, fn):
        self.__fn__ = fn

    def getGroupNumber(self):
        return self.__group__

    def setGroupNumber(self, gn):
        self.__group__ = gn

    def getTZ(self):
        return self.__tz__


class Timelapse:
    __epoch__ = int()
    __localtime__ = str()
    __ISO__ = str()
    __lat__ = float()
    __lon__ = float()
    __fn__ = str()
    __groupnumber__ = int()
    __tz__ = str()

    def __init__(self, epoch, fn, lat, lon, tz):
        self.__epoch__ = epoch
        self.__fn__ = fn
        self.__lat__ = lat
        self.__lon__ = lon
        self.__ISO__ = arrow.get(epoch)
        self.__localtime__ = self.__ISO__.to(tz).format('YYYY-MM-DD HH:mm:ss')

    def getEpoch(self):
        return self.__epoch__

    def getLocal(self):
        return self.__localtime__

    def getISO(self):
        return self.__ISO__

    def getLocation(self):
        return self.__lat__, self.__lon__

    def getFilename(self):
        return self.__fn__

    def setFilename(self, fn):
        self.__fn__ = fn

    def getGroupNumber(self):
        return self.__group__

    def setGroupNumber(self, gn):
        self.__group__ = gn

    def getTZ(self):
        return self.__tz__
