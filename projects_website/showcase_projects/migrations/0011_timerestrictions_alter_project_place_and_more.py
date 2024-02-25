# Generated by Django 5.0 on 2024-02-25 16:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('showcase_projects', '0010_project_lecturer_motivationletters'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeRestrictions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='project',
            name='place',
            field=models.IntegerField(default=6),
        ),
        migrations.AddField(
            model_name='motivationletters',
            name='timeRestrictions',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='motivationLetters', to='showcase_projects.timerestrictions'),
        ),
        migrations.AddField(
            model_name='participation',
            name='timeRestrictions',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participation', to='showcase_projects.timerestrictions'),
        ),
    ]