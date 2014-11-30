#!/usr/bin/python
import sys
import re
import os
import crypt

# Regular expressions were made using kodos !! (great tool!!)

def usage():
  print """%s <Passwd file> <Dictionary file>
This script will try to recover the password contained in the Passwd File (in a UNIX format) 
userid:passwd:lstChng:minDays:maxDays:daysExpr:daysInact:daysDisabl:flag
Using the dictionary file provided"""

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

def getUP(passwd_f):
  # This function will return a list of tuples. Each tuple in the form (userid, passwd)
  # Taken from the contents of a shadow file in unix systems
  us_passwd = []
  lines = ret_lines(passwd_f)
  # Regular expressions written with the help of the Program named Kodos
  user_re = '[$\w./]+'
  passwd_re = ':[$\w./]+'
  for line in lines:
    match = re.search(user_re, line)
    userid = match.group()
    match = re.search(passwd_re, line)
    passwd = match.group().strip(':')
    us_passwd.append((userid, passwd))
  return us_passwd

def encrypt_compare(us_passw, dict_passwd):
  # This is where the real work is done... Pay attention
  for element in us_passw:
    # For each (user, passwd) tuple. We will perform a comparison
    found = False
    user = element[0]
    passwd = element[1]
    print '[!] Running dictionary attack for user: %s' %(user)
    for dpasswd in dict_passwd:
    # Comparing (user, passwd) against the encoded version of whatever is in the dictionary file (no new lines characters though)
      dpasswd = dpasswd.strip('\n')
      # The crypt function will receive: 1. text to encrypt and 2. Algorithm info and salt
      # In my case receives something like: $6$F/Do7VWE81MLz1bm$60H1RRTd/zCt504a4iBq8whiK2flBljBFumHJ7w.FvZtYSYFn61j954X.vlvLA/MMIXPOX6UXDNpiTMrKCIji1
      # $6$ means we are using SHA-512 as hashing algorithm (Refer to man crypt)
      # F/Do7VWE81MLz1bm is the salt. The rest is the hashed result. Which will be ignored by crypt
      got = crypt.crypt(dpasswd, passwd)
      # The result is the complete string. Containing the hashing algorithm, the salt and the hashed result. Which will be compared 
      if got == passwd:
        print '  [+] Password found. \n   User: %s\n   Password: %s' %(user, dpasswd)
	found = True
	break
    if found == False:
      print 'No Password found for user: %s' %(user)

def main():
  if len(sys.argv) < 3:
    usage()
  else:
    args = sys.argv[1:]
    passwd_f = args[0]
    dict_f = args[1]
    us_passw = getUP(passwd_f)
    dict_passwd = ret_lines(dict_f)
    encrypt_compare(us_passw, dict_passwd)

if __name__ == '__main__':
  main()
