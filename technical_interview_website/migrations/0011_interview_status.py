# Generated by Django 4.0.6 on 2022-07-31 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0010_rename_questionnare_name_questionnaire_questionnaire_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='Status',
            field=models.BooleanField(default=False),
        ),
    ]