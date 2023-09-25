#!/usr/bin/env python
# coding: utf-8
from impala.dbapi import connect
import pandas as pd
import sys

##create dinamic input with
fileName = sys.argv[1]
dateval = sys.argv[2]

#Define Impala Connection
impala_host='gzplr4cdpdat05.banglalink.net'
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

xldf['location']=xldf[['zero','LAC','CI']].agg(''.join, axis=1)

xldf=xldf.drop(['zero'],axis=1)

'''
SL,LAC,CI,BTS Type(micro/mini/regular),	2G/3G,Cell,Cellid,Site,Short site,Antenna DIRECTION,LATITUDE,LONGITUDE,Site ADDRESS,Comment,BSC
'''

i = 0
insertLs=[]
while (r-1>i) :
    i+=1
    dt1='("'+xldf.iloc[i]['LAC']+'","'+xldf.iloc[i]['CI']+'","'+\
    xldf.iloc[i]['2G/3G']+'","'+xldf.iloc[i]['Cell']+'","'+\
    xldf.iloc[i]['Cellid']+'","'+xldf.iloc[i]['Site']+'","'+xldf.iloc[i]['Short site']+'","'+\
    xldf.iloc[i]['Antenna DIRECTION']+'","'+xldf.iloc[i]['LATITUDE']+'","'+xldf.iloc[i]['LONGITUDE']+'","'+xldf.iloc[i]['Site ADDRESS']+'","'+\
    xldf.iloc[i]['location']+'")'
    print(dt1)
    insertLs.append(dt1) ##change: no evetdate
    
    if i%10000==0:
        insertStr=str(insertLs)
        insertStr=insertStr[1:len(insertStr)-1].replace("'","")
        print(i)
        ##change: evetdate as partition
        query = "insert into lookups.bts_address_2g3g (`lac`,`ci`,`bts_2g3g`,`cell`,`cellid`,`site`,`short_site`,`antenna_direction`,`latitude`,`longitude`,`site_address`,`location`) PARTITION(eventdate='"+dateval+"') values "+insertStr
        cur.execute(query)
        insertLs.clear()

insertStr=str(insertLs)
insertStr=insertStr[1:len(insertStr)-1].replace("'","")
##change: evetdate as partition
query = "insert into lookups.bts_address_2g3g (`lac`,`ci`,`bts_2g3g`,`cell`,`cellid`,`site`,`short_site`,`antenna_direction`,`latitude`,`longitude`,`site_address`,`location`) PARTITION(eventdate='"+dateval+"') values "+insertStr
cur.execute(query)
insertLs.clear()
print(i)
