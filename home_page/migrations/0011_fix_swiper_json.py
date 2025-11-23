from django.db import migrations
import json


def convert_string_to_json(apps, schema_editor):
    SwiperItem = apps.get_model("home_page", "SwiperItem")

    for item in SwiperItem.objects.all():
        changed = False

        # Convert name
        if isinstance(item.name, str):
            try:
                item.name = json.loads(item.name)
                changed = True
            except:
                pass

        # Convert title
        if isinstance(item.title, str):
            try:
                item.title = json.loads(item.title)
                changed = True
            except:
                pass

        if changed:
            item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0012_alter_swiperitem_options_remove_swiperitem_name_en_and_more'),
        ]

    operations = [
        migrations.RunPython(convert_string_to_json),
    ]
