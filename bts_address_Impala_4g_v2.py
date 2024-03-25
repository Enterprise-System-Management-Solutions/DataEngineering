#!/usr/bin/env python
# coding: utf-8

"""
1. inserting data from a excel to impala database using impala CLI inside from any impala cluster
2. Keep the excel in a Fixed header in any landing node.
2.1 only insert the 4G BTS address 
3. pass file name and event date as a varibale
4. last changes : add columns Division, District, Thana
5. Date : Feb 2024
"""

from impala.dbapi import connect
import pandas as pd
import sys

##create dinamic input with 
fileName = sys.argv[1]
dateval = sys.argv[2]
netType = sys.argv[3]

#Define Impala Connection
impala_host='gzplr4cdpdat07.banglalink.net'
impala_port=21050
impala_ssl=True
impala_db='layer2'
impala_user='bl_impala_user'
impala_krb_service_name='impala'
impala_auth='GSSAPI'

def impala_init():
    conn = connect(host=impala_host, port=impala_port, use_ssl=impala_ssl, database=impala_db, user=impala_user, kerberos_service_name=impala_krb_service_name, auth_mechanism=impala_auth)
    return conn

conn=impala_init()
cur = conn.cursor()

xldf = pd.read_excel(fileName, engine='openpyxl')

xldf = xldf.replace('\n|\'|,|"', '', regex=True)

xldf=xldf.fillna(0)

r, c = xldf.shape

xldf=xldf.astype('string')

xldf['zero']='0'

xldf['location']=xldf[['zero','eNodeB ID','Cell ID']].agg(''.join, axis=1)

xldf=xldf.drop(['zero'],axis=1)


i = 0
insertLs=[]
while (r-1>i) :
    i+=1
    insertLs.append('("'+xldf.iloc[i]['Cell Name']+'","'+xldf.iloc[i]['*eNodeB Name']+'","'+xldf.iloc[i]['Vendor ']+'","'+ netType +'","'+
    xldf.iloc[i]['Division']+'","'+xldf.iloc[i]['District']+'","'+xldf.iloc[i]['Thana']+'","'+
    xldf.iloc[i]['eNodeB ID']+'","'+xldf.iloc[i]['Cell ID']+'","'+xldf.iloc[i]['EUTRANCELLID(source-Huawei)']+'","'+
    xldf.iloc[i]['TAC']+'","'+xldf.iloc[i]['Antenna DIRECTION']+'","'+xldf.iloc[i]['LATITUDE']+'","'+xldf.iloc[i]['LONGITUDE']+'","'+
    xldf.iloc[i]['Address']+'","'+xldf.iloc[i]['location']+'")') ##change: no evetdate
    if i%10000==0:
        insertStr=str(insertLs)
        insertStr=insertStr[1:len(insertStr)-1].replace("'","")
        print(i)
        ##change: evetdate as partition
        query = "insert into lookups.lkp_btsaddress (cell_name,enodeb_name_site,vendor,network_type,division,district,thana,enodeb_id,cell_id,eutrancellid,tac_lac,antenna_direction,latitude,longitude,`address`,`location`) PARTITION(eventdate='"+dateval+"') values "+insertStr
        cur.execute(query)
        insertLs.clear()

insertStr=str(insertLs)
insertStr=insertStr[1:len(insertStr)-1].replace("'","")
##change: evetdate as partition
query = "insert into lookups.lkp_btsaddress (cell_name,enodeb_name_site,vendor,network_type,division,district,thana,enodeb_id,cell_id,eutrancellid,tac_lac,antenna_direction,latitude,longitude,`address`,`location`) PARTITION(eventdate='"+dateval+"') values "+insertStr
cur.execute(query)
insertLs.clear()
print(i)


