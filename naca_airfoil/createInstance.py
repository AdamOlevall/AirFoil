import os, time, sys

def createWorker(currentWorkers, numWorkers):
    
config = {'user':"olevall",
					'key':"zo5tuRLjuL",
					'tenant_name':"g2015034",
					'authurl':"http://130.238.29.253:5000/v3"}

conn = swiftclient.client.Connection(auth_version=3, **config)

workerIPs = []
keypair = nova.keypairs.find(name="adamolevallkey")

for x in range(currentWorkers, numWorkers):
    
    image = nova.images.find(name="Group3_airfoil_image")
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
