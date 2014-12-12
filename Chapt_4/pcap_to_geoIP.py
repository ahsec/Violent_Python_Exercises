#!/usr/bin/python
import scapy
import pygeoip
from scapy.all import *

# Violent Python. With modifications made by me.
# This script reads a pcap file and prints all the IP addresses source and destination
# Found, along with a summary of the location of those IP addresses (if found by the 
# GeoLiteCity database

gi = pygeoip.GeoIP('GeoLiteCity.dat')

def printRecord(src, dst):
  # Where the juice is produced !!
  # Gets the info from the DB file and formats the output
  Loc_Info = ''
  for i in range (0,2):
    if i == 0:
      tgt = src
      char = '->'
    else:
      tgt = dst
      char = ' '
    rec = gi.record_by_name(tgt)
    if rec != None:
      city = rec['city']
      region = rec['metro_code']
      country = rec['country_name']
      Loc_Info = Loc_Info + '  %s, %s, %s   %s ' %(city, region, country, char)
    elif rec == None:
      Loc_Info = Loc_Info + '  Location not registered %s' %(char)
  return Loc_Info

def print_src_dest(pkts_list):
  # From the list of packets, reads the source and dest IP for each packet
  for p in pkts_list:
    if p.haslayer(IP):
      print '%s -> %s' %(p[IP].src, p[IP].dst)
      Loc_Info = printRecord(p[IP].src, p[IP].dst)
      print Loc_Info

def read_pcap(pcapFile):
  # Returns the content of the pcap file as a list
  pkts_list = rdpcap(pcapFile)
  return pkts_list

def main():
  pcapFile = 'attack-trace.pcap'
  pkts_list = read_pcap(pcapFile)
  print_src_dest(pkts_list)

if __name__ == '__main__':
  main()
