# Generated by Django 2.0.6 on 2018-07-30 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='访问地址'),
        ),
    ]
