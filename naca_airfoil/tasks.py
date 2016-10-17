from celery import Celery
import os
import swiftclient.client
import json
import time
import urllib2
import subprocess
from container import putContainer
import glob
from dolfin_convert import gmsh2xml

app = Celery('tasks', backend='amqp', broker='amqp://ad:ol@130.238.29.13:5672/adol')

@app.task()
def runApp(start,stop,n,nodes,levels):
	subprocess.call("sudo ./run.sh %d %d %d %d %d" %(start, stop, n, nodes, levels), shell = True)
	print
	files_to_xml()
	print 'Converted all .msh files to .xml'

	xmlList = glob.glob("/home/ubuntu/AirFoil/naca_airfoil/msh/*.xml")
	for xmlFile in xmlList:
		list_of_path = xmlFile.split('/')
		filename = list_of_path[-1]
		putContainer(filename, '/home/ubuntu/AirFoil/naca_airfoil/msh/')

	print 'Everything is in the container!'

def files_to_xml():
	mshList = glob.glob("/home/ubuntu/AirFoil/naca_airfoil/msh/*.msh")

	for filename in mshList:
		output_name = filename[:-3] + "xml"
		gmsh2xml(filename, output_name)






