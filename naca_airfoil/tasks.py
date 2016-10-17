from celery import Celery
import os
import swiftclient.client
import json
import time
import urllib2
import subprocess
from container import putContainer
import glob
from dolfin-convert import gmsh2xml

app = Celery('tasks', backend='amqp', broker='amqp://ad:ol@130.238.29.13:5672/adol')

@app.task()
def runApp(start,stop,n,nodes,levels):
	subprocess.call("sudo ./run.sh %d %d %d %d %d" %(start, stop, n, nodes, levels), shell = True)

	files_to_xml()

	xmlList = glob.glob("*.xml")
	for xmlFile in xmlList:
		putContainer(xmlFile, "/home/ubuntu/AirFoil/naca_airfoil/msh")

def files_to_xml()
	mshList = glob.glob("/home/ubuntu/AirFoil/naca_airfoil/msh/*.msh")

	for filename in mshList:
		#convert to .xml
		pathList = filename.split('/')
		output_name = filename[-1].split('.')
		gmsh2xml(filename, output_name[0] + ".xml")






