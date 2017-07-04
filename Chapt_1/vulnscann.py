#!/usr/bin/env python3
'''
Basic banner grabber that compares obtained banners against a known list of
vulnerable services.
Intentionally, it doesn't use multithreads.
Additions that are not in the book's solution are: Use of argparser and use of
generators to read the culnerabilities file content, generate the list of
hosts we'll iterate over and the list of the banners retrieved from the
connections.
'''
import sys
import socket
import argparse
import ipaddress
import timeit
from pympler import tracker
sys.path.append('../')
import mypack.fileops as fileops

def get_banner(addr, port):
    try:
        socket.setdefaulttimeout(3)
        s = socket.socket()
        s.connect((str(addr), port))
        print('[+] Connection established to {} port {}'.format(addr, port))
        banner = s.recv(1024)
        s.close()
        return banner.decode('utf-8').strip('\n')
    except Exception as excpt:
#        print('[-] Connection failed. {} port {}. {}'.format(addr, port, excpt))
        s.close()
        return ' '

def main():
    parser = argparse.ArgumentParser(description='''Basic banner grabber and
                                                    vuln scanner''')
    parser.add_argument('--addr', help='IP Address to scan', required=True)
    parser.add_argument('--cidr', help='CIDR prefix to apply to the IP address',
                         required=True)
    parser.add_argument('--vuln', help='File containing known vulnerable banners',
                         required=True)
    args = parser.parse_args()

    addr = args.addr
    cidr = args.cidr
    fname = args.vuln
    portlist = [21,22,25,80,110,443]

    t1 = timeit.default_timer()
    tr = tracker.SummaryTracker()
    try:
        net_hosts = ipaddress.IPv4Network(addr + '/' + cidr)
    except ValueError as excpt:
        print('Check your address and CIDR: {}'.format(excpt))
        exit(1)

    hosts = (host for host in net_hosts.hosts())
    banners = (get_banner(host, port) for host in hosts for port in portlist)

    freader = fileops.FileReader(fname)
    for banner in banners:
        for vuln_line in freader:
            if banner == vuln_line:
               print(' [!] Server is vulnerable, {}'.format(banner))

    t2 = timeit.default_timer()
    print("\nTotal time to execute was: {} seconds".format(t2-t1))
    tr.print_diff()

if __name__ == '__main__':
    main()
