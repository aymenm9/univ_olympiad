# Generated by Django 5.2 on 2025-05-07 10:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='Organization',
            field=models.CharField(choices=[('Hospital', 'Hospital'), ('DSP', 'DSP'), ('APC', 'APC'), ('Court', 'Court')], default='Hospital', max_length=50),
        ),
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('wilaya', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('dsp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='court', to='users.dsp')),
            ],
        ),
        migrations.AddField(
            model_name='userinfo',
            name='court',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='users.court'),
        ),
    ]
