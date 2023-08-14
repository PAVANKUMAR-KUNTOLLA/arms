# from django.conf import settings
from rest_framework import serializers

from .models import *
from users.models import User

class DepartmentSerializer(serializers.ModelSerializer):
    hod = serializers.SerializerMethodField()
    class Meta:
        model = Department
        fields = "__all__"
    def get_hod(self, instance):
        return instance.hod.meta.name

class BranchSerializer(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()
    class Meta:
        model = Branch
        fields = ('id', 'name', 'department')

    def get_department(self, instance):
        return instance.department.name

class CourseMETASerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=[(each, each) for each in COURSE_TYPE_CHOICES], source="_type", required=True)
    credits = serializers.ChoiceField(choices=[(each, each) for each in CREDIT_CHOICES], source="_credits", required=True)
    
    class Meta:
        model = CourseMETA
        fields = ('id', 'name', 'code',  'department', 'type', 'credits')

class CourseSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    faculty = serializers.SerializerMethodField()
    students = serializers.StringRelatedField(many=True)
    total_class = serializers.SerializerMethodField()
    total_hours = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields =  "__all__" 
        extra_kwargs={"code":{"required":False, "allow_null":True}, "students":{"required":False, "allow_null":True}}
    
    def get_category(self, instance):
        return instance.category.code
    def get_faculty(self, instance):
        return instance.faculty.meta.register_no
    def get_total_class(self, instance):
        return instance.total_class
    def get_total_hours(self, instance):
        return instance.total_hours
        
class CourseViewSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    total_class = serializers.SerializerMethodField()
    total_hours = serializers.SerializerMethodField()
    faculty = serializers.SerializerMethodField()
    students = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ('id','name', 'code', 'category', 'faculty', 'students', 'semester', 'academic_year', 'start_date', 'end_date', 'is_active', 'total_class', 'total_hours', 'is_completed', 'is_result_published', 'created_at')

    def get_total_class(self, instance):
        return instance.total_class
    def get_total_hours(self, instance):
        return instance.total_hours
    def get_category(self, instance):
        return instance.category.code
    def get_faculty(self, instance):
        return instance.faculty.meta.register_no
    def get_students(self, instance):
        queryset = CourseEnrollment.objects.filter(course__id=instance.id)
        return_dict = list()
        for each_student in queryset:
            each_student = {"id":each_student.student.id, "register_no":each_student.student.meta.register_no, "name":each_student.student.meta.name, "attendance":each_student.attendance, "enrolled_on":each_student.created_at}
            return_dict.append(each_student)
        return return_dict

class CourseEnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    attendance = serializers.SerializerMethodField()
    enrolled_on = serializers.SerializerMethodField()
    class Meta:
        model = CourseEnrollment
        fields = ("student", "course", "attendance", "enrolled_on")

    def get_student(self, instance):
        return instance.student.meta.register_no
    
    def get_course(self, instance):
        return instance.course.code

    def get_enrolled_on(self, instance):
        return instance.created_at.strftime("%Y-%m-%d")
    
    def get_attendance(self, instance):
        return instance.attendance

class RequestSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=[(each, each) for each in REQUEST_CHOICES], source="_type", required=True)
    is_accepted = serializers.SerializerMethodField()
    class Meta:
        model = Request
        fields = ('id','student', 'course', 'type', 'is_faculty_approved', 'is_hod_approved', 'is_mentor_approved', 'is_accepted', 'is_rejected')

    def get_is_accepted(self, instance):
        return instance.is_accepted

class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    hours = serializers.SerializerMethodField()
    lecture_date = serializers.SerializerMethodField()
    class Meta:
        model = Attendance
        fields = ('student', 'course', 'hours', 'is_present', 'lecture_date')

    def get_student(self, instance):
        return instance.student.meta.register_no

    def get_course(self, instance):
        return instance.lecture.course.code
    
    def get_hours(self, instance):
        return instance.lecture.hours
    
    def get_lecture_date(self, instance):
        return instance.created_at.strftime("%Y-%m-%d")

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"

class AssignmentViewSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    deadline = serializers.SerializerMethodField()
    class Meta:
        model = Assignment
        fields = ('id', 'name', 'course', 'max_marks', 'deadline', 'created_at')
    
    def get_course(self, instance):
        return instance.course.code
    def get_deadline(self, instance):
        if instance.deadline:
            return instance.deadline.strftime("%Y-%m-%d")
        else:
            return None

class SubmittedAssignmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedAssignments
        fields = "__all__"
        extra_kwargs = {"student":{"required":False, "allow_null":True}}

class SubmittedAssignmentsViewSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = SubmittedAssignments
        fields = ('id', 'student', 'name', 'course', 'marks', 'is_verified', 'created_at')
    
    def get_student(self, instance):
        return instance.student.meta.register_no
    def get_name(self, instance):
        return instance.assignment.name
    def get_course(self, instance):
        return instance.assignment.course.code
    def get_name(self, instance):
        return instance.assignment.name

class ExaminationSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    conducted_on = serializers.SerializerMethodField()
    class Meta:
        model = Examination
        fields = ('id', 'name', 'course', 'max_marks', 'conducted_on')
    
    def get_student(self, instance):
        return instance.student.meta.register_no
    def get_course(self, instance):
        return instance.course.code
    def get_conducted_on(self, instance):
        return instance.conducted_on.strftime("%Y-%m-%d")

class ExaminationResultsSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    examination = serializers.SerializerMethodField()
    conducted_on = serializers.SerializerMethodField()
    class Meta:
        model = ExaminationResults
        fields = ('id', 'student', 'examination', 'course', 'marks', 'conducted_on', 'created_at')
    
    def get_student(self, instance):
        return instance.student.meta.register_no
    def get_course(self, instance):
        return instance.examination.course.code
    def get_name(self, instance):
        return instance.examination.name
    def get_conducted_on(self, instance):
        return instance.examination.conducted_on.strftime("%Y-%m-%d")

class ResultSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    month_year_of_passing = serializers.SerializerMethodField()
    class Meta:
        model = Result
        fields = ('id', 'student', 'code', 'name', 'grade', 'status', 'month_year_of_passing')
    
    def get_student(self, instance):
        return instance.student.meta.register_no
    def get_code(self, instance):
        return instance.course.code
    def get_course(self, instance):
        return instance.course.name
    def get_conducted_on(self, instance):
        return instance.month_year_of_passing.strftime("%b %Y")

