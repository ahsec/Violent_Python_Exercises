#!/usr/bin/python
import scapy
import pygeoip
from scapy.all import *

# This file gets reads a pcap file, extracts the IP Addresses in it
# as a conversation (source, destination) and tries to obtain the 
# phisycal location of each (using Geocity DB) If found prints all the
# found locations to a KML file for visualazing in Google earth


gi = pygeoip.GeoIP('GeoLiteCity.dat')
def printRecord(src, dst):
  # Where the juice is produced !!
  # Gets the info from the DB file and formats the output
  Loc_Info = ''
  kml_cont = ''
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
      longitude = rec['longitude']
      latitude = rec['latitude']
      Loc_Info = Loc_Info + '  %s, %s, %s   %s ' %(city, region, country, char)
      if (longitude != None) and (latitude != None):
        kml_cont = kml_cont + retKML(tgt)
    elif rec == None:
      Loc_Info = Loc_Info + '  Location not registered %s' %(char)
  return kml_cont

def print_src_dest(pkts_list):
  for p in pkts_list:
    if p.haslayer(IP):
#      print '%s -> %s' %(p[IP].src, p[IP].dst)
      Loc_Info = printRecord(p[IP].src, p[IP].dst)
      return Loc_Info

def read_pcap(pcapFile):
  pkts_list = rdpcap(pcapFile)
  return pkts_list

def retKML(ip):
  rec = gi.record_by_name(ip)
  try:
    longitude = rec['longitude']
    latitude = rec['latitude']
    kml = ('<Placemark>\n'+
           '<name>%s</name>\n'+
	   '<Point>\n'+
	   '<coordinates>%6f,%6f</coordinates>\n'+
	   '</Point>\n'
	   '</Placemark>\n') %(ip, longitude, latitude)
    return kml
  except Exception as e:
    return ''

def main():
  pcapFile = 'attack-trace.pcap'
  pkts_list = read_pcap(pcapFile)
  kml_info = print_src_dest(pkts_list)
  kmlheader = '<?xml version="1.0" encoding="UTF-8"?>\n'+\
              '<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
  kmlfooter = '</Document>\n</kml>\n'
  kmldoc = kmlheader + kml_info + kmlfooter
  print kmldoc
	      
if __name__ == '__main__':
  main()
