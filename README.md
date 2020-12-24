# Python_System_Monitor
Python Script that records CPU, Memory, Bandwidth, Traffic, and Open-Ports
Created on Mon Dec 21 14:52:07 2020
#https://psutil.readthedocs.io/en/latest/#
@author: elilieberman

1. The "monitor" collects system utilization data in ten second intervals, cross-platform  
   tested in Windows and Linux, uses standard Python libraries. (OS, Sys, Time, Psutil, Datetime, Pandas).

2. To exit BASELINE, after prompted TYPE 0 (zero) at any time

3. The script can be run from the command line, "python baseline.py", 
   or executed by an IDLE i.e. Spyder

4. A "performance" report is created with; cpu usage, virtual memory usage, data sent, bandwidth, 
   and number of ports open, with username and timestamp.

5. The data points are exported as a csv with labels, easily reviewed in Excel, 
   called performanceTimeStamp.csv (filename = performance + timestamp), 
   forensic reference for suspected intrusions.

6. Additionally, a "ports" reports is created about all open-port numbers,
   (Established connection) adapters, with timestamp (aligning with performance data), 
   memoralizing forensic data to identify suspicious connections.

7. Both reports are saved to the USER's "downloads" directory ( Linx and Windows) as CSV's.
