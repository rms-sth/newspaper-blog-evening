# Generated by Django 4.1.1 on 2022-09-13 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("personal_blog", "0002_category_tag_post_featured_image_post_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="featured_image",
            field=models.ImageField(upload_to="featured_images/%Y/%m/%d"),
        ),
    ]