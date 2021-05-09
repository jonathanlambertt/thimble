# Generated by Django 3.1.5 on 2021-05-08 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_auto_20210411_1948'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='groups.group'),
        ),
    ]
