# Generated by Django 4.2.3 on 2023-08-11 07:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.CharField(max_length=255, unique=True)),
                ('register_no', models.CharField(editable=False, max_length=255, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('mobile_no', models.IntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=users.models.get_image_path)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account_terminated', models.BooleanField(default=False, editable=False)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='created_by_user', to=settings.AUTH_USER_MODEL)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(choices=[('LAB TECHINICIAN', 'LAB TECHNICIAN'), ('ASSITANT PROFESSOR', 'ASSISTANT PROFESSOR'), ('ASSOCIATE PROFESSOR', 'ASSOCIATE PROFESSOR'), ('PROFESSOR', 'PROFESSOR'), ('HOD', 'HOD'), ('DEAN', 'DEAN'), ('VP', 'VP'), ('PRINCIPAL', 'PRINCIPAL')], max_length=255)),
                ('education', models.TextField(blank=True, null=True)),
                ('is_phd_holder', models.BooleanField(default=False)),
                ('experience', models.IntegerField(blank=True, null=True)),
                ('achievements', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, related_name='faculty_creator', to=settings.AUTH_USER_MODEL)),
                ('meta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserOrganisationRoleTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255, unique=True)),
                ('is_student', models.BooleanField(default=False)),
                ('is_faculty', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('program', models.CharField(choices=[('UG', 'UNDER GRADUATION'), ('PG', 'POST GRADUATION'), ('DIPLOMA', 'DIPLOMA')], max_length=255)),
                ('academic_year', models.DateTimeField()),
                ('education', models.TextField(blank=True, null=True)),
                ('achievements', models.TextField(blank=True, null=True)),
                ('father_name', models.CharField(blank=True, max_length=255, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=255, null=True)),
                ('parent_mobile_no', models.IntegerField(blank=True, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, related_name='student_creator', to=settings.AUTH_USER_MODEL)),
                ('mentor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.faculty')),
                ('meta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notify_for', models.CharField(choices=[('STUDENT', 'STUDENT'), ('FACULTY', 'FACULTY'), ('ALL', 'ALL')], max_length=255)),
                ('notify_type', models.CharField(choices=[('ATTENDANCE', 'ATTENDANCE'), ('COURSE', 'COURSE'), ('BRANCH', 'BRANCH'), ('DEPARTMENT', 'DEPARTMENT'), ('ALL', 'ALL')], max_length=100)),
                ('message', models.TextField()),
                ('input_file', models.FileField(blank=True, null=True, upload_to=users.models.get_file_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.RESTRICT, to='users.faculty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_organisation_role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.userorganisationroletable'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
