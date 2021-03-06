# Generated by Django 3.2.9 on 2021-11-19 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reservation_code', models.CharField(max_length=200)),
                ('check_in', models.DateField()),
                ('check_out', models.DateField()),
                ('days', models.IntegerField(default=0)),
                ('adult', models.IntegerField(default=0)),
                ('children', models.IntegerField(default=0)),
                ('deleted_at', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'reservations',
            },
        ),
    ]
