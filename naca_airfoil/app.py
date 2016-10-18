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
import glob

from tasks import runApp

app = Flask(__name__)


@app.route('/naca/api', methods=['GET'])
def basic_api():
	tup = (0, 6, 3, 200,0);
	tup2 = (6, 10, 2, 200,0);

	tuplelist = [tup,tup2]

	job = group(runApp.s(*i) for i in tuplelist)
	dataTask = job.apply_async()
	print "Celery is working..."

	while (not dataTask.ready()):
		pass
	print "The task is done!"


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
            input_time = int(request.form['time'])
        except:
            return "invalid input"


        iList = createAngles(angle_start, angle_stop, n_angles)

        num_workers = calculateNumWorkers(len(iList), n_nodes, n_levels)

        tupleList = []
        for i in iList:
            tupleList.append((i, n_nodes, n_levels, num_samples, viscosity, speed, input_time))
        startTime = time.time()
        job = group(runApp.s(*i) for i in tupleList)
        dataTask = job.apply_async()
	print "Celery is working..."

        while (not dataTask.ready()):
	        pass

        time_elapsed = (time.time() - startTime)
        print "The task is done! Time: " + str(int(time_elapsed)) + "s"

        toReturn = dataTask.get()
        print str(toReturn)
        return ""
    else:
        return render_template('form.html')


def createAngles(angle_start, angle_stop, n_angles):
        angle_diff = (angle_stop - angle_start)/n_angles
        iList = []
        for i in range(n_angles+1):
            iList.append(angle_start + angle_diff*i)
        return iList


def calculateNumWorkers(i,n_nodes, n_levels):
        weights = [1,1,1] # weights for calculating total workload
        num_workers = 0
        workLoad = i*weights[0]*n_nodes*weights[1]*n_levels*weights[2] #TODO
        if workLoad > 100:
            num_workers = 5
        elif workLoad > 80:
            num_workers = 4
        elif workLoad > 60:
            num_workers = 3
        elif workLoad > 40:
            num_workers = 2
        elif workLoad > 20:
            num_workers = 1
        else:
            num_workers = 0


def properParse(d):
    jString = '{'
    for (k,v) in d.iteritems():
        dqK = str(k).replace('\'', '"')
        dqV = str(v).replace('\'', '"')
        jString += "\"" + str(dqK) + "\":\"" + str(dqV) + "\"" + ","
    jString = jString[:-1]
    jString += '}'
    return jString


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)
