"""
Created on Sun Jun 27 13:02:38 2023

@author: khairul
4g subscription_report
"""

import os
import time
from datetime import datetime, timedelta

JDBC="jdbc:hive2://gzplr1cdpmas01.banglalink.net:2181,gzplr2cdpmas02.banglalink.net:2181,gzplr3cdpmas03.banglalink.net:2181/default;principal=hive/_HOST@BANGLALINK.NET;serviceDiscoveryMode=zooKeeper;ssl=true;sslTrustStore=/var/lib/cloudera-scm-agent/agent-cert/cm-auto-global_truststore.jks;zooKeeperNamespace=hiveserver2"

dtobj=datetime.today()
dtyes= dtobj - timedelta(days=1)
dt=dtobj.strftime('%Y%m%d')
dtt=dtobj.strftime('%Y-%m-%d')
dtyy=dtyes.strftime('%Y-%m-%d')
#dt='20220623'

rowcount_part=os.system('beeline -u "{}" -e "select count(*) from layer3.4g_subs_traffic_fact where processing_date=\'{}\';"'.format(JDBC,dtt))

if rowcount_part>1000:
    print('Current Date:\'{}\' is already exists. Please check manually'.format(dtt))
    os.system('echo "data loading status:4g_subs_traffic_fact" | mailx -s "Layer3.4g_subs_traffic_fact refresh status\'{}\' : Failed" mdkhasan@banglalink.net'.format(dtt))
else:
    os.system('''beeline -u "{}" -e "insert into layer3.4g_subs_traffic_fact \
                                    (eventtimestamp,msisdnaparty,msisdnbparty,domesticindicator,location,roamingposition,hour,totaldatavolume,processing_date,eventdate) \
                                    select eventtimestamp,msisdnaparty,msisdnbparty,domesticindicator,location,roamingposition,substr(eventtimestamp,12,2) as hour, \
                                    sum(totaldatavolume) as totaldatavolume,\'{}\',eventdate \
                                    from layer2.es_telecomtraffic  \
                                    where  \
                                    eventtype='Data' \
                                    and networktype='4G' \
                                    and processing_date=\'{}\' \
                                    group by eventtimestamp,msisdnaparty,msisdnbparty,domesticindicator,location,roamingposition,eventdate,substr(eventtimestamp,12,2);"'''.format(JDBC,dtyy,dtt))
    os.system('beeline -u "{}" -e "select count(*) from layer3.4g_subs_traffic_fact where processing_date=\'{}\';"'.format(JDBC,dtt))
    mail_s = 'Dear Team,\n4g_subs_traffic_fact is done. Please check.\n\nThanks,\nTeam BDS\n\n\nThis is system generated mail. Please do not reply.'
    os.system('echo "data loading status:4g_subs_traffic_fact is done\n\n\n {}" | mailx -r mdkhasan@banglalink.net -s "Layer3.4g_subs_traffic_fact refresh status\'{}\' " mdkhasan@banglalink.net'.format(mail_s,dtt))

