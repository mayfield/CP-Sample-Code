# directory: ./demo/redlion_cub5
## Router App/SDK sample applications

This demo includes a thread (task) to allow it to be combined with other
demos. The demo runs on an IBR1100, reading the digital input on the 2x2
power connector. sample application creates 3 sub-tasks (so four total). 
The main application starts 3 sub-tasks, which loop, sleeping with a random
delay before printing out a logger INFO message.  

## hardware Device:
The RedLion CUB5 is a small counter/meter, for panel cut outs 1.30 x 2.68 in.
This demo is specifically using it as a counter - to demo counting something
like people entering a door, motion detection, or Mike tossing a basketball
through a hoop.

* http://files.redlion.net/filedepot_download/213/3984
* http://www.redlion.net/products/industrial-automation/hmis-and-panel-meters/panel-meters/cub5-panel-meters 

The first 2 sub-tasks will run 'forever' - or on a PC, when you do a ^C or
keyboard interrupt, the main task will abort, using an event() to stop
all three sub-tasks.

The third task will exit after each loop, and the main task will re-run it
when it notices that it is not running.

## File: __init__.py

The Python script with the class RouterApp(CradlepointAppBase) instance,
with will be run by main.py

## File: hello_world.py

The main files of the application.

## File: settings.ini

The Router App settings, including a few required by this code:

In section [power_loss]:

* check_input_delay=5 sec
* input_on_power_loss=True
* on_delay=1
* off_delay=0
 

