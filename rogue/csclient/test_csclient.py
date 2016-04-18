"""
Probe the GPS hardware, return a report as both list of text, and actual ASCII file
"""
import sys

from cp_lib.cs_client import init_cs_client_on_my_platform


def test_csclient(logger, sets):
    """

    :param logger: a log/trace object which acts like logging (but may not be)
    :param dict sets: the processed settings.json file
    :return list:
    """

    logger.info("Running simple test of CSClient")

    # handle the Router API client, which is different between PC testing and router HW
    try:
        client = init_cs_client_on_my_platform(logger, sets)
    except:
        logger.exception("CSClient init failed")
        raise

    # user may have passed in another path
    tree_path = "status/product_info/product_name"
    if "csclient" in sets:
        if "path" in sets["csclient"]:
            tree_path = sets["csclient"]["path"]

    # fetch and record the type of Router we are running on
    result = client.get(tree_path)
    logger.info("Result was ({})".format(result))

    return 0


if __name__ == "__main__":
    from cp_lib.cp_logging import get_recommended_logger
    from cp_lib.load_settings_json import load_settings_json

    _my_settings = load_settings_json("simple/csclient")
    _logger = get_recommended_logger(_my_settings)

    _result = test_csclient(_logger, sets=_my_settings)

    _logger.info("Exiting, status code is {}".format(_result))

    sys.exit(_result)
