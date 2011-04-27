#!/usr/bin/env python
# encoding: utf-8
"""
farmer.py
"""

import sys
import os
import tempfile
import subprocess
import threading

import settings
from django.core.management import setup_environ

setup_environ(settings)
from server.latex.models import *

WORK_DIR = "/Users/jainbasil/temp/" 

def make_project(project_id):
	project = Project.objects.get(id=project_id)
	print WORK_DIR
	wdir = WORK_DIR + str(project_id) +"/"
	print wdir
	os.mkdir(wdir)
	print "created directory"
	file_list = project.file_set.all()
	#generating temporary files
	for f in file_list:
		tmp_file = tempfile.NamedTemporaryFile(dir=wdir, delete=False)
		tmp_content = str(f.content)
		tmp_file.write(tmp_content)
		tmp_file.close()
		new_name = wdir + f.file_name + f.file_type
		print new_name
		print tmp_file.name
		os.rename(tmp_file.name, new_name)
	
	#done
	#TODO: May need a change. try to do with ajax
	#compiling the project.
	print project.commands
	cmd_list = str(project.commands).split(',')
	print cmd_list
		
	cmd_dict = {}
	for c in cmd_list:
		key, value = c.split(' ')
		cmd_dict[key] = value
	print cmd_dict
	#Processing
	odir = '-output-directory='+ wdir
	print odir
	ofor = '-output-format=pdf'
	out=""
	err=""
	for key in cmd_dict.iterkeys():
		print key, odir, ofor, cmd_dict[key]
		name = wdir + cmd_dict[key]
		process = subprocess.Popen([key, odir, ofor, name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out,err = process.communicate()
		print out
	return out
	

class TeXFarm(threading.Thread):
	def __init__(self, project_id):
		threading.Thread.__init__(self)
		self.project_id = project_id #associated project id for the thread.
		
	def run(self):
		log = make_project(self.project_id)
		return log
