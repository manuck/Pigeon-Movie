# Generated by Django 2.1.8 on 2019-05-15 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_myuser_favorite_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='username',
            field=models.CharField(max_length=255, unique=True, verbose_name='ID'),
        ),
    ]
