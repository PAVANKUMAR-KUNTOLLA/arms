import os
import io
import re
import copy
import datetime
from django.utils import timezone
from django.db import transaction

from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import *
from .models import Department, Branch, CourseMETA, Course, Request, CourseEnrollment, Lecture, Attendance, REQUEST_CHOICES
from users.models import User, Student, Faculty, Notification
# Create your views here.

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class DepartmentViewSet(ViewSet):

    def list(self, request):
        queryset = Department.objects.all()
        serializer = DepartmentSerializer(queryset, many=True)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

    def create(self, request):
        if not request.user.user_organisation_role.is_admin:
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_201_CREATED, "message": "success"}
            return Response(status=status.HTTP_201_CREATED, data= context)
        else:
            context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
            return Response(status=status.HTTP_400_BAD_REQUEST, data= context)

    def retrieve(self, request, pk=None):
        if Department.objects.filter(id=pk).exists():
            queryset = Department.objects.all()
            department = get_object_or_404(queryset, pk=pk)
            serializer = DepartmentSerializer(department)
            context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "Department not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

    def update(self, request, pk=None):
        if not request.user.user_organisation_role.is_admin:
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if Department.objects.filter(id=pk).exists():
            queryset = Department.objects.all()
            department = get_object_or_404(queryset, pk=pk)
            serializer = DepartmentSerializer(department, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": "success"}
                return Response(status=status.HTTP_200_OK, data= context)
            else:
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
        else:
            message = "Department not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)


    def partial_update(self, request, pk=None):
        if not request.user.user_organisation_role.is_admin:
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if Department.objects.filter(id=pk).exists():
            queryset = Department.objects.all()
            department = get_object_or_404(queryset, pk=pk)
            serializer = DepartmentSerializer(department, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": "success"}
                return Response(status=status.HTTP_200_OK, data= context)
            else:
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
        else:
            message = "Department not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

    def destroy(self, request, pk=None):
        if not request.user.user_organisation_role.is_admin:
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if Department.objects.filter(id=pk).exists():
            queryset = Department.objects.all()
            department = get_object_or_404(queryset, pk=pk)
            department.delete()
            context = {"data":None, "status_flag":True, "status":status.HTTP_200_OK, "message": "successfully deleted"}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "Department not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)
    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BranchViewSet(ViewSet):

    def list(self, request):
        queryset = Branch.objects.all()
        serializer = BranchSerializer(queryset, many=True)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

    def create(self, request):
        if not request.user.user_organisation_role.is_admin:
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        serializer = BranchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {"data":None, "status_flag":True, "status":status.HTTP_201_CREATED, "message": "success"}
            return Response(status=status.HTTP_201_CREATED, data= context)
        else:
            context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
            return Response(status=status.HTTP_400_BAD_REQUEST, data= context)

    def retrieve(self, request, pk=None):
        if Branch.objects.filter(id=pk).exists():
            queryset = Branch.objects.all()
            branch = get_object_or_404(queryset, pk=pk)
            serializer = BranchSerializer(branch)
            context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "Branch not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

    def update(self, request, pk=None):
        if not request.user.user_organisation_role.is_admin:
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if Branch.objects.filter(id=pk).exists():
            queryset = Branch.objects.all()
            branch = get_object_or_404(queryset, pk=pk)
            serializer = BranchSerializer(branch, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": "success"}
                return Response(status=status.HTTP_200_OK, data= context)
            else:
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
        else:
            message = "Branch not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)


    def partial_update(self, request, pk=None):
        if not request.user.user_organisation_role.is_admin:
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if Branch.objects.filter(id=pk).exists():
            queryset = Branch.objects.all()
            branch = get_object_or_404(queryset, pk=pk)
            serializer = BranchSerializer(branch, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": "success"}
                return Response(status=status.HTTP_200_OK, data= context)
            else:
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
        else:
            message = "Branch not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

    def destroy(self, request, pk=None):
        if not request.user.user_organisation_role.is_admin:
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if Branch.objects.filter(id=pk).exists():
            queryset = Branch.objects.all()
            branch = get_object_or_404(queryset, pk=pk)
            branch.delete()
            context = {"data":None, "status_flag":True, "status":status.HTTP_200_OK, "message": "successfully deleted"}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "Branch not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)


@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CourseMETAViewSet(ViewSet):

    def list(self, request):
        queryset = CourseMETA.objects.all()
        serializer = CourseMETASerializer(queryset, many=True)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

    def create(self, request):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        serializer = CourseMETASerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {"data":None, "status_flag":True, "status":status.HTTP_201_CREATED, "message": "success"}
            return Response(status=status.HTTP_201_CREATED, data= context)
        else:
            context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
            return Response(status=status.HTTP_400_BAD_REQUEST, data= context)

    def retrieve(self, request, pk=None):
        if CourseMETA.objects.filter(id=pk).exists():
            queryset =CourseMETA.objects.all()
            course_meta = get_object_or_404(queryset, pk=pk)
            serializer = CourseMETASerializer(course_meta)
            context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "CourseMETA not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

    def update(self, request, pk=None):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if CourseMETA.objects.filter(id=pk).exists():
            queryset = CourseMETA.objects.all()
            course_meta = get_object_or_404(queryset, pk=pk)
            serializer = CourseMETASerializer(course_meta, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": "success"}
                return Response(status=status.HTTP_200_OK, data= context)
            else:
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
        else:
            message = "CourseMETA not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)


    def partial_update(self, request, pk=None):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if CourseMETA.objects.filter(id=pk).exists():
            queryset = CourseMETA.objects.all()
            course_meta = get_object_or_404(queryset, pk=pk)
            serializer = CourseMETASerializer(course_meta, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": "success"}
                return Response(status=status.HTTP_200_OK, data= context)
            else:
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
        else:
            message = "CourseMETA not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

    def destroy(self, request, pk=None):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if CourseMETA.objects.filter(id=pk).exists():
            queryset = CourseMETA.objects.all()
            course_meta = get_object_or_404(queryset, pk=pk)
            course_meta.delete()
            context = {"data":None, "status_flag":True, "status":status.HTTP_200_OK, "message": "successfully deleted"}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "CourseMETA not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CourseViewSet(ViewSet):

    def list(self, request):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

    def create(self, request):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {"data":None, "status_flag":True, "status":status.HTTP_201_CREATED, "message": "success"}
            return Response(status=status.HTTP_201_CREATED, data= context)
        else:
            context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
            return Response(status=status.HTTP_400_BAD_REQUEST, data= context)

    def retrieve(self, request, pk=None):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if Course.objects.filter(id=pk).exists():
            queryset = Course.objects.all()
            course = get_object_or_404(queryset, pk=pk)
            serializer = CourseViewSerializer(course)
            context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "Course not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

    def destroy(self, request, pk=None):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if Course.objects.filter(id=pk).exists():
            queryset = Course.objects.all()
            course = get_object_or_404(queryset, pk=pk)
            course.delete()
            context = {"data":None, "status_flag":True, "status":status.HTTP_200_OK, "message": "successfully deleted"}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "Course not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CourseEnrollmentViewSet(ViewSet):

    def list(self, request):
        if request.user.user_organisation_role.is_student:
            queryset = CourseEnrollment.objects.filter(student__meta__id=request.user.id, course__is_active=True)
        elif request.user.user_organisation_role.is_faculty:
            queryset = CourseEnrollment.objects.filter(course__faculty__meta__id=request.user.id, course__is_active=True)
        else:
            queryset = CourseEnrollment.objects.all(course__is_active=True)
        serializer = CourseEnrollmentSerializer(queryset, many=True)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RequestViewSet(ViewSet):
    
    def list(self, request):
        if not (request.user.user_organisation_role.is_student or request.user.user_organisation_role.is_faculty):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Student and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)

        if request.user.user_organisation_role.is_student:
            student_ins = Student.objects.get(meta__id=request.user.id)
            queryset = Request.objects.filter(student__meta__id=student_ins.meta.id)
        elif request.user.user_organisation_role.is_faculty:
            faculty_ins = Faculty.objects.get(meta__id=request.user.id)
            queryset = Request.objects.filter(course__faculty__meta__id=faculty_ins.meta.id)
        else:
            queryset = Request.objects.all()
        serializer = RequestSerializer(queryset, many=True)
        print(serializer.data)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

    def create(self, request):
        if not request.user.user_organisation_role.is_student:
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Student users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)

        request_data = request.data.copy()
        student_ins = Student.objects.get(meta__id=request.user.id)
        course_ins = Course.objects.get(id=request_data["course_id"])
        request_type = [each[0] for each in REQUEST_CHOICES if each[0] == request_data["type"]]
        if not request_type:
            message = "Request type is not a valid choice"
            context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":message}
            return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
        request_ins = Request.objects.create(student=student_ins, course=course_ins, _type=request_type[0])
        if "input_file" in request_data.keys():
            request_ins.input_file = request_data["input_file"]
        request_ins.save()
        
        context = {"data":None, "status_flag":True, "status":status.HTTP_201_CREATED, "message": "success"}
        return Response(status=status.HTTP_201_CREATED, data= context)


    def partial_update(self, request, pk=None):
        if not request.user.user_organisation_role.is_faculty:
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)

        if Request.objects.filter(id=pk).exists():
            queryset = Request.objects.all()
            request_ins = get_object_or_404(queryset, pk=pk)
        else:
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":"Request id not found"}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

        request_data = request.data.copy()
        student_ins = Student.objects.get(id=request_ins.student.id)
        course_ins = Course.objects.get(id=request_ins.course.id)
           
        if request_ins.type == "ENROLLMENT":
            if not ("is_faculty_approved" in request_data.keys() and "is_rejected" in request_data.keys()):
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":"Course Approval and Rejection status is required"}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
            
            if request_data["is_faculty_approved"]:
                enrollment_ins = CourseEnrollment.objects.create(student=student_ins, course=course_ins)
                enrollment_ins.save()

                course_ins.students.add(student_ins.id)
                course_ins.save()

                request_ins.is_faculty_approved = True
                request_ins.save()
                message = f"{course_ins.name} - Enrolled Successfully."

            else:
                if CourseEnrollment.objects.filter(student=student_ins, course=course_ins).exists():
                    enrollment_ins = CourseEnrollment.objects.get(student=student_ins, course=course_ins)
                    enrollment_ins.delete()
                
                    course_ins.students.remove(student_ins.id)
                    course_ins.save()
                    message = f"You are removed from {course_ins.name}."
                else:
                    message = f"Your Enrollment request was rejected for {course_ins.name}."

                request_ins.is_faculty_approved = False
                request_ins.is_rejected = True
                request_ins.save()

            user_ins = User.objects.get(id=student_ins.meta.id)
            notify_ins = Notification.objects.create(user=user_ins, notify_for="STUDENT", notify_type="COURSE", message=message)
            notify_ins.save()

        queryset = Request.objects.filter(course__faculty__meta__id=request.user.id)
        serializer = RequestSerializer(queryset, many=True)

        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AttendanceViewSet(ViewSet):

    def list(self, request):
        if request.user.user_organisation_role.is_student:
            queryset = Attendance.objects.filter(student__meta__id=request.user.id,  lecture__course__is_active=True)
        elif request.user.user_organisation_role.is_faculty:
            queryset = Attendance.objects.filter(lecture__course__faculty__meta__id=request.user.id, lecture__course__is_active=True)
        else:
            queryset = Attendance.objects.all(lecture__course__is_active=True)
        serializer = AttendanceSerializer(queryset, many=True)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

    def create(self, request):
        try:
            if not request.user.user_organisation_role.is_faculty:
                context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Faculty users are allowed"}
                return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)

            request_data = request.data.copy()
            if not "course" in request_data.keys():
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":"Course id is required"}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)

            if Lecture.objects.all().count():
                latest_ins =  Lecture.objects.latest("created_at")
                if latest_ins.created_at.strftime("%Y-%m-%d") ==  timezone.now().strftime("%Y-%m-%d"):
                    message = "Attendance can be taken only once in a day"
                    context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":message}
                    return Response(status=status.HTTP_400_BAD_REQUEST, data= context)

            if not Course.objects.filter(id=request_data["course"], is_active=True).exists():
                context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":"Course not found"}
                return Response(status=status.HTTP_404_NOT_FOUND, data= context)
            
            with transaction.atomic():
                course_ins = Course.objects.get(id=request_data["course"])
                lecture_ins = Lecture.objects.create(course=course_ins, hours=request_data["hours"])
                lecture_ins.save()

                for student_ins in course_ins.students.all():
                    is_present = request_data["students"][student_ins.meta.register_no]
                    attendance_ins = Attendance.objects.create(student=student_ins, lecture=lecture_ins, is_present=is_present)
                    attendance_ins.save()

                    if is_present:
                        user_ins = User.objects.get(id=student_ins.meta.id)
                        notify_ins = Notification.objects.create(user=user_ins, notify_for="STUDENT", notify_type="COURSE", message=f"{course_ins.code} - Attendance Posted Successfully.")
                        notify_ins.save()

            context = {"data":None, "status_flag":True, "status":status.HTTP_200_OK, "message": "Attendance marked successfully"}
            return Response(status=status.HTTP_200_OK, data= context)
        except Exception as excepted_message:
            context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":str(excepted_message)}
            return Response(status=status.HTTP_400_BAD_REQUEST, data= context)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class AssignmentViewSet(ViewSet):

    def list(self, request):
        if request.user.user_organisation_role.is_student:
            queryset = Assignment.objects.filter(student__meta__id=request.user.id, course__is_active=True)
        elif request.user.user_organisation_role.is_faculty:
            queryset = Assignment.objects.filter(course__faculty__meta__id=request.user.id, course__is_active=True)
        else:
            queryset = Assignment.objects.all(course__is_active=True)
        serializer = AssignmentViewSerializer(queryset, many=True)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

    def create(self, request):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # We can add email notification feature  here to notify all the students in the course
            context = {"data":None, "status_flag":True, "status":status.HTTP_201_CREATED, "message": "Assignment created successfully"}
            return Response(status=status.HTTP_201_CREATED, data= context)
        else:
            context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
            return Response(status=status.HTTP_400_BAD_REQUEST, data= context)


    def update(self, request, pk=None):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if Assignment.objects.filter(id=pk).exists():
            queryset = Assignment.objects.all()
            assignment_ins = get_object_or_404(queryset, pk=pk)
            serializer = AssignmentSerializer(assignment_ins, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": "success"}
                return Response(status=status.HTTP_200_OK, data= context)
            else:
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
        else:
            message = "Assignment not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

    def partial_update(self, request, pk=None):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if Assignment.objects.filter(id=pk).exists():
            queryset = Assignment.objects.all()
            assigment_ins = get_object_or_404(queryset, pk=pk)
            serializer = AssignmentSerializer(assignment_ins, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": "success"}
                return Response(status=status.HTTP_200_OK, data= context)
            else:
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
        else:
            message = "Assignment not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)
    
    def retrieve(self, request, pk=None):
        if Assignment.objects.filter(id=pk).exists():
            queryset = Assignment.objects.all()
            assignment_ins = get_object_or_404(queryset, pk=pk)
            serializer = AssignmentSerializer(assignment_ins)
            context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "Assignment not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

    def destroy(self, request, pk=None):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if Assignment.objects.filter(id=pk).exists():
            queryset = Assignment.objects.all()
            assignment_ins = get_object_or_404(queryset, pk=pk)
            assignment_ins.delete()
            context = {"data":None, "status_flag":True, "status":status.HTTP_200_OK, "message": "successfully deleted"}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "Assignment not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SubmittedAssignmentsViewSet(ViewSet):

    def list(self, request):
        if request.user.user_organisation_role.is_student:
            queryset = SubmittedAssignments.objects.filter(student__meta__id=request.user.id, assignment__course__is_active=True)
        elif request.user.user_organisation_role.is_faculty:
            queryset = SubmittedAssignments.objects.filter(assignment__course__faculty__meta__id=request.user.id, assignment__course__is_active=True)
        else:
            queryset = SubmittedAssignments.objects.all(assignment__course__is_active=True)
        serializer = SubmittedAssignmentsViewSerializer(queryset, many=True)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

    def create(self, request):
        if (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Student users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        serializer = SubmittedAssignmentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {"data":None, "status_flag":True, "status":status.HTTP_201_CREATED, "message": "Assignment submitted successfully"}
            return Response(status=status.HTTP_201_CREATED, data= context)
        else:
            context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
            return Response(status=status.HTTP_400_BAD_REQUEST, data= context)

    def update(self, request, pk=None):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if SubmittedAssignments.objects.filter(id=pk).exists():
            queryset = SubmittedAssignments.objects.all()
            assignment_ins = get_object_or_404(queryset, pk=pk)
            serializer = SubmittedAssignmentsSerializer(assignment_ins, data=request.data)
            if serializer.is_valid():
                serializer.save()
                context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": "success"}
                return Response(status=status.HTTP_200_OK, data= context)
            else:
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
        else:
            message = "Assignment not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

    def partial_update(self, request, pk=None):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if SubmittedAssignments.objects.filter(id=pk).exists():
            queryset = SubmittedAssignments.objects.all()
            assignment_ins = get_object_or_404(queryset, pk=pk)
            serializer = SubmittedAssignmentsSerializer(assignment_ins, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": "success"}
                return Response(status=status.HTTP_200_OK, data= context)
            else:
                context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":serializer.errors}
                return Response(status=status.HTTP_400_BAD_REQUEST, data= context)
        else:
            message = "Assignment not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)
    
    def retrieve(self, request, pk=None):
        if SubmittedAssignments.objects.filter(id=pk).exists():
            queryset = SubmittedAssignments.objects.all()
            assignment_ins = get_object_or_404(queryset, pk=pk)
            serializer = SubmittedAssignmentsViewSerializer(assignment_ins)
            context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "Assignment not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

    def destroy(self, request, pk=None):
        if (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Student users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        
        if SubmittedAssignments.objects.filter(id=pk).exists():
            queryset = SubmittedAssignments.objects.all()
            assignment_ins = get_object_or_404(queryset, pk=pk)
            assignment_ins.delete()
            context = {"data":None, "status_flag":True, "status":status.HTTP_200_OK, "message": "successfully deleted"}
            return Response(status=status.HTTP_200_OK, data= context)
        else:
            message = "Assignment not found"
            context = {"data":None, "status_flag":False, "status":status.HTTP_404_NOT_FOUND, "message":message}
            return Response(status=status.HTTP_404_NOT_FOUND, data= context)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ExaminationViewSet(ViewSet):

    def list(self, request):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)
        if request.user.user_organisation_role.is_faculty:
            queryset = Examination.objects.filter(course__faculty__meta__id=request.user.id, course__is_active=True)
        else:
            queryset = Examination.objects.all(course__is_active=True)
        serializer = ExaminationSerializer(queryset, many=True)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ExaminationResultsViewSet(ViewSet):

    def list(self, request):
        if request.user.user_organisation_role.is_student:
            queryset = ExaminationResults.objects.filter(student__meta__id=request.user.id, examination__course__is_active=True)
        elif request.user.user_organisation_role.is_faculty:
            queryset = ExaminationResults.objects.filter(examination__course__faculty__meta__id=request.user.id, examination__course__is_active=True)
        else:
            queryset = ExaminationResults.objects.all(examination__course__is_active=True)
        serializer = ExaminationResultsSerializer(queryset, many=True)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

    def create(self, request):
        if not (request.user.user_organisation_role.is_faculty or request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin and Faculty users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)

        request_data = request.data.copy()
        if not "course_id" in request_data.keys():
            context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":"Course id is required"}
            return Response(status=status.HTTP_400_BAD_REQUEST, data= context)

        with transaction.atomic():
            course_ins = Course.objects.get(id=request_data["course_id"])
            examination_meta = Examination.objects.create(name=request_data["name"], course=course_ins, max_marks=request_data["max_marks"], conducted_on=request_data["conducted_on"])
            examination_meta.save()

            for index, each_student in enumerate(request_data["students"]):
                student_ins = Student.objects.get(id=each_student["id"])
                examination_ins = ExaminationResults.objects.create(student=student_ins, examination=examination_meta, is_present=each_student["is_present"], marks=each_student["marks"])
                examination_ins.save()

        context = {"data":None, "status_flag":True, "status":status.HTTP_200_OK, "message": "Attendance marked successfully"}
        return Response(status=status.HTTP_200_OK, data= context)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ResultViewSet(ViewSet):

    def list(self, request):
        if request.user.user_organisation_role.is_student:
            queryset = Result.objects.filter(student__meta__id=request.user.id)
        else:
            queryset = Result.objects.all()
        serializer = ResultSerializer(queryset, many=True)
        context = {"data":serializer.data, "status_flag":True, "status":status.HTTP_200_OK, "message": None}
        return Response(status=status.HTTP_200_OK, data= context)

    def create(self, request):
        if not (request.user.user_organisation_role.is_admin):
            context = {"data":None, "status_flag":False, "status": status.HTTP_401_UNAUTHORIZED, "message":"Only Admin users are allowed"}
            return Response(status= status.HTTP_401_UNAUTHORIZED, data= context)

        request_data = request.data.copy()
        if not "course_id" in request_data.keys():
            context = {"data":None, "status_flag":False, "status":status.HTTP_400_BAD_REQUEST, "message":"Course id is required"}
            return Response(status=status.HTTP_400_BAD_REQUEST, data= context)

        with transaction.atomic():
            course_ins = Course.objects.get(id=request_data["course_id"])
            course_meta = CourseMETA.objects.get(id=course_ins.category.id)

            for index, each_student in enumerate(request_data["students"]):
                student_ins = Student.objects.get(id=each_student["id"])
                result_ins = Result.objects.create(name=request_data["name"], student=student_ins, course=course_meta, max_marks=request_data["max_marks"], marks=each_student["marks"],\
                           status=request_data["status"] , grade=request_data["grade"], month_year_of_passing=request_data["month_year_of_passing"]) 
                result_ins.save()

        context = {"data":None, "status_flag":True, "status":status.HTTP_200_OK, "message": "Attendance marked successfully"}
        return Response(status=status.HTTP_200_OK, data= context)