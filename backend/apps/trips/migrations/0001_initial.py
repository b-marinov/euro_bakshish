# Generated migration file for trips app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_location_name', models.CharField(max_length=255)),
                ('start_latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('start_longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('end_location_name', models.CharField(max_length=255)),
                ('end_latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('end_longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('distance_km', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('estimated_duration_minutes', models.IntegerField(blank=True, null=True)),
                ('fare', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('requested_at', models.DateTimeField(auto_now_add=True)),
                ('accepted_at', models.DateTimeField(blank=True, null=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('cancelled_at', models.DateTimeField(blank=True, null=True)),
                ('passenger_notes', models.TextField(blank=True)),
                ('driver_notes', models.TextField(blank=True)),
                ('number_of_passengers', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trips_as_passenger', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trips_as_driver', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['passenger', '-created_at'], name='apps_trips_trip_passenger_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['driver', '-created_at'], name='apps_trips_trip_driver_idx'),
        ),
        migrations.AddIndex(
            model_name='trip',
            index=models.Index(fields=['status'], name='apps_trips_trip_status_idx'),
        ),
    ]
