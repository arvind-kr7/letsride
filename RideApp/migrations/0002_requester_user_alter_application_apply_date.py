# Generated by Django 4.1.3 on 2022-11-26 01:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('RideApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requester',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='application',
            name='apply_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
