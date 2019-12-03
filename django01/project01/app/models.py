# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)
    permission = models.ForeignKey('AuthPermission', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    action_flag = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

class SurveyAnswer(models.Model):
    created = models.DateTimeField()
    question = models.ForeignKey('SurveyQuestion', on_delete=models.CASCADE)
    response = models.ForeignKey('SurveyResponse', on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=True)
    updated = models.DateTimeField()
    # newly added track user who submits survey
	#user = models.ForeignKey(User)

#user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False # changed from False
        db_table = 'survey_answer'


class SurveyCategory(models.Model):
    name = models.CharField(max_length=400)
    order = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=2000, blank=True, null=True)
    survey = models.ForeignKey('SurveySurvey', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'survey_category'


class SurveyQuestion(models.Model):
    text = models.TextField()
    order = models.IntegerField()
    required = models.BooleanField()
    type = models.CharField(max_length=200)
    choices = models.TextField(blank=True, null=True)
    survey = models.ForeignKey('SurveySurvey', on_delete=models.CASCADE)
    category = models.ForeignKey(SurveyCategory, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'survey_question'


class SurveyResponse(models.Model):
    created = models.DateTimeField()
    updated = models.DateTimeField()
    interview_uuid = models.CharField(max_length=36)
    survey = models.ForeignKey('SurveySurvey', on_delete=models.CASCADE)
	# change many-to-one relationship to many-to-many 
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, blank=True, null=True)


#user2 = models.ManyToManyField(AuthUser)

    class Meta:
        managed = False # changed from False
        db_table = 'survey_response'


class SurveySurvey(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    is_published = models.BooleanField()
    need_logged_user = models.BooleanField()
    display_by_question = models.BooleanField()
    template = models.CharField(max_length=255, blank=True, null=True)
    editable_answers = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'survey_survey'
