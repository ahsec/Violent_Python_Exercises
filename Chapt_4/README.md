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
characteristics
