# Generated by Django 4.1.6 on 2023-02-14 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_comment_downvote_comment_upvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='pubStatus',
            field=models.BooleanField(default=False),
        ),
    ]
