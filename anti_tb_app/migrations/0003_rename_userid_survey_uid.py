# Generated by Django 3.2 on 2021-04-10 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anti_tb_app', '0002_survey'),
    ]

    operations = [
        migrations.RenameField(
            model_name='survey',
            old_name='userid',
            new_name='uid',
        ),
    ]
