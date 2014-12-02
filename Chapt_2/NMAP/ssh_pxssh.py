#!/usr/bin/python
import pxssh

# Violent Python
# Chapt 2. pxssh. Starting ssh sessions and sending commands
# Real Passwords have been modified with the intention of 
# protecting their real identities

def connect(host, user, passwd):
  # Start and return the ssh session
  try:
    session = pxssh.pxssh()
    session.login(host, user, passwd)
    return session
  except:
    # Unless of course there is an exception
    print '[!] Error connecting to host'
    exit(0)

def send_command(session, command):
  # Once we have a session we will send commands through it.
  # And close the session once we are done
  session.sendline(command)
  session.prompt()
  session.close()
  print session.before

def session_ssh(host, user, passwd, command):
  # To call both methods defined before
  session = connect(host, user, passwd)
  send_command(session, command)

def main():
  # We could insert a good bruteforcer here !!
  host = 'localhost'
  user = 'angelus'
  passwd = 'TopSecret2012'
  command = 'cat /etc/passwd'
  session_ssh(hostu, user, passwd, command)

if __name__ == '__main__':
  main()
