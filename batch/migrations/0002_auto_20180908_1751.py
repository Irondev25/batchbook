# Generated by Django 2.1 on 2018-09-08 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchmodel',
            name='department',
            field=models.CharField(choices=[('ISE', 'Information Science Engg.'), ('CSE', 'Computer Science Engg.')], max_length=3),
        ),
    ]