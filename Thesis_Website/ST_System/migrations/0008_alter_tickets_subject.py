# Generated by Django 3.2.7 on 2021-12-14 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ST_System', '0007_alter_tickets_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='subject',
            field=models.CharField(max_length=200),
        ),
    ]
