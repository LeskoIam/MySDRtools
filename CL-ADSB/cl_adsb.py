import os
import sys
import argparse
import requests
from pprint import pprint
from prettytable import PrettyTable


# Color definitions for Linux terminal
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
# Why not?
else:
    def beep():
        print "Computer says: BEEP"


    def add_color(text, color=None):
        return text


# A few (heh) helper functions
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
        return "AirCraft {0}".format(self.get_data("Icao"))

    def get_data(self, data):
        """
        This method is used because we are never sure
        if all or any data will be present.

        :param data: AirCraft attribute as string
        :return: attribute if it exists otherwise None
        """
        data = str(data)
        try:
            return self.__getattribute__(data)
        except AttributeError:
            return None

    def show_all_data(self):
        pprint(self.__dict__)


class AdsB(object):
    def __init__(self, json_address=None):
        """
        Gets and parses data from supplied json_address
        :param json_address: address of server that serves adsb data in json form (VirtualRadar)
        """
        if json_address is None:
            raise AttributeError("json_address (server) not specified")
        self.json_address = json_address
        self.data = None

    def __str__(self):
        return "ADSB data from: {addr}".format(addr=self.json_address)

    def parse(self):
        """
        Main parse method.
        It maps json field names to class attributes.
        """
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


# Setup argparser
def parse_args():
    parser = argparse.ArgumentParser(description="CL-ADSB - Command line tool to display aircraft adsb information in a table.")
    parser.add_argument("-s", type=str, dest="server_address", help="server address. Default is SDRSharps server.")
    parser.add_argument("-c", help="count all aircraft", action="store_true", dest="all_count")
    parser.add_argument("-m", help="count military aircraft", action="store_true", dest="mil_count")
    parser.add_argument("-im", help="use imperial measurements (feet)", action="store_true", dest="imperial")
    return parser.parse_args()


def main():
    args = parse_args()

    # Server setup
    ###########################################################################
    server_address = "http://sdrsharp.com:8080/virtualradar/AircraftList.json"  # SDRSharps server
    if args.server_address is not None:
        server_address = args.server_address
        if not server_address.endswith(".json"):  # Should this check be removed?
            print "Server address is in wrong format. No .json found."
            exit()
    adsb = AdsB(server_address)
    ###########################################################################
    adsb.parse()

    # Setup pretty litle table
    header = ["Icao", "Mil", "Alt", "Reg", "Call", "Sqk", "Op", "Lat", "Long"]
    planes_table = PrettyTable(field_names=header)
    planes_table.align["Op"] = "l"  # Align left
    planes_table.align["Reg"] = "l"
    planes_table.align["Call"] = "l"
    planes_table.align["Alt"] = "l"
    planes_table.align["Sqk"] = "l"

    # Lets count military and Slovenian aircraft, all aircraft are counted different (len(adsb.data)).
    mil_count = 0
    slo_count = 0
    for plane in adsb.data:
        # Restrict maximum number of characters in Operator name
        if plane.get_data("Op") is not None and len(plane.get_data("Op")) > 11:
            plane.Op = plane.get_data("Op")[:7] + " ..."  # 7 + len(" ...") => 7 + 4 = 11

        # Fill row with plane data
        row = []
        # First handle all exceptions
        # 506 is the starting number of Slovenian aircraft. I want to know they are up.
        if plane.get_data("Icao").startswith("506"):
            slo_count += 1
            row.append(add_color(plane.get_data("Icao"), color=bcolors.OKBLUE))
        else:
            row.append(plane.get_data("Icao"))
        # Military aircraft
        if plane.get_data("Mil"):
            mil_count += 1
            # beep()
            row.append(add_color(plane.get_data("Mil"), color=bcolors.WARNING))
        else:
            row.append(plane.get_data("Mil"))
        # By default
        if args.imperial:
            row.append(plane.get_data("Alt"))
        else:
            row.append(feet_to_meters(plane.get_data("Alt")))
        # Append all other data as they appear in header. First two are already handled
        for cell in header[3:]:
            row.append(plane.get_data(cell))

        planes_table.add_row(row=row)

    print planes_table
    if args.all_count:
        print "All count: {0}".format(len(adsb.data))
    if args.mil_count:
        print "Mill count: {0}".format(mil_count)
        # print "Slo count:  {0}".format(slo_count)
        # plane.show_all_data()


if __name__ == '__main__':
    main()
