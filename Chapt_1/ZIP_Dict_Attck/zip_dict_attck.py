#!/usr/bin/python
import optparse
import zipfile
import os
from threading import Thread

# From the book: Violent Python. TJ Oconnor
# This script performs a dictionary attack on a password protected zip file. 
# It uses the zipfile library and Threads 

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

def extract_zip(z, passwd):
  # here is where the real work is performed. This script will try to extract the zip file contents using 
  # passwords provided by the dictionary list files
  try:
    z.extractall(pwd=passwd)
    print '  [!] Password found: %s' %(passwd)
    exit(0)
  except:
    pass

def dict_attck_zip(zip_f, passwd_l):
  # This function iterates through the dictionary passwd file and calls the extract zip file function through a Thread
  z = zipfile.ZipFile(zip_f, mode='r')
  for passwd in passwd_l:
    passwd = passwd.strip('\n')
    t = Thread(target=extract_zip, args=(z, passwd))
    t.start()

def main():
  parser = optparse.OptionParser('usage: prog ' +\
                                 '-f <zipfile> -d <dictionary>' +\
				 '\nThis script will perform a dictionary attack on a password protected zip file')
  parser.add_option('-f', dest='zip_f', type='string', \
                    help='Specify zip file')
  parser.add_option('-d', dest='dict_f', type='string', \
                    help='Specify dictionary file')
  (options, args) = parser.parse_args()
  if (options.zip_f == None) or (options.dict_f == None):
    print parser.usage
    exit(0)
  else:
    zip_f = options.zip_f
    dict_f = options.dict_f
    passwd_l = ret_lines(dict_f)
    dict_attck_zip(zip_f, passwd_l)

if __name__ == '__main__':
  main()
