from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'server.latex.views.home', name='home'),
    url(r'^register/$', 'server.latex.views.register_user'),
	url(r'^login/$', 'server.latex.views.user_login'),
	url(r'^logout/$', 'server.latex.views.logout'),
	url(r'^test/$', 'server.latex.views.is_logged_in'),

	url(r'^newproject/$', 'server.latex.views.create_project'),
	url(r'^projects/$', 'server.latex.views.projects'),
	url(r'^projects/(?P<project_id>\d+)/$', 'server.latex.views.project_view'),
	url(r'^projects/(?P<project_id>\d+)/editproject$', 'server.latex.views.edit_project'),
	url(r'^projects/(?P<project_id>\d+)/delproject$', 'server.latex.views.delete_project'),
	url(r'^projects/(?P<project_id>\d+)/compile$', 'server.latex.views.compile_project'),

	url(r'^projects/(?P<project_id>\d+)/addfile/$','server.latex.views.create_file'),
	url(r'^projects/(?P<project_id>\d+)/(?P<file_id>\d+)/editfile$','server.latex.views.edit_file'),
	url(r'^projects/(\d+)/(?P<file_id>\d+)/delfile$', 'server.latex.views.delete_file'),
    # url(r'^server/', include('server.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
