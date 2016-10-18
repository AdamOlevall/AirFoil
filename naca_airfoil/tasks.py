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
from Calculations import calc_mean

app = Celery('tasks', backend='amqp', broker='amqp://ad:ol@130.238.29.208:5672/adol')
app.conf.update(CELERY_ACKS_LATE = True,
	CELERYD_PREFETCH_MULTIPLIER = 1)
#app = Celery('tasks', backend='amqp', broker='amqp://') #Local debugging

def clean_folders():
	if len(glob.glob('/home/ubuntu/AirFoil/naca_airfoil/msh/*')) > 0:
		subprocess.check_call("sudo rm /home/ubuntu/AirFoil/naca_airfoil/msh/*", shell=True)
	if len(glob.glob('/home/ubuntu/AirFoil/naca_airfoil/geo/*')) > 0:
		subprocess.check_call("sudo rm /home/ubuntu/AirFoil/naca_airfoil/geo/*", shell=True)
	if len(glob.glob('/home/ubuntu/AirFoil/naca_airfoil/results/*')) > 0:
		subprocess.check_call("sudo rm /home/ubuntu/AirFoil/naca_airfoil/results/*", shell=True)


def create_msh(i,n_nodes,n_levels):
	subprocess.call("sudo ./run.sh %d %d %d %d %d" %(i, i, 1, n_nodes, n_levels), shell = True)


def msh_to_xml(i):
	mshList = glob.glob("msh/r*a" + str(i) + "n*.msh")

	for filename in mshList:
		output_name = filename[:-3] + "xml"
		gmsh2xml(filename, output_name)

	print 'Converted all .msh files to .xml'

	# xmlList = glob.glob("/home/ubuntu/AirFoil/naca_airfoil/msh/*.xml")
	# for xmlFile in xmlList:
	# 	list_of_path = xmlFile.split('/')
	# 	filename = list_of_path[-1]
	# 	putContainer(filename, '/home/ubuntu/AirFoil/naca_airfoil/msh/')

	# print 'Everything is in the container!'


def runAirfoil(i, num_samples, viscosity, speed, time):
	xmlFiles = glob.glob("msh/r*a" + str(i) + "n*.xml")
	for file in xmlFiles:
		name = "sudo ./navier_stokes_solver/airfoil " + str(num_samples) + " " + str(viscosity) + " " + str(speed) + " " + str(time) + " " + file
		print "Starting airfoil: " + name
		subprocess.check_call(name, shell=True)
		print "Finished airfoil: " + name


@app.task()
def runApp(i,n_nodes,n_levels, num_samples, viscosity, speed ,time):
	clean_folders()
	create_msh(i,n_nodes,n_levels)
	msh_to_xml(i)
	runAirfoil(i, num_samples, viscosity, speed, time)
	lift_mean, drag_mean = calc_mean('/home/ubuntu/AirFoil/naca_airfoil/results/drag_ligt.m')
	return {str(i):(lift_mean, drag_mean)}







