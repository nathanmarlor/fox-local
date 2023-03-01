"""Extensions to fox message"""
from fox_message import FoxMessage


class ModbusMessage(FoxMessage):
    """Extensions to fox message"""

    _request_message = 0x11
    _response_message = 0x91

    def address_is_present(self, start, length):
        """Is address present in data"""
        set(self._expand_addresses(start, length)).issubset(self._get_all_addresses())

    def is_read_request(self):
        """Is request"""
        return self[2] == self._request_message

    def is_read_response(self):
        """Is request"""
        return self[2] == self._response_message

    def _get_all_addresses(self):
        """Get array of addresses"""
        return [self._get_start_address() + 1 * i for i in range(self._get_length())]

    def _get_start_address(self):
        """Get modbus read address"""
        return (self[0xB] << 8) | self[0xC]

    def _get_length(self):
        """Get modbus read length"""
        return (self[0xD] << 8) | self[0xE]

    def _expand_addresses(self, start, length):
        """Expand addresses into array"""
        return [start + 1 * i for i in range(length)]
