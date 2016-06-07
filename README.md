# Collection (in the making) of SDR tools

### CL-ADSB tool

Command line tool to show adsb aircraft information in a nice table.
Easy configurable and upgradable, please see script itself.

![alt text](http://i.imgur.com/urKAuWn.png "CL-ADSB")

CL-ADSB now supports command line arguments.
```
usage: cl_adsb.py [-h] [-s SERVER_ADDRESS] [-c] [-m]

CL-ADSB

optional arguments:
  -h, --help         show this help message and exit
  -s SERVER_ADDRESS  server address
  -c                 count all aircraft
  -m                 count military aircraft
```

CL-ADSB parses AircraftList.json feed coming from VirtualRadar server.
If you have or find a public server just replace the .html in server address

**http://sdrsharp.com:8080/virtualradar/desktop.html**

with

**http://sdrsharp.com:8080/virtualradar/AircraftList.json**

Point it to your server or some public one like [SDRSharp](http://sdrsharp.com:8080/virtualradar/desktop.html) and run it.

If you are on Linux there is a sh script that runs it in a loop, check it out.
