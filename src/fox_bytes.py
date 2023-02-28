"""Extensions to built in bytes"""


class FoxBytes(bytes):
    """Extensions to built in bytes"""

    def to_string(self, index):
        """Convert bytes to string"""
        s = self[index : index + self.data_length()].decode("utf8", "ignore")
        print(s)
        return s

    def data_length(self):
        """Get length of data portion"""
        return self[0x08] | (self[0x07] << 8)
