__author__ = 'Lynn'

# project: serial service
# Validate the JSONRPC

# --> {"jsonrpc": "2.0", "method": "subtract", "params": {"subtrahend": 23, "minuend": 42}, "id": 3}
# <-- {"jsonrpc": "2.0", "result": 19, "id": 3}
#
# --> {"jsonrpc": "2.0", "method": 1, "params": "bar"}
# <-- {"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": null}


METHOD_LIST = ["echo", "open"]

PARAMS_LIST = {
    "echo": ['*'],
    "open": ["target", "access_mode", "share_mode"]
}