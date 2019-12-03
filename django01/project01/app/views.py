from django.shortcuts import render, redirect, reverse
from django.urls import resolve
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from django.views import View
from braces.views import LoginRequiredMixin
from django import forms
from django.contrib.auth.models import User
from .models import AuthUser # attempt to make surveys secure
from .models import SurveyAnswer
from .models import SurveySurvey # Survey
from django.db.models import Avg, Max, Min, Sum
import sqlite3

#attempt to make surveys secure
from django.conf import settings
from django.http import HttpResponseRedirect
import re

#import os

# attempt to make surveys secure
'''class RequireLoginMiddleware(object):
    def __init__(self):
        self.urls = tuple([re.compile(url) for url in settings.LOGIN_REQUIRED_URLS])
        self.require_login_path = getattr(settings, 'LOGIN_URL', '/accounts/login/')
    
    def process_request(self, request):
        for url in self.urls:
            if url.match(request.path) and request.user.is_anonymous():
                return HttpResponseRedirect('%s?next=%s' % (self.require_login_path, request.path))'''
# end attempt to make surveys secure

# custom UserCreationForm 
class RegisterForm(UserCreationForm):
	email = forms.EmailField(label = "Email")
	first_name = forms.CharField(label = "First Name")
	last_name = forms.CharField(label = "Last Name")

	class Meta:
		model = User # changes User to AuthUser in attempt to make surveys secure
#changed back to User
		fields = ("email", "first_name", "last_name", "username")

	# override save method
	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.first_name = self.cleaned_data["first_name"]
		user.last_name = self.cleaned_data["last_name"]
		user.email = self.cleaned_data["email"]
		#user.user_permissions.set(['Judges'])
		if commit:
			user.save()
		return user

# custom AuthenticationForm 
'''class AuthenticateForm(AuthenticationForm):
	email = forms.EmailField(
		label=("Email Address"),
	)

	def clean(self):
		email = self.cleaned_data.get('email')
		return self
'''
	# must confirm email before authenticated 
'''	def confirm_login_allowed(self, user):
		if not user.is_active or not user.is_validated:
			raise forms.ValidationError('Authentication failed.', code=invalid_login)'''

def index(request):
	return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
	return render(request, 'homepage.html', {})

def createSessions(request):
	return render(request, 'create-sessions.html', {})

class SignUpView(View):
#@csrf_protect	
	def get(self, request):
		return render(request, 'signup.html', {'form': RegisterForm()})
		
	def post(self, request):
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			return redirect(reverse('login'))
			#return render(request, 'login.html')

		#return render(request, 'survey/register.html', { 'form': form })
		return render(request, 'signup.html', {'form': form})

#	if request.method == 'POST':
#		form = UserCreationForm(request.POST)
#		if form.is_valid():
#			form.save()
#			username = form.cleaned_data.get('username')
#			raw_password = form.cleaned_data.get('password1')
#			user = authenticate(username=username, password=raw_password)
#			auth_login(request, user)
			# os.chdir("../../static/templates/registration/login.html")
#response = redirect(reverse('login.html'))
#return redirect(resolve('/accounts/login/')) # new new
#	return redirect(reverse('accounts/login'))
#			return render(request, 'login.html') # new new new
#		return render(request, 'winners.html', {'form': form}) # sign up w errors
#if request.method == 'GET':
#	return render(request, 'signup.html', {'form': UserCreationForm()})

class LogInView(View):
	def get(self, request):
		#return render(request, 'survey/login.html', { 'form':  AuthenticationForm })
		return render(request, 'accounts/login.html', { 'form':  AuthenticationForm })

    # really low level
	def post(self, request):
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = authenticate(
				request,
				email=form.cleaned_data.get('email'), # changed username to email 2x
				password=form.cleaned_data.get('password')
			)
			
			if user is None:
				return render(
					request,
					'accounts/login.html',
					{ 'form': form, 'invalid_creds': True }
				)
				
			try:
				form.confirm_login_allowed(user)
			except ValidationError:
				return render(
					request,
					'accounts/login.html',
					{ 'form': form, 'invalid_creds': True }
				)
				auth_login(request, user)
			
#user.is_authenticated = True # attempt to make system more secure
			return redirect(reverse('profile'))
			#return redirect('profile/html')	

#def login(request):
#	if request.method == 'POST':
#		form = AuthenticationForm(request, data=request.POST)
#		if form.is_valid():
#			user = authenticate(
#					request,
#					username=form.cleaned_data.get('username'),
#					password=form.cleaned_data.get('password')
#					)
#			if user is None:
#				return render(
#					request,
#					'survey/login.html',
#					{ 'form': form, 'invalid_creds': True }
#				)
#			try:
#				form.confirm_login_allowed(user)
#			except ValidationError:
#				return render(
#					request,
#					'survey/login.html',
#					{ 'form': form, 'invalid_creds': True }
#				)
#			login(request, user)
#		
#			return redirect('profile.html')
#	else:
#		return render(request, 'accounts/login.html', { 'form':  AuthenticationForm })
#'survey/login.html'

#def adminindex(request):
#	return render(request, 'adminindex.html', {})

class ProfileView(LoginRequiredMixin, TemplateView):
	def get(self, request):
		# attempt to show only allowed surveys based on group:
		

		#surveys = SurveySurvey.objects.filter().all()
		#assigned_surveys = SurveyAssignment.objects.filter(assigned_to=request.user).all()

# .objects.filter(created_by=request.user).all()
		
		context = {
			'surveys': '/survey/1', 
			#'assigned_surveys': assigned_surveys
		}

		'''if self.AuthGroup == 'Bioengineering 1':
			content = {'surveys': '/survey/6'}'''
			# changed context to content


		return render(request, 'profile.html', context)

#############################################################
################### OVERALL AVERAGES ########################
#############################################################
def design_experience(request):	
	all_forms = SurveyAnswer.objects.all()

	# overall evaluation averages
	# get the average for all design_experience questions (16 - 26)
	final_sum = 0
	question_sum = 0
	total_forms = 0 
	for form in all_forms: # sum of all of the scores for the first question 
		fields = all_forms.filter(question_id=16)
		for field in fields:
			if field.body and field.body[0] != '0': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body[0]) 
				total_forms += 1
	if total_forms != 0: #if no forms (or only N/A answers) were filled out for this question, set the sum to 0
		average16 = question_sum / total_forms
		final_sum += average16
	
	
	question_sum = 0
	total_forms = 0 
	for form in all_forms: # sum of all of the scores for the second question
		fields = all_forms.filter(question_id=17)
		for field in fields:
			if field.body and field.body[0] != '0': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body[0]) # body holds the judge's answer for one question
				total_forms += 1
	if total_forms != 0: #if no forms (or only N/A answers) were filled out for this question, set the sum to 0
		average17 = question_sum / total_forms
		final_sum += average17

	
	question_sum = 0
	total_forms = 0 
	for form in all_forms: 
		fields = all_forms.filter(question_id=18)
		for field in fields:
			if field.body and field.body[0] != '0': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body[0]) # body holds the judge's answer for one question
				total_forms += 1
	if total_forms != 0: #if no forms (or only N/A answers) were filled out for this question, set the sum to 0
		average18 = question_sum / total_forms
		final_sum += average18

	
	question_sum = 0
	total_forms = 0 
	for form in all_forms: 
		fields = all_forms.filter(question_id=19)
		for field in fields:
			if field.body and field.body[0] != '0': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body[0]) # body holds the judge's answer for one question
				total_forms += 1
	if total_forms != 0: #if no forms (or only N/A answers) were filled out for this question, set the sum to 0
		average19 = question_sum / total_forms
		final_sum += average19


	question_sum = 0
	total_forms = 0 
	for form in all_forms: 
		fields = all_forms.filter(question_id=20)
		for field in fields:
			if field.body and field.body[0] != '0': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body[0]) # body holds the judge's answer for one question
				total_forms += 1
	if total_forms != 0: #if no forms (or only N/A answers) were filled out for this question, set the sum to 0
		average20 = question_sum / total_forms
		final_sum += average20


	question_sum = 0
	total_forms = 0 
	for form in all_forms: 
		fields = all_forms.filter(question_id=21)
		for field in fields:
			if field.body and field.body[0] != '0': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body[0]) # body holds the judge's answer for one question
				total_forms += 1
	if total_forms != 0: #if no forms (or only N/A answers) were filled out for this question, set the sum to 0
		average21 = question_sum / total_forms
		final_sum += average21


	question_sum = 0
	total_forms = 0 
	for form in all_forms: 
		fields = all_forms.filter(question_id=22)
		for field in fields:
			if field.body and field.body[0] != '0': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body[0]) # body holds the judge's answer for one question
				total_forms += 1
	if total_forms != 0: #if no forms (or only N/A answers) were filled out for this question, set the sum to 0
		average22 = question_sum / total_forms
		final_sum += average22


	question_sum = 0
	total_forms = 0 
	for form in all_forms: 
		fields = all_forms.filter(question_id=23)
		for field in fields:
			if field.body and field.body[0] != '0': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body[0]) # body holds the judge's answer for one question
				total_forms += 1
	if total_forms != 0: #if no forms (or only N/A answers) were filled out for this question, set the sum to 0
		average23 = question_sum / total_forms
		final_sum += average23


	question_sum = 0
	total_forms = 0 
	for form in all_forms: 
		fields = all_forms.filter(question_id=24)
		for field in fields:
			if field.body and field.body[0] != '0': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body[0]) # body holds the judge's answer for one question
				total_forms += 1
	if total_forms != 0: #if no forms (or only N/A answers) were filled out for this question, set the sum to 0
		average24 = question_sum / total_forms
		final_sum += average24


	question_sum = 0
	total_forms = 0 
	for form in all_forms: 
		fields = all_forms.filter(question_id=25)
		for field in fields:
			if field.body and field.body[0] != '0': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body[0]) # body holds the judge's answer for one question
				total_forms += 1
	if total_forms != 0: #if no forms (or only N/A answers) were filled out for this question, set the sum to 0
		average25 = question_sum / total_forms
		final_sum += average25


	question_sum = 0
	total_forms = 0 
	for form in all_forms: 
		fields = all_forms.filter(question_id=26)
		for field in fields:
			if field.body and field.body[0] != '0': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body[0]) # body holds the judge's answer for one question
				total_forms += 1
	if total_forms != 0: #if no forms (or only N/A answers) were filled out for this question, set the sum to 0
		average26 = question_sum / total_forms
		final_sum += average26

#	final_sum = average16 + average17 + average18 + average19 + average20 + average21 + average22 + average23 + average24 + average25 + average26
		
	
	context = {
		'average16': average16,
		'average17': average17,
		'average18': average18,
		'average19': average19,
		'average20': average20,
		'average21': average21,
		'average22': average22,
		'average23': average23,
		'average24': average24,
		'average25': average25,
		'average26': average26,
		'final_sum': final_sum,
	}
	return render(request, 'results.html', context)

	
	
def winners(request):
	#discipline = SurveyAnswer.objects.filter()
	#project evalutation forms
	#1. sort by major/dicipline
	#2. sort by sessoin
	#3. for each group, find their average score
	#4. compare group averages to all other groups in their sessions
	#5. return the highest average score & team name for each session winner
	
	all_forms = SurveyAnswer.objects.all()
	

	# Each of the following lists is associated with a session. Each will hold the average scores (for all questions & all judges) of each team,
	# which will be uesed to find the session winners
	bio1 = {}
	bio2 = {}
	civil1 = {}
	civil2 = {}
	coen1 = {}
	coen2 = {}
	elen1 = {}
	elen2 = {}
	interdisciplinary1 = {}
	interdisciplinary2 = {}
	mech1 = {}
	mech2 = {}

	############# NEW GAMEPLAN ################
	# Find the average score for a team by 
	# 1. iterating through all responses for a team name 
	# 2. then going through each question (194-204) & store that judge's total score (sum all answers) for that team
	# 3. find average score for team by doing: (total1 + total2 + ... + totaln) / # of judges & store in bio1
	# 4. Iterate through bio1 to find the session winner
	# BioE session 1: find  #193 - 204
#total_forms = 0
	question_sum = 0
	title = ''
	group_total = []
	bio1_answers = [] # list to store each response to 1 judges survey for 1 team
	conn = sqlite3.connect('db.sqlite3')
	c = conn.cursor()
	c1 = conn.cursor()
	c2 = conn.cursor()
	final = c.execute('SELECT MAX(response_id) FROM survey_answer') # iterate through all the rows & order by response_id
	data = c.execute('SELECT question_id, response_id, body FROM survey_answer ORDER BY response_id') 
	for item in final: # this for loop is only used to find end, the largest response_id
		end = int(item[1]) # currently 22
#	bio1_answers.append('Should be 22: '+ str(end))

	data = c1.execute('SELECT question_id, response_id, body FROM survey_answer ORDER BY response_id') 
	for row in data: # list of all rows
 		# Note: row is a tuple in this form (question_id, response_id, body) as row[0], row[1], and row[2] respectively
		for i in range(1, end+1): # i is the current response_id in data --> now find a way to connect these two!
			if int(row[1]) == i and row[0] == 192: # when question_id == 192 #TODO: this stops at first one, we want ALL
				row_id = row[1] # store the response_id
#				bio1_answers.append('Row[2]: ' +  row[2] + ' Title: ' + title)
				if row[2] != title:
					bio1_answers.append('Updating title to: ' + row[2])
					title = row[2] # store the name (body)
					question_sum = 0
#					del bio1_answers[:] # remove all elts in bio1_answers
#					bio1_answers = []
				#bio1_answers.append('Updated: ')
				bio1_answers.append(title)

#			group = all_forms.filter(response_id=row[1]) # current response_id
				q = 'SELECT question_id, response_id, body FROM survey_answer WHERE response_id=' + str(row_id)
				for score in c2.execute(q): # gets one judges evaluation for one team
					if score[0] == 192 and score[2] != title: # TODO: never entering into this if statement
#						bio1_answers.append('Incorrect: ' + score[2])
						continue # stop this iteration of the loop b/c it consists of the wrong group!
#						bio1_answers.append('Updating title to: ' + score[2])
#						title = score[2]
					if score[0] >= 193 and score[0] < 205:
						question_sum += int(score[2]) # body
						bio1_answers.append(score[2])
					elif score[0] == 205: # this will happen for 192, 205 & 206
#score[0] == 192: # once all of the scores for one judge have been added, store that total
#if score[2] == title:
#						if total_forms == 0:
#							bio1[title] = question_sum # add the new team to list
#						else:
#							bio1[title] += question_sum # add new judge's average to that team 
#						total_forms += 1
						group_total.append(question_sum)

						bio1_answers.append('group_total: ' + str(group_total))
#bio1_answers.append('t_forms: ' + str(total_forms))
	
			else:
				continue
			
			judges = len(group_total)
			group_score = 0
			for t in range(0, judges):
				group_score += group_total[t]
			if judges > 0:
				bio1[title] = group_score / judges
			else: 
				bio1[title] = 'No judges have submitted scores for this group.'
			question_sum = 0
#			team_avg = bio1[title] / total_forms # bio1[title] should just be the question_sum 
#			bio1[title] = team_avg # add the new team to list
			
