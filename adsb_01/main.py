import os
import sys
import requests
from pprint import pprint
from prettytable import PrettyTable


# Color definitions for terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Platform specific function definitions
if sys.platform.startswith("linux"):
    def beep():
        os.system('play --no-show-progress --null --channels 1 synth %s sine %f' % (0.1, 2000))

    def add_color(text, color=bcolors.OKGREEN):
        return "{color}{text}{end}".format(color=color, text=text, end=bcolors.ENDC)
elif sys.platform.startswith("win"):
    import winsound

    def beep():
        winsound.Beep(0.1, 2000)

    def add_color(text, color=None):
        return text
else:
    def beep():
        print "Computer says: BEEP"

    def add_color(text, color=None):
        return text


# A few helper functions
def feet_to_meters(feet, to_int=False):
    try:
        out = float(feet) * 0.3048
        if to_int:
            return int(out)
        return out
    except TypeError:
        return feet


class AirCraft(object):
    """This class will hold single aircraft data.
    """
    def __str__(self):
        return self.get_data("Icao")

    def get_data(self, data):
        data = str(data)
        try:
            return self.__getattribute__(data)
        except AttributeError:
            return None

    def show_all_data(self):
        pprint(self.__dict__)


class AdsB(object):
    def __init__(self, json_address="http://192.168.1.55:8080/VirtualRadar/AircraftList.json"):
        self.json_address = json_address
        self.data = None

    def __str__(self):
        return "ADSB data from: {addr}".format(addr=self.json_address)

    def parse(self):
        r = requests.get(self.json_address)
        data = r.json()
        plane_data = data["acList"]

        all_aircraft = []
        for plane in plane_data:
            aircraft = AirCraft()
            for p in plane:
                data_point = plane[p]
                aircraft.__setattr__(p, data_point)
            all_aircraft.append(aircraft)
        self.data = all_aircraft


if __name__ == '__main__':

    adsb = AdsB()  # "http://sdrsharp.com:8080/virtualradar/AircraftList.json")
    adsb.parse()

    # Setup Pretty lille table
    planes_table = PrettyTable(["Icao", "Reg", "Call", "Sqk", "Alt", "Op", "Mil", "Lat", "Long"])
    planes_table.align["Op"] = "l"
    planes_table.align["Reg"] = "l"
    planes_table.align["Call"] = "l"
    planes_table.align["Alt"] = "l"
    planes_table.align["Sqk"] = "l"

    # Lets count military and Slovenian aircraft
    m_count = 0
    slo_count = 0
    for plane in adsb.data:
        if plane.get_data("Mil"):
            # beep()
            m_count += 1
        if plane.get_data("Icao").startswith("506"):
            slo_count += 1
        if plane.get_data("Op") is not None and len(plane.get_data("Op")) > 11:
            plane.Op = plane.get_data("Op")[:7] + " ..."

        # Fill row with plane data
        planes_table.add_row([plane.get_data("Icao") if not plane.get_data("Icao").startswith("506") else
                                                            add_color(plane.get_data("Icao"), color=bcolors.OKBLUE),
                              plane.get_data("Reg"),
                              plane.get_data("Call"),
                              plane.get_data("Sqk"),
                              feet_to_meters(plane.get_data("Alt"), to_int=True),
                              plane.get_data("Op"),
                              plane.get_data("Mil") if not plane.get_data("Mil") else add_color(plane.get_data("Mil"),
                                                                                     color=bcolors.WARNING),
                              plane.get_data("Lat"),
                              plane.get_data("Long")])

    print planes_table
    print "Mill count: " + str(m_count)
    print "Slo count:  " + str(slo_count)
    # plane.show_all_data()
