# Generated by Django 4.1.2 on 2022-10-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coplate', '0007_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, to='coplate.profile'),
        ),
    ]
