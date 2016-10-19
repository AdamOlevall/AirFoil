def createWorker(nc, workers, beginNr):
    workerIPs = []
    keypair = nc.keypairs.find(name="chliKey")

    for x in range(beginNr,(workers+beginNr)):
        nc.images.list()
        image = nc.images.find(name="CprojWorkerSnap")
        flavor = nc.flavors.find(name="m1.medium")

        nc.networks.list()
        network = nc.networks.find(label="ACC-Course-net")

        print "Getting userdata..."
        userData = open("/home/ubuntu/cloudproject/udWorker.yml","r")

        print "Creating server..."
        server = nc.servers.create(name = "CprojWorker{}".format(x), image = image, flavor = flavor, network = network, key_name = keypair.name, userdata=userData)

        status = server.status
        while status == 'BUILD':
            time.sleep(5)
            # Retrieve the instance again so the status field updates
            instance = nc.servers.get(server.id)
            status = instance.status
        print "status: %s" % status

        floating_ip = ''
        while floating_ip == '':
            iplist = nc.floating_ips.list()
            for ip_obj in iplist:
                if ((getattr(ip_obj,'instance_id')) == None):
                    floating_ip = getattr(ip_obj, 'ip')
                    workerIPs.append(floating_ip)
                    break

        print "Attaching IP:"
        print floating_ip
        server.add_floating_ip(floating_ip)
