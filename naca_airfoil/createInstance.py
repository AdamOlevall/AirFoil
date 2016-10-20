import time, os, sys
import inspect
from os import environ as env
from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session

def createWorker(currentWorkers, numWorkers):
    
	loader = loading.get_plugin_loader('password')
	auth = loader.load_from_options(auth_url="http://130.238.29.253:5000/v3",
                                username="olevall,
                                password="zo5tuRLjuL",
                                project_name=""g2015034",
                                user_domain_name="Default",
                                project_domain_name="Default")


	sess = session.Session(auth=auth)
	nova = client.Client('2.1', session=sess)
	

	workerIPs = []
	keypair = nova.keypairs.find(name="adamolevallkey")

	for x in range(currentWorkers, numWorkers):
    
    		image = nova.images.find(name="ubuntu 14.04")
    		flavor = nova.flavors.find(name="m1.small")

   

    		if private_net != None:
        		net = nova.networks.find(label=private_net)
       			nics = [{'net-id': net.id}]
    		else:
        		sys.exit("private-net not defined.")

   

    		print "Getting userdata..."
    		ud = open('userdataW.yml', 'r')

   		print "Creating server..."
    		instance = nova.servers.create(name = "Group3_Worker" + str(x), image = image, flavor = flavor,nics=nics, userdata=ud,key_name = keypair.name)

   		inst_status = instance.status
    		while inst_status == 'BUILD':
        		time.sleep(5)
        # Retrieve the instance again so the status field updates
        		instance = nova.servers.get(instance.id)
        		inst_status = instance.status
    		print "status: %s" % inst_status

    		floating_ip = ''
    		while floating_ip == '':
        		iplist = nova.floating_ips.list()
        		for ip_obj in iplist:
            			if ((getattr(ip_obj,'instance_id')) == None):
                			floating_ip = getattr(ip_obj, 'ip')
                			workerIPs.append(floating_ip)
                			break    

    		print "Attaching IP:"
    		print floating_ip
    		instance.add_floating_ip(floating_ip)
