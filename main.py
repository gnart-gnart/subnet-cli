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

    @classmethod
    def from_int(cls, ip_int: int) -> "IPv4Address":
        """Alternative constructor to instantiate an address from a 32-bit integer."""
        # Unpack the integer back into dotted decimal notation via masking and shifting
        octet1 = (ip_int >> 24) & 0xFF
        octet2 = (ip_int >> 16) & 0xFF
        octet3 = (ip_int >> 8) & 0xFF
        octet4 = ip_int & 0xFF
        return cls(f"{octet1}.{octet2}.{octet3}.{octet4}")

    def __str__(self) -> str:
        return self.ip_str


class SubnetPlanner:
    """Executes the bitwise logic gates to discover network boundaries and capacity."""

    def __init__(self, ip: IPv4Address, cidr: int):
        if not (0 <= cidr <= 32):
            raise ValueError("CIDR prefix must be an integer between 0 and 32.")

        self.ip = ip
        self.cidr = cidr

        # Calculate mask: Shift all 1s left by (32 - CIDR), then bound it to a 32-bit space
        self.mask_int = (0xFFFFFFFF << (32 - cidr)) & 0xFFFFFFFF
        self.subnet_mask = IPv4Address.from_int(self.mask_int)

        # Trigger core structural calculations
        self._calculate_topology()

    def _calculate_topology(self):
        """Applies raw boolean filters to locate the exact subnet boundaries."""
        # Network Address: IP bitwise-AND Mask
        self.network_int = self.ip.as_int & self.mask_int
        self.network_address = IPv4Address.from_int(self.network_int)

        # Broadcast Address: IP bitwise-OR Inverted Mask
        inverted_mask = ~self.mask_int & 0xFFFFFFFF
        self.broadcast_int = self.ip.as_int | inverted_mask
        self.broadcast_address = IPv4Address.from_int(self.broadcast_int)

        # Handle unique infrastructure edge cases (/31 point-to-point and /32 host loops)
        if self.cidr == 32:
            self.total_hosts = 1
            self.first_usable = self.network_address
            self.last_usable = self.network_address
        elif self.cidr == 31:
            self.total_hosts = 2
            self.first_usable = self.network_address
            self.last_usable = self.broadcast_address
        else:
            # Standard subnets follow the (2^(32-CIDR)) - 2 framework
            self.total_hosts = (2 ** (32 - self.cidr)) - 2
            self.first_usable = IPv4Address.from_int(self.network_int + 1)
            self.last_usable = IPv4Address.from_int(self.broadcast_int - 1)


def main():
    if len(sys.argv) > 1:
        target_input = sys.argv[1]
    else:
        target_input = input("Enter network block (e.g., 192.168.1.1/24): ")
