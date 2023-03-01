"""Extensions to fox message"""
from fox_message import FoxMessage


class ModbusMessage(FoxMessage):
    """Extensions to fox message"""

    _request_message = 0x11
    _response_message = 0x91

    def get_start_address(self):
        """Get modbus read address"""
        return (self[0xB] << 8) | self[0xC]

    def get_all_addresses(self):
        """Get array of addresses"""
        return [self.get_start_address() + 1 * i for i in range(self.get_length())]

    def get_length(self):
        """Get modbus read length"""
        return (self[0xD] << 8) | self[0xE]

    def is_read_request(self):
        """Is request"""
        return self[2] == self._request_message

    def is_read_response(self):
        """Is request"""
        return self[2] == self._response_message
