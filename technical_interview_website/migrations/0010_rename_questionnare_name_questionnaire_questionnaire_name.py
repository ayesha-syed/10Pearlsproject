# Generated by Django 4.0.6 on 2022-07-27 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0009_alter_interview_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='questionnaire',
            old_name='Questionnare_name',
            new_name='Questionnaire_name',
        ),
    ]
