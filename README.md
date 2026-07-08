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

CIDR stands for Classless Inter-Domain Routing. See more on its history here:
[Understanding CIDR Notation in IP Subnets by Matthew Fisher](https://networkcalc.com/articles/cidr-notation/)

## Calculating IP Ranges from CIDR
It is helpful to convert IP addresses into 32-bit long binary.
For example, `192.168.1.1` is `11000000 10101000 00000001 00000001`.
The `/24` in the previous example makes the first 24 bits (first 3 groups
of bits) into the network portion of the address. 