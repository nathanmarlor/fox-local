"""Modbus request message"""
import time


class ModbusRequest:
    """Modbus request message"""

    _start_byte = 0x7F
    _type_byte = 0x11

    def modbus_request(
        self,
        function,
        address,
        quantity,
    ):
        """Modbus request"""
        data = [
            1,
            function,
            (address >> 8) & 0xFF,
            address & 0xFF,
            (quantity >> 8) & 0xFF,
            quantity & 0xFF,
        ]
        return self._to_bytes(int(time.time()), data)

    def _to_bytes(self, sequence, data_array):
        """To a byte array"""
        data = bytearray()
        data.extend(self._start_byte.to_bytes(1))
        data.extend(self._start_byte.to_bytes(1))
        data.extend(self._type_byte.to_bytes(1))
        data.extend(sequence.to_bytes(4))
        data.extend(len(data_array).to_bytes(2))
        data.extend([v & 0xFF for v in data_array])
        crc = self._calculate_crc(data[2:])
        data.extend(crc.to_bytes(2, byteorder="little"))
        end_byte = ((self._start_byte & 0xF) << 4) | ((self._start_byte & 0xF0) >> 4)
        data.extend(end_byte.to_bytes(1))
        data.extend(end_byte.to_bytes(1))
        return bytes(data)

    def _calculate_crc(self, data: bytes) -> int:
        """Calculate CRC"""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x0001:
                    crc = (crc >> 1) ^ 0xA001
                else:
                    crc >>= 1
        return crc & 0xFFFF
