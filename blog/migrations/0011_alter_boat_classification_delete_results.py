# Generated by Django 4.1.6 on 2023-04-20 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_remove_results_rankings_registration_ranking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boat',
            name='classification',
            field=models.CharField(max_length=2),
        ),
        migrations.DeleteModel(
            name='Results',
        ),
    ]