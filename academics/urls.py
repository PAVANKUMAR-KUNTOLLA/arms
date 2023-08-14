from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'department', DepartmentViewSet, basename="department")
router.register(r'branch', BranchViewSet, basename="branch")
router.register(r'course_meta', CourseMETAViewSet, basename="course_meta")
router.register(r'course', CourseViewSet, basename="course")
router.register(r'course_enrollment', CourseEnrollmentViewSet, basename="course_enrollment")
router.register(r'request', RequestViewSet, basename="request")
router.register(r'attendance', AttendanceViewSet, basename="attendance")
router.register(r'assignment', AssignmentViewSet, basename="assignment")
router.register(r'submitted_assignments', SubmittedAssignmentsViewSet, basename="submitted_assignments")

urlpatterns = [
    path('api/v1/', include(router.urls)),
]