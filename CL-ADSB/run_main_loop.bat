echo off

echo CL-ADSB tool
echo
echo You must be in the same directory as cl_adsb.py for this to work
echo

if "%~1"=="" (
    echo No argument supplied
    echo Use:
    echo      ./run_main_loop.sh t
    echo      t .... seconds to sleep between refreshes
    goto :eof
)


set /A t = %1 + 1

:loop
cls
python cl_adsb.py -c -m
ping -n %t% 127.0.0.1 >nul
goto loop

:eof
