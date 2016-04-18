"""CSClient Object"""

import json
import socket


class CSClient(object):
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 1337
    DEFAULT_MSIZE = 1024

    """Wrapper for the TCP interface to the router config store."""

    def get(self, base, query='', tree=0):
        """Send a get request."""
        cmd = "get\n{}\n{}\n{}\n".format(base, query, tree)
        return self._dispatch(cmd)

    def put(self, base, value='', query='', tree=0):
        """Send a put request."""
        value = json.dumps(value).replace(' ', '')
        cmd = "put\n{}\n{}\n{}\n{}\n".format(base, query, tree, value)
        return self._dispatch(cmd)

    def append(self, base, value='', query=''):
        """Send an append request."""
        value = json.dumps(value).replace(' ', '')
        cmd = "post\n{}\n{}\n{}\n".format(base, query, value)
        return self._dispatch(cmd)

    def delete(self, base, query=''):
        """Send a delete request."""
        cmd = "delete\n{}\n{}\n".format(base, query)
        return self._dispatch(cmd)

    def alert(self, name='', value=''):
        """Send a request to create an alert."""
        cmd = "alert\n{}\n{}\n".format(name, value)
        return self._dispatch(cmd)

    def log(self, name='', value=''):
        """Send a request to create a log entry."""
        cmd = "log\n{}\n{}\n".format(name, value)
        return self._dispatch(cmd)

    def _dispatch(self, cmd):
        """Send the command and return the response."""
        resl = ''
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.DEFAULT_HOST, self.DEFAULT_PORT))
            sock.sendall(bytes(cmd, 'ascii'))

            header = str(sock.recv(self.DEFAULT_MSIZE), 'ascii')
            if header.strip() == 'status: ok':
                msg = str(sock.recv(self.DEFAULT_MSIZE), 'ascii')
                mlen = int(msg.strip().split(' ')[1])
                if str(sock.recv(self.DEFAULT_MSIZE), 'ascii') == '\r\n\r\n':
                    while mlen > 0:
                        resl += str(sock.recv(self.DEFAULT_MSIZE), 'ascii')
                        mlen -= self.DEFAULT_MSIZE
        return resl
