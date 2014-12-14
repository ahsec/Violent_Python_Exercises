from scapy.all import *

# This script will "listen" the 802.11 channels  searching for Probe Reqs
# Packets send by a wifi client to connect to its AP. It will show the name of
# the BSSID being looked for

# List containing the found BSSIDs
prob_reqs = []

def sniffProbe(pkt):
  # When recieving a packet it will look for a .11 layer
  # and a Probe Request layer, once found it will print 
  # the name of the found network
  if pkt.haslayer(Dot11ProbeReq):
    netName = pkt.getlayer(Dot11ProbeReq).info
    if netName not in prob_reqs:
      prob_reqs.append(netName)
      print '[+] Detected Probe Req: %s' %(netName)
    
def main():
  # The starnge name of my wifi interface 
  # And starting the scapy sniffer (sending the packets to 
  # the handler function
  interface = 'wlp0s19f2u2'
  sniff(iface=interface, prn=sniffProbe)

if __name__ == '__main__':
  main()
