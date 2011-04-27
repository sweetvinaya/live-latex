# Create your views here.
import datetime
import random
import hashlib

from django.template.loader import get_template
from django.template import Context, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import render_to_response, get_object_or_404
from django.core.context_processors import csrf

from latex.models import *
from latex.forms import *
from texfarm.farmer import *

def home(request):
	site_template  = get_template('template.html')
	html = site_template.render(Context({}))
	return HttpResponse(html)

#Project view, which is to be shown after user login.
def projects(request):
	if request.user.is_authenticated():
		u = User.objects.get(username=request.user.username)
		project_list = Project.objects.filter(author=u)
		return render_to_response("projects.html", {'project_list' : project_list})
		
#create a project
def create_project(request):
	if request.POST:
		new_data = request.POST.copy()
		form = ProjectForm(new_data)
		
		for i in new_data.values():
			if i == "":
				return HttpResponse("Do not leave as blank")
	
		if not form.is_valid():
			print "error"
		user = User.objects.get(username=request.user.username)
		long_name = form.data['long_name']
		description = form.data['description']
		commands = form.data['commands']
		
		new_project = Project(author=user, long_name=long_name, description=description, commands=commands)
		new_project.save()
		
		return HttpResponse("Created new project successfully")
		
	else:
		form = ProjectForm()
		return render_to_response('new_project.html', {'form':form,}, context_instance=RequestContext(request))
		
#project_view: shows the files in a project.
def project_view(request, project_id):
	if request.POST:
		thread = TeXFarm(project_id)
		log = thread.run()
		return HttpResponse(log)
	else:
		project = Project.objects.get(id=project_id)
		file_list = Project.objects.get(id=project_id).file_set.all().order_by("-created")
		return render_to_response('project-view.html', {'project':project, 'file_list': file_list}, context_instance=RequestContext(request))

#edit_project_view

def edit_project(request, project_id):
	new_project = Project.objects.get(id=project_id)
	if request.POST:
		#update the content using the post data.
		new_data = request.POST.copy()
		form = ProjectForm(new_data)

		if not form.is_valid():
			print "error"
			
		new_project.long_name = form.data['long_name']
		new_project.description = form.data['description']
		commands = form.data['commands']
		new_project.save()
		return HttpResponse("Project updated.")
	else:
		#show the project form, with current data embedded in it.
		
		form = ProjectForm(initial={'long_name':new_project.long_name, 'description':new_project.description, 'commands':new_project.commands})
		return render_to_response('edit_project.html', {'form':form,}, context_instance=RequestContext(request))
	
#create_file: create a new file, and add it to database
def create_file(request, project_id):
	if request.POST:
		new_data = request.POST.copy()
		form = FileCreateForm(new_data)
		
		for i in new_data.values():
			if i == "":
				return HttpResponse('Do not leave as blank')
		print project_id
		project = Project.objects.get(id=project_id) #project to which file is associated.
		file_name = form.data['file_name']
		file_type = form.data['file_type']
		content = form.data['content']
		created = datetime.datetime.today()
		
		new_file = File(project=project, file_name=file_name, file_type=file_type, content=content, created=created)
		new_file.save()
		return HttpResponse("Created file!")
	else:
		form = FileCreateForm()
		return render_to_response('file-edit.html', {'form':form}, context_instance=RequestContext(request))

#User Registration
def register_user(request):
	if request.POST:
		new_data = request.POST.copy()
		form = RegistrationForm(new_data)
		
		valid_user = True
		
		for i in new_data.values():
			if i == "":
				return HttpResponse("Do not leave as blank")
				
		try:
			User.objects.get(username=str(form.data['user']))
			return HttpResponse("Username already taken.")
		except User.DoesNotExist:
			valid_user = False
			
		if form.is_valid() == False:
			return HttpResponse("Invalid Email ID")
			
		if valid_user==False and form.data['password1']==form.data['password2']:
			if len(form.data['password1']) < 6:
				return HttpResponse("Passwords should be atleast <br /> 6 characters in length")
			new_user = form.save()
			salt = hashlib.new('sha', str(random.random())).hexdigest()[:5]
			activation_key = hashlib.new('sha', salt+new_user.username).hexdigest()
			key_expires = datetime.datetime.today()+datetime.timedelta(2)
			new_profile = UserProfile(user=new_user, activation_key=activation_key, key_expires=key_expires, is_active=True)
			new_profile.save()
			
			return HttpResponse('User added successfully')
		else:
			return HttpResponse('Re-enter passwords again.')
			
	else:
		form = RegistrationForm()
		return render_to_response('register.html', {'form':form,}, context_instance=RequestContext(request))


#User login
def user_login(request):
	if request.POST:
		new_data = request.POST.copy()
		if new_data.has_key('logout'):
			auth.logout(request)
			return HttpResponse('True')
			
		user = str(new_data['username'])
		password = str(new_data['password'])
		user_session = auth.authenticate(username=user, password=password)
		
		if user_session:
			auth.login(request, user_session)
			return HttpResponse('True')
		else:
			return HttpResponse('False')
	else:
		form = UserLogin()
		return render_to_response('user_login.html', {'form':form}, context_instance=RequestContext(request))


#To check user logged in or not
def is_logged_in(request):
	if request.user.is_authenticated():
		return HttpResponse(str(request.user.username))
	else:
		return HttpResponse('False')

