"""
A basic but complete echo server
"""

from http.server import BaseHTTPRequestHandler, HTTPServer

from cp_lib.app_base import CradlepointAppBase

# avoid 8080, as the router may have servcie on it.
DEF_HOST_PORT = 9001
DEF_HOST_IP = ""
DEF_WEB_MESSAGE = "Hello World"


def run_router_app(app_base):
    """

    :param CradlepointAppBase app_base: prepared resources: logger, cs_client
    :return:
    """
    if "web_server" in app_base.settings:
        host_port = int(app_base.settings["web_server"].get(
            "host_port", DEF_HOST_PORT))

        host_ip = app_base.settings["web_server"].get(
            "host_ip", DEF_HOST_IP)

        web_message = app_base.settings["web_server"].get(
            "message", DEF_WEB_MESSAGE)
    else:
        # we create, so WebServerRequestHandler can obtain
        app_base.settings["web_server"] = dict()

        host_port = DEF_HOST_PORT
        app_base.settings["web_server"]["host_port"] = host_port

        host_ip = DEF_HOST_IP
        app_base.settings["web_server"]["host_ip"] = host_ip

        web_message = DEF_WEB_MESSAGE
        app_base.settings["web_server"]["message"] = web_message

    # we want on all interfaces
    server_address = (host_ip, host_port)

    app_base.logger.info("Starting Server:{}".format(server_address))
    app_base.logger.info("Web Message is:{}".format(web_message))

    httpd = HTTPServer(server_address, WebServerRequestHandler)
    # set by singleton - pushes in any/all instances
    WebServerRequestHandler.APP_BASE = app_base

    try:
        httpd.serve_forever()

    except KeyboardInterrupt:
        app_base.logger.info("Stopping Server, Key Board interrupt")

    return 0


class WebServerRequestHandler(BaseHTTPRequestHandler):
    """

    """

    # a singleton to support pass-in of our settings and logger
    APP_BASE = None

    START_LINES = '<!DOCTYPE html><html lang="en"><head>' +\
                  '<meta charset="UTF-8"><title>The Count Is</title>' +\
                  '</head><body><TABLE border="1"><TR>'

    IMAGE_LINES = '<TD><img src="%s"></TD>'

    END_LINES = '</TR></TABLE></body></html>'

    IMAGES = {
        '0': "digit_0.jpg",
        '1': "digit_1.jpg",
        '2': "digit_2.jpg",
        '3': "digit_3.jpg",
        '4': "digit_4.jpg",
        '5': "digit_5.jpg",
        '6': "digit_6.jpg",
        '7': "digit_7.jpg",
        '8': "digit_8.jpg",
        '9': "digit_9.jpg",
        '.': "digit_dot.jpg",
        ' ': "digit_blank.jpg",
    }

    PATH = "network/digit_web/"

    def do_GET(self):

        if self.path == "/":
            self.path = "/counter.html"

        if self.APP_BASE is not None:
            self.APP_BASE.logger.debug("Path={}".format(self.path))

        try:

            mime_type = 'text/html'
            send_reply = False
            if self.path.endswith(".html"):
                count = "  310"
                web_message = self.START_LINES
                for ch in count:
                    web_message += self.IMAGE_LINES % self.IMAGES[ch]
                web_message += self.END_LINES
                web_message = bytes(web_message, "utf-8")
                send_reply = True

            elif self.path.endswith(".jpg"):
                mime_type = 'image/jpg'
                f = open(self.PATH + self.path, 'rb')
                web_message = f.read()
                send_reply = True

            else:
                raise IOError

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)
            return

        if send_reply:
            # Send response status code
            self.send_response(200)

            # Send headers
            self.send_header('Content-type', mime_type)
            self.end_headers()

            # Send message back to client
            # Write content as utf-8 data
            self.wfile.write(web_message)

        return


if __name__ == "__main__":
    import sys

    my_app = CradlepointAppBase("network/simple_web")
    _result = run_router_app(my_app)
    my_app.logger.info("Exiting, status code is {}".format(_result))
    sys.exit(_result)
