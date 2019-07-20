# Generated by Django 2.2.1 on 2019-07-20 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0006_book_book_requested'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_count',
        ),
        migrations.RemoveField(
            model_name='book',
            name='book_requested',
        ),
        migrations.RemoveField(
            model_name='book',
            name='books_checked_out',
        ),
        migrations.AddField(
            model_name='book',
            name='book_available',
            field=models.BooleanField(default=True),
        ),
    ]
