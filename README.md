# Collection (in the making) of SDR tools

### CL-ADSB tool

Command line tool to show adsb aircraft information in a nice table.
Easy configurable and upgradable, please see script itself.

![alt text](http://i.imgur.com/urKAuWn.png "CL-ADSB")

CL-ADSB now supports command line arguments.
```
$ python cl_adsb.py -h
usage: cl_adsb.py [-h] [-s SERVER_ADDRESS] [-c] [-m] [-im]

CL-ADSB - Command line tool to display aircraft adsb information in a table.

optional arguments:
  -h, --help         show this help message and exit
  -s SERVER_ADDRESS  server address. Default is SDRSharps server.
  -c                 count all aircraft
  -m                 count military aircraft
  -im                use imperial measurements (feet)
```

CL-ADSB parses AircraftList.json feed coming from VirtualRadar server.
If you have or find a public server just replace the .html in server address

**http://sdrsharp.com:8080/virtualradar/desktop.html**

with

**http://sdrsharp.com:8080/virtualradar/AircraftList.json**

Point it to your server or some public one like [SDRSharp](http://sdrsharp.com:8080/virtualradar/desktop.html) and run it.

There are bat (Win) and sh (Linux) scripts that run CL-ADSB in a loop, check it out.
