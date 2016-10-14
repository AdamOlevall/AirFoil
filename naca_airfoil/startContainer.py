import os
import swiftclient.client

config = {'user':"olevall",
					'key':"zo5tuRLjuL",
					'tenant_name':"g2015034",
					'authurl':"http://130.238.29.253:5000/v3"}

conn = swiftclient.client.Connection(auth_version=3, **config)


bucket_name = "Group3_container"
conn.put_container(bucket_name)