# Generated by Django 4.2.3 on 2023-08-11 07:21

import academics.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(editable=False, max_length=255, unique=True)),
                ('semester', models.CharField(choices=[('1-1', '1-1'), ('1-2', '1-2'), ('2-1', '2-1'), ('2-2', '2-2'), ('3-1', '3-1'), ('3-2', '3-2'), ('4-1', '4-1'), ('4-2', '4-2'), ('5-1', '5-1'), ('5-2', '5-2')], max_length=100)),
                ('academic_year', models.DateTimeField()),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_completed', models.BooleanField(default=False)),
                ('is_result_published', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Course',
            },
        ),
        migrations.CreateModel(
            name='Examination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('MID-1', 'MID-1'), ('MID-2', 'MID-2'), ('LAB', 'LAB'), ('IA', 'IA'), ('PROJECT', 'PROJECT'), ('SEMESTER', 'SEMESTER')], max_length=255)),
                ('max_marks', models.IntegerField(default=100)),
                ('conducted_on', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.course')),
            ],
            options={
                'verbose_name': 'Examination',
                'unique_together': {('name', 'course')},
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_type', models.CharField(choices=[('ENROLLMENT', 'ENROLLMENT'), ('OD', 'OD'), ('HALLTICKET', 'HALLTICKET')], max_length=255)),
                ('message', models.TextField(blank=True, null=True)),
                ('input_file', models.FileField(blank=True, null=True, upload_to=academics.models.get_request_file_path)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('is_faculty_approved', models.BooleanField(default=False)),
                ('is_mentor_approved', models.BooleanField(default=False)),
                ('is_hod_approved', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'verbose_name': 'Request',
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, related_name='published_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Publication',
            },
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hours', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)], default=1, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='academics.course')),
            ],
            options={
                'verbose_name': 'Lecutre',
            },
        ),
        migrations.CreateModel(
            name='Disciplinary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue', models.TextField()),
                ('complaint', models.TextField()),
                ('submitted_file', models.FileField(blank=True, null=True, upload_to=academics.models.get_disciplinary_filepath)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('raised_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, related_name='issue_raised_by', to='users.faculty')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='issue_raised_on', to='users.student')),
            ],
            options={
                'verbose_name': 'Disciplinary Action',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('hod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='head', to='users.faculty')),
            ],
            options={
                'verbose_name': 'Department',
            },
        ),
        migrations.CreateModel(
            name='CourseMETA',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=255, unique=True)),
                ('_type', models.CharField(choices=[('PROGRAM CORE', 'PROGRAM CORE'), ('PROGRAM ELECTIVE', 'PROGRAM ELECTIVE'), ('UNIVERSITY CORE', 'UNIVERSITY CORE'), ('UNIVERSITY ELECTIVE', 'UNIVERSITY ELECTIVE'), ('SOC', 'SOC'), ('NPTEL', 'NPTEL'), ('MINI-PROJECT-1', 'MINI-PROJECT-1'), ('MINI-PROJECT-2', 'MINI-PROJECT-2'), ('MINI-PROJECT-3', 'MINI-PROJECT-3'), ('MAJOR-PROJECT', 'MAJOR-PROJECT'), ('INDUSTRIAL INTERNSHIP', 'INDUSTRIAL INTERNSHIP'), ('INTERNSHIP', 'INTERNSHIP')], max_length=255)),
                ('_credits', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (12, 12)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, related_name='meta_created_by', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academics.department')),
            ],
            options={
                'verbose_name': 'Course META',
                'unique_together': {('name', 'code')},
            },
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='academics.coursemeta'),
        ),
        migrations.AddField(
            model_name='course',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='users.faculty'),
        ),
        migrations.AddField(
            model_name='course',
            name='students',
            field=models.ManyToManyField(related_name='enrolled', to='users.student'),
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=555)),
                ('message', models.TextField(blank=True, null=True)),
                ('input_file', models.FileField(blank=True, null=True, upload_to=academics.models.get_file_path)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('max_marks', models.IntegerField(default=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.course')),
            ],
            options={
                'verbose_name': 'Assignment',
                'unique_together': {('name', 'course')},
            },
        ),
        migrations.CreateModel(
            name='SubmittedAssignments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, null=True)),
                ('input_file', models.FileField(blank=True, null=True, upload_to=academics.models.get_student_assignment_file_path)),
                ('marks', models.IntegerField(default=0)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.assignment')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'verbose_name': 'Submitted Assignment',
                'unique_together': {('student', 'assignment')},
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(editable=False, max_length=555)),
                ('max_marks', models.IntegerField(default=100, editable=False)),
                ('marks', models.IntegerField(default=0, editable=False)),
                ('status', models.CharField(choices=[('PASS', 'PASS'), ('FAIL', 'FAIL'), ('ABSENT', 'ABSENT'), ('RA', 'RA')], editable=False, max_length=255)),
                ('grade', models.IntegerField(choices=[(10, 'O'), (9, 'A'), (8, 'B'), (7, 'C'), (6, 'D'), (5, 'E'), (0, 'F')], editable=False)),
                ('month_year_of_passing', models.DateTimeField(editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, to='academics.coursemeta')),
                ('course', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, to='academics.course')),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, related_name='declared_by', to=settings.AUTH_USER_MODEL)),
                ('student', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, to='users.student')),
            ],
            options={
                'verbose_name': 'Result',
                'unique_together': {('student', 'course')},
            },
        ),
        migrations.CreateModel(
            name='ExaminationResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.IntegerField(default=0)),
                ('is_present', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('examination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academics.examination')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'verbose_name': 'Examination Result',
                'unique_together': {('student', 'examination')},
            },
        ),
        migrations.CreateModel(
            name='CourseEnrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hallticket', models.FileField(blank=True, null=True, upload_to=academics.models.get_hallticket_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='academics.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='users.student')),
            ],
            options={
                'verbose_name': 'Course Enrollment',
                'unique_together': {('student', 'course')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('code', 'category')},
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academics.department')),
            ],
            options={
                'verbose_name': 'Branch',
                'unique_together': {('name', 'department')},
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_present', models.BooleanField(default=True, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('lecture', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='academics.lecture')),
                ('student', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='users.student')),
            ],
            options={
                'verbose_name': 'Attendance',
                'unique_together': {('student', 'lecture')},
            },
        ),
    ]