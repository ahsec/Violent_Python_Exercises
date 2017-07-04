# Vulnerability Scanner  
This is the first exercise proposed in this chapter.
It uses the socket library to perform a TCP connection to an address and port
number.

The solution provided by the book __1-vulnScanner.py__ has the following
performance when scanning over 14 hosts,
``` bash
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

The solution proposed by me __vulnscann.py__ has the following performance over
the same number of hosts  
``` bash  
Total time to execute was: 102.96117617600248 seconds

                              types |   # objects |   total size
=================================== | =========== | ============
                       <class list |        2136 |    201.72 KB
                        <class str |        2138 |    148.27 KB
                        <class int |         379 |     10.38 KB
                       <class code |           3 |    432     B
                       <class dict |           2 |    288     B
      <class ipaddress.IPv4Address |           4 |    224     B
                  <class generator |           2 |    176     B
              function (store_info) |           1 |    136     B
                       <class cell |           2 |     96     B
                      <class tuple |           1 |     72     B
      <class ipaddress.IPv4Network |           1 |     56     B
  <class mypack.fileops.FileReader |           1 |     56     B
                     <class method |          -1 |    -64     B
```
The execution time and memory usage in both cases is similar (the book's
proposed solution is slightly better), however my proposed solution implements
argument parsing and makes use of the ipaddress module to validate and
generate the list of hosts to scan.

# UNIX Password Cracker  

The book proposes the challenge of performing a dictionary attack on a UNIX shadow file. [Wikipedia](https://en.wikipedia.org/wiki/Passwd#Shadow_file) has a good entry on the shadow file structure, including hashing algorithm and salt, both necessary to understand for this exercise.

For both the book's and mine solution, the password was located at the bottom of the __4090-worst-passwords.txt__ file.

The book's proposed solution stores the passwords to recover in the file __passwords.txt__  
``` bash
$ python 2-passwdCrack.py
[*] Cracking Password For: victim
[+] Found Password: egg

[*] Cracking Password For: root
[-] Password Not Found.

                  types |   # objects |   total size
======================= | =========== | ============
                   list |        1520 |    155.12 KB
                    str |        1522 |     85.98 KB
                    int |         148 |      3.47 KB
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

Total time to execute: 0.229640960693 seconds
```

My proposed solution stores the passwords to recover in the file __a_shadow__
``` bash
python3 shadow_breaker.py -s a_shadow -d 500-worst-passwords.txt
[+] Recovered, userid user1 password contrasena123
[+] Recovered, userid user2 password password
[-] User sync. Doesnt have a password set.
                                       types |   # objects |   total size
============================================ | =========== | ============
                                <class list |        2142 |    202.23 KB
                                 <class str |        2146 |    148.94 KB
                                 <class int |         379 |     10.36 KB
                  <class _io.BufferedReader |           1 |      4.17 KB
                                <class code |           2 |    288     B
                   <class _io.TextIOWrapper |           1 |    216     B
                           <class generator |           2 |    176     B
                       function (store_info) |           1 |    136     B
           <class mypack.fileops.FileReader |           2 |    112     B
                                <class cell |           2 |     96     B
          <class builtin_function_or_method |           1 |     72     B
                          <class _io.FileIO |           1 |     72     B
  <class encodings.utf_8.IncrementalDecoder |           1 |     56     B
       <class _io.IncrementalNewlineDecoder |           1 |     40     B
                               <class bytes |           1 |     39     B


Total time to execute: 0.29569214599905536 seconds
```
Execution time difference is 0.075 seconds, the added functionality increases the memory usage to a total of ~366 KB against the ~246 KB of the original solution.  

# ZIP File password dictionary attack  
This exercise intends to implement a dictionary attack (dictionary file __4090-worst-passwords.txt__) on a password protected ZIP file (__evil.zip__), it adds to the previous ones by introducing multi-threading.

The book's proposed solution file __3-zipCrack.py__ has the following benchmarks.
``` shell
$ python 3-zipCrack.py -f evil.zip -d 4090-worst-passwords.txt
types                       |   # objects |   total size
=========================== | =========== | ============
 list                       |        1775 |    180.59 KB
  str                       |        1789 |    101.32 KB
 dict                       |          13 |      8.05 KB
  int                       |         176 |      4.12 KB
builtin_function_or_method  |          11 |    792     B
wrapper_descriptor          |           9 |    720     B
<class zipfile.ZipInfo      |           2 |    400     B
tuple                       |           5 |    352     B
 file                       |           2 |    288     B
getset_descriptor           |           4 |    288     B
<class threading._Condition |           4 |    256     B
member_descriptor           |           3 |    216     B
weakref                     |           2 |    176     B
thread.lock                 |           4 |    128     B
<class threading.Thread     |           2 |    128     B

Total time to execute: 2.34107589722 seconds
[+] Found password secret
```  

My proposed solution __zip_breaker.py__ has the following,
``` bash
$ python3 zip_breaker.py -z evil.zip -d 4090-worst-passwords.txt
                               types |   # objects |   total size
==================================== | =========== | ============
                        <class dict |        7501 |      1.30 MB
           <class collections.deque |        1873 |      1.13 MB
  <class builtin_function_or_method |        7493 |    526.85 KB
                        <class list |        4058 |    383.51 KB
                         <class str |        5940 |    363.24 KB
                       <class tuple |        5629 |    337.23 KB
                     <class weakref |        3751 |    293.05 KB
                      <class method |        3747 |    234.19 KB
                <class _thread.lock |        3746 |    146.33 KB
         <class zipfile._SharedFile |        1873 |    102.43 KB
         <class threading.Condition |        1873 |    102.43 KB
               <class list_iterator |        1873 |    102.43 KB
             <class threading.Event |        1873 |    102.43 KB
            <class threading.Thread |        1873 |    102.43 KB
                        <class cell |        1875 |     87.89 KB

Total time to execute: 2.163734988993383 seconds
ZIP file extracted with password: secret
```  

Execution times are very close with a small difference of 0.18 seconds.
Both scripts were executed against the same ZIP file and used the same dictionary file.
