# Generated by Django 4.2.17 on 2024-12-22 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_comment_options_remove_comment_parent_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
