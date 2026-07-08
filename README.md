# Subnet CLI
A python utility designed to parse IPv4 addresses with CIDR notation
to instantly map out the entire subnet topology.

## CIDR Notation
This notation consists of an IP address, a slash, and the number of
subnet bits. For example, the CIDR block `192.168.1.1/24` indicates that
the network portion of the address is 24 bits long. Since IPv4 addresses
are 32 bits long, that leaves 8 bits for the number of hosts.

In this example, the first subnet would be `192.168.1` and the next one
would be located at `192.168.21`. Each subnet would have 254 host addresses
available, since 8 bits allows for 256 addresses, and one address is used for
the network address and another is used for the broadcast address (`256 - 2`).
