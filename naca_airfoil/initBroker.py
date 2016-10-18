import time, os, sys
import inspect
from os import environ as env
from  novaclient import client
import keystoneclient.v3.client as ksclient
from keystoneauth1 import loading
from keystoneauth1 import session




#config = {'username':os.environ['OS_USERNAME'], 
 #         'api_key':os.environ['OS_PASSWORD'],
  #        'project_id':os.environ['OS_TENANT_NAME'],
   #       'auth_url':os.environ['OS_AUTH_URL'],
    #       }

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
# Create instanovae
import time 
keypair = nova.keypairs.find(name="new_cloud")#Insert name of you key

nova.images.list()
image = nova.images.find(name="ubuntu 14.04")
flavor = nova.flavors.find(name="m1.small")

nova.networks.list()
private_net = "g2015034-net_2"
secgroups = "default"


net = ""
if private_net != None:
    net = nova.networks.find(label=private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")
    
print "Getting userdata..."
ud = open('userdataB.yml', 'r')

secgroup = nova.security_groups.find(name="default")
secgroups = [secgroup.id]

print "Creating broker ... "
instance = nova.servers.create(name="Grupp3_johe", image=image, flavor=flavor, network = net, nics = nics, userdata=ud,security_groups = secgroups, key_name = keypair.name)
inst_status = instance.status


while inst_status == 'BUILD':
    time.sleep(5)
    print "Instance: "+instance.name+" is in "+inst_status+" state, sleeping for 5 seconds more..."
    instance = nova.servers.get(instance.id)
    inst_status = instance.status

print "Instance: "+ instance.name +" is in " + inst_status + "state"

floating_ip = nova.floating_ips.create("public")
print "Attaching IP:"


if floating_ip.ip != None: 
    instance.add_floating_ip(floating_ip)

try:
    nova.security_group_rules.create(secgroup.id,
                               ip_protocol="tcp",
                               from_port=5672,
                                to_port=5672)
    print "port 5672 opened"
except:
    print "couldn't open port 5672"
