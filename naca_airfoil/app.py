from celery import Celery
from celery import group

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
import math

from tasks import runApp

app = Flask(__name__)
@app.route('/naca/api', methods=['GET', 'POST'])
def basic_api():
        
	#req = urllib2.request(0,10,5,200,0)
	#response = urllib2.urlopen(req)
        
	#divide into tuples
	tup = (0, 6, 3, 200,0);
	tup2 = (6, 10, 2, 200,0);
        
	tuplelist = [tup,tup2]
	        
	job = group(runApp.s(*i) for i in tuplelist)
	dataTask = job.apply_async()
	print "Celery is working..."
	
	while (not dataTask.ready()):
		pass
        #time_elapsed = (time.time() - startTime)	
        print "The task is done!"
        #getContainer()
        
        
def createCallTuples(angle_start, angle_stop, n_angles, n_nodes, n_levels):
        workLoad = n_levels*n_nodes*n_angles*(angle_stop-angle_start)
        #numWorkers = ceil(workLoad) #TODO: create
        num_workers = 3
        tupleList = []
        for i in range(num_workers):
                tupleList.append((math.floor((angle_start/num_workers)*i,
                                 math.floor((angle_stop/num_workers)*i,
                                 math.floor(n_angles / num_workers-math.ceil(i)),
                                 n_nodes,n_levels))
        return tupleList
        

@app.route('/naca/service', methods=['GET', 'POST'])
def web_api():
        if request.method == 'POST':
	        angle_start = int(request.form['angles_start'])
                angle_stop = int(request.form['angles_stop'])
                n_angles = int(request.form['n_angles'])
                n_nodes = int(request.form['n_nodes'])
                n_levels = int(request.form['n_levels'])

                viscosity = int(request.form['viscosity'])
                speed = int(request.form['speed'])
                num_samples = int(request.form['num_samples'])
                time = int(request.form['time'])
                

                
	        tup = (0, 6, 3, 200,0);
	        tup2 = (6, 10, 2, 200,0);
                
	        tuplelist = [tup,tup2]
	        
	        job = group(runApp.s(*i) for i in tuplelist)
	        dataTask = job.apply_async()
	        print "Celery is working..."
	
	        while (not dataTask.ready()):
		        pass
                #time_elapsed = (time.time() - startTime)	
                print "The task is done!"
                #getContainer()
                return render_template('return_page.html')
        else:
                return render_template('req_file.html')
        
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
