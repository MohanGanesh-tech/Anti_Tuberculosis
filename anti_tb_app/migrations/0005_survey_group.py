# Generated by Django 3.2 on 2021-04-10 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anti_tb_app', '0004_auto_20210410_1759'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='group',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
