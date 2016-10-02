import arrow


class MediaObject:

    # Media object has variable as named below
    __location_name__ = str()
    __epoch__ = int()
    __localtime__ = str()
    __iso__ = str()
    __lat__ = float()
    __lon__ = float()
    __fn__ = str()
    __group_number__ = int()
    __tz__ = str()

    # When creating a Media Object, all that is required is to tell the epoch. Will automatically calculate the iso
    # and local time
    def __init__(self, epoch, fn, lat, lon, tz):
        self.__epoch__ = epoch
        self.__fn__ = fn
        self.__lat__ = lat
        self.__lon__ = lon
        self.__iso__ = arrow.get(epoch)
        self.__localtime__ = self.__iso__.to(tz).format('YYYY-MM-DD HH:mm:ss')
        self.__location_name__ = ""

    # Getters and Setters as needed
    def get_epoch(self):
        return self.__epoch__

    def get_local(self):
        return self.__localtime__

    def get_iso(self):
        return self.__iso__

    def get_location(self):
        return self.__lat__, self.__lon__

    def set_location(self, lat, lon):
        self.__lat__ = lat
        self.__lon__ = lon

    def get_filename(self):
        return self.__fn__

    def set_filename(self, fn):
        self.__fn__ = fn

    def get_group_number(self):
        return self.__group_number__

    def set_group_number(self, gn):
        self.__group_number__ = gn

    def get_location_name(self):
        return self.__location_name__

    def set_location_name(self, location_name):
        self.__location_name__ = location_name

    def get_tz(self):
        return self.__tz__
