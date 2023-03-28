# Generated by Django 4.1.2 on 2022-10-22 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship_task_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='form',
            name='creation_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.CreateModel(
            name='Responses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.JSONField()),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internship_task_app.form')),
            ],
        ),
    ]
