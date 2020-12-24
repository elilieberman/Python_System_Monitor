#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 14:52:07 2020
#https://psutil.readthedocs.io/en/latest/#
@author: elilieberman

1. The "monitor" collects system utilization data in ten second intervals, 
   tested in Windows and Linux, using standard 
   native Python libraries (OS, Sys, Time, Psutil, Datetime, Pandas).

2. The script can be run from the command line, "python baseline.py", 
   or executed by an IDLE i.e. Spyder

3. A "performance" report is created with; cpu usage, virtual memory usage, data sent, bandwidth, and 
   number of ports open, with username and timestamp.

4. The data points are exported as a csv with labels, easily imported/reviewed in Excel, called performanceTimeStamp.csv (filename = performance + timestamp), over time a frame of reference for suspected intrusions.

5. Additionally, a "ports" reports is created about all open-port numbers,
   (Established connection) adapters, with timestamp (aligning with performance data), 
   memoralizing forensic data to identify suspicious connections.

6. Both reports are saved to the USER's "downloads" directory (both Linx and Windows) as CSV's.

"""
#%%
terminate_flag = False

def monitor():
    'Required Libraries'
    import os
    import sys
    import time
    import psutil
    import datetime
    import pandas as pd
    #import platform; print(platform.system())
    
    print('Confirmed: running',sys.platform)
    
    'Containers for reports'
    perf = pd.DataFrame(columns=['Date', 'User','CPU_pct', 'Mem_pct', 'DataSent_mb', 'BandwidthUsed_mb','PortsOpen_cnt'])
    ports = pd.DataFrame(columns=['Date', 'OpenPorts'])
    
        
    'Retrieve port data for report'
    flag = 1
    while not terminate_flag:
        try:
            psutil.net_connections()
            port  = [x[3][1] for x in psutil.net_connections() if x.status == psutil.CONN_ESTABLISHED]  
            port.sort(reverse = False)
            port_cnt = len(port)
            #concatenate ports as strings for report
            port_string = [str(int) for int in port] 
            port_str = ",".join(port_string)
        
        
            
        except psutil.AccessDenied:
            print("Python can't open your network adapter connections")
            
        except:
            print('Unable to read io_counter byte traffic')   
        
        'Retrieve user and system performance data'
        try:
            user = psutil.users()[0][0]
            cpu = psutil.cpu_percent()  #cpu usage 
            vmem = psutil.virtual_memory()[2] #memory usage
        
        except:
           print('Unable to read a user/cpu/memory variable')      
        
        
        'Retrieve network internet traffic data, set datestamp'
        try:
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            start_bytes = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            sleep = 1 ; time.sleep(sleep)
            end_bytes = psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv
            sent_mb = round((end_bytes - start_bytes)/((1024**2)*6), 6)
            bandwidth_mb =round(((end_bytes - start_bytes)*8)/(1024**2), 4)
                    
            'Collect results and create reports, convert bytes to bit and megabits'
            perf_summary = [dt_string, user,cpu,vmem, sent_mb, bandwidth_mb,port_cnt]
            perf.loc[len(perf),:] = perf_summary
            port_summary = (dt_string,port_str)
            ports.loc[len(ports),:] = port_summary
            
        except:
            print('Unable to read io_counter byte traffic')
      
    print('Preview of Performance Report saved to file:',"\n",perf_summary)
    time.sleep(1)
    print('Preview of Ports_Open Report saved to file:',"\n",port_summary)
    time.sleep(2)
    
    'Save Reports'
    tm_str = now.strftime("%H%M%S")
    
    if "win" in sys.platform.lower():
        try:
            file1 = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + '\downloads\\'+'performance_'+tm_str+'.csv'
            file2 = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + '\downloads\\'+'ports_'+tm_str+'.csv'
        except:
            print("Was not able to Save file, Windows file issue")
    
    else:
        try:
            file1 = os.environ['HOME'] +'/Downloads/performance_'+tm_str+'.csv'
            file2 = os.environ['HOME'] +'/Downloads/ports_'+tm_str+'.csv'
        except:
            print("Was not able to Save file, Linux file issue")
        
    
    try:
        perf.to_csv(file1, index = False)
        ports.to_csv(file2, index = False)
        
    except OSError:
        print("Couldn't save the report to", os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'])
    except:
        print("Couldn't save the report to", os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'])
    

from threading import Thread
p = Thread(target=monitor)
p.start()
try:
    input('Hit enter or ctrl-c to terminate ...')
except KeyboardInterrupt:
    pass
terminate_flag = True # tell monitor it is time to terminate
p.join() # wait for monitor to gracefully terminate