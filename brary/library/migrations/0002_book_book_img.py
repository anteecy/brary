# Generated by Django 2.2.1 on 2019-06-29 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_img',
            field=models.CharField(default='', max_length=500),
        ),
    ]
