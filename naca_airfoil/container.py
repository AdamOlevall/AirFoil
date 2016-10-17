
import os
import swiftclient.client
import uuid


def putContainer(file_name, file_path):
	config = {'user':"olevall",
					'key':"zo5tuRLjuL",
					'tenant_name':"g2015034",
					'authurl':"http://130.238.29.253:5000/v3"}

	conn = swiftclient.client.Connection(auth_version=3, **config)

	with open(file_name, 'r') as f:
		file_data = f.read()

	conn.put_object("Group3_container", file_name,file_data)


def getContainer(file_name, file_path):
	config = {'user':"olevall",
					'key':"zo5tuRLjuL",
					'tenant_name':"g2015034",
					'authurl':"http://130.238.29.253:5000/v3"}
	conn = swiftclient.client.Connection(auth_version=3, **config)

	conn.get_object("Group3_container", file_name)
	f = open(file_path, 'w')
	f.write(obj[1])
	f.close()

#def cleanContainer():
# Clean up container in Swift
	#(r, obj_list) = conn.get_container("Group3_container")#elete all objects
	#for obj in obj_list:
	#	conn.delete_object("Group3_container", obj['name']) # Delete container
	#print ('Deleteing container: ' + "Group3_container")
	#conn.delete_container("Group3_container")