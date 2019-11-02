from django.shortcuts import render
from django.http import HttpResponse


def index(request):
        return HttpResponse("Hello, world. You're at the polls index.")

def home(request):
        return HttpResponse("Homepage")

def createSessions(request):
    return render(request, 'app/create-sessions.html', {})