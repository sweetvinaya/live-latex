"""
Definitions of different models used in livelatex.

.. moduleauthor:: Jain Basil Aliyas <jainbasil@gmail.com>

""" 

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from server.settings import INPUT_FILE_TYPES, OUTPUT_FILE_TYPES, BUILDERS

class UserProfile(models.Model):
	user = models.OneToOneField(User)
	is_active = models.BooleanField()
	activation_key = models.CharField(max_length=40)
	key_expires = models.DateTimeField()
	
class Project(models.Model):
	"""
	This module defines a project in LiveLaTeX.
	"""
	author = models.ForeignKey(User)
	date = models.DateTimeField(auto_now_add=True)
	long_name = models.CharField(blank=False, max_length=64)
	description = models.CharField(blank=True, max_length=100)
	output_file = models.URLField(blank=True) #to store the local file location. 
	commands = models.CharField(help_text="Separate using comma.(for eg. latex main.tex, bibtex a.bib)", blank=True, max_length=300) #comma separated values of commands
	
	def __unicode__(self):
		return self.short_name

class File(models.Model):
	"""
	This module define a file in a project. This will
	reside in the Project as many-to-one relationship
	"""
	project = models.ForeignKey(Project)
	file_name = models.CharField(max_length=32)
	file_type = models.CharField(max_length=5, choices=INPUT_FILE_TYPES)
	created = models.DateTimeField()
	modified = models.DateTimeField(auto_now_add=True)
	content = models.TextField()
	
	def __unicode__(self):
		return self.file_name
	
#for storing the list of projects requested for compilation		
class TeXFarmQueue(models.Model):
	id = models.IntegerField(primary_key=True)
	request_date = models.DateTimeField(auto_now_add=True)
	
#for storing the list of projects processed currently
class OnProgressQueue(models.Model):
	id = models.IntegerField(primary_key=True)
	work_dir = models.URLField()
	output_file = models.URLField()

	
#TODO: The following class is not a good method of implementation. Need to change it.

#A model which store the commands for compilation of a project.
'''
class CommandList(models.Model):
	project = models.OneToOneField(Project)
	
class Command(models.Model):
	command_name = models.CharField(max_length=10, choices=BUILDERS)
	arguments = models.CharField(max_length=50) #expects the filename of latex document here.
	commander = models.ForeignKey(CommandList)
	
'''