# Chapter 4. Network Traffic Analysis  with Python.  

## Exercise 1 - Where is that IP traffic headed Pt. 1
ip_to_geo.py retrieves the physical location of an IP address by using
[ipinfodb](http://ipinfodb.com/).
A subscription is required to use the service

## Exercise 2 - Where is that IP traffic headed Pt. 2
pcap_to_geo.py parses the content of a pcap file by using the dpkt library.  
It extracts information about the IPv4 traffic flows and retrieves the geo
location of the traffic source, and destination, for public IP addresses, by
using Exercise 1 as a library

## Exercise 3 - Is Anonymous really Anonymous? Analyzing LOIC traffic
The original exercise in the book parses a pcap file and looks for the strings
zip, and loic in HHTP traffic or port 6667 in either the source or the
destination. It then flags the packets that match either of those characteristics.

pcap_parse.py parses a pcap file looking for a string (that can be specified
through the command line) on HTTP traffic or a source/destination port number on
any type of TCP/UDP traffic. It then prints any packet(s) that match these
characteristics.

## Exercise 4 & 5 - Detecting Fast Flux Traffic with Scapy  
In this exercise a pcap file is provided (___domainFLux.pcap___). The pcap file
is analyzed in search of DNS requests and responses.  
The following details about the DNS traffic are then printed,
* Domain queried
* IP address or addresses returned from the query or queries  

Additionaly it also returns a list of all the domains for which DNS couldn't return a valid address. Multiple and similar domains constantly failing is an indicative of domain flux traffic.

Having multiple DNS requests that frequently return unrelated addresses could be a indication of Fast Flux traffic, specifically domain flux.

Filename for this solution is, domain_count.py

## Exercise 6 - Foiling Intrusion Detection Systems with Scapy  
This scripts works as a framework to send one of 3 groups of attacks:
* Linux Exploits  
* Network scans  
* DDoS Attacks  

Each category contains a group of packets that match IDS snort signatures.

The snort signatures being replicated are the following:

### Linux Exploits
``` python
alert udp $EXTERNAL_NET any -> $HOME_NET 518 (msg:"EXPLOIT ntalkd x86 Linux overflow"; content:"|01 03 00 00 00 00 00 01 00 02 02 E8|"; reference:bugtraq,210; classtype:attempted-admin; sid:313; rev:4;)  
alert udp $EXTERNAL_NET any -> $HOME_NET 635 (msg:"EXPLOIT x86 Linux mountd overflow"; content:"^|B0 02 89 06 FE C8 89|F|04 B0 06 89|F"; reference:bugtraq,121; reference:cve,1999-0002; classtype:attempted-admin; sid:315; rev:6;)
```

### Network Scans
``` python
alert udp $EXTERNAL_NET any -> $HOME_NET 7 (msg:"SCAN cybercop udp bomb"; content:"cybercop"; reference:arachnids,363; classtype:bad-unknown; sid:636; rev:1;)  
alert udp $EXTERNAL_NET any -> $HOME_NET 10080:10081 (msg:"SCAN Amanda client version request"; content:"Amanda"; nocase; classtype:attempted-recon; sid:634; rev:2;)
```

### DDoS Attacks
``` python
alert icmp $EXTERNAL_NET any -> $HOME_NET any (msg:"DDOS TFN Probe"; icmp_id:678; itype:8; content:"1234"; reference:arachnids,443; classtype:attempted-recon; sid:221; rev:4;)
alert icmp $EXTERNAL_NET any -> $HOME_NET any (msg:"DDOS tfn2k icmp possible communication"; icmp_id:0; itype:0; content:"AAAAAAAAAA"; reference:arachnids,425; classtype:attempted-dos; sid:222; rev:2;)
alert udp $EXTERNAL_NET any -> $HOME_NET 31335 (msg:"DDOS Trin00 Daemon to Master PONG message detected"; content:"PONG"; reference:arachnids,187; classtype:attempted-recon; sid:223; rev:3;)
alert icmp $EXTERNAL_NET any -> $HOME_NET any (msg:"DDOS TFN client command BE"; icmp_id:456; icmp_seq:0; itype:0; reference:arachnids,184; classtype:attempted-dos; sid:228; rev:3;)
```
