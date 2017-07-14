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
