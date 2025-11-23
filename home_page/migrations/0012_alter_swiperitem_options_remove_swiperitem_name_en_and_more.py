# home_page/migrations/0012_update_swiperitem.py

from django.db import migrations, models
import json

def convert_string_to_json(apps, schema_editor):
    SwiperItem = apps.get_model('home_page', 'SwiperItem')
    for item in SwiperItem.objects.all():
        # Агар майдонҳо ҳамчун string монда бошанд, онҳоро ба dict табдил диҳед
        if isinstance(item.name, str):
            item.name = json.loads(item.name)
        if isinstance(item.title, str):
            item.title = json.loads(item.title)
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0010_alter_swiperitem_options_and_more'),  # migration-и қаблӣ
    ]

    operations = [
        migrations.RemoveField(
            model_name='swiperitem',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='swiperitem',
            name='name_ru',
        ),
        migrations.RemoveField(
            model_name='swiperitem',
            name='name_tj',
        ),
        migrations.RemoveField(
            model_name='swiperitem',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='swiperitem',
            name='title_ru',
        ),
        migrations.RemoveField(
            model_name='swiperitem',
            name='title_tj',
        ),
        migrations.AddField(
            model_name='swiperitem',
            name='name',
            field=models.JSONField(default=dict),
        ),
        migrations.AddField(
            model_name='swiperitem',
            name='title',
            field=models.JSONField(default=dict),
        ),
        migrations.RunPython(convert_string_to_json),
    ]
