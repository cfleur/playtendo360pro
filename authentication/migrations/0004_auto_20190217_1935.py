# Generated by Django 2.0.3 on 2019-02-17 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20190216_0324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='avatar',
            field=models.ImageField(blank=True, default='static/default_avatar.png', upload_to='profile_avatar'),
        ),
    ]
