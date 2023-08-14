from django.db import models
from django.db.models import Sum
from crum import get_current_user
# Create your models here.

from users.models import User, Student, Faculty

SEMESTER_CHOICES = [("1-1", "1-1"), ("1-2", "1-2"), ("2-1", "2-1"), ("2-2", "2-2"), ("3-1", "3-1"), ("3-2", "3-2"), ("4-1","4-1"), ("4-2", "4-2"), ("5-1","5-1"), ("5-2", "5-2")]
EXAMINATION_CHOICES = [("MID-1", "MID-1"), ("MID-2", "MID-2"), ("LAB", "LAB"), ("IA", "IA"), ("PROJECT", "PROJECT"), ("SEMESTER", "SEMESTER")]
RESULT_CHOICES = [("PASS", "PASS"), ("FAIL", "FAIL"), ("ABSENT", "ABSENT"), ("RA", "RA")]
GRADE_CHOICES = [(10, "O"), (9, "A"), (8, "B"), (7, "C"), (6, "D"), (5, "E"), (0, "F")]
COURSE_TYPE_CHOICES = [("PROGRAM CORE", "PROGRAM CORE"), ("PROGRAM ELECTIVE", "PROGRAM ELECTIVE"), ("UNIVERSITY CORE", "UNIVERSITY CORE"), ("UNIVERSITY ELECTIVE", "UNIVERSITY ELECTIVE"), ("SOC", "SOC"), ("NPTEL", "NPTEL"), ("MINI-PROJECT-1", "MINI-PROJECT-1"), ("MINI-PROJECT-2", "MINI-PROJECT-2"),  ("MINI-PROJECT-3", "MINI-PROJECT-3"), ("MAJOR-PROJECT", "MAJOR-PROJECT"), ("INDUSTRIAL INTERNSHIP", "INDUSTRIAL INTERNSHIP"), ("INTERNSHIP", "INTERNSHIP")]
HOURS_CHOICES = [(1,1), (2,2), (3,3)]
CREDIT_CHOICES = [(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (12, 12)]
REQUEST_CHOICES = [("ENROLLMENT", "ENROLLMENT"), ("OD", "OD"), ("HALLTICKET", "HALLTICKET")]

class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    hod = models.ForeignKey("users.Faculty", on_delete=models.SET_NULL, blank=True, null=True, related_name="head")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.User', on_delete=models.RESTRICT, editable=False)

    class Meta:
        verbose_name = "Department"

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not user.user_organisation_role.is_admin:
            raise Exception("Only Admin users are allowed")
        
        self.created_by = user
        super(Department, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        user = get_current_user()
        if not user.user_organisation_role.is_admin:
            raise Exception("Only Admin users are allowed")
        super(Department, self).delete(*args, **kwargs)

class Branch(models.Model):
    name = models.CharField(max_length=255, unique=True)
    department = models.ForeignKey("academics.Department", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.User', on_delete=models.RESTRICT, editable=False)

    class Meta:
        verbose_name = "Branch"
        unique_together = ['name', 'department']

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not user.user_organisation_role.is_admin:
            raise Exception("Only Admin users are allowed")
        
        self.created_by = user
        super(Branch, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        user = get_current_user()
        if not user.user_organisation_role.is_admin:
            raise Exception("Only Admin users are allowed")
        super(Branch, self).delete(*args, **kwargs)

class CourseMETA(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code =  models.CharField(max_length=255, unique=True)
    _type = models.CharField(max_length=255, choices=COURSE_TYPE_CHOICES)
    department = models.ForeignKey("academics.Department", on_delete=models.SET_NULL, blank=True, null=True)
    _credits = models.IntegerField(choices=CREDIT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.User', on_delete=models.RESTRICT, editable=False, related_name="meta_created_by")

    class Meta:
        verbose_name = "Course META"
        unique_together = ['name', 'code']

    def __str__(self):
        return str(self.name)

    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value):
        self._type = value

    @property
    def credits(self):
        return self._credits
    
    @type.setter
    def credits(self, value):
        self._credits = value

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not user.user_organisation_role.is_faculty:
            raise Exception("Only Faculty users are allowed")
        self.created_by = user

        super(CourseMETA, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        user = get_current_user()
        if not user.user_organisation_role.is_admin:
            raise Exception("Only Admin users are allowed")
        super(CourseMETA, self).delete(*args, **kwargs)

class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True, editable=False)
    category = models.ForeignKey("academics.CourseMETA", on_delete=models.RESTRICT)
    faculty = models.ForeignKey("users.Faculty", on_delete=models.RESTRICT)
    students = models.ManyToManyField("users.Student", related_name="enrolled")
    semester =  models.CharField(max_length=100, choices=SEMESTER_CHOICES)
    academic_year = models.DateTimeField()
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    is_result_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Course"
        unique_together = ['code', 'category']

    def __str__(self):
        return str(self.code)

    @property
    def total_class(self):
        return Lecture.objects.filter(course__id=self.id).count()
    @property
    def total_hours(self):
        return Lecture.objects.filter(course__id=self.id).aggregate(Sum("hours"))["hours__sum"]

    def save(self, *args, **kwargs):
        user = get_current_user()
        faculty_ins = Faculty.objects.get(meta__id=self.faculty.meta.id)
        if not ((faculty_ins.meta.id == user.id) or user.user_organisation_role.is_admin):
            raise Exception("Only Admin and Course concerned faculty are allowed")

        if self._state.adding:
            prev_count = Course.objects.filter(category__code=self.category.code).count()
            self.code = f'{self.category.code}{prev_count + 1}' 

        super(Course, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user = get_current_user()
        if not (user.user_organisation_role.is_admin or user.id == self.faculty.meta.id):
            raise Exception("Only Admin and Course concerned faculty are allowed")
        super(Course, self).delete(*args, **kwargs)

def get_hallticket_path(instance, filename):
    return f'HallTickets/{instance.id}_{filename}'

class CourseEnrollment(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, related_name="students")
    course = models.ForeignKey("academics.Course", on_delete=models.CASCADE, related_name="enrollments")
    hallticket = models.FileField(blank=True, null=True, upload_to=get_hallticket_path)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Course Enrollment"
        unique_together = ['student', 'course']

    def __str__(self):
        return f'{self.course.code} - {self.course.name}'
    
    @property
    def attendance(self):
        total_class = Lecture.objects.filter(course__id=self.course.id).count()
        total_hours = Lecture.objects.filter(course__id=self.course.id).aggregate(Sum("hours"))["hours__sum"]
        class_attended = Attendance.objects.filter(lecture__course__id=self.course.id, is_present=True, student__id=self.student.id).count()
        attended_hours = Attendance.objects.filter(lecture__course__id=self.course.id, is_present=True, student__id=self.student.id).aggregate(Sum("lecture__hours"))["lecture__hours__sum"]
        total = round(float(attended_hours/total_hours),2) if total_class and attended_hours else 0
        return {"total_class":total_class, "total_hours":total_hours, "class_attended":class_attended, "attended_hours":attended_hours,"total":total*100 }

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.course.faculty.meta.id == user.id:
            raise Exception("Only Course Concerned Faculty is Allowed")
           
        super(CourseEnrollment, self).save(*args, **kwargs)

class Lecture(models.Model):
    course = models.ForeignKey("academics.Course", on_delete=models.CASCADE, related_name="courses", editable=False)
    hours = models.IntegerField(default=1, choices=HOURS_CHOICES, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Lecutre"

    def __str__(self):
        return f'Lecture for {self.course.code} - {self.course.name} on {self.created_at.strftime("%Y-%m-%d")}'

    def save(self, *args, **kwargs):
        user = get_current_user()
        faculty_ins = Faculty.objects.get(meta__id=self.course.faculty.meta.id)
        if not faculty_ins.meta.id == user.id:
            raise Exception("Only Course Concerned Faculty is Allowed")
        super(Lecture, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user = get_current_user()
        if not (user.user_organisation_role.is_admin or user.id == self.faculty.meta.id):
            raise Exception("Only Admin and Course concerned faculty are allowed")
        if self.course.is_active:
            raise Exception("Attendance for course that is active can not be deleted")
        super(Lecture, self).delete(*args, **kwargs)

class Attendance(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, editable=False)
    lecture = models.ForeignKey('academics.Lecture', on_delete=models.CASCADE, editable=False)
    is_present = models.BooleanField(default=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    
    class Meta:
        verbose_name = "Attendance"
        unique_together = ['student', 'lecture']

    def __str__(self):
        return f'Attendance for {self.student.meta.register_no} on {self.created_at.strftime("%Y-%m-%d")}'
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if not self.lecture.course.faculty.meta.id == user.id:
            raise Exception("Only Course Concerned Faculty is Allowed")
           
        super(Attendance, self).save(*args, **kwargs)

def get_file_path(instance, filename):

    return f'AssignmentFiles/{instance.course.faculty.meta.register_no}_{instance.course.code}_{instance.name}_{filename}'

class Assignment(models.Model):
    name = models.CharField(max_length=555)
    course = models.ForeignKey('academics.Course', on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    input_file = models.FileField(blank=True, null=True, upload_to=get_file_path)
    deadline = models.DateTimeField(blank=True, null=True)
    max_marks = models.IntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Assignment"
        unique_together = ['name', 'course']
    
    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        faculty_ins = Faculty.objects.get(meta__id = self.course.faculty.meta.id)
        if not faculty_ins.meta.id == user.id:
            raise Exception("Only Course Concerned Faculty is Allowed")
        
        super(Assignment, self).save(*args, **kwargs)

def get_student_assignment_file_path(instance, filename):
    return f'StudentAssignmentFiles/{instance.student.meta.register_no}_{instance.assignment.course.code}_{instance.assignment.name}_{filename}'

class SubmittedAssignments(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    assignment = models.ForeignKey("academics.Assignment", on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    input_file = models.FileField(blank=True, null=True, upload_to=get_student_assignment_file_path)
    marks = models.IntegerField(default=0)
    remarks = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Submitted Assignment"
        unique_together = ['student', 'assignment']
    
    def __str__(self):
        return str(self.assignment.name)
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        if self._state.adding:
            if not self.student.meta.id == user.id:
                raise Exception("One can not submit the Assignment on behalf of other one.")
            student_ins = Student.objects.get(meta__id=user.id)
            self.student = student_ins

        if self.marks > self.assignment.max_marks:
            raise Exception("Marks of the Assignment can not be greater than Max Marks")
        super(SubmittedAssignments, self).save(*args, **kwargs)

class Examination(models.Model):
    name = models.CharField(max_length=255, choices=EXAMINATION_CHOICES)
    course = models.ForeignKey("academics.Course", on_delete=models.CASCADE)
    max_marks = models.IntegerField(default=100)
    conducted_on = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Examination"
        unique_together = ['name', 'course']

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        user = get_current_user()
        faculty_ins = Faculty.objects.get(meta__id=self.faculty.meta.id)
        if not faculty_ins.meta.id == user.id:
            raise Exception("Only Course Concerned Faculty is Allowed")
        super(Examination, self).save(*args, **kwargs)

class ExaminationResults(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    examination = models.ForeignKey("academics.Examination", on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    is_present = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Examination Result"
        unique_together = ['student', 'examination']

    def __str__(self):
        return str(self.examination.name)

    def save(self, *args, **kwargs):
        user = get_current_user()
        faculty_ins = Faculty.objects.get(meta__id=self.examination.faculty.meta.id)
        if not faculty_ins.meta.id == user.id:
            raise Exception("Only Course Concerned Faculty is Allowed")

        if self.marks > self.examination.max_marks:
            raise Exception("Marks of the Examination can not be greater than Max Marks")

        super(ExaminationResults, self).save(*args, **kwargs)
   
class Result(models.Model):
    name = models.CharField(max_length=555, editable=False)
    student = models.ForeignKey("users.Student", on_delete=models.RESTRICT, editable=False)
    course = models.ForeignKey('academics.Course', on_delete=models.RESTRICT, editable=False)
    category = models.ForeignKey('academics.CourseMETA', on_delete=models.RESTRICT, editable=False)
    max_marks = models.IntegerField(default=100, editable=False)
    marks = models.IntegerField(default=0, editable=False)
    status = models.CharField(max_length=255, choices=RESULT_CHOICES, editable=False)
    grade = models.IntegerField(choices=GRADE_CHOICES, editable=False)
    month_year_of_passing = models.DateTimeField(editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    created_by = models.ForeignKey('users.User', on_delete=models.RESTRICT, related_name="declared_by", editable=False)

    class Meta:
        verbose_name = "Result"
        unique_together = ['student', 'course']

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        user = get_current_user()
        if not user.user_organisation_role.is_admin:
            raise Exception("Only Admin Users allowed")
        self.created_by = user
        super(Result, self).save(*args, **kwargs)

def get_request_file_path(instance, filename):

    return f'RequestFiles/{instance.id}_{instance.student.meta.register_no}_{filename}'

class Request(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE)
    course = models.ForeignKey("academics.Course", on_delete=models.CASCADE)
    _type = models.CharField(max_length=255, choices=REQUEST_CHOICES)
    message = models.TextField(blank=True, null=True)
    input_file = models.FileField(blank=True, null=True, upload_to=get_request_file_path)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_faculty_approved = models.BooleanField(default=False)
    is_mentor_approved = models.BooleanField(default=False)
    is_hod_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Request"

    def __str__(self):
        return str(self.student.meta.email)

    @property
    def type(self):
        return self._type
    
    @type.setter
    def type(self, value):
        self._type = value
    
    @property
    def is_accepted(self):
        if self.type == "ENROLLMENT" or self.type == "ASSIGNMENT":
            if self.is_faculty_approved:
                return True
            else:
                return False
        else:
            if self.is_faculty_approved and self.is_hod_approved and self.is_mentor_approved:
                return True
            else:
                False

    def save(self, *args, **kwargs):
        user = get_current_user()
        if self._state.adding:
            if not self.student.meta.id == user.id:
                raise Exception("One can not make the request on behalf of other one.")

        super(Request, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user = get_current_user()
        if not self.student.meta.id == user.id:
            raise Exception("Only Requested student can delete this request")
        super(Request, self).delete(*args, **kwargs)

class Publication(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('users.User', on_delete=models.RESTRICT, editable=False, related_name="published_by")
   
    class Meta:
        verbose_name ="Publication"

    def __str__(self):
        return str(self.name)
    
    def save(self, *args, **kwargs):
        user = get_current_user()
        self.created_by = user

        super(Publication, self).save(*args, **kwargs)

def get_disciplinary_filepath(instance, filename):
    return f'DisciplinaryFiles/{instance.id}_{filename}'

class Disciplinary(models.Model):
    student = models.ForeignKey("users.Student", on_delete=models.CASCADE, related_name="issue_raised_on")
    issue = models.TextField()
    complaint = models.TextField()
    submitted_file = models.FileField(blank=True, null=True, upload_to=get_disciplinary_filepath)
    created_at = models.DateTimeField(auto_now_add=True)
    raised_by = models.ForeignKey('users.Faculty', on_delete=models.RESTRICT, editable=False, related_name="issue_raised_by")

    class Meta:
        verbose_name ="Disciplinary Action"
        
    def __str__(self):
        return str(self.student.meta.email)