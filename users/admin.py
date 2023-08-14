from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'register_no', 'email'] # user_location
    search_fields = ['name', 'email', 'register_no']
    list_filter = ['is_active']
    readonly_fields = ["created_at", "created_by"]

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['meta', 'program', 'branch',]
    search_fields = ['meta__name', 'meta__email', 'meta__register_no']
    list_filter = ['meta__is_active']
    readonly_fields = ["created_at", "created_by"]

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['meta', 'designation', 'department']
    search_fields = ['meta__name', 'meta__email', 'meta__register_no']
    list_filter = ['meta__is_active']
    readonly_fields = ["created_at", "created_by"]


@admin.register(UserOrganisationRoleTable)
class UserOrganisationRoleTableAdmin(admin.ModelAdmin):
    list_display = ['role', 'is_student', 'is_faculty', 'is_admin', 'created_by', 'created_at']
    readonly_fields = ["created_at", "created_by"]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notify_type', 'notify_for']
    readonly_fields = ["created_at", "created_by"]