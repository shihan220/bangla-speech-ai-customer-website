from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_contact_and_api_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='api_code_lang',
            field=models.CharField(default='Python', max_length=40),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='api_code_content',
            field=models.TextField(default=(
                "import bangla_speech_ai as bsa\n\n"
                "client = bsa.Client(api_key='your-api-key')\n\n"
                "audio = client.tts.generate(\n"
                "    text='Thank you for using our service.',\n"
                "    voice_id='bangla-female-1',\n"
                "    output_format='mp3'\n"
                ")\n\n"
                "# Stream or save your audio\n"
                "audio.save('output.mp3')"
            )),
        ),
    ]
