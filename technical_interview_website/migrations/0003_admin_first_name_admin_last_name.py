# Generated by Django 4.0.6 on 2022-07-25 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0002_remove_admin_firt_name_remove_admin_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='first_Name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='admin',
            name='last_Name',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
