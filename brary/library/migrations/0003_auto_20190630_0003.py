# Generated by Django 2.2.1 on 2019-06-30 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_book_book_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_descr',
            field=models.CharField(max_length=2000),
        ),
    ]
