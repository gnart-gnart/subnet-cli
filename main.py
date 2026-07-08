import sys

class IPv4Address:
    """Represents a 32-bit IPv4 address and handles text-to-binary conversions."""
    def __init__(self, ip_str: str):
        self.ip_str = ip_str.strip()
        self.octets = self._validate_and_parse()
        # Pack the 4 octets into a single 32-bit integer using bit-shifts
        self.as_int = (
            (self.octets[0] << 24)
            | (self.octets[1] << 16)
            | (self.octets[2] << 8)
            | self.octets[3]
        )

def main():
    if len(sys.argv) > 1:
        target_input = sys.argv[1]
    else:
        target_input = input("Enter network block (e.g., 192.168.1.1/24): ")
