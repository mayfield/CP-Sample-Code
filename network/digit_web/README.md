# directory: ./network/digit_web
## Router App/SDK sample applications

A more complex basic web server, using the standard Python 3 "http.server" 
module. It returns a slightly dynamic page of 5 'digit' images, representing
a 'counter'. In the sample, the digits are fixed at "00310", but a richer
design could allow new numbers to be used.

More importantly, the fact we have images on the text page means any
one client request results in up to 6 requests - the first returns the
text page with the 5 images, and then up to 5 more are submitted to
fetch the images.

## File: __init__.py

The Python script with the class RouterApp(CradlepointAppBase) instance,
which will be run by main.py

## File: web_server.py

The main files of the application.

## File: settings.ini

The Router App settings, including a few required by this code:

In section [web_server]:

* host_port=9001, define the listening port, which on Cradlepoint Router
SDK must be greater than 1024 due to permissions. 
Also, avoid 8001 or 8080, as router may be using already. 
