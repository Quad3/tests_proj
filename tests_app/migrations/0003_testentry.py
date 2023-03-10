# Generated by Django 4.1.5 on 2023-01-25 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests_app', '0002_alter_theme_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('questions', models.ManyToManyField(to='tests_app.question')),
            ],
        ),
    ]
