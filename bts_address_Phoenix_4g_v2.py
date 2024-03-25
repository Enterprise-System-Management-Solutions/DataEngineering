"""
1. inserting data from a excel to Hbase database using Phonix CLI inside from any Phonix node
2. Keep the excel in a Fixed header in any landing node.
2.1 only insert the 4G BTS address 
3. pass file name and event date as a varibale
4. last changes : add columns Division, District,Thana
5. Date : Feb 2024
"""

import jaydebeapi as jdbc
import pandas as pd
import jpype
import sys 
import os

##jar ="/opt/cloudera/parcels/CDH-7.1.3-1.cdh7.1.3.p1.6631775/jars/phoenix-5.0.0.7.1.3.1-2-client.jar"
jar ="/opt/cloudera/parcels/CDH/jars/phoenix-client-hbase-2.2-5.1.1.7.1.7.2026-3.jar"
args="-Djava.class.path=/data01/phoenix/conf:%s"% jar
jvm_path=jpype.getDefaultJVMPath()
jpype.startJVM(jvm_path,args)

drivername="org.apache.phoenix.jdbc.PhoenixDriver"
url = 'jdbc:phoenix:gzplr1cdpmas01.banglalink.net,gzplr2cdpmas02.banglalink.net,gzplr3cdpmas03.banglalink.net:2181:/hbase:phoenix/gzplr3cdpmas03.banglalink.net@BANGLALINK.NET:/etc/security/keytabs/phoenix.keytab'
conn = jdbc.connect(drivername, url,['', ''], jar)

curs = conn.cursor()

if len(sys.argv) > 1:
    dateval = sys.argv[1]

if len(sys.argv) > 2:
    file_name = sys.argv[2]

if len(sys.argv) > 3:
    nettype = sys.argv[3]
xldf = pd.read_excel(file_name, engine='openpyxl')
xldf = xldf.replace('\n|\'|"', '', regex=True)
r, c = xldf.shape
i = 0

#print(xldf['2G/3G'])
#print(list(xldf.columns))

while (r>i) :
    query = "Upsert into RND01.BTSADDRESS(SITEID,CELLID,DIVISION,DISTRICT,THANA,NETWORK_TYPE, LAC_ID, CI,ADDRESS,EVENTDATE) values('{}', '{}', '{}', '{}', '{}', '{}','{}', '{}', '{}', '{}')" \
.format(xldf.iloc[i]['*eNodeB Name'],xldf.iloc[i]['Cell Name'],xldf.iloc[i]['Division'],xldf.iloc[i]['District'],xldf.iloc[i]['Thana'], nettype,  xldf.iloc[i]['TAC'], xldf.iloc[i]['EUTRANCELLID(source-Huawei)'],xldf.iloc[i]['Address'], dateval)
    try:
#        print("Executing query:", query)
        curs.execute(query)
#        print("Query executed successfully!")
    except Exception as e:
        print("Error executing query:", e)
        # Optionally, print the problematic row
        print("Problematic row:", xldf.iloc[i])
    #conn.commit()
    #print(query)
    i+=1
    if i%100==0:
        conn.commit()

print(r,' - row have processed!!!!')

conn.commit()
conn.close()
jpype.shutdownJVM()
 
