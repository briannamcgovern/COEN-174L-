from django.db import models
#from app.models import model
from app.models import AuthUser, SurveySurvey, SurveyResponse
#import sqlite3

# Create your models here.

class SurveySubmits(models.Model):
	judged_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
	survey = models.ForeignKey(SurveySurvey, on_delete=models.CASCADE)


