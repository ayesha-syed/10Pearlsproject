# Generated by Django 4.0.6 on 2022-08-14 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0013_alter_actualquestion_actual_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='interview_email',
            field=models.CharField(max_length=1000),
        ),
    ]
