from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin
#from .models import SurveyAnswer
#from project01.models import SurveyAnswer
#import os
#import survey

def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
	return render(request, 'homepage.html', {})

def createSessions(request):
	return render(request, 'create-sessions.html', {})

@csrf_protect	
def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			auth_login(request, user)
			# os.chdir("../../static/templates/registration/login.html")
			response = redirect(reverse('login.html'))
			return response
	else:
		return render(request, 'signup.html', {'form': UserCreationForm()})

def login(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = authenticate(
					request,
					username=form.cleaned_data.get('username'),
					password=form.cleaned_data.get('password')
					)
			if user is None:
				return render(
					request,
					'survey/login.html',
					{ 'form': form, 'invalid_creds': True }
				)
			try:
				form.confirm_login_allowed(user)
			except ValidationError:
				return render(
					request,
					'survey/login.html',
					{ 'form': form, 'invalid_creds': True }
				)
			login(request, user)
		
			return redirect('profile.html')
	else:
		return render(request, '/accounts/login.html', { 'form':  AuthenticationForm })
#'survey/login.html'

def winners(request):
	win = 'hello, this is the winner speaking' #survey.objects.all()
	
	context = {
		'win': win,
		#'servery_answer': SurveryAnswer.objects.all(),
	}
	return render(request, 'winners.html', context)

def adminindex(request):
	return render(request, 'adminindex.html', {})

class ProfileView(LoginRequiredMixin, TemplateView):
	def get(self, request):
#surveys = Survey.objects.filter(created_by=request.user).all()
#		assigned_surveys = SurveyAssignment.objects.filter(assigned_to=request.user).all()
		
#		context = {
#         'surveys': surveys,
#         'assigned_surveys': assigned_surveys
# }

		return render(request, 'profile.html', {})
