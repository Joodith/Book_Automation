# Generated by Django 3.1.7 on 2021-04-05 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userproduct',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]