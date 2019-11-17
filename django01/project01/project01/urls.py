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
from django.urls import include, path
from app import views
from django.conf import settings
from django.conf.urls import include, url
from app.views import signup
#from . import views

urlpatterns = [
    path('app/', include('app.urls')), #we don't need this anymore --> do any buttons lead to it?
    path('admin/', admin.site.urls),
    path('create-sessions/', views.createSessions, name='createSessions'), # this page doesn't render properly --> do any buttons lead to it?
    path('', views.home, name='home'),
	path('accounts/', include('django.contrib.auth.urls')), # this needs an additonal /<something>/ at the end to work (example: /accounts/login/) Is that the expected use for this route?
	path('winners/', views.winners, name='winners'),
	path('signup/redirect/', views.login), # this page doesn't render properly --> do any buttons lead to it?
#path('redirect/', '/accounts/login/'),
	path('login/', views.login, name='login'), # new
	url(r'^signup/$', views.signup, name='signup'),
	path('profile/', views.ProfileView.as_view(), name='profile'),
	path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
	path('adminindex/', views.adminindex, name='adminindex'),
]

if 'survey' in settings.INSTALLED_APPS:
    urlpatterns += [
        url(r'^survey/', include('survey.urls'))
    ]
