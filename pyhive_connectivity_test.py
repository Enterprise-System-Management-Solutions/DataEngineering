#hive_connectivity test
from pyhive import hive
import pandas as pd

# Hive connection parameters
JDBC = "jdbc:hive2://gzplr1cdpmas01.banglalink.net:2181,gzplr2cdpmas02.banglalink.net:2181,gzplr3cdpmas03.banglalink.net:2181/default;principal=hive/_HOST@BANGLALINK.NET;serviceDiscoveryMode=zooKeeper;ssl=true;sslTrustStore=/var/lib/cloudera-scm-agent/agent-cert/cm-auto-global_truststore.jks;zooKeeperNamespace=hiveserver2"

# Hive query
query = "select count(*) from lookups.date_dim;"

# Establish the Hive connection and create a cursor
connection = hive.connect(JDBC)
cursor = connection.cursor()

try:
    # Execute the Hive query
    cursor.execute(query)

    # Fetch the result
    result = cursor.fetchone()

    # Print the result
    print("Result:", result[0])

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()

