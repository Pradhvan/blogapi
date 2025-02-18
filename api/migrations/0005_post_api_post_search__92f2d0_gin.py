# Generated by Django 5.1.6 on 2025-02-17 12:46

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_post_api_post_created_a6ef6d_idx"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="post",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["search_vector"], name="api_post_search__92f2d0_gin"
            ),
        ),
    ]
