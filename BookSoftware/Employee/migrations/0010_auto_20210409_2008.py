# Generated by Django 3.1.7 on 2021-04-09 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0009_auto_20210409_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]
