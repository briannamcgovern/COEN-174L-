"""project01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views # for logout
#from django.contrib.auth import request  # for restricted page access
from app.views import LogInView  # for restricted page access
from django.urls import include, path
from app import views
from django.conf import settings
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
#from app.views import signup
#from . import views

from decorator_include import decorator_include
#from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
#from django.conf.urls.defaults import patterns

urlpatterns = [
    path('app/', include('app.urls')), #we don't need this anymore --> do any buttons lead to it?
    path('admin/', admin.site.urls),
    path('create-sessions/', views.createSessions, name='createSessions'), # this page doesn't render properly --> do any buttons lead to it?
    path('', views.home, name='home'),
	path('accounts/', include('django.contrib.auth.urls')), # this needs an additonal /<something>/ at the end to work (example: /accounts/login/) Is that the expected use for this route?
	path('winners/', views.winners, name='winners'),
	path('results/', views.design_experience, name='results'),
#	path('signup/redirect/', views.login, name='login'), # this page doesn't render properly --> do any buttons lead to it?
#path('redirect/', '/accounts/login/'),
#	path('accounts/login/', views.login, name='login'), # new
#path('registration/login/', views.login, name='login'), # new new 
#	url(r'^signup/$', views.signup, name='signup'),
	
	path('profile/', views.ProfileView.as_view(), name='profile'),
	path('signup/', views.SignUpView.as_view(), name='signup'),
	path('accounts/login/', views.LogInView.as_view(), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),

#path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
#	path('adminindex/', views.adminindex, name='adminindex'),
]

urlpatterns += [
	url(r'^survey/', decorator_include(login_required, 'survey.urls')),
]

#@login_required
#if 'survey' or 'survey.apps.DjangoSurveyAndReportConfig' in settings.INSTALLED_APPS:
#if auth_views: # attempt to make surveys restricted to authenticated users
#@login_required
'''urlpatterns += [
#url(r'^survey/', include('survey.urls')) # works to show surveys to all users

#url(r'^survey/', login_required('survey.urls')), # makes survey hidden if not logged in, but breaks survey url if logged in 
#url(r'^survey/', decorated_includes(login_required, include(survey.urls)))

#		path('', include('survey.urls')),
#path('survey/', request.user.is_authenticated(), name='survey')
    ]'''
