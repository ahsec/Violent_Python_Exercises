#!/usr/bin/env python3
'''Reads packets from a pcap file, extracts the DNS queries and responses from
the packets and prints all the domains along with the number of different IPs
that were found per domain. This help detect domain flux traffic.
'''
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import argparse
import scapy.all
from pprint import pprint
from collections import defaultdict

class Capture(object):
    def __init__(self, fname):
        self.fname = fname
        self.pkts = scapy.all.rdpcap(self.fname)
        self.dns_info, self.dns_fails = self.get_dns_records()
    def get_dns_records(self):
        dns_info = defaultdict(list)
        dns_fails = []
        for pkt in self.pkts:
            if pkt.haslayer(scapy.all.DNSRR):
                rcode = pkt.getlayer(scapy.all.DNS).rcode
                qname = pkt.getlayer(scapy.all.DNSQR).qname
                if rcode == 3:
                    # Failed DNS request
                    dns_fails.append(qname)
                else:
                    rrname = pkt.getlayer(scapy.all.DNSRR).rrname
                    rdata = pkt.getlayer(scapy.all.DNSRR).rdata
                    try:
                        dns_info[rrname.decode('utf-8')].append(rdata)
                    except UnicodeDecodeError:
                        dns_info[rrname.decode('utf-8')].append('ERROR')
        return dns_info, dns_fails

def main():
    parser = argparse.ArgumentParser(description='''Reads packets from a given
                                        pcap file, prints the DNS domains and
                                        addresses related to the DNS queries
                                        found in the pcap file.''')
    parser.add_argument('-f','--file', help='pcap file to read', required=True)
    args = parser.parse_args()
    pcap_fname = args.file

    capture = Capture(pcap_fname)
    dns_entries = capture.get_dns_records()
    for key, value in capture.dns_info.items():
        print('Domain: {} resolved to {} different addresses.'.format(key, len(value)))
    print("\n##### Possible domains for which DNS req didn't return a valid address")
    pprint(capture.dns_fails)

if __name__ == '__main__':
    main()
