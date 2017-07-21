# Chapter 2. Penetration Testing with Python.

## Exercise 1  
This script will attempt to establish a TCP connection to a specified host
and port list. If the connection attempt is successful it will retrieve the
banner presented by the service listening and will print the results to the
screen.

The performance of this exercise is directly proportional to the performance
of the service being queried, for this reason, I'm not presenting benchmark
comparisons for this exercise.

Book's proposed solution filename: 1-portScan.py
My proposed solution filename: tcp_synscan.py

## Exercise 2
nmap port scanner implementation using Python.  
This exercise uses the python nmap library and performs a scan, which can be
one of the following Xmas scan, syn scan, null scan or a FIN scan.
It prints the results to the screen.

The performance of this exercise is directly proportional to the performance
of the service being queried, for this reason, I'm not presenting benchmark
comparisons for this exercise.

Book's proposed solution filename: 2-nmapScan.py  
My proposed solution filename: nmap_scan.py  
The only difference between both solutions is that the later prints the whole
nmap output to the screen, including the arguments, scan details and scan
results. The former prints the results only.

## Exercise 3  
For this exercise, the book introduces both pexpect and pxssh libraries.
It then proposes the idea of a Dictionary attack on a SSH server using those
libraries.  

Books proposed solutions are:
* 3-botNet.py
* 3-pxsshCommand.py
* 3-sshBrute.py
* 3-sshCommand.py

My proposed solution uses paramiko instead. I decided to use paramiko due to its
popularity. Due to these exercises using different libraries for establishing
SSH connections, I'm not presenting benchmarks for this.

My proposed solution is: ssh_dict_atck.py

## Exercise 4
