# Generated by Django 2.1 on 2018-09-08 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20180908_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='batch',
            field=models.ManyToManyField(related_name='students', to='batch.BatchModel'),
        ),
    ]
