# Generated by Django 4.1.6 on 2023-02-13 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_post_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comBody',
            new_name='comment',
        ),
    ]
