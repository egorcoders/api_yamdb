# Generated by Django 2.2.16 on 2022-04-29 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0005_auto_20220429_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='genre', to='reviews.Genre'),
        ),
    ]