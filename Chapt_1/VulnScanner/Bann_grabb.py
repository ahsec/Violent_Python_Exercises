#!/usr/bin/python
import sys
import socket
import os

# Violent Python. TJ O'Connor. Syngress
# Banner grabber which compares banners against a 
# known list of vulnerable services

def ret_Banner(ip, port):
  try:
    socket.setdefaulttimeout(1)
    s = socket.socket()
    s.connect((ip, port))
    banner = s.recv(1024)
    return banner
  except:
    return

def readfile(vulns_file):
  f = open(vulns_file, 'r')
  lines = f.readlines()
  f.close()
  return lines

def checkVulns(banner, lines):
  for line in lines:
    line = line.strip('\n')
    if line in banner:
      print '  [+] Vulnerable Service: %s' %(banner)

def verify_file(vulns_file):
  if not os.path.isfile(vulns_file):
    print '[-] %s doesn\'t exist' %(vulns_file)
    exit(0)
  elif not os.access(vulns_file, os.R_OK):
    print '[-] %s Access Denied' %(vulns_file)
    exit(0)
  print '[*] Reading file: %s for vulnerability information' %(vulns_file)

def usage():
  print '[-] Usage: %s <vulns_file>' %(sys.argv[0])

def main():
  if len(sys.argv) != 2:
    usage()
  else:
    vulns_file = sys.argv[1]
    verify_file(vulns_file)
    lines = readfile(vulns_file)
    portList = [22, 80, 443]
    for x in range(1,10):
      ip = '192.168.1.%s' %(x)
      for port in portList:
        print '[+] Scanning %s:%s' %(ip, port)
        banner = ret_Banner(ip,port)
        if banner:
          print '  [+] %s : %s' %(ip, banner.strip('\n'))
          checkVulns(banner, lines)
      print '\n'

if __name__ == '__main__':
  main()
