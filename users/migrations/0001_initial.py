# Generated by Django 3.2.9 on 2021-11-19 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=45, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=45)),
                ('phone', models.CharField(max_length=17, null=True)),
                ('profile_image_url', models.CharField(max_length=1000, null=True)),
                ('social_id', models.CharField(max_length=2000, null=True)),
                ('social_type', models.CharField(max_length=100, null=True)),
                ('deleted_at', models.DateTimeField(null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]
