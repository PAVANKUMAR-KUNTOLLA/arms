# Generated by Django 4.2.3 on 2023-08-11 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_faculty_department_notification_branch_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='branch',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='course',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='dept',
        ),
    ]
