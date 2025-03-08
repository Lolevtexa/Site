# Generated by Django 5.1.7 on 2025-03-08 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='theme_preference',
            field=models.CharField(choices=[('system', 'System'), ('light', 'Light'), ('dark', 'Dark')], default='system', max_length=10),
        ),
    ]
