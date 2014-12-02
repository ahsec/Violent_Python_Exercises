#!/usr/bin/python
import nmap
import optparse

# From Violent Python. Syngress. TJ O'Connor
# Chapter 2. Nmap port scanner integrated into Python 

def scan_nmap(host, port):
  # This is where the magic happens
  nm = nmap.PortScanner()
  # Scanning per ip address and port
  nm.scan(host, port)
  state = nm[host]['tcp'][int(port)]['state']
  # Format and print the output
  print '[*] %s -> TCP/%s: %s' %(host, port, state)

def main():
  # Most of it is option parsing 
  p = optparse.OptionParser('Usage: %prog -H <Host IP> -p <port or ports>')
  p.add_option('-H', dest='host', type='string', help='IP Address of the host to scan')
  p.add_option('-p', dest='ports', type='string', help='Port(s) separated by commas (no spaces)')
  (options, args) = p.parse_args()
  host = options.host
  # Split the port numbers passed as arguments
  ports_l = str(options.ports).split(',')
  if (host == None) or (len(ports_l) == 0):
    print p.usage
  else:
    for port in ports_l:
      # For each port received we will run a scan
      scan_nmap(host, port)

if __name__ == '__main__':
  main()
