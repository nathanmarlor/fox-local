"""Extensions to built in bytes"""


class FoxBytes(bytes):
    """Extensions to built in bytes"""

    def to_string(self, index) -> str:
        """Convert bytes to string"""
        return self[index : index + self.data_length()].decode("utf8", "ignore")

    def data_length(self) -> int:
        """Get length of data portion"""
        return self[0x08] | (self[0x07] << 8)
