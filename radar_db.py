import math


class RadarDB:

    __title__ = str()
    __updateInterval__ = int()
    __location__ = float(), float()
    __64__ = False
    __128__ = True
    __256__ = True
    __512__ = True
    __doppler__ = False
    __nsew64__ = float(), float(), float(), float()
    __nsew128__ = float(), float(), float(), float()
    __nsew256__ = float(), float(), float(), float()
    __nsew512__ = float(), float(), float(), float()

    def __init__(self, idr_code):
        idr = str(idr_code[:-1]) + "3"
        self.select_radar(idr)

    def calculate_nsew_s(self):  # Function to return the radar bounds for KML File

        def calculate_nsew(latitude, longitude, distance):

            d = float(distance)
            r = float(6371)

            be = float(math.radians(0))
            lat2 = math.asin(math.sin(latitude) * math.cos(d / r) + math.cos(latitude) * math.sin(d / r) * math.cos(be))

            lat2 = math.degrees(lat2)

            north = lat2

            be = float(math.radians(90))
            lat2 = math.asin(math.sin(latitude) * math.cos(d / r) + math.cos(latitude) * math.sin(d / r) * math.cos(be))
            lon2 = longitude + math.atan2(math.sin(be) * math.sin(d / r) * math.cos(latitude),
                                          math.cos(d / r) - math.sin(latitude) * math.sin(lat2))
            lon2 = math.degrees(lon2)
            east = lon2

            be = float(math.radians(180))
            lat2 = math.asin(math.sin(latitude) * math.cos(d / r) + math.cos(latitude) * math.sin(d / r) * math.cos(be))
            lat2 = math.degrees(lat2)
            south = lat2

            be = float(math.radians(270))
            lat2 = math.asin(math.sin(latitude) * math.cos(d / r) + math.cos(latitude) * math.sin(d / r) * math.cos(be))
            lon2 = longitude + math.atan2(math.sin(be) * math.sin(d / r) * math.cos(latitude),
                                          math.cos(d / r) - math.sin(latitude) * math.sin(lat2))
            lon2 = math.degrees(lon2)
            west = lon2

            return north, south, east, west

        distance64 = 64
        distance128 = 128
        distance256 = 256
        distance512 = 512

        lat = self.__location__[0]
        lon = self.__location__[1]

        lat = float(math.radians(lat))
        lon = float(math.radians(lon))

        self.__nsew64__ = calculate_nsew(lat, lon, distance64)
        self.__nsew128__ = calculate_nsew(lat, lon, distance128)
        self.__nsew256__ = calculate_nsew(lat, lon, distance256)
        self.__nsew512__ = calculate_nsew(lat, lon, distance512)

    def select_radar(self, idr):
        if idr == 'IDR773':
            self.__title__ = 'Warruwi'
            self.__updateInterval__ = 6
            self.__location__ = -11.6488, 133.385
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR093':
            self.__title__ = 'Gove'
            self.__updateInterval__ = 10
            self.__location__ = -12.28, 136.82
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR633':
            self.__title__ = 'Darwin (Berrimah)'
            self.__updateInterval__ = 10
            self.__location__ = -12.46, 130.93
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR783':
            self.__title__ = 'Weipa'
            self.__updateInterval__ = 6
            self.__location__ = -12.67, 141.92
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR423':
            self.__title__ = 'Katherine (Tindal)'
            self.__updateInterval__ = 10
            self.__location__ = -14.51, 132.45
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR073':
            self.__title__ = 'Wyndham'
            self.__updateInterval__ = 10
            self.__location__ = -15.45, 128.12
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR413':
            self.__title__ = 'Willis Island'
            self.__updateInterval__ = 10
            self.__location__ = -16.288, 149.965
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR363':
            self.__title__ = 'Mornington Island (Gulf of Carpentaria)'
            self.__updateInterval__ = 10
            self.__location__ = -16.67, 139.17
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR193':
            self.__title__ = 'Cairns'
            self.__updateInterval__ = 6
            self.__location__ = -16.82, 145.68
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR173':
            self.__title__ = 'Broome'
            self.__updateInterval__ = 10
            self.__location__ = -17.95, 122.23
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR393':
            self.__title__ = 'Halls Creek'
            self.__updateInterval__ = 10
            self.__location__ = -18.23, 127.66
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR733':
            self.__title__ = 'Townsville (Hervey Range)'
            self.__updateInterval__ = 10
            self.__location__ = -19.42, 146.55
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR243':
            self.__title__ = 'Bowen'
            self.__updateInterval__ = 10
            self.__location__ = -19.88, 148.08
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR163':
            self.__title__ = 'Port Hedland'
            self.__updateInterval__ = 10
            self.__location__ = -20.37, 118.63
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR153':
            self.__title__ = 'Dampier'
            self.__updateInterval__ = 10
            self.__location__ = -20.65, 116.69
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR753':
            self.__title__ = 'Mount Isa'
            self.__updateInterval__ = 6
            self.__location__ = -20.7114, 139.5553
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR223':
            self.__title__ = 'Mackay'
            self.__updateInterval__ = 10
            self.__location__ = -21.12, 149.22
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR293':
            self.__title__ = 'Learmonth'
            self.__updateInterval__ = 10
            self.__location__ = -22.1, 114
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR563':
            self.__title__ = 'Longreach'
            self.__updateInterval__ = 10
            self.__location__ = -23.43, 144.29
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR723':
            self.__title__ = 'Emerald'
            self.__updateInterval__ = 10
            self.__location__ = -23.5494, 148.2392
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR253':
            self.__title__ = 'Alice Springs'
            self.__updateInterval__ = 10
            self.__location__ = -23.82, 133.9
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR233':
            self.__title__ = 'Gladstone'
            self.__updateInterval__ = 10
            self.__location__ = -23.86, 151.26
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR053':
            self.__title__ = 'Carnarvon'
            self.__updateInterval__ = 10
            self.__location__ = -24.88, 113.67
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR443':
            self.__title__ = 'Giles'
            self.__updateInterval__ = 10
            self.__location__ = -25.03, 128.3
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR083':
            self.__title__ = 'Gympie (Mt Kanigan)'
            self.__updateInterval__ = 10
            self.__location__ = -25.957, 152.577
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR673':
            self.__title__ = 'Warrego'
            self.__updateInterval__ = 10
            self.__location__ = -26.44, 147.35
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR503':
            self.__title__ = 'Brisbane (Marburg)'
            self.__updateInterval__ = 10
            self.__location__ = -27.61, 152.54
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR663':
            self.__title__ = 'Brisbane (Mt Stapylton)'
            self.__updateInterval__ = 6
            self.__location__ = -27.718, 153.24
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR063':
            self.__title__ = 'Geraldton'
            self.__updateInterval__ = 10
            self.__location__ = -28.8, 114.7
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR623':
            self.__title__ = 'Norfolk Island'
            self.__updateInterval__ = 10
            self.__location__ = -29.033, 167.933
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR533':
            self.__title__ = 'Moree'
            self.__updateInterval__ = 10
            self.__location__ = -29.5, 149.85
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR283':
            self.__title__ = 'Grafton'
            self.__updateInterval__ = 10
            self.__location__ = -29.62, 152.97
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR483':
            self.__title__ = 'Kalgoorlie'
            self.__updateInterval__ = 6
            self.__location__ = -30.79, 121.45
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR693':
            self.__title__ = 'Namoi (Blackjack Mountain)'
            self.__updateInterval__ = 10
            self.__location__ = -31.024, 150.1915
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR273':
            self.__title__ = 'Woomera'
            self.__updateInterval__ = 10
            self.__location__ = -31.16, 136.8
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR333':
            self.__title__ = 'Ceduna'
            self.__updateInterval__ = 10
            self.__location__ = -32.13, 133.7
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR703':
            self.__title__ = 'Perth (Serpentine)'
            self.__updateInterval__ = 6
            self.__location__ = -32.39, 115.87
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR043':
            self.__title__ = 'Newcastle'
            self.__updateInterval__ = 6
            self.__location__ = -32.73, 152.027
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR713':
            self.__title__ = 'Sydney (Terrey Hills)'
            self.__updateInterval__ = 6
            self.__location__ = -33.701, 151.21
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR323':
            self.__title__ = 'Esperance'
            self.__updateInterval__ = 10
            self.__location__ = -33.83, 121.89
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR303':
            self.__title__ = 'Mildura'
            self.__updateInterval__ = 10
            self.__location__ = -34.23, 142.08
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR033':
            self.__title__ = 'Wollongong (Appin)'
            self.__updateInterval__ = 6
            self.__location__ = -32.264, 150.874
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR643':
            self.__title__ = 'Adelaide (Buckland Park)'
            self.__updateInterval__ = 6
            self.__location__ = -34.617, 138.469
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR313':
            self.__title__ = 'Albany'
            self.__updateInterval__ = 10
            self.__location__ = -34.94, 117.8
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR553':
            self.__title__ = 'Wagga Wagga'
            self.__updateInterval__ = 10
            self.__location__ = -35.17, 147.47
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR463':
            self.__title__ = 'Adelaide (Sellicks Hill)'
            self.__updateInterval__ = 10
            self.__location__ = -35.33, 138.5
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR403':
            self.__title__ = 'Canberra (Captains Flat)'
            self.__updateInterval__ = 6
            self.__location__ = -35.66, 149.51
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR493':
            self.__title__ = 'Yarrawonga'
            self.__updateInterval__ = 10
            self.__location__ = -36.03, 146.03
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR143':
            self.__title__ = 'Mt Gambier'
            self.__updateInterval__ = 10
            self.__location__ = -37.75, 140.77
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR023':
            self.__title__ = 'Melbourne'
            self.__updateInterval__ = 6
            self.__location__ = -37.86, 144.76
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR683':
            self.__title__ = 'Bairnsdale'
            self.__updateInterval__ = 10
            self.__location__ = -37.89, 147.53
            self.__64__ = False
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = False
        elif idr == 'IDR523':
            self.__title__ = 'NW Tasmania (West Takone)'
            self.__updateInterval__ = 6
            self.__location__ = -41.181, 145.579
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True
        elif idr == 'IDR763':
            self.__title__ = 'Hobart (Mt Koonya)'
            self.__updateInterval__ = 6
            self.__location__ = -43.1122, 147.8061
            self.__64__ = True
            self.__128__ = True
            self.__256__ = True
            self.__512__ = True
            self.__doppler__ = True

        self.calculate_nsew_s()

    def get_doppler(self, idr_code):
        idr = str(idr_code[:-1]) + "3"
        self.select_radar(idr)
        return self.__doppler__

    def get_64(self, idr_code):
        idr = str(idr_code[:-1]) + "3"
        self.select_radar(idr)
        return self.__64__

    def get_128(self, idr_code):
        idr = str(idr_code[:-1]) + "3"
        self.select_radar(idr)
        return self.__128__

    def get_256(self, idr_code):
        idr = str(idr_code[:-1]) + "3"
        self.select_radar(idr)
        return self.__256__

    def get_location(self, idr_code):
        idr = str(idr_code[:-1]) + "3"
        self.select_radar(idr)
        return self.__location__

    def get_title(self, idr_code):
        idr = str(idr_code[:-1]) + "3"
        self.select_radar(idr)
        return self.__title__

    def get_update_interval(self, idr_code):
        idr = str(idr_code[:-1]) + "3"
        self.select_radar(idr)
        return self.__updateInterval__

    def get_nsew(self, idr_code):
        if idr_code[-1] == "2":
            return self.__nsew256__
        elif idr_code[-1] == "I":
            return self.__nsew128__
        elif idr_code[-1] == "1":
            return self.__nsew512__
        elif idr_code[-1] == "3":
            return self.__nsew128__
        elif idr_code[-1] == "4":
            return self.__nsew64__
