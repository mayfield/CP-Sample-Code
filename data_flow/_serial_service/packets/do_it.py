
# a simple test - run a server & echo the response

import packets.handler_tcp_server as tcp_server
import time
import logging


logging.basicConfig(level=logging.DEBUG)

# start the server
srv = tcp_server.TcpServerThread('anna', 'srv')
srv.import_params('{"ip_port": 9999}')
srv.start_server()

assert srv.is_alive()

logging.info("waiting")
time.sleep(120.0)
srv.stop_server()
