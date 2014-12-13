from scapy.all import *
from IPy import IP as IPTEST

# Violent Python
# My own variant of a program that tries to detect when is receiving traffic that may come 
# from and spoofed IP address, by comparing the TTL value of such packet against the received
# TTL value when sending an ICMP packet to the IP Address in question. 17 yrs old H.D. Moore solution
# It contains a threshold...

threshold = 7
ttl_list = {}

def testTTL(pkt):
  # The function that receives the sniffed traffic and prints the IP address and TTL value (if existing)
  try:
    if pkt.haslayer(IP):
      ipsrc = pkt[IP].src
      ttl = pkt.ttl
      if IPTEST(ipsrc).iptype() != 'PRIVATE' :
        # Only when coming from a Public IP address
        print '[+] Packet received from: %s - TTL: %s' %(ipsrc, str(ttl))
	valid(ipsrc, ttl)
  except Exception as e:
      pass

def valid(ipsrc, ttl):
  # This function tries to validate the origin by comparing TTL values
  if ttl_list.has_key(ipsrc):
    # If we already have a TTL value stored, weĺl use it for comparison,
    # else we'ĺl go to the else statement...
    ttl_g = ttl_list.get(ipsrc)
    ttl_values = range(ttl_g-threshold, ttl_g+threshold)
    if ttl not in ttl_values:
      print '  [!] Possible spoof packet from: %s !!!' %(ipsrc)
  else:
    # Creating ICMP packet with scapy 
    ans = sr1(IP(dst=ipsrc)/ICMP(), retry=0, timeout=3, verbose=0)
    # from the answer we get the received packet and the ICMP section of it
    # specifically the ttl value. That will get stored in a list
    ttl_g = ans.ttl
    ttl_list[ipsrc] = ttl_g

def main():
  sniff(prn=testTTL, store=0)

if __name__ == '__main__':
  main()
