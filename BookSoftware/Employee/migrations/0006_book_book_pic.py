# Generated by Django 3.1.7 on 2021-04-09 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0005_auto_20210409_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_pic',
            field=models.ImageField(default='book-genres.jpg', upload_to='book_pictures'),
        ),
    ]
