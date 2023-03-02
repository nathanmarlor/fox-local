"""Extensions to fox message"""
import logging

from fox_message import FoxMessage

_LOGGER = logging.getLogger(__name__)


class ModbusMessage(FoxMessage):
    """Extensions to fox message"""

    _request_message = 0x11
    _response_message = 0x91

    def address_is_present(self, start, length):
        """Is address present in data"""
        all_addr = self.get_all_addresses()
        parser_addr = self._expand_addresses(start, length)
        return set(parser_addr).issubset(all_addr)

    def is_read_request(self):
        """Is request"""
        return self[2] == self._request_message

    def is_read_response(self):
        """Is request"""
        return self[2] == self._response_message

    def get_data(self):
        """Get data from message"""
        data = []
        for i in range(self[0xB] // 2):
            part = 0xC + i * 2
            value = (self[part] << 8) + self[part + 1]
            data.append(value)
        return data

    def get_all_addresses(self):
        """Get array of addresses"""
        return self._expand_addresses(self._get_start_address(), self._get_length())

    def _get_start_address(self):
        """Get modbus read address"""
        return (self[0xB] << 8) | self[0xC]

    def _get_length(self):
        """Get modbus read length"""
        return (self[0xD] << 8) | self[0xE]

    def _expand_addresses(self, start, length):
        """Expand addresses into array"""
        return [start + (1 * i) for i in range(length)]
