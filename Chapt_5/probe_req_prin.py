#!/usr/bin/env python3
"""Listens to Wireless probe requests over a specific interface. Once it
identifies a request/response pair, it prints the BSSID details
"""
import argparse
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy import all as scapy
import scapy.layers.dot11 as dot11

def get_probes(pkt):
    '''When receiving a packet from scapy's sniif function; it looks for a
    Dot11 Probe request and prints it's information.
    '''
    prob_reqs = []
    if pkt.haslayer(dot11.Dot11ProbeReq):
        prob_info = pkt.getlayer(dot11.Dot11ProbeReq).info
        if prob_info not in prob_reqs:
            prob_reqs.append(prob_info)
            print('Detected 802.11 probe: {}'.format(prob_info))

def main():
    ''' Argument Parsing and main procedure.
    '''
    parser = argparse.ArgumentParser(description='''Listens to Wireless probe
                                     requests over a specific interface. Once
                                     it identifies a request/response pair, it
                                     prints the BSSID details''')
    parser.add_argument('interface', help='''Interface to listen for 802.11
                                          probes''')
    args = parser.parse_args()
    user_intf = args.interface
    try:
        print("Sniffing for 802.11 probes on interface {}".format(user_intf))
        scapy.sniff(iface=user_intf, prn=get_probes)
    except PermissionError:
        raise SystemExit('Error: Execute with sudo privileges')
    except OSError:
        raise SystemExit("Error: Interface doesn't exist")
if __name__ == '__main__':
    main()
