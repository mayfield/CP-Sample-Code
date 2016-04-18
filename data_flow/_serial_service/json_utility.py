__author__ = 'Lynn'

USE_JSONRPC_VERSION = "2.0"


JSONRPC_PARSE_ERROR = -32700
JSONRPC_INVALID_REQUEST = -32600
JSONRPC_METHOD_NOT_FOUND = -32601
JSONRPC_INVALID_PARAMS = -32602
JSONRPC_INTERNAL_ERROR = -32603

JSONRPC_ERROR_MESSAGE = {
    JSONRPC_PARSE_ERROR: "Parse Error",
    JSONRPC_INVALID_REQUEST: "Invalid Request",
    JSONRPC_METHOD_NOT_FOUND: "Method not Found",
    JSONRPC_INVALID_PARAMS: "Invalid Params",
    JSONRPC_INTERNAL_ERROR: "Internal Error",
}


def make_jsonrpc_request(method_name, identifier=None):
    """
    start a JSONRPC dictionary

    :return:
    """
    request = dict()
    request["jsonrpc"] = USE_JSONRPC_VERSION
    request["method"] = method_name
    if identifier is not None:
        request["id"] = identifier
    return request


def make_json_error(error_code, error_message=None, identifier=None):
    """
    Force create a valid JSONRPC error response
    :param error_code:
    :param error_message:
    :return:
    """
    if error_message is None:
        # handle the common errors
        if error_code in JSONRPC_ERROR_MESSAGE:
            error_message = JSONRPC_ERROR_MESSAGE[error_code]

    result = dict()
    result["jsonrpc"] = USE_JSONRPC_VERSION
    result["error"] = dict(code=error_code, message=error_message)
    if identifier is not None:
        result["id"] = identifier
    return result


def clean_json_result(result):
    """
    Force create a valid JSONRPC error response
    :param result:
    :type result: dict
    :return:
    """

    if "params" in result:
        del result["params"]

    if "method" in result:
        del result["method"]

    assert "result" in result

    return result
