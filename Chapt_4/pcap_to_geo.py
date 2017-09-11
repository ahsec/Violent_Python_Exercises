#!/usr/bin/env python3
'''
pcap file for this script was taken from the Network Forensic Puzzle Contest
site. http://forensicscontest.com/2009/09/25/puzzle-1-anns-bad-aim
'''
import ip_to_geo
import argparse
import ipaddress
import dpkt

class ReadPcap(object):
    def __init__(self, fname):
        self.fname = fname
    def __iter__(self):
        with open(self.fname, 'rb') as fopen:
            pcap = dpkt.pcap.Reader(fopen)
            for line in pcap:
                yield line

def get_src_dst(pcap_line):
    '''For a pcap line. Returns the SRC and DST of the traffic if the IPs
    are public.
    Also, doesn't return duplicated traffic flows.
    '''
    ip_src, ip_dst = False, False
    ts, buf = pcap_line
    try:
        eth = dpkt.ethernet.Ethernet(buf)
        ip = eth.data
        ip_src = ipaddress.ip_address(ip.src)
        ip_dst = ipaddress.ip_address(ip.dst)
    except AttributeError:
        pass
    finally:
        return(ip_src, ip_dst)

def main():
    parser = argparse.ArgumentParser(description='''For a given pcap file, it
                                    returns the source and destination
                                    geo locations for traffic with public
                                    IPs''')
    parser.add_argument('-f', '--file', help='Path to pcap file to read.',
                        required=True)
    parser.add_argument('-k', '--key', help='''Key file for the ipinfodb
                        service (for geo location''', required=True)
    args = parser.parse_args()
    pcap_fname = args.file
    key_fname = args.key

    key = ip_to_geo.get_key(key_fname)
    src_dst_list = []
    pcap_lines = ReadPcap(pcap_fname)
    pcap_src_dst = (get_src_dst(pcap_line) for pcap_line in pcap_lines)
    try:
        '''Will do 3 checks in this cycle:
           1. If scr and dst exist. Meaning, they're different than False
           2. At least one (src or dst) is global (public IP address)
           3. They do not exist in the src_dst_list meaning. We haven't printed
              this traffic flow (src-dst) in the past.
        '''
        for src, dst in pcap_src_dst:
            if ( (src and dst) and 
                 (src.is_global or dst.is_global) and
                 (str(src)+'-'+str(dst) not in src_dst_list)
               ):
                src_loc = ip_to_geo.get_ipgeo(key, src) if src.is_global else ' Private Address '
                dst_loc = ip_to_geo.get_ipgeo(key, dst) if dst.is_global else ' Private Address '
                src_dst_list.append(str(src)+'-'+str(dst))
                print('[+] SRC: {} -> DST: {}'.format(src, dst))
                print('   [-] SRC Loc: {} -> DST Loc: {}'.format(src_loc, dst_loc))
    except UnboundLocalError:
        pass
    except TypeError:
        pass

if __name__ == '__main__':
    main()
