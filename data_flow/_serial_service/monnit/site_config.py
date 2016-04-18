# Site configuration details

# PYSERIAL CONFIG - how unit talks to Monnit USB GATEWAY
#
# the pyserial requires 2 configs. I suppose the 'ID" can probably be derived from the name
# but at the moment it's easiest to use both here.
# - Windows will have a name like 'COM15' and ID like 14
# - Linux will have a name like '/dev/ttyUSB0' and ID like (TBD)
SERIAL_PORT_NAME = 'COM15'
SERIAL_PORT_ID = 14
POLL_CYCLE_SECS = 1.0
assert isinstance(SERIAL_PORT_NAME, str)
assert isinstance(SERIAL_PORT_ID, int)


# MONNIT USB GATEWAY CONFIG
#
# - GWAY_ADDRESS is the internal id of the gateway - you need to read the label (TBD - dyn query?)
# - SENSOR_ADDRESS_LIST is the id of fixed sensors - TBD, this may be supplemented from iMonnit
GWAY_ADDRESS = 200
SENSOR_ADDRESS_LIST = [95411, 95412, 95413, 96001, 96002]
assert isinstance(GWAY_ADDRESS, int)
assert isinstance(SENSOR_ADDRESS_LIST, list)


# DUMP FILES
#
# set LOGGING_FILENAME to None to disable
MESSAGE_FILENAME = 'messages.txt'
LOGGING_FILENAME = 'log.txt'
assert isinstance(MESSAGE_FILENAME, str)


# DIRECT EMAIL
EMAIL_TO_LIST = ['llinse@cradlepoint.com', 'nrf2016cp@gmail.com', 'lynn@linse.org']
EMAIL_FROM = 'mondy@linse.org'


# iMonnit upload - set IMONNIT_HOSTNAME to None to disable
IMONNIT_HOSTNAME = "t1.sensorsgateway.com"
IMONNIT_PORT = 3000
# IMONNIT_COALESCE defines a delay, to hopefully collect more data before upload
IMONNIT_COALESCE = 0
# IMONNIT_HEARTBEAT defines how iMonnit treats the 'health' of the
IMONNIT_HEARTBEAT = 890
