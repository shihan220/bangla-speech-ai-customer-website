from django.db import migrations


def seed(apps, schema_editor):
    VoiceCard      = apps.get_model('core', 'VoiceCard')
    StatItem       = apps.get_model('core', 'StatItem')
    FAQItem        = apps.get_model('core', 'FAQItem')
    UseCaseSlide   = apps.get_model('core', 'UseCaseSlide')
    HowItWorksStep = apps.get_model('core', 'HowItWorksStep')

    # Voice Cards — names & scripts stay Bangla (they are voice demos)
    voices = [
        ("Rahela",  "শুভ সকাল। আপনার অর্ডারটি প্রস্তুত এবং আজই ডেলিভারি দেওয়া হবে।",      4.2, 42),
        ("Karim",   "আপনার অ্যাপয়েন্টমেন্ট আগামীকাল সকাল দশটায় নিশ্চিত করা হয়েছে।",    3.8, 137),
        ("Nila",    "আপনার পেমেন্ট সফলভাবে গ্রহণ করা হয়েছে। ধন্যবাদ।",                  3.5, 280),
        ("Sadia",   "আপনার ডেলিভারি কালকের মধ্যে পৌঁছে যাবে। এখনই ট্র্যাক করুন।",       3.6, 195),
        ("Faruk",   "আপনার সার্ভিস রিকোয়েস্ট সফলভাবে সম্পন্ন হয়েছে।",                   3.4, 318),
        ("Mita",    "আপনার রিনিউয়াল প্রম্পট সক্রিয় করা হয়েছে। বিস্তারিত জানতে ক্লিক করুন।", 4.0, 456),
        ("Tanvir",  "আপনার পডকাস্ট এপিসোড প্রকাশের জন্য প্রস্তুত। এখনই পাবলিশ করুন।",    3.9, 73),
        ("Sumaiya", "আমাদের সেবা ব্যবহার করার জন্য আন্তরিক ধন্যবাদ।",                    3.7, 521),
    ]
    for i, (name, script, dur, seed_val) in enumerate(voices):
        VoiceCard.objects.create(name=name, script_text=script, duration=dur, wave_seed=seed_val, order=i)

    # Stats — English
    stats_data = [
        ("100%",   "speech stability. Same input, same output, every time"),
        ("Zero",   "skipped words with sentence-level checks"),
        ("15 min", "from script to polished audio"),
        ("90%",    "less time spent on voiceovers vs studio recording"),
        ("100+",   "languages and dialects tested for natural pronunciation"),
    ]
    for i, (num, lbl) in enumerate(stats_data):
        StatItem.objects.create(number=num, label=lbl, order=i)

    # FAQs — English
    faqs_data = [
        ("Can I use the generated voices commercially?",
         "Yes. All voices generated with Bangla Speech AI can be used for commercial purposes. Paid plans include full commercial licensing rights."),
        ("How realistic are the Bangla AI voices?",
         "Our Bangla AI voices are trained on thousands of hours of professional recordings, capturing natural intonation, pauses, and emotional inflection."),
        ("Can I upload an audio file for each voice?",
         "Yes. From the Admin panel you can upload an MP3 or WAV file for each Voice Card. The player will use the real audio instead of the simulated animation."),
        ("How does voice cloning work?",
         "Upload just a few minutes of clean audio. Our AI analyses the voice characteristics and creates a custom voice model you can use to generate any text."),
        ("Where can I find the API?",
         "Go to Developer platform → Voice API for full documentation, code samples, and your API keys."),
        ("What subscription plans are available?",
         "We offer a free plan to get started, plus paid plans for individuals, teams, and enterprise customers. Visit our pricing page to compare."),
    ]
    for i, (q, a) in enumerate(faqs_data):
        FAQItem.objects.create(question=q, answer=a, order=i)

    # Use Case Slides — English
    slides_data = [
        ("Podcasts",          "Record intros, ads, and episode segments with consistent AI voice hosts.",                  "podcast",   "Record.\nEdit.\nPublish.",     "Live Episode"),
        ("Audiobooks",        "Create chapter-by-chapter narrations by simply uploading a PDF file.",                     "audio",     "Your story,\nyour voice.",     ""),
        ("Marketing content", "Turn scripts into ads, demos, or other marketing content with pronunciation control.",     "marketing", "Every word.\nPerfect.",        ""),
        ("Training & lessons","Build engaging e-learning modules and corporate training with realistic AI voices.",        "training",  "Learn at\nyour pace.",         ""),
        ("Accessibility",     "Make written content available to everyone with natural-sounding text-to-speech.",         "access",    "Voice\nfor all.",              ""),
        ("Video voiceovers",  "Add professional narration to explainers, tutorials, and YouTube videos in minutes.",      "video",     "Scene.\nTake.\nAction.",       ""),
    ]
    for i, (title, desc, stype, overlay, badge) in enumerate(slides_data):
        UseCaseSlide.objects.create(title=title, description=desc, slide_type=stype,
                                    overlay_text=overlay, badge_text=badge, order=i)

    # How It Works — English
    steps_data = [
        ("01", "Chat with AI",        "Describe the voice, tone, and style you need. Upload your script or type directly."),
        ("02", "Generate instantly",  "Select from 1000+ Bangla voices and generate studio-quality audio in seconds."),
        ("03", "Edit like a doc",     "Fine-tune pronunciation, pacing, and emphasis directly in the text editor."),
        ("04", "Export & publish",    "Download in MP3, WAV, or publish directly to your platform of choice."),
    ]
    for i, (num, title, desc) in enumerate(steps_data):
        HowItWorksStep.objects.create(step_number=num, title=title, description=desc, order=i)


def unseed(apps, schema_editor):
    for model_name in ['VoiceCard', 'StatItem', 'FAQItem', 'UseCaseSlide', 'HowItWorksStep']:
        apps.get_model('core', model_name).objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
