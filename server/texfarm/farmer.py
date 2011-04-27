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
	try:
		os.mkdir(wdir)
	except OSError:
		print "already exists!"
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
	
	cmd_list = str(project.commands).split(',')
	
	'''	
	cmd_dict = {}
	for c in cmd_list:
		c = c.strip()
		print c
		value, key = c.split(' ') #here, value: program name, and key will be file name
		cmd_dict[key] = value # {a:latex, b:bibtex} etc.
	'''
	
	#Processing
	odir = '-output-directory='+ wdir
	out=""
	err=""
	compile_log=""
	cwd = os.getcwd()
	os.chdir(wdir)
	print "Changing Work Directory : %s" % wdir
	for command in cmd_list:
		command = command.strip()
		key, value = command.split(' ') 
		name = value
		print "key : " + key
		print "name : " + name
		process = subprocess.Popen([key, name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		out,err = process.communicate()
		compile_log = compile_log + "<br /> " + out
	os.chdir(cwd)
	print "Changing Work Directory : %s" % cwd
	return compile_log
	
class TeXFarm(threading.Thread):
	def __init__(self, project_id):
		threading.Thread.__init__(self)
		self.project_id = project_id #associated project id for the thread.
		
	def run(self):
		log = make_project(self.project_id)
		return log
		

