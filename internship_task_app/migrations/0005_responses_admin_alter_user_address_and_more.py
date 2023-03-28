# Generated by Django 4.1.2 on 2022-10-27 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internship_task_app', '0004_remove_responses_name_of_responder_responses_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='responses',
            name='admin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='internship_task_app.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=1000),
        ),
    ]
