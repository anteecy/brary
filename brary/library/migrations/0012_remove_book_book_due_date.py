# Generated by Django 2.2.1 on 2019-07-26 23:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_auto_20190726_2338'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='book_due_date',
        ),
    ]