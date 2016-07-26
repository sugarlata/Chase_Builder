class RadarDB:

    title=str()
    updateInterval=int()
    location=float(),float()
    km64=bool()
    km128=bool()
    km256=bool()
    km512=bool()
    dopp=bool()

    locationdb=[]

    def __init__(self, IDR):
        IDR = str(IDR[:-1]) + "3"
        self.selectRadar(IDR)

    def selectRadar(self,IDR):
        if IDR == 'IDR773':
            self.title = 'Warruwi'
            self.updateInterval = 6
            self.location = -11.6488, 133.385
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR093':
            self.title = 'Gove'
            self.updateInterval = 10
            self.location = -12.28, 136.82
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR633':
            self.title = 'Darwin (Berrimah)'
            self.updateInterval = 10
            self.location = -12.46, 130.93
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR783':
            self.title = 'Weipa'
            self.updateInterval = 6
            self.location = -12.67, 141.92
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR423':
            self.title = 'Katherine (Tindal)'
            self.updateInterval = 10
            self.location = -14.51, 132.45
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR073':
            self.title = 'Wyndham'
            self.updateInterval = 10
            self.location = -15.45, 128.12
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR413':
            self.title = 'Willis Island'
            self.updateInterval = 10
            self.location = -16.288, 149.965
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR363':
            self.title = 'Mornington Island (Gulf of Carpentaria)'
            self.updateInterval = 10
            self.location = -16.67, 139.17
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR193':
            self.title = 'Cairns'
            self.updateInterval = 6
            self.location = -16.82, 145.68
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR173':
            self.title = 'Broome'
            self.updateInterval = 10
            self.location = -17.95, 122.23
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR393':
            self.title = 'Halls Creek'
            self.updateInterval = 10
            self.location = -18.23, 127.66
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR733':
            self.title = 'Townsville (Hervey Range)'
            self.updateInterval = 10
            self.location = -19.42, 146.55
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR243':
            self.title = 'Bowen'
            self.updateInterval = 10
            self.location = -19.88, 148.08
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR163':
            self.title = 'Port Hedland'
            self.updateInterval = 10
            self.location = -20.37, 118.63
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR153':
            self.title = 'Dampier'
            self.updateInterval = 10
            self.location = -20.65, 116.69
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR753':
            self.title = 'Mount Isa'
            self.updateInterval = 6
            self.location = -20.7114, 139.5553
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR223':
            self.title = 'Mackay'
            self.updateInterval = 10
            self.location = -21.12, 149.22
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR293':
            self.title = 'Learmonth'
            self.updateInterval = 10
            self.location = -22.1, 114
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR563':
            self.title = 'Longreach'
            self.updateInterval = 10
            self.location = -23.43, 144.29
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR723':
            self.title = 'Emerald'
            self.updateInterval = 10
            self.location = -23.5494, 148.2392
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR253':
            self.title = 'Alice Springs'
            self.updateInterval = 10
            self.location = -23.82, 133.9
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR233':
            self.title = 'Gladstone'
            self.updateInterval = 10
            self.location = -23.86, 151.26
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR053':
            self.title = 'Carnarvon'
            self.updateInterval = 10
            self.location = -24.88, 113.67
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR443':
            self.title = 'Giles'
            self.updateInterval = 10
            self.location = -25.03, 128.3
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR083':
            self.title = 'Gympie (Mt Kanigan)'
            self.updateInterval = 10
            self.location = -25.957, 152.577
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR673':
            self.title = 'Warrego'
            self.updateInterval = 10
            self.location = -26.44, 147.35
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR503':
            self.title = 'Brisbane (Marburg)'
            self.updateInterval = 10
            self.location = -27.61, 152.54
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR663':
            self.title = 'Brisbane (Mt Stapylton)'
            self.updateInterval = 6
            self.location = -27.718, 153.24
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR063':
            self.title = 'Geraldton'
            self.updateInterval = 10
            self.location = -28.8, 114.7
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR623':
            self.title = 'Norfolk Island'
            self.updateInterval = 10
            self.location = -29.033, 167.933
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR533':
            self.title = 'Moree'
            self.updateInterval = 10
            self.location = -29.5, 149.85
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR283':
            self.title = 'Grafton'
            self.updateInterval = 10
            self.location = -29.62, 152.97
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR483':
            self.title = 'Kalgoorlie'
            self.updateInterval = 6
            self.location = -30.79, 121.45
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR693':
            self.title = 'Namoi (Blackjack Mountain)'
            self.updateInterval = 10
            self.location = -31.024, 150.1915
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR273':
            self.title = 'Woomera'
            self.updateInterval = 10
            self.location = -31.16, 136.8
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR333':
            self.title = 'Ceduna'
            self.updateInterval = 10
            self.location = -32.13, 133.7
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR703':
            self.title = 'Perth (Serpentine)'
            self.updateInterval = 6
            self.location = -32.39, 115.87
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR043':
            self.title = 'Newcastle'
            self.updateInterval = 6
            self.location = -32.73, 152.027
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR713':
            self.title = 'Sydney (Terrey Hills)'
            self.updateInterval = 6
            self.location = -33.701, 151.21
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR323':
            self.title = 'Esperance'
            self.updateInterval = 10
            self.location = -33.83, 121.89
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR303':
            self.title = 'Mildura'
            self.updateInterval = 10
            self.location = -34.23, 142.08
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR033':
            self.title = 'Wollongong (Appin)'
            self.updateInterval = 6
            self.location = -32.264, 150.874
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR643':
            self.title = 'Adelaide (Buckland Park)'
            self.updateInterval = 6
            self.location = -34.617, 138.469
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR313':
            self.title = 'Albany'
            self.updateInterval = 10
            self.location = -34.94, 117.8
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR553':
            self.title = 'Wagga Wagga'
            self.updateInterval = 10
            self.location = -35.17, 147.47
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR463':
            self.title = 'Adelaide (Sellicks Hill)'
            self.updateInterval = 10
            self.location = -35.33, 138.5
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR403':
            self.title = 'Canberra (Captains Flat)'
            self.updateInterval = 6
            self.location = -35.66, 149.51
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR493':
            self.title = 'Yarrawonga'
            self.updateInterval = 10
            self.location = -36.03, 146.03
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR143':
            self.title = 'Mt Gambier'
            self.updateInterval = 10
            self.location = -37.75, 140.77
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR023':
            self.title = 'Melbourne'
            self.updateInterval = 6
            self.location = -37.86, 144.76
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR683':
            self.title = 'Bairnsdale'
            self.updateInterval = 10
            self.location = -37.89, 147.53
            self.km64 = False
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = False
        elif IDR == 'IDR523':
            self.title = 'NW Tasmania (West Takone)'
            self.updateInterval = 6
            self.location = -41.181, 145.579
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
        elif IDR == 'IDR763':
            self.title = 'Hobart (Mt Koonya)'
            self.updateInterval = 6
            self.location = -43.1122, 147.8061
            self.km64 = True
            self.km128 = True
            self.km256 = True
            self.km512 = True
            self.dopp = True
