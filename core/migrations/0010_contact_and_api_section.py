from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_add_pricingplan'),
    ]

    operations = [
        # API section fields on SiteSettings
        migrations.AddField(
            model_name='sitesettings',
            name='api_badge',
            field=models.CharField(default='For Developers', max_length=60),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='api_heading',
            field=models.CharField(default='Build with Voice API', max_length=200),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='api_body',
            field=models.TextField(default='Integrate Bangla AI voices into your app with our developer-friendly API. Streaming support, voice cloning, and 24/7 SLA included.'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='api_features',
            field=models.TextField(
                default='Streaming support for real-time applications\nVoice cloning for custom brand voices\nStarting at $0.50 per hour with 24/7 SLA\nBangla language fully supported',
                help_text='One feature per line',
            ),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='api_btn_text',
            field=models.CharField(default='Contact Us', max_length=60),
        ),
        # ContactSubmission model
        migrations.CreateModel(
            name='ContactSubmission',
            fields=[
                ('id',         models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name',       models.CharField(max_length=200)),
                ('email',      models.EmailField()),
                ('phone',      models.CharField(blank=True, default='', max_length=30)),
                ('message',    models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Contact Submission',
                'verbose_name_plural': 'Contact Submissions',
                'ordering': ['-created_at'],
            },
        ),
    ]
