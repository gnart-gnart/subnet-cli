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

CIDR stands for Classless Inter-Domain Routing. See more on its history, and 
how to calculate subnet topology with it, here:
[Understanding CIDR Notation in IP Subnets by Matthew Fisher](https://networkcalc.com/articles/cidr-notation/)

## How the Script Works
1. Run the script and enter an IPv4 address.
```terminaloutput
--- IPv4 Subnet Planner CLI ---
Enter network block (e.g., 192.168.1.1/24):
```
2. A class will be automatically detected. If you input an address starting 
with `0.` or `127.`, the IP will be marked as "sepcial/classless".
3. The first table displays the subnet mask, network address,
broadcast address, host range, and total usable hosts within the subnet.

Example output:
```terminaloutput
=============================================
 NETWORK TOPOLOGY REPORT FOR: 192.168.1.1/27
=============================================
Detected IP Class : Class C
Subnet Mask       : 255.255.255.224
Network Address   : 192.168.1.0
Broadcast Address : 192.168.1.31
---------------------------------------------
Usable Host Range : 192.168.1.1 -> 192.168.1.30
Total Usable Hosts: 30
Available Subnets : 8
=============================================
```

## Project Background Info
See this write-up explaining why and how I built this project:
[Subnet CLI Project](grantoxford.com/project-subnet.html)