from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'hod', "created_at", "created_by"]
    search_fields = ['name']
    readonly_fields = ["created_at", "created_by"]

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', "created_at", "created_by"]
    search_fields = ['name', 'department__name']
    readonly_fields = ["created_at", "created_by"]

@admin.register(CourseMETA)
class CourseMETAAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'department',  'type', '_credits', 'created_by']
    search_fields = ['name', 'code', 'department']
    list_filter = ["_type", "_credits"]
    readonly_fields = ["created_at", "created_by"]

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'faculty','semester', 'is_active', 'is_completed' ]
    search_fields = ['name', 'code']
    readonly_fields = ["code", "total_class", "total_hours", "created_at"]

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "created_at"]
    readonly_fields = ["attendance", "created_at",]

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    list_display = ["course", "hours", "created_at"]
    search_fields = ['course__name', 'course__code']
    readonly_fields = ["course", "hours", "created_at"]

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ["student", "lecture", "is_present", "created_at"]
    search_fields = ['student__register_no', 'lecture__name', 'lecture__code']
    readonly_fields = ["lecture", "is_present", "created_at"]

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["name", "course", "max_marks", "deadline", "created_at"]
    search_fields = ['name', 'course__name', 'course__code']
    readonly_fields = ["created_at"]

@admin.register(SubmittedAssignments)
class SubmittedAssignmentsAdmin(admin.ModelAdmin):
    list_display = ["student", "assignment", "marks", "created_at"]
    search_fields = ['student__register_no', 'assignment__name', 'assignment__course__code']
    readonly_fields = ["created_at"]

@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ["name", "course", "max_marks", "conducted_on", "created_at"]
    search_fields = ['name', 'course__name']
    readonly_fields = [ "created_at"]

@admin.register(ExaminationResults)
class ExaminationResultsAdmin(admin.ModelAdmin):
    list_display = ["student", "examination", "marks", "created_at"]
    search_fields = ['student__register_no', 'examination__name', 'examination__course__code']
    readonly_fields = ["created_at"]

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display=["student", "course", "_type", "is_accepted"]
    readonly_fields = ["created_at"]

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]

@admin.register(Disciplinary)
class DisciplinaryAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]