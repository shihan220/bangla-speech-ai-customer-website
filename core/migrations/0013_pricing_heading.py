from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_usecases_heading'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='pricing_badge',
            field=models.CharField(default='Pricing', max_length=60),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='pricing_heading',
            field=models.CharField(default='Simple, transparent pricing', max_length=200),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='pricing_sub',
            field=models.CharField(default='Choose the plan that works for you. No hidden fees.', max_length=200),
        ),
    ]
