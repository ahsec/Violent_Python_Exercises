#!/usr/bin/python
import optparse
from socket import *
from threading import *
# Screen Lock will let our threads lock the screen 
# so printing doesn't look random and chaotic
screenLock = Semaphore(value=1)

# From Violent Python. TJ O'Connor
# Chapter 2. TCP Port scanner with banner grabbing and threads

def connScan(tgtHost, tgtPort):
  # Will attempt to connect (full tcp connection) to a host through a port,
  # Send data (violent python) and retrieve whatever comes back
  # If successful it will lock the screen for printing and print results
  # Otherwise, it will lock the screen and print an error message
  # In any case it will release the lock and close the socket
  try:
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((tgtHost, tgtPort))
    s.send('Violent Python\r\n')
    result = s.recv(1024)
    screenLock.acquire()
    print '  [.] Scanning port: %s' %(tgtPort)
    print '    [+] %d/tcp port open' %(tgtPort)
    print '      [>] %s' %(result.strip('\n'))
  except Exception as e: 
    screenLock.acquire()
    print '    [+] %d/tcp port close' %(tgtPort)
    print e
  finally: 
    screenLock.release()
    s.close()

def portScan(tgtHost, tgtPorts):
  # Will perform basic tests to make sure the host is reachable.
  # Get host by name (IP to FQDN)
  # Get host by address (FQDN to IP Addr)
  # And will create and execute threads for each port specified 
  try:
    tgtIP = gethostbyname(tgtHost)
  except:
    print '[-] Cannot resolve %s: Unknown host' %(tgtHost)
    return 
  try:
    tgtName = gethostbyaddress(tgtIP)
    print '[+] Scan results for: %s' %(tgtIP)
  except: 
    print '[+] Scan results for: %s' %(tgtIP)
  setdefaulttimeout(2)
  for tgtPort in tgtPorts:
    tgtPort = tgtPort.strip(',')
    tgtPort = int(tgtPort)
    # Creating and starting threads for port scanning
    t = Thread(target=connScan, args=(tgtHost, tgtPort))
    t.start()

def main():
  # Option parser (a lot of code) but looks really good for the end user
  parser = optparse.OptionParser('Usage: %prog -H ' +\
                                 '<target host> -p <target port>')
  parser.add_option('-H', dest='tgtHost', type='string',\
                     help='Specify target hostname')
  parser.add_option('-p', dest='tgtPort', type='string',\
                    help='Specify port or ports to scan (separated by commas. No spaces.)')
  (options, args) = parser.parse_args()
  tgtHost = options.tgtHost
  tgtPorts = options.tgtPort.split(',')
  if(tgtHost == None) or (tgtPorts[0] == None):
    print parser.usage
    exit(0)
  else:
    portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
  main()
