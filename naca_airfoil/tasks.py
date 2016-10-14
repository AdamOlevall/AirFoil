from celery import Celery
import os
import swiftclient.client
import json
import time
import urllib2
import subprocess
from container import putContainer
import glob

app = Celery('tasks', backend='amqp', broker='amqp://ad:ol@130.238.29.13:5672/adol')

@app.task()
def runApp(start,stop,n,nodes,levels):
	subprocess.call("sudo ./run.sh %d %d %d %d %d" %(start, stop, n, nodes, levels), shell = True)

	listMesh = glob.glob("/home/ubuntu/AirFoil/naca_airfoil/msh")
	
	for i in listMesh:
		print i
		putContainer(listMesh[i],"/home/ubuntu/AirFoil/naca_airfoil/msh")






