# Generated by Django 3.1.7 on 2021-04-09 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Employee', '0007_auto_20210409_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_pic',
            field=models.ImageField(default='book_pictures/book-genres.jpg', upload_to='book_pictures/'),
        ),
    ]