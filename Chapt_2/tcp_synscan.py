#!/usr/bin/env python3
''' TCP syn scanner that receives a host ip address and ports to scan.
It performs a syn scan and returns the banner received.
'''
import argparse
import socket
import threading

slock = threading.Semaphore(value=1)

def host_scan(host, port):
    '''Performs a scan per host and port.
    '''
    socket.setdefaulttimeout(5)
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        c_socket.connect((host, port))
        message = "         \r\n\r\n"
        c_socket.sendall(message.encode())
        banner = c_socket.recv(100)
        slock.acquire()
    except OSError as os_err:
        print('[!] Host {} port {} - Error: {}'.format(host, port, os_err))
    else:
        print('[+] Connected to host {} on port {}'.format(host, port))
        print('    Banner: {}'.format(banner))
    finally:
        slock.release()
        c_socket.close()

def main():
    parser = argparse.ArgumentParser(description='''TCP syn scanner that
                                      returns the received banners.''')
    parser.add_argument('-o', '--host', help='Host to scan', required=True)
    parser.add_argument('-p', '--port', help='Ports to scan', required=True,
                        nargs='+')
    args = parser.parse_args()
    host = args.host
    ports = args.port
    for port in ports:
        port = int(port.strip(','))
        thr = threading.Thread(target=host_scan, args=(host, port))
        thr.start()

if __name__ == '__main__':
    main()
