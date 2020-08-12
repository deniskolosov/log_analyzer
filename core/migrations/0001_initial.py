# Generated by Django 3.1 on 2020-08-12 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('date', models.DateTimeField()),
                ('http_method', models.CharField(blank=True, choices=[('GET', 'Get'), ('POST', 'Post'), ('DELETE', 'Delete'), ('PUT', 'Put'), ('PATCH', 'Patch'), ('OPTIONS', 'Options')], max_length=8)),
                ('request_uri', models.URLField()),
                ('status_code', models.IntegerField()),
                ('response_size', models.IntegerField()),
            ],
            options={
                'verbose_name_plural': 'Entries',
            },
        ),
        migrations.AddConstraint(
            model_name='logentry',
            constraint=models.UniqueConstraint(fields=('ip', 'date', 'request_uri'), name='unique_records'),
        ),
    ]