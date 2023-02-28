"""Extensions to built in bytes"""


class FoxMessage(bytes):
    """Extensions to built in bytes"""

    def to_string(self, index, length) -> str:
        """Convert bytes to string"""
        return self[index : index + length].decode("utf8", "ignore")

    def data_length(self) -> int:
        """Get length of data portion"""
        return self[0x08] | (self[0x07] << 8)

    def is_info(self):
        """Info read message"""
        start_marker = self[:2] == bytes.fromhex("7E7E")
        end_marker = self[-2:] == bytes.fromhex("E7E7")

        return all([start_marker, end_marker])

    def is_modbus(self):
        """Modbus message"""
        start_marker = self[:2] == bytes.fromhex("7F7F")
        end_marker = self[-2:] == bytes.fromhex("F7F7")

        return all([start_marker, end_marker])
