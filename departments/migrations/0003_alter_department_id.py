# Generated by Django 5.1.5 on 2025-01-19 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('departments', '0002_alter_department_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='id',
            field=models.IntegerField(editable=False, primary_key=True, serialize=False),
        ),
    ]
