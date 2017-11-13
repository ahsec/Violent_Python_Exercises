#!/usr/bin/env python3
''' Script to parse a pcap file.
Identifies a string in HTTP traffic or traffic with an specific destination
port.
'''
import dpkt
import argparse
import ipaddress

class ReadPcap(object):
    def __init__(self, fname):
        self.fname = fname
    def __iter__(self):
        with open(self.fname, 'rb') as fopen:
            pcap = dpkt.pcap.Reader(fopen)
            for line in pcap:
                yield line

def break_pcap(pcap_line):
    '''For a pcap line (returned  by ReadPcap class) it returns
    (eth, ip, ip_src, ip_dst, tcp, port_src, port_dst, http)
    if any of these doesn't exist in the pcap file, it returns False instead
    '''
    eth, ip, ip_src, ip_dst = False, False, False, False
    tcp, port_src, port_dst, http = False, False, False, False
    ts, buf = pcap_line
    try:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        ip_src = ipaddress.ip_address(ip.src)
        ip_dst = ipaddress.ip_address(ip.dst)
        tcp = ip.data
        port_src = tcp.sport
        port_dst = tcp.dport
        http = dpkt.http.Request(tcp.data)
    except AttributeError:
        pass
    finally:
        pcap_attr = {'eth':eth, 'ip':ip, 'ip_src':ip_src, 'ip_dst':ip_dst,
                     'tcp':tcp, 'port_src':port_src, 'port_dst':port_dst,
                     'http':http}
        return pcap_attr

def main():
    parser = argparse.ArgumentParser(description='''Parses a pcap file. It
                                    identifies a specific string on HTTP traffic
                                    (port 80) or prints all the traffic that
                                    has a specific destination port.''')
    parser.add_argument('pcap', help='Path to pcap file to parse')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--http', help='''Looks for a specific string in HTTP
                       traffic''', type=str)
    group.add_argument('--port', help='''Looks for traffic going to a specific
                       destination port''', type=int)
    args = parser.parse_args()
    fname = args.pcap

    pcap_lines = ReadPcap(fname)
    pcap_args = (break_pcap(pcap_line) for pcap_line in pcap_lines)
    if args.http:
        http_string = args.http
        # HTTP String Search
        for element in pcap_args:
            http_uri = element.get('http')
            if http_uri and (http_string.lower() in str(http_uri).lower()):
                print('[*] String {} found in HTTP traffic'.format(http_string))
                print('[-] Traffic Source: {}:{}'.format(element.get('ip_src'),
                                                         element.get('port_src')))
                print('[-] Traffic Destination: {}:{}'.format(element.get('ip_dst'),
                                                              element.get('port_dst')))
                print(str(http_uri))
    if args.port:
        port_num = args.port
        # Port number traffic search
        for element in pcap_args:
            port_dst = int(element.get('port_dst'))
            port_src = int(element.get('port_src'))
            if port_dst and (args.port in [port_dst, port_src]):
                print('[*] Port {} found in traffic'.format(args.port))
                print('[-] Traffic Source: {}:{}'.format(element.get('ip_src'),
                                                      element.get('port_src')))
                print('[-] Traffic Destination: {}:{}'.format(element.get('ip_dst'),
                                                      element.get('port_dst')))
                print()

if __name__ == '__main__':
    main()
