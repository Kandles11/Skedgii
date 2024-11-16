# Generated by Django 5.1.3 on 2024-11-16 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='professor',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='professor',
            name='last_name',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
