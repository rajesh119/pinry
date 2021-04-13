# Generated by Django 2.2.19 on 2021-02-28 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200825_0800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Look',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insta_id', models.CharField(blank=True, max_length=512, null=True)),
                ('insta_post_id', models.CharField(blank=True, max_length=512, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('image_url', models.CharField(blank=True, max_length=512, null=True)),
                ('published', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]