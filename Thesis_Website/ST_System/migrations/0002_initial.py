# Generated by Django 3.2.7 on 2021-12-04 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ST_System', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='agent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tickets',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ST_System.categories'),
        ),
        migrations.AddField(
            model_name='tickets',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tickets',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ST_System.departments'),
        ),
        migrations.AddField(
            model_name='tickets',
            name='priority',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ST_System.priorities'),
        ),
        migrations.AddField(
            model_name='tickets',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ST_System.ticket_statuses'),
        ),
        migrations.AddField(
            model_name='tickets',
            name='sub_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ST_System.sub_categories'),
        ),
        migrations.AddField(
            model_name='sub_categories',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ST_System.categories'),
        ),
        migrations.AddField(
            model_name='sub_categories',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ST_System.departments'),
        ),
        migrations.AddField(
            model_name='replies',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='replies',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ST_System.tickets'),
        ),
        migrations.AddField(
            model_name='categories',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ST_System.departments'),
        ),
        migrations.AddField(
            model_name='accepted_tickets',
            name='agent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='accepted_tickets',
            name='ticket',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ST_System.tickets'),
        ),
    ]