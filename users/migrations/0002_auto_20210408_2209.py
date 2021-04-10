# Generated by Django 2.2.12 on 2021-04-08 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='country',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='date_birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='facebook_link',
            field=models.URLField(null=True),
        ),
    ]
