# Generated by Django 4.0.6 on 2022-09-13 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_customuser_about'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('react_type', models.CharField(choices=[('like', 'like'), ('dislike', 'dislike')], max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='post_reactions',
            field=models.ManyToManyField(blank=True, related_name='posts', through='blog.Reaction', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reaction',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.post'),
        ),
        migrations.AddField(
            model_name='reaction',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
