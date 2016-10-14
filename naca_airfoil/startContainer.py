import os
import swiftclient.client

config = {'user':os.environ['OS_USERNAME'],
                  'key':os.environ['OS_PASSWORD'],
                  'tenant_name':os.environ['OS_TENANT_NAME'],
                  'authurl':os.environ['OS_AUTH_URL']}

conn = swiftclient.client.Connection(auth_version=3, **config)


bucket_name = "Group3_container"
conn.put_container(bucket_name)