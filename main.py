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

    @property
    def classful_info(self) -> tuple[str, int | None]:
        """Returns a tuple of (Class Letter, Default Mask Prefix)."""
        first = self.octets[0]
        if 1 <= first <= 126:
            return ("A", 8)
        elif 128 <= first <= 191:
            return ("B", 16)
        elif 192 <= first <= 223:
            return ("C", 24)
        elif 224 <= first <= 239:
            return ("D (Multicast)", None)
        elif 240 <= first <= 255:
            return ("E (Experimental)", None)
        else:
            return ("None/Loopback", None)

    @classmethod
    def from_int(cls, ip_int: int) -> "IPv4Address":
        """Alternative constructor to instantiate an address from a 32-bit integer."""
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
        self._calculate_subnet_matrix()

    def _calculate_topology(self):
        """Applies raw boolean filters to locate the exact subnet boundaries."""
        self.network_int = self.ip.as_int & self.mask_int
        self.network_address = IPv4Address.from_int(self.network_int)

        inverted_mask = ~self.mask_int & 0xFFFFFFFF
        self.broadcast_int = self.ip.as_int | inverted_mask
        self.broadcast_address = IPv4Address.from_int(self.broadcast_int)

        if self.cidr == 32:
            self.total_hosts = 1
            self.first_usable = self.network_address
            self.last_usable = self.network_address
        elif self.cidr == 31:
            self.total_hosts = 2
            self.first_usable = self.network_address
            self.last_usable = self.broadcast_address
        else:
            self.total_hosts = (2 ** (32 - self.cidr)) - 2
            self.first_usable = IPv4Address.from_int(self.network_int + 1)
            self.last_usable = IPv4Address.from_int(self.broadcast_int - 1)

    def _calculate_subnet_matrix(self):
        """Determines how many subnets of this size fit into its classful block."""
        ip_class, default_prefix = self.ip.classful_info
        self.ip_class = ip_class

        if default_prefix is None:
            self.available_subnets = "N/A (Special/Classless IP)"
        elif self.cidr < default_prefix:
            self.available_subnets = "N/A (Supernetted Network)"
        else:
            borrowed_bits = self.cidr - default_prefix
            total_subnets = 2 ** borrowed_bits
            self.available_subnets = f"{total_subnets:,}"


def display_dashboard(planner: SubnetPlanner):
    """Output Layer: Formats the calculated data cleanly into the terminal console."""
    print("\n" + "=" * 45)
    print(f" NETWORK TOPOLOGY REPORT FOR: {planner.ip}/{planner.cidr}")
    print("=" * 45)
    print(f"Detected IP Class : Class {planner.ip_class}")
    print(f"Subnet Mask       : {planner.subnet_mask}")
    print(f"Network Address   : {planner.network_address}")
    print(f"Broadcast Address : {planner.broadcast_address}")
    print("-" * 45)

    if planner.cidr >= 31:
        print(f"Usable Host Range : {planner.first_usable} - {planner.last_usable} (Special Link Type)")
    else:
        print(f"Usable Host Range : {planner.first_usable} -> {planner.last_usable}")

    print(f"Total Usable Hosts: {planner.total_hosts:,}")
    print(f"Available Subnets : {planner.available_subnets}")
    print("=" * 45 + "\n")


def main():
    print("--- IPv4 Subnet Planner CLI ---")

    try:
        # Step 1: Prompt for and validate the target IP address baseline
        raw_ip = input("Step 1: Enter base IP address (e.g., 192.168.1.50): ")
        validated_ip = IPv4Address(raw_ip)

        # Display detected baseline info to confirm user input before proceeding
        detected_class, _ = validated_ip.classful_info
        print(f"   [Validated] Detected as a Class {detected_class} address space.")

        # Step 2: Prompt for the custom mask boundary length
        raw_cidr = input("Step 2: Enter CIDR block suffix prefix (e.g., 24): ")
        raw_cidr = raw_cidr.replace("/", "").strip()  # Strip out trailing slashes if typed out

        if not raw_cidr.isdigit():
            raise ValueError(f"CIDR prefix '{raw_cidr}' must be a pure numerical value.")

        # Instantiate coordinator and pass objects down to display engine
        completed_plan = SubnetPlanner(validated_ip, int(raw_cidr))
        display_dashboard(completed_plan)

    except ValueError as err:
        print(f"\n[!] Input Error: {err}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()