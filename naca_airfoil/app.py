from celery import Celery
from celery import group
from tasks import runApp
from flask import Flask, jsonify
import subprocess
import sys
import os
import swiftclient.client
import json
import time
import urllib2
from collections import Counter
from container import getContainer

app = Flask(__name__)
@app.route('/AirFoil/naca_airfoil', methods=['GET'])
def cow_say():
	#req = urllib2.Request(0,10,5,200,0)
	#response = urllib2.urlopen(req)

	#divide into tuples
	tup = (0, 6, 3, 200,0);
	tup2 = (6, 10, 2, 200,0);
	#tupleslist 
	tuplelist = [tup,tup2]

	
	
	job = group(runApp.s(*i) for i in tuplelist)
	dataTask = job.apply_async()
	print "Celery is working..."
	
	while (dataTask.ready() == False):
		#print "... %i s" %(counter)
		counter = 0
	#time_elapsed = (time.time() - startTime)	
	print "The task is done!"


	#getContainer()
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)