#total_forms = 0
	################# Find session winner by finding max of bio1 ##############	
	if len(bio1.values()) > 0: # ensure that at least one elt exists (& set that to current max) before trying to find actual max
		sort = sorted(bio1.items(), key = lambda t:t[1]) # sort by the max average
		bio1_winner = sort[len(bio1.values())-1][0]
		bio1_winner_num = bio1[bio1_winner]


	else:
		bio1_winner = "No session winner was determined. Either no judges have scored this session yet, or all of the scores were 'NA'"
		bio1_winner_num = 0

	################ TODO: FIX these to represent actual titile values associated with the max for each session ####################
	bio2_winner = "Winner not yet determined for this session" 
	civil1_winner =	"Winner not yet determined for this session" 
	civil2_winner = "Winner not yet determined for this session" 
	coen1_winner = "Winner not yet determined for this session" 
	coen2_winner = "Winner not yet determined for this session" 
	elen1_winner = "Winner not yet determined for this session" 
	elen2_winner = "Winner not yet determined for this session" 
	interdisciplinary1_winner = "Winner not yet determined for this session" 
	interdisciplinary2_winner = "Winner not yet determined for this session" 
	mech1_winner = "Winner not yet determined for this session" 
	mech2_winner = "Winner not yet determined for this session" 


	context = {
		'bio1_winner': 'Should be <bioe-1-group-2-title> with score <52>: ' + str(bio1_winner),
		'bio1_winner_num': bio1_winner_num,
#		'bio1': bio1,
		'bio1_answers': bio1_answers,
		'bio2_winner': bio2_winner,
		'civil1_winner': civil1_winner,
		'civil2_winner': civil2_winner,
		'coen1_winner': coen1_winner,
		'coen2_winner': coen2_winner,
		'elen1_winner': elen1_winner,
		'elen2_winner': elen2_winner,
		'interdisciplinary1_winner': interdisciplinary1_winner,
		'interdisciplinary2_winner': interdisciplinary2_winner,
		'mech1_winner': mech1_winner,
		'mech2_winner': mech2_winner,
	}
	return render(request, 'winners.html', context)
	
	'''
	
	############# WORKS #############################
	#initialize all of the forms you want to look though
	f = []
	for i in range(193, 205):
		f.append("all_forms.filter(question_id=" + str(i) + ")")
	
	###########	Generates #########################
	fields = [ # this time, you can't iterate by question, rather for each team, you must iterate through each judges' score for them 
		'all_forms.filter(question_id=193).body', 
		all_forms.filter(question_id=194), 
		all_forms.filter(question_id=195), 
		all_forms.filter(question_id=196), 
		all_forms.filter(question_id=197), 
		all_forms.filter(question_id=198), 
		all_forms.filter(question_id=199), 
		all_forms.filter(question_id=200), 
		all_forms.filter(question_id=201), 
		all_forms.filter(question_id=202), 
		all_forms.filter(question_id=203), 
		all_forms.filter(question_id=204), 
	]
	

	############# DOESN'T WORK Yet ##################
	for form in all_forms: # go through every form 
		for questions in f: # go through every question in the survey
			for field in questions: # go through every judge's submission for each question
				field = exec(field)
				if field.body and field.body != 'NA': # else if body is empty or if judge deemed question NA, skip adding it into the average
					question_sum += int(field.body[0]) # body holds the judge's answer for one question
					total_forms += 1
	if total_forms != 0: #if no forms (or only NA answers) were filled out for this question, set the sum to 0
		team1 = question_sum / total_forms
		
		
		
		
		fields = all_forms.filter(question_id=194) # TODO: use another filter here to only get the responses from 1 judge
		for field in fields: # fields hold all instances of where there is a group title for the bioe session 1
			if field.body and field.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body) # body holds the judge's answer for one question
		fields = all_forms.filter(question_id=195) # TODO: use another filter here to only get the responses from 1 judge
		for field in fields: # fields hold all instances of where there is a group title for the bioe session 1
			if field.body and field.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body) # body holds the judge's answer for one question
		fields = all_forms.filter(question_id=196) # TODO: use another filter here to only get the responses from 1 judge
		for field in fields: # fields hold all instances of where there is a group title for the bioe session 1
			if field.body and field.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body) # body holds the judge's answer for one question
		fields = all_forms.filter(question_id=197) # TODO: use another filter here to only get the responses from 1 judge
		for field in fields: # fields hold all instances of where there is a group title for the bioe session 1
			if field.body and field.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body) # body holds the judge's answer for one question
		fields = all_forms.filter(question_id=198) # TODO: use another filter here to only get the responses from 1 judge
		for field in fields: # fields hold all instances of where there is a group title for the bioe session 1
			if field.body and field.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body) # body holds the judge's answer for one question
		fields = all_forms.filter(question_id=199) # TODO: use another filter here to only get the responses from 1 judge
		for field in fields: # fields hold all instances of where there is a group title for the bioe session 1
			if field.body and field.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body) # body holds the judge's answer for one question
		fields = all_forms.filter(question_id=200) # TODO: use another filter here to only get the responses from 1 judge
		for field in fields: # fields hold all instances of where there is a group title for the bioe session 1
			if field.body and field.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body) # body holds the judge's answer for one question
		fields = all_forms.filter(question_id=201) # TODO: use another filter here to only get the responses from 1 judge
		for field in fields: # fields hold all instances of where there is a group title for the bioe session 1
			if field.body and field.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body) # body holds the judge's answer for one question
		fields = all_forms.filter(question_id=202) # TODO: use another filter here to only get the responses from 1 judge
		for field in fields: # fields hold all instances of where there is a group title for the bioe session 1
			if field.body and field.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body) # body holds the judge's answer for one question
		fields = all_forms.filter(question_id=203) # TODO: use another filter here to only get the responses from 1 judge
		for field in fields: # fields hold all instances of where there is a group title for the bioe session 1
			if field.body and field.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body) # body holds the judge's answer for one question
		fields = all_forms.filter(question_id=204) # TODO: use another filter here to only get the responses from 1 judge
		for field in fields: # fields hold all instances of where there is a group title for the bioe session 1
			if field.body and field.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
				question_sum += int(field.body) # body holds the judge's answer for one question
		
#	for form in all_forms:
	for each_id in unique_ids: # a list of all the response_ids
# fields hold all instances of where there is a group title for the bioe session 1
#if field.body 
	unique_ids = SurveyAnswer.objects.distinct('response_id').all() #.filter(response_id=1) # TODO: use another filter here to only get the responses from 1 judge
		uuid = all_forms.filter(response_id=each_id) # TODO: this needs to get a section of all the rows with this uuid
		for u in uuid:
################## INSERT THIS INTO FOR ABOVE
			if uuid.question_id == 192: #"WINNER -- right now, this shows the total average of all scores in this session (regardless of team)" #all_forms.filter(question_id=192) #all_forms.filter(question_id=192) # TODO: update the title here, I think
				title = uuid.body
			if uuid.question_id in range(193, 205): # 193 - 204
				if uuid.body != 'NA': # else if body is empty or if judge deemed question N/A, skip adding it into the average
					bio1_answers.append(uuid.body)
					question_sum += int(uuid.body) # body holds the judge's answer for one question
			total_forms += 1 # TODO: this only appears here, is that okay???????????
	
		if total_forms != 0: # if no forms (or only NA answers) were filled out for this question, set the sum to 0
			team_avg = question_sum / total_forms
			bio1[team_avg] = title  # iterate throuh this to find session winner
		
	
	
	
	
	
		all_values = list(bio1.values())
		bio1_winner = all_values[0] # this should store the team name value (not team average)
		bio1_winner_num = bio1[bio1_winner] 
		for team in all_values: # iterate through all of the values in bio1 to find the max
			if team > bio1_winner_num: # TODO:  ############### SHOULD WE DO ANYTHING IF 2 TEAMS HAVE THE SAME SCORE & TIE FOR WINNER????
				bio1_winner_num = team # update max to higher value
				bio1_winner = bio1[team] # store the group's name to return on the winner screen

	'''
		
