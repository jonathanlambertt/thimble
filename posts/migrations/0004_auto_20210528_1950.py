# Generated by Django 3.1.5 on 2021-05-28 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_linkpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkpost',
            name='link',
            field=models.URLField(max_length=500),
        ),
    ]
