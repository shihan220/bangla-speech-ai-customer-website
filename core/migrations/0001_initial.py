from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('announcement_text', models.CharField(default='আমাদের Ambassadors বিনামূল্যে Bangla Speech AI ব্যবহার করেন। আপনিও?', max_length=250)),
                ('announcement_link_text', models.CharField(default='Apply now.', max_length=60)),
                ('hero_badge', models.CharField(default='Bangla AI Voice Generator', max_length=100)),
                ('hero_title', models.CharField(default='১০০০+ রিয়েলিস্টিক বাংলা AI ভয়েস', max_length=200)),
                ('hero_title_highlight', models.CharField(default='যেকোনো মুডের জন্য', max_length=100)),
                ('hero_subtitle', models.TextField(default='Bangla Speech AI দিয়ে স্টুডিও-মানের অডিও তৈরি করুন। ১০০০+ বাংলা AI ভয়েস থেকে বেছে নিন এবং সেকেন্ডের মধ্যে ভয়েসওভার তৈরি করুন।')),
                ('hero_btn_primary', models.CharField(default='বিনামূল্যে চেষ্টা করুন', max_length=60)),
                ('hero_btn_secondary', models.CharField(default='API দিয়ে তৈরি করুন', max_length=60)),
                ('voices_heading', models.CharField(default='বাস্তব ব্যবসায়িক পরিস্থিতিতে ম্যাপ করা বাংলা ভয়েস ক্লিপ শুনুন', max_length=200)),
                ('stats_heading', models.CharField(default='TTS প্রযুক্তির উপর নির্ভর করুন যা স্কেলে তৈরি', max_length=200)),
                ('cta_title', models.CharField(default='বিনামূল্যে তৈরি শুরু করুন', max_length=200)),
                ('cta_subtitle', models.TextField(default='৫০,০০০+ ক্রিয়েটর Bangla Speech AI ব্যবহার করে মিনিটে স্টুডিও-মানের অডিও তৈরি করছেন')),
            ],
            options={'verbose_name': 'Site Settings', 'verbose_name_plural': 'Site Settings'},
        ),
        migrations.CreateModel(
            name='VoiceCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('script_text', models.TextField()),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='voice_audio/')),
                ('duration', models.FloatField(default=4.0)),
                ('wave_seed', models.IntegerField(default=42)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['order'], 'verbose_name': 'Voice Card', 'verbose_name_plural': 'Voice Cards'},
        ),
        migrations.CreateModel(
            name='StatItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=20)),
                ('label', models.CharField(max_length=150)),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order'], 'verbose_name': 'Stat Item', 'verbose_name_plural': 'Stat Items'},
        ),
        migrations.CreateModel(
            name='FAQItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=300)),
                ('answer', models.TextField()),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['order'], 'verbose_name': 'FAQ', 'verbose_name_plural': 'FAQs'},
        ),
        migrations.CreateModel(
            name='UseCaseSlide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('slide_type', models.CharField(choices=[('podcast', 'Podcast'), ('audio', 'Audiobook'), ('marketing', 'Marketing'), ('training', 'Training'), ('access', 'Accessibility'), ('video', 'Video')], default='podcast', max_length=20)),
                ('overlay_text', models.CharField(default='Record. Edit. Publish.', max_length=120)),
                ('badge_text', models.CharField(blank=True, default='Live', max_length=50)),
                ('order', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['order'], 'verbose_name': 'Use Case Slide', 'verbose_name_plural': 'Use Case Slides'},
        ),
        migrations.CreateModel(
            name='HowItWorksStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_number', models.CharField(default='01', max_length=5)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={'ordering': ['order'], 'verbose_name': 'How It Works Step', 'verbose_name_plural': 'How It Works Steps'},
        ),
    ]
