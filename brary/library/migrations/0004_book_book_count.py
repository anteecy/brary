# Generated by Django 2.2.1 on 2019-07-04 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_auto_20190630_0003'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_count',
            field=models.SmallIntegerField(default=0),
        ),
    ]
