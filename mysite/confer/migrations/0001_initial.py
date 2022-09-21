# Generated by Django 3.2.1 on 2021-06-12 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='candidat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('github', models.URLField()),
                ('linkedin', models.URLField()),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'confer_candidat',
            },
        ),
        migrations.CreateModel(
            name='offre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salaire', models.FloatField()),
                ('annonce', models.TextField()),
                ('date_publication', models.DateField()),
                ('deadline', models.DateField()),
                ('question', models.TextField()),
                ('extraction', models.JSONField(null=True)),
            ],
            options={
                'db_table': 'confer_offre',
            },
        ),
        migrations.CreateModel(
            name='submit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cv', models.FileField(upload_to='pdf')),
                ('cv_extraction', models.JSONField(null=True)),
                ('res_cv', models.FloatField(null=True)),
                ('test', models.TextField()),
                ('res_test', models.FloatField(null=True)),
                ('res_photo', models.FloatField(null=True)),
                ('video', models.FileField(upload_to='mp4')),
                ('res_video', models.FloatField(null=True)),
                ('rank', models.FloatField(null=True)),
                ('candidat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='confer.candidat')),
                ('offre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='confer.offre')),
            ],
            options={
                'db_table': 'confer_submit',
            },
        ),
        migrations.CreateModel(
            name='recruteur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
                ('societe', models.CharField(max_length=100)),
                ('photo', models.ImageField(blank=True, default='profile.jpg', null=True, upload_to='')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'confer_recrutement',
            },
        ),
        migrations.AddField(
            model_name='offre',
            name='recruteur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='confer.recruteur'),
        ),
    ]
