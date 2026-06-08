from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_api_code_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='usecases_heading',
            field=models.CharField(default='What can you create with Bangla AI voices?', max_length=200),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='usecases_heading_highlight',
            field=models.CharField(default='Everything!', max_length=100),
        ),
    ]
