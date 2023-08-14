from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import validate_email
from rest_framework import serializers
from users.models import *
from academics.models import Branch, Department
import datetime
from users.models import DESIGNATION_CHOICES

class SignupSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    register_no = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=[(each, each) for each in list(UserOrganisationRoleTable.objects.all().values_list("role", flat=True))], required=True)
    dob = serializers.DateTimeField(required=False)
    mobile_no = serializers.IntegerField(required=False)

    def validate_email(self, email):
        is_valid_email = False
        try:
            validate_email(email)
        except Exception as excepted_message:
            raise Exception('Please use valid email for registration.')
            
        if User.objects.filter(email__iexact=email).exists():
            raise Exception('This user already exists. Please sign in.')
        return str(email).strip().lower()

    def validate_register_no(self, register_no):
        is_valid_register_no = False
        
        if len(register_no)!= 10:
            raise Exception('Please use valid Register Id for registration.')
            
        if User.objects.filter(register_no__iexact=register_no).exists():
            raise Exception('This user already exists. Please sign in.')
        return str(register_no).strip().upper()

    def save(self):
        name = self.validated_data['name']
        email = self.validated_data['email']
        register_no = self.validated_data["register_no"]
        password = "welcome"
        role_ins = UserOrganisationRoleTable.objects.get(role=self.validated_data["role"])

        user = User.objects.create(name=name, email=email, register_no=register_no, user_organisation_role=role_ins)
        user.is_active = True

        if "dob" in self.validated_data:
            user.dob = self.validated_data["dob"]
        if "mobile_no" in self.validated_data:
            user.mobile_no = self.validated_data["mobile_no"]

        user.set_password(password)
        user.save()
        return user

class StudentSignupSerializer(serializers.Serializer):
    register_no = serializers.ChoiceField(choices=[(each, each) for each in list(User.objects.all().values_list("register_no", flat=True))], required=True)
    program = serializers.ChoiceField(choices=[(each, each) for each in ACADEMIC_PROGRAMS], required=True)
    branch = serializers.ChoiceField(choices=[(each, each) for each in list(Branch.objects.all().values_list("name", flat=True))], required=True)
    academic_year = serializers.CharField(required=True)
    father_name = serializers.CharField(required=False)
    mother_name = serializers.CharField(required=False)
    parent_mobile_no = serializers.CharField(required=False)
    address = serializers.CharField(required=False)

    def validate_academic_year(self, academic_year):
        try:
            datetime_ins = datetime.datetime.strptime(academic_year, "%Y-%m-%d")
            if datetime_ins.year < datetime.datetime.now().year:
                raise Exception('Academic year can not be in past for registration.')
        except Exception as excepted_message:
            raise Exception (str(excepted_message))
        return datetime_ins

    def validate_register_no(self, register_no):
        if Student.objects.filter(meta__register_no__iexact=register_no).exists():
            raise Exception('This user already exists. Please sign in.')
        return str(register_no).strip().upper()

    def save(self):
        user_ins = User.objects.get(register_no=self.validated_data["register_no"])
        for each_choice in ACADEMIC_PROGRAMS:
            if each_choice[1] == self.validated_data["program"]:
                program = each_choice[0]
        branch_ins = Branch.objects.get(name=self.validated_data["branch"])
        academic_year = self.validated_data["academic_year"]

        student_ins = Student.objects.create(meta=user_ins, program=program, branch=branch_ins, academic_year = academic_year)
       
        if "father_name" in self.validated_data:
            student_ins.father_name = self.validated_data["father_name"]
        if "mother_name" in self.validated_data:
            student_ins.mother_name = self.validated_data["mother_name"]
        if "parent_mobile_no" in self.validated_data:
            student_ins.parent_mobile_no = self.validated_data["parent_mobile_no"]
        if "address" in self.validated_data:
            student_ins.address = self.validated_data["address"]

        student_ins.save()
        return student_ins
        
class FacultySignupSerializer(serializers.Serializer):
    register_no = serializers.ChoiceField(choices=[(each, each) for each in list(User.objects.all().values_list("register_no", flat=True))], required=True)
    department = serializers.ChoiceField(choices=[(each, each) for each in list(Department.objects.all().values_list("name", flat=True))], required=True)
    designation = serializers.ChoiceField(choices=[(each, each) for each in DESIGNATION_CHOICES], required=True)
    is_phd_holder = serializers.BooleanField(required=True)

    def validate_register_no(self, register_no):
        if Faculty.objects.filter(meta__register_no__iexact=register_no).exists():
            raise Exception('This user already exists. Please sign in.')
        return str(register_no).strip().upper()

    def save(self):
        user_ins = User.objects.get(register_no=self.validated_data["register_no"])
        department_ins = Department.objects.get(name=self.validated_data["department"])
        designation = self.validated_data["designation"]
        is_phd_holder = self.validated_data["is_phd_holder"]

        faculty_ins = Faculty.objects.create(meta=user_ins, department=department_ins, designation=designation, is_phd_holder=is_phd_holder)
        faculty_ins.save()
        return faculty_ins

class AuthenticationSerializer(serializers.Serializer):

    register_no = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        register_no = attrs['register_no']
        password = attrs['password']
        if register_no and password:
            user = authenticate(request=self.context['request'], register_no=str(register_no).strip().upper(), password=password)

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg = _('User is set Not Active')
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = "__all__"


class UserProfileSerializer(serializers.ModelSerializer):
    academic_info = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'name', 'email',  'register_no', 'role', 'academic_info']

    def get_academic_info(self, instance):
        if instance.user_organisation_role.is_student:
            info = StudentSerializer(read_only=True, many=True)
        elif instance.user_organisation_role.is_faculty:
            info = FacultySerializer(read_only=True, many=True)
        else:
            info = []
        return info

    def get_role(self, instance):
        return instance.user_organisation_role.role
