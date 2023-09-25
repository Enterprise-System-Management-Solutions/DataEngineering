"""
Created on Sun Jun 27 13:02:38 2023

@author: khairul

list hive partitions 

"""

import os
import sys
import time
import subprocess
from datetime import datetime, timedelta

JDBC="jdbc:hive2://gzplr1cdpmas01.banglalink.net:2181,gzplr2cdpmas02.banglalink.net:2181,gzplr3cdpmas03.banglalink.net:2181/default;principal=hive/_HOST@BANGLALINK.NET;serviceDiscoveryMode=zooKeeper;ssl=true;sslTrustStore=/var/lib/cloudera-scm-agent/agent-cert/cm-auto-global_truststore.jks;zooKeeperNamespace=hiveserver2"

dtobj=datetime.today()
dt=dtobj.strftime('%Y%m%d')
dtt=dtobj.strftime('%Y-%m-%d')
#dt='20220623'
input_file = '/home/airflow/DevOps/td_backup_object_list.txt'
output_file = '/home/airflow/DevOps/td_partitions_output.txt'


f = open(input_file)
for line in f:
    line = line.strip('\n')
    print('The Table Name : '.format(line))
    os.system('beeline -u "{}" -e "select \'{}\';"'.format(JDBC,line))
    os.system('beeline -u "{}" -e "show partitions {};"'.format(JDBC,line))

