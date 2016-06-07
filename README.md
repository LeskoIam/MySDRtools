# Collection (in the making) of SDR tools

### CL-ADSB tool

Command line tool to show adsb aircraft information in a nice table.
Easy configurable and upgradable, please see script itself.

![alt text](http://i.imgur.com/urKAuWn.png "CL-ADSB")

CL-ADSB parses AircraftList.json feed coming from VirtualRadar server. If you have or find a public server just replace

**http://sdrsharp.com:8080/virtualradar/desktop.html**

with

**http://sdrsharp.com:8080/virtualradar/AircraftList.json**

To configure the server open cl_adsb.py file and close to the end change
```python
adsb = AdsB("http://192.168.1.55:8080/VirtualRadar/AircraftList.json")
```
to address you wish.

Point it to your server or some public one like [SDRSharp](http://sdrsharp.com:8080/virtualradar/desktop.html) and run it.

If you are on Linux there is a sh script that runs it in a loop, check it out.
