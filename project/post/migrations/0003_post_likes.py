# Generated by Django 4.2.3 on 2023-07-19 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_comment_writer_alter_post_writer'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='likes',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]