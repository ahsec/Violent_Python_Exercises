# Vulnerability Scanner  
This is the first exercise proposed in this chapter.
It uses the socket library to perform a TCP connection to an address and port number.

The solution provided by the book _1-vulnScanner.py_ has the following performance when scanning over 14 hosts,
```
Total time to execute was: 101.722756863 seconds

                  types |   # objects |   total size
======================= | =========== | ============
                   list |        1516 |    154.77 KB
                    str |        1517 |     85.72 KB
                    int |         146 |      3.42 KB
                   dict |           1 |      1.02 KB
     wrapper_descriptor |           4 |    320     B
      member_descriptor |           2 |    144     B
                   code |           1 |    128     B
  function (store_info) |           1 |    120     B
                   cell |           2 |    112     B
                weakref |           1 |     88     B
      getset_descriptor |           1 |     72     B
                  tuple |           0 |      8     B
         instancemethod |          -1 |    -80     B
```

The solution proposed by me has the following performance over the same number of hosts  
```
Total time to execute was: 102.96117617600248 seconds

                              types |   # objects |   total size
=================================== | =========== | ============
                       <class 'list |        2136 |    201.72 KB
                        <class 'str |        2138 |    148.27 KB
                        <class 'int |         379 |     10.38 KB
                       <class 'code |           3 |    432     B
                       <class 'dict |           2 |    288     B
      <class 'ipaddress.IPv4Address |           4 |    224     B
                  <class 'generator |           2 |    176     B
              function (store_info) |           1 |    136     B
                       <class 'cell |           2 |     96     B
                      <class 'tuple |           1 |     72     B
      <class 'ipaddress.IPv4Network |           1 |     56     B
  <class 'mypack.fileops.FileReader |           1 |     56     B
                     <class 'method |          -1 |    -64     B
```
The execution time and memory usage in both cases is similar (the book's proposed solution is slightly better), however my proposed solution implements argument parsing and makes use of the ipaddress module to validate and generate the list of hosts to scan.
