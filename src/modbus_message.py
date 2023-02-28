"""Extensions to fox message"""
from fox_message import FoxMessage


class ModbusMessage(FoxMessage):
    """Extensions to fox message"""

    _request_message = 0x11
    _response_message = 0x91

    def get_address(self):
        """Get modbus read address"""
        return (self[0xB] << 8) | self[0xC]

    def is_read_request(self):
        """Is request"""
        return self[2] == self._request_message

    def is_read_response(self):
        """Is request"""
        return self[2] == self._response_message
