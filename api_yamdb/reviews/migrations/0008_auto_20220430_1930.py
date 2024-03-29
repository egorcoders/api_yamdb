# Generated by Django 3.2.13 on 2022-04-30 16:30

from django.db import migrations, models
import django.db.models.deletion
import reviews.models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0007_title_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(max_length=200, null=True),
        ),
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(default=reviews.models.current_year),
        ),
        migrations.CreateModel(
            name='TitleGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.genre')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.title')),
            ],
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(through='reviews.TitleGenre', to='reviews.Genre'),
        ),
    ]
