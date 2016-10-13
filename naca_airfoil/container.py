
import os
import swiftclient.client
import uuid

config = {'user':os.environ['OS_USERNAME'],
                  'key':os.environ['OS_PASSWORD'],
                  'tenant_name':os.environ['OS_TENANT_NAME'],
                  'authurl':os.environ['OS_AUTH_URL']}

def createContainer():
	bucket_name = "grupp3_Container"
	conn.put_container(bucket_name)

def putContainer(fileMesh):
	object_id = conn.put_object(bucket_name, fileMesh)

def getContainer():
	object_id2 = conn.get_object(bucket, sizes)

def cleanContainer():
# Clean up container in Swift
	(r, obj_list) = conn.get_container(grupp3_Container)#elete all objects
	for obj in obj_list:
		conn.delete_object(grupp3_Container, obj['name']) # Delete container
	print ('Deleteing container: ' + grupp3_Container)
	conn.delete_container(grupp3_Container)