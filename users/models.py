from django.db import models
from crum import get_current_user
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.authtoken.models import Token

from arms.settings import DEFAULT_FROM_EMAIL
import datetime

# Create your models here.

DESIGNATION_CHOICES = [("LAB TECHINICIAN", "LAB TECHNICIAN"), ("ASSITANT PROFESSOR", "ASSISTANT PROFESSOR"), ("ASSOCIATE PROFESSOR", "ASSOCIATE PROFESSOR"), ("PROFESSOR", "PROFESSOR"), ("HOD", "HOD"), ("DEAN", "DEAN"), ("VP", "VP"), ("PRINCIPAL", "PRINCIPAL")]
ACADEMIC_PROGRAMS = [("UG", "UNDER GRADUATION"), ("PG", "POST GRADUATION"), ("DIPLOMA", "DIPLOMA")]

def get_image_path(instance, filename):
    return f'user_data/{instance.id}_{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}_{filename}'

class UserManager(BaseUserManager):

    def create_user(self, email, register_no, password, **extra_fields):
        if not email:
            raise ValueError('Email for user must be set.')
        if not register_no:
            raise ValueError('Register number for user must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.register_no = register_no
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, email, register_no, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, register_no, password, **extra_fields)

class User(AbstractUser):

    ADMIN_ROLE = 'admin'

    email = models.CharField(max_length=255, unique=True)
    register_no = models.CharField(max_length=255, unique=True, editable=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    dob = models.DateTimeField(blank=True, null=True)
    mobile_no = models.IntegerField(blank=True, null=True)

    username = None
    USERNAME_FIELD = 'register_no'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    user_organisation_role = models.ForeignKey("users.UserOrganisationRoleTable",on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(blank=True, null=True, upload_to=get_image_path)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey('self', on_delete=models.RESTRICT, blank=True, null=True, related_name='created_by_user', editable=False)
    account_terminated = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return str(self.register_no.upper())

    def users_return(self):
        return User.objects.filter(account_terminated=False)
    
    def students_return(self):
        return User.objects.filter(user_organisation_role="student", account_terminated=False)

    def faculties_return(self):
        return User.objects.filter(user_organisation_role="faculty", account_terminated=False)

    def save(self, *args, **kwargs):
        user = get_current_user()
        
        if not self.created_by:
            self.created_by = user

        if not self.is_active:
            token_ins = Token.objects.filter(user_id=self.id)
            if token_ins:
                token_ins.delete()

        super(User, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.account_terminated = True
        self.is_active = False
        super(User, self).save(*args, **kwargs)

class Student(models.Model):
    meta = models.ForeignKey("users.User", on_delete=models.CASCADE)
    program = models.CharField(max_length=255, choices=ACADEMIC_PROGRAMS)
    academic_year = models.DateTimeField()
    branch = models.ForeignKey("academics.Branch", on_delete=models.SET_NULL, blank=True, null=True)
    mentor = models.ForeignKey("users.Faculty", on_delete=models.SET_NULL, blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    achievements =  models.TextField(blank=True, null=True)
    father_name = models.CharField(max_length=255, blank=True, null=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    parent_mobile_no = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey('users.User', on_delete=models.RESTRICT, related_name='student_creator', editable=False)

    def __str__(self):
        return self.meta.register_no.upper()

    def save(self, *args, **kwargs):
        user = get_current_user()
        if self._state.adding:
            if not self.meta.user_organisation_role.is_student:
                raise Exception("User Organisation role for user must be Student")
            self.created_by = user

        super(Student, self).save(*args, **kwargs)

class Faculty(models.Model):
    meta = models.ForeignKey("users.User", on_delete=models.CASCADE)
    department = models.ForeignKey("academics.Department", on_delete=models.SET_NULL, blank=True, null=True)
    designation = models.CharField(max_length=255, choices=DESIGNATION_CHOICES)
    education = models.TextField(blank=True, null=True)
    is_phd_holder = models.BooleanField(default=False)
    experience = models.IntegerField(blank=True, null=True)
    achievements =  models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey('users.User', on_delete=models.RESTRICT, related_name='faculty_creator', editable=False)

    def __str__(self):
        return str(self.meta.name.upper())

    def save(self, *args, **kwargs):
        user = get_current_user()
        if self._state.adding:
            if not self.meta.user_organisation_role.is_faculty:
                raise Exception("User Organisation role for user must be Faculty")
            self.created_by = user

        super(Faculty, self).save(*args, **kwargs)

class UserOrganisationRoleTable(models.Model):
    role = models.CharField(max_length=255, unique=True)
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey('users.User', on_delete=models.RESTRICT, editable=False)
    
    def __str__(self):
        return str(self.role)

    def save(self, *args, **kwargs):
        user = get_current_user()
        self.created_by = user

        super(UserOrganisationRoleTable, self).save(*args, **kwargs)

def get_file_path(instance, filename):

    return f'NotificationFiles/{instance.id}_{filename}'

NOTIFY_FOR_CHOICES = [('STUDENT', 'STUDENT'),('FACULTY', 'FACULTY'),('ALL', 'ALL')]

NOTIFY_TYPE_CHOICES = [("ATTENDANCE", "ATTENDANCE"), ('COURSE', 'COURSE'),('BRANCH', 'BRANCH'),('DEPARTMENT', 'DEPARTMENT'),('ALL', 'ALL')]

class Notification(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    notify_for = models.CharField(max_length=255, choices=NOTIFY_FOR_CHOICES)
    notify_type = models.CharField(max_length=100, choices=NOTIFY_TYPE_CHOICES)
    message = models.TextField()
    input_file = models.FileField(blank=True, null=True, upload_to=get_file_path)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.Faculty', on_delete=models.RESTRICT, editable=False)

    def __str__(self):
        return str(self.message)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if self._state.adding:
            if user.user_organisation_role.is_student:
                raise Exception("Students are not allowed to create the Notification")
            faculty_ins = Faculty.objects.get(meta__id=user.id)
            self.created_by = faculty_ins
        super(Notification, self).save(*args, **kwargs)