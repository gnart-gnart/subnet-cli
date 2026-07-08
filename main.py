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

    def _validate_and_parse(self) -> list[int]:
        """Validates that the IP string consists of 4 valid decimal octets."""
        parts = self.ip_str.split(".")
        if len(parts) != 4:
            raise ValueError("IP address must contain exactly 4 octets separated by dots.")

        octets = []
        for part in parts:
            if not part.isdigit():
                raise ValueError(f"Invalid non-numeric character found in octet: '{part}'")
            val = int(part)
            if not (0 <= val <= 255):
                raise ValueError(f"Octet value '{val}' is outside the valid 0-255 range.")
            octets.append(val)
        return octets

def main():
    if len(sys.argv) > 1:
        target_input = sys.argv[1]
    else:
        target_input = input("Enter network block (e.g., 192.168.1.1/24): ")
