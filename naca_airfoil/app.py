from celery import Celery
from celery import group

from flask import Flask, jsonify, request, render_template
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
@app.route('/naca/api', methods=['GET'])
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

@app.route('/naca/service', methods=['GET', 'POST'])
def web_api():
        if request.method == 'POST':
                try:
	                angle_start = int(request.form['angles_start'])
                        angle_stop = int(request.form['angles_stop'])
                        n_angles = int(request.form['n_angles'])
                        n_nodes = int(request.form['n_nodes'])
                        n_levels = int(request.form['n_levels'])

                        viscosity = int(request.form['viscosity'])
                        speed = int(request.form['speed'])
                        num_samples = int(request.form['samples'])
                        time = int(request.form['time'])
                except:
                        return "invalid input"

                #tup = (0, 6, 3, 200,0);
	        #tup2 = (6, 10, 2, 200,0);

                #return str(time)
                
                tupleList = createCallTuples(angle_start, angle_stop, n_angles, n_nodes, n_levels)
	        #tuplelist = [tup,tup2]

        
	        return "it worked"
	        job = group(runApp.s(*i) for i in tuplelist)
	        dataTask = job.apply_async()
	        print "Celery is working..."
	
	        while (not dataTask.ready()):
		        pass
                #time_elapsed = (time.time() - startTime)	
                print "The task is done!"
                #getContainer()
                #return render_template('return_page.html')
        else:
                return render_template('grupp3.html')

def createCallTuples(angle_start, angle_stop, n_angles, n_nodes, n_levels, num_workers):
        #workLoad = n_levels*n_nodes*n_angles*(angle_stop-angle_start)
        t = int(((angle_stop - angle_start) / num_workers))*num_workers
        t2 = angle_stop - angle_start - t
        nA = int(n_angles / num_workers)*num_workers
        nA2 = n_angles - nA
        print str(t) + " " + str(t2)
        #numWorkers = ceil(workLoad) #TODO: create
        tupleList = []
        
        tupleList.append((int((angle_start)),
                          int(angle_stop/num_workers),
                          int(n_angles/num_workers),
                          n_nodes,
                          n_levels))
        _angle_start = 0
        _angle_stop = 0
        _nA = 0
        for i in range(1, num_workers):
                if i > num_workers - t2-1:
                        _angle_stop += 1
                if i > num_workers - t2:
                        _angle_start = 1
                if i > num_workers - nA2 - 1:
                        _nA = 1
                tupleList.append(((int(angle_stop/num_workers)*(i)) + _angle_start,
                                 (int(angle_stop/num_workers)*(i+1)) + _angle_stop,
                                 int(n_angles/num_workers)+_nA,
                                 n_nodes  ,
                                 n_levels))
        return tupleList
        
        
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
