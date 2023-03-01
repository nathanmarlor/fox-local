"""Base parser"""


class BaseParser:
    """Base parser"""

    def can_parse(self, data):
        """Can parse"""
        pass

    def parse(self, data, index):
        """Parse data"""
        pass

    def is_info(self, data):
        """Check if info message"""
        return (data[0] == 0x7E and data[1] == 0x7E) and (
            data[-1] == 0xE7 and data[-2] == 0xE7
        )
