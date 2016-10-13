import time, os, sys
import inspect
from os import environ as env
from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session


flavor = "m1.small" 
private_net = "g2015034-net_2"
#floating_ip_pool_name = None
#floating_ip = None

loader = loading.get_plugin_loader('password')
auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_domain_name=env['OS_PROJECT_DOMAIN_NAME'])


sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)
print "user authorization completed."
iimport paramiko
import time

workerIPs = []
keypair = nova.keypairs.find(name="adamolevallkey")

for x in range(1,3):
    
    image = nova.images.find(name="Ubuntu-16.04")
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
