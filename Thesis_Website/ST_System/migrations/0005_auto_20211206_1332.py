# Generated by Django 3.2.7 on 2021-12-06 05:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ST_System', '0004_alter_ticket_statuses_ticket_status_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='accepted_tickets',
            name='invited_agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invited_agent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accepted_tickets',
            name='agent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actual_agent', to=settings.AUTH_USER_MODEL),
        ),
    ]