# Generated by Django 2.1 on 2018-09-08 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0001_initial'),
        ('accounts', '0005_default_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='batch',
            field=models.ManyToManyField(null=True, related_name='students', to='batch.BatchModel'),
        ),
        migrations.AlterField(
            model_name='student',
            name='last_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.IntegerField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)], help_text='Year which you joined the college.', null=True, verbose_name='Year'),
        ),
    ]
