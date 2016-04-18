__author__ = 'llinse'

from data.cp_api import ApiRouter
from serial_object import SerialNoSupport


class SerialStatsPublish(object):
    """
    Why does this exist?

        SerialStatsPublish abstracts the publish (to uploading) of the basic serial statistics
        and control signal status.

    Variability:
    DCE-vs-DTE - I handle this by defining things like DTRDSR_OUT or DTRDSR_IN,
        because with the IBR1100, engineering is calling the DCE-DSR "DTR", which the DTE name,
        but the DTE CD/RI need to be inputs in RS-232.
    Enable RTS/CTS hand-shaking - when RTS/CTS is enabled, we do not allow showing the
        value of RTS or CTS
    product differences - some products (like 850) only have the RTS/CTS, which we likely assume
        are for handshaking or nothing
    RS-485/422 will also lack DTR/DSR, and RTS (if it exists) is likely used for XMTR enable.
    """

    MAPS = {
        "dtrdsr_out": {"api": "UART_DTRDSR_OUT", "output": True,
                       "desc": "DTR/DSR/Device-Ready pair output signal"},
        "dtrdsr_in": {"api": "UART_DTRDSR_IN", "output": False,
                      "desc": "DTR/DSR/Device-Ready pair input signal"},
        "rtscts_out": {"api": "UART_RTSCTS_OUT", "output": True,
                       "desc": "RTS/CTS/Can-Send pair output signal"},
        "rtscts_in": {"api": "UART_RTSCTS_IN", "output": False,
                      "desc": "RTS/CTS/Can-Send pair input signal"},
        "cd_out": {"api": "UART_DCD_OUT", "output": True,
                   "desc": "CD/Carrier-Detect as output signal"},
        "cd_in": {"api": "UART_DCD_IN", "output": False,
                  "desc": "CD/Carrier-Detect as input signal"},
        "ri_out": {"api": "UART_RI_OUT", "output": True,
                   "desc": "RI/Ring-Indicate as output signal"},
        "ri_in": {"api": "UART_RI_IN", "output": False,
                  "desc": "RI/Ring-Indicate as input signal"},
        "last_activity": {"api": "LAST_ACTIVITY", "desc": "Last Serial Activity time"},
    }

    # what products have which control signals; missing keys means False
    PRODUCT_USB232DTE = "U232DTE"
    PRODUCT_8X0 = "8X0"
    PRODUCT_11X0 = "11X0"
    PRODUCT_31X0 = "31X0"
    PRODUCT_LIST = (PRODUCT_USB232DTE, PRODUCT_8X0, PRODUCT_11X0, PRODUCT_31X0)
    PRODUCT_FANCY_NAME = {
        PRODUCT_USB232DTE: "USB Serial 232 DTE",
        PRODUCT_8X0: "CBA850",
        PRODUCT_11X0: "IBR1100",
        PRODUCT_31X0: "AER3100"
    }
    # not sure all of these exist, but the conversion doesn't really care
    PRODUCT_NAME_IMPORT = {
        PRODUCT_USB232DTE: PRODUCT_USB232DTE, "DTE": PRODUCT_USB232DTE,
        PRODUCT_8X0: PRODUCT_8X0, "8X0": PRODUCT_8X0, "800": PRODUCT_8X0, "850": PRODUCT_8X0,
        "CBA800": PRODUCT_8X0, "CBA850": PRODUCT_8X0,
        PRODUCT_11X0: PRODUCT_11X0, "11X0": PRODUCT_11X0,  "1100": PRODUCT_11X0, "1150": PRODUCT_11X0,
        "IBR1100": PRODUCT_11X0, "IBR1150": PRODUCT_11X0,
        PRODUCT_31X0: PRODUCT_31X0, "31X0": PRODUCT_31X0, "3100": PRODUCT_31X0,  "3150": PRODUCT_31X0,
        "AER3100": PRODUCT_31X0,  "AER3150": PRODUCT_31X0,
    }
    PRODUCT_HAS_DTRDSR = (PRODUCT_USB232DTE, PRODUCT_11X0, PRODUCT_31X0)
    PRODUCT_HAS_RTSCTS = (PRODUCT_USB232DTE, PRODUCT_8X0, PRODUCT_11X0, PRODUCT_31X0)
    PRODUCT_HAS_CD_OUT = PRODUCT_11X0
    PRODUCT_HAS_CD_IN = PRODUCT_USB232DTE
    PRODUCT_HAS_RI_OUT = PRODUCT_11X0
    PRODUCT_HAS_RI_IN = PRODUCT_USB232DTE

    def __init__(self, base_path: str, api_object: ApiRouter):
        """
        :param base_path: should be like "/status/serial_1/stats/"
        :param api_object: passed in handler to get/put to Router API
        """
        self.data = {"path": base_path, "last_activity": 0}
        self._api = api_object

        # for now, default to 1100/1150
        self._product = self.PRODUCT_11X0

        self.rtscts_flow = False

        self.dtrdsr_out = False
        self.dtrdsr_in = False
        self.rtscts_out = False
        self.rtscts_in = False
        self.cd_out = False
        self.cd_in = False
        self.ri_out = False
        self.ri_in = False

        return

    # def __delattr__(self, name):
    #     del self.attrib[name]
    #
    # def __getattr__(self, name):
    #     return self.attrib[name]
    #
    # def __setattr__(self, name, value):
    #     self.attrib[name] = value

    def set_product_support_details(self, product=None):
        """
        Given the self._product value, fill in the various control signal details

        Warning: call this BEFORE calling set_product_support_rtscts()

        :return:
        """
        if product is not None:
            self._product = product
        # else assume self._product is already set, so validate it, throw exception if bad
        self._validate_product_name_in_self()

        # TODO - get this fed in
        self.rtscts_flow = False

        self.dtrdsr_out = self.product_has_dtrdsr(self._product)
        if self.dtrdsr_out:
            self.data['dtrdsr_out'] = None

        self.dtrdsr_in = self.product_has_dtrdsr(self._product)
        if self.dtrdsr_in:
            self.data['dtrdsr_in'] = None

        # handle default
        self.set_product_support_rtscts(self.rtscts_flow)

        self.cd_out = self.product_has_cd_out(self._product)
        if self.cd_out:
            self.data['cd_out'] = None

        self.cd_in = self.product_has_cd_in(self._product)
        if self.cd_in:
            self.data['cd_in'] = None

        self.ri_out = self.product_has_ri_out(self._product)
        if self.ri_out:
            self.data['ri_out'] = None

        self.ri_in = self.product_has_ri_in(self._product)
        if self.ri_in:
            self.data['ri_in'] = None

        return

    def _validate_product_name_in_self(self):
        """Special, retest the self._product, throw exception if bad"""
        self._product = self._product.upper().strip()
        if self._product not in self.PRODUCT_NAME_IMPORT:
            raise ValueError("Product name '{0}' is not valid".format(self._product))
        # map input to the internal code
        self._product = self.PRODUCT_NAME_IMPORT[self._product]
        return True

    def set_product_support_rtscts(self, flow_control: bool):
        """
        Special handler to enable/disable on the fly
        :param flow_control: if RTS/CTS flow_control is on or off
        """
        self._validate_product_name_in_self()
        self.rtscts_flow = flow_control
        if flow_control:
            # if flow-control is enabled, we can't really publish RTS/CTS levels
            self.rtscts_out = False
            self.rtscts_in = False
        else:
            # else we handle per the product
            self.rtscts_out = self.product_has_rtscts(self._product)
            self.rtscts_in = self.product_has_rtscts(self._product)

        # seed (or delete) the initial value based on support
        if self.rtscts_out:
            self.data['rtscts_out'] = None
        elif 'rtscts_out' in self.data:
            del self.data['rtscts_out']

        if self.rtscts_in:
            self.data['rtscts_in'] = None
        elif 'rtscts_out' in self.data:
            del self.data['rtscts_in']

        return

    def validate_232_signal_tag(self, tag: str):
        """
        Given a name (like "ri_out"), make lower-case and validate is in possible set.
        Note: this does NOT test if this signal is supported; test the name only

        :param tag: the string to test
        :return: the tested string, or throws ValueError exception if not valid
        """
        tag = tag.lower()
        if tag not in self.MAPS:
            raise ValueError("RS232 signal tag:'{0}' is not valid".format(tag))
        return tag

    def product_has_dtrdsr(self, product):
        return product in self.PRODUCT_HAS_DTRDSR

    def product_has_rtscts(self, product):
        return product in self.PRODUCT_HAS_RTSCTS

    def product_has_cd_out(self, product):
        return product in self.PRODUCT_HAS_CD_OUT

    def product_has_cd_in(self, product):
        return product in self.PRODUCT_HAS_CD_IN

    def product_has_ri_out(self, product):
        return product in self.PRODUCT_HAS_RI_OUT

    def product_has_ri_in(self, product):
        return product in self.PRODUCT_HAS_RI_IN

    def _make_product_no_support_string(self, tag: str):
        """
        Assuming the tag is correct, format a string like:
            "Product:11x0 has no DTR/DSR support
        :param tag:
        :return:
        """
        return "Product:{0} has no {1} support".format(
            self.PRODUCT_FANCY_NAME[self._product], tag)

    def publish_dtrdsr_output(self, value: bool, force: bool):
        """If appropriate, publish the value we set on our DTR/DSR pair output."""
        if not self.dtrdsr_out:
            raise SerialNoSupport(self._make_product_no_support_string('dtrdsr_out'))
        return self._refresh_value('dtrdsr_out', value, force)

    def publish_dtrdsr_input(self, value: bool, force: bool):
        """If appropriate, publish the value we read from our DTR/DSR pair input."""
        if not self.dtrdsr_in:
            raise SerialNoSupport(self._make_product_no_support_string('dtrdsr_in'))
        return self._refresh_value('dtrdsr_in', value, force)

    def publish_rtscts_output(self, value: bool, force: bool):
        """If appropriate, publish the value we set on our RTS/CTS pair output."""
        if self.rtscts_flow:
            raise SerialNoSupport("RTS/CTS configured for flow-control")
        if not self.rtscts_out:
            raise SerialNoSupport(self._make_product_no_support_string('rtscts_out'))
        return self._refresh_value('rtscts_out', value, force)

    def publish_rtscts_input(self, value: bool, force: bool):
        """If appropriate, publish the value we read from our DTR/DSR pair input."""
        if self.rtscts_flow:
            raise SerialNoSupport("RTS/CTS configured for flow-control")
        if not self.rtscts_out:
            raise SerialNoSupport(self._make_product_no_support_string('rtscts_in'))
        return self._refresh_value('rtscts_in', value, force)

    def publish_cd_output(self, value: bool, force: bool):
        """If appropriate, publish the value we set on our CD output."""
        if not self.cd_out:
            raise SerialNoSupport(self._make_product_no_support_string('cd_out'))
        return self._refresh_value('cd_out', value, force)

    def publish_cd_input(self, value: bool, force: bool):
        """If appropriate, publish the value we read from our CD input."""
        if not self.cd_in:
            raise SerialNoSupport(self._make_product_no_support_string('cd_in'))
        return self._refresh_value('cd_in', value, force)

    def publish_ri_output(self, value: bool, force: bool):
        """If appropriate, publish the value we set on our RI output."""
        if not self.cd_out:
            raise SerialNoSupport(self._make_product_no_support_string('ri_out'))
        return self._refresh_value('ri_out', value, force)

    def publish_ri_input(self, value: bool, force: bool):
        """If appropriate, publish the value we read from our RI input."""
        if not self.cd_in:
            raise SerialNoSupport(self._make_product_no_support_string('ri_in'))
        return self._refresh_value('ri_in', value, force)

    def publish_activity_time(self, value: float, force: bool):
        """If appropriate, publish the time of our last activity."""
        return self._refresh_value('last_activity', value, force)

    def _refresh_value(self, tag: str, value, force=False):
        """
        Update our value (& Router API) only if value changed - or forced
        :param tag: the name in self.attrib
        :param value: the value (type can be any!)
        :param force: if True, update REGARDLESS of change
        :return: True if refreshed, else False
        :rtype: bool
        :raises: KeyError if tag is not in self.attrib
        """
        if self.data[tag] != value or force:
            # then we need to update Router API
            print("change={0}".format(tag))
            self.data[tag] = value
            self._api.put(self.data["path"] + self.MAPS[tag]["api"], value)
            return True
        return False
