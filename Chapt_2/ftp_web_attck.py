#!/usr/bin/env python3
'''
FTP client that looks for anonymous enabled FTP servers.
'''
import argparse
import socket
import sys
import ftplib
from pprint import pprint
sys.path.append('../')
import mypack.fileops as fileops


def ftp_anon_conn(ftp_site):
    ''' Function that attempts to establish a FTP anonymous connection.
    '''
    try:
        client = ftplib.FTP(timeout=5)
        client.connect(ftp_site)
        client.login('anonymous', 'user@host.com')
    except ConnectionRefusedError:
        print('[-] Connection refused for {}'.format(ftp_site))
        return False
    except socket.gaierror or NameError:
        print('[-] Name or service not known {}'.format(ftp_site))
        return False
    except ftplib.error_perm:
        print('[-] Anonymous login disabled for {}'.format(ftp_site))
        return False
    except socket.timeout:
        print('[-] Server {} not responding'.format(ftp_site))
        return False
    else:
        print('[+] Anonymous login enabled on {}'.format(ftp_site))
        return True
    finally:
        client.close()
    
def main():
    parser = argparse.ArgumentParser(description='''Given a list of FTP
                                     servers. Looks for anonymous login
                                     enabled servers.''')
    parser.add_argument('-f', '--file', help='''File containing list of FTP
                        servers to read from.''', required=True)
    args = parser.parse_args()
    ftp_fname = args.file
    ftp_anons = []

    f_reader = fileops.FileReader(ftp_fname)
    for ftp_site in f_reader:
        anon_enabled = ftp_anon_conn(ftp_site)
        if anon_enabled:
            ftp_anons.append(ftp_site)
    pprint(ftp_anons)

if __name__ == '__main__':
    main()

