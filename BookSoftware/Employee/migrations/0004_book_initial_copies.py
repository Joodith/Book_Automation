# Generated by Django 3.1.7 on 2021-04-08 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0003_auto_20210402_1125'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='initial_copies',
            field=models.IntegerField(default=10),
        ),
    ]