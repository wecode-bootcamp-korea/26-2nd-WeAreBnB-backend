# Generated by Django 3.2.9 on 2021-11-19 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image_url', models.CharField(max_length=1000, null=True)),
            ],
            options={
                'db_table': 'options',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('max_guest', models.IntegerField(default=0)),
                ('bedroom', models.IntegerField(default=0)),
                ('bed', models.IntegerField(default=0)),
                ('bath', models.IntegerField(default=0)),
                ('created_at', models.DateField()),
                ('host_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'rooms',
            },
        ),
        migrations.CreateModel(
            name='RoomLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=14, default=0.0, max_digits=16)),
                ('longitude', models.DecimalField(decimal_places=14, default=0.0, max_digits=17)),
            ],
            options={
                'db_table': 'room_locations',
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'room_types',
            },
        ),
        migrations.CreateModel(
            name='RoomOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.option')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.room')),
            ],
            options={
                'db_table': 'room_options',
            },
        ),
        migrations.CreateModel(
            name='RoomImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=1000, null=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_images', to='rooms.room')),
            ],
            options={
                'db_table': 'room_images',
            },
        ),
        migrations.AddField(
            model_name='room',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.roomlocation'),
        ),
        migrations.AddField(
            model_name='room',
            name='options',
            field=models.ManyToManyField(through='rooms.RoomOption', to='rooms.Option'),
        ),
        migrations.AddField(
            model_name='room',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.reservation'),
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rooms.roomtype'),
        ),
    ]
