from django.db import models


class SiteSettings(models.Model):
    """Singleton — one row controls site-wide text content."""

    # Branding
    company_name = models.CharField(max_length=100, blank=True, default='',
        help_text='Shown in navbar & footer. Leave empty to use the default BSA text.')
    logo_white = models.FileField(upload_to='logos/', null=True, blank=True,
        help_text='Logo for dark backgrounds (navbar, footer). PNG/SVG/WebP recommended.')
    logo_black = models.FileField(upload_to='logos/', null=True, blank=True,
        help_text='Logo for light/white backgrounds. PNG/SVG/WebP recommended.')
    favicon = models.FileField(upload_to='logos/', null=True, blank=True,
        help_text='Browser tab icon. Recommended: 32×32 or 64×64 PNG/ICO/SVG.')

    # Announcement bar
    announcement_text = models.CharField(max_length=250, default="Our Ambassadors use Bangla Speech AI for free. You in?")
    announcement_link_text = models.CharField(max_length=60, default="Apply now.")

    # Hero
    hero_badge = models.CharField(max_length=100, default="Bangla AI Voice Generator")
    hero_title = models.CharField(max_length=200, default="1000+ realistic Bangla AI voices")
    hero_title_highlight = models.CharField(max_length=100, default="for any mood")
    hero_subtitle = models.TextField(default="Generate studio-quality audio with Bangla Speech AI. Choose from 1000+ Bangla AI voices and create voiceovers in seconds.")
    hero_btn_primary = models.CharField(max_length=60, default="Try now for free")
    hero_btn_secondary = models.CharField(max_length=60, default="Build with API")

    # Voice section
    voices_heading = models.CharField(max_length=200, default="Bangla voice clips mapped to real business scenarios")

    # Stats section heading
    stats_heading = models.CharField(max_length=200, default="Rely on TTS technology built for scale")

    # Use Cases section heading
    usecases_heading           = models.CharField(max_length=200, default="What can you create with Bangla AI voices?")
    usecases_heading_highlight = models.CharField(max_length=100, default="Everything!")

    # Pricing section heading
    pricing_badge   = models.CharField(max_length=60,  default="Pricing")
    pricing_heading = models.CharField(max_length=200, default="Simple, transparent pricing")
    pricing_sub     = models.CharField(max_length=200, default="Choose the plan that works for you. No hidden fees.")

    # CTA section
    cta_title = models.CharField(max_length=200, default="Start creating for free")
    cta_subtitle = models.TextField(default="Join 50,000+ creators using Bangla Speech AI to produce studio-quality audio in minutes")

    # API section
    api_badge    = models.CharField(max_length=60, default='For Developers')
    api_heading  = models.CharField(max_length=200, default='Build with Voice API')
    api_body     = models.TextField(default='Integrate Bangla AI voices into your app with our developer-friendly API. Streaming support, voice cloning, and 24/7 SLA included.')
    api_features = models.TextField(
        default='Streaming support for real-time applications\nVoice cloning for custom brand voices\nStarting at $0.50 per hour with 24/7 SLA\nBangla language fully supported',
        help_text='One feature per line'
    )
    api_btn_text     = models.CharField(max_length=60, default='Contact Us')
    api_code_lang    = models.CharField(max_length=40, default='Python')
    api_code_content = models.TextField(default=
        "import bangla_speech_ai as bsa\n\n"
        "client = bsa.Client(api_key='your-api-key')\n\n"
        "audio = client.tts.generate(\n"
        "    text='Thank you for using our service.',\n"
        "    voice_id='bangla-female-1',\n"
        "    output_format='mp3'\n"
        ")\n\n"
        "# Stream or save your audio\n"
        "audio.save('output.mp3')"
    )

    # Contact
    contact_email = models.EmailField(blank=True, default='',
        help_text='Shown as "Or email directly" link on the Book a Demo form')

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    def api_features_list(self):
        return [f.strip() for f in self.api_features.splitlines() if f.strip()]

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class VoiceCard(models.Model):
    name = models.CharField(max_length=100, help_text="Voice name shown on the card")
    script_text = models.TextField(help_text="Bangla sentence this voice will say")
    audio_file = models.FileField(
        upload_to='voice_audio/',
        null=True, blank=True,
        help_text="Upload MP3/WAV. If empty, a simulated animation plays."
    )
    duration = models.FloatField(default=4.0, help_text="Simulated duration in seconds (used when no audio file)")
    wave_seed = models.IntegerField(default=42, help_text="Controls the waveform bar shape (any integer)")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Voice Card"
        verbose_name_plural = "Voice Cards"

    def __str__(self):
        return self.name


class StatItem(models.Model):
    number = models.CharField(max_length=20, help_text="e.g. 100%, 15 min, 90%")
    label = models.CharField(max_length=150, help_text="Description shown below the number")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Stat Item"
        verbose_name_plural = "Stat Items"

    def __str__(self):
        return f"{self.number} — {self.label}"


class FAQItem(models.Model):
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class UseCaseSlide(models.Model):
    SLIDE_TYPES = [
        ('podcast',   'Podcast'),
        ('audio',     'Audiobook'),
        ('marketing', 'Marketing'),
        ('training',  'Training'),
        ('access',    'Accessibility'),
        ('video',     'Video'),
    ]
    title = models.CharField(max_length=100)
    description = models.TextField()
    slide_type = models.CharField(max_length=20, choices=SLIDE_TYPES, default='podcast')
    overlay_text = models.CharField(max_length=120, default="Record. Edit. Publish.", help_text="Bold text overlaid on the card image area")
    badge_text = models.CharField(max_length=50, default="Live", blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Use Case Slide"
        verbose_name_plural = "Use Case Slides"

    def __str__(self):
        return self.title


class PricingPlan(models.Model):
    name         = models.CharField(max_length=100)
    badge_text   = models.CharField(max_length=50, blank=True, default='', help_text="e.g. 'Most Popular'")
    price        = models.CharField(max_length=20, help_text="e.g. '$0', '$49', 'Custom'")
    price_period = models.CharField(max_length=50, blank=True, default='per month')
    description  = models.CharField(max_length=200)
    features     = models.TextField(help_text='One feature per line')
    cta_text     = models.CharField(max_length=60, default='Get started')
    cta_url      = models.CharField(max_length=200, blank=True, default='#')
    is_featured  = models.BooleanField(default=False, help_text='Highlighted card with accent border')
    is_active    = models.BooleanField(default=True)
    order        = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Pricing Plan'
        verbose_name_plural = 'Pricing Plans'

    def __str__(self):
        return f'{self.name} — {self.price}'

    def features_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]


class DemoBooking(models.Model):
    USE_CASE_CHOICES = [
        ('podcast',   'Podcast / Content Creation'),
        ('audiobook', 'Audiobook / E-learning'),
        ('ivr',       'IVR / Call Center'),
        ('marketing', 'Marketing / Advertising'),
        ('training',  'Training / Corporate'),
        ('app',       'Mobile / Web App'),
        ('other',     'Other'),
    ]

    full_name        = models.CharField(max_length=200, default='')
    company          = models.CharField(max_length=200, blank=True, default='')
    email            = models.EmailField()
    monthly_volume   = models.CharField(max_length=100, blank=True, default='')
    use_case         = models.CharField(max_length=50, choices=USE_CASE_CHOICES, blank=True, default='')
    business_context = models.TextField(blank=True, default='')
    agreed           = models.BooleanField(default=False)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Demo Booking"
        verbose_name_plural = "Demo Bookings"

    def __str__(self):
        return f"{self.full_name} — {self.email}"


class HowItWorksStep(models.Model):
    step_number = models.CharField(max_length=5, default="01")
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "How It Works Step"
        verbose_name_plural = "How It Works Steps"

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


class ContactSubmission(models.Model):
    name       = models.CharField(max_length=200)
    email      = models.EmailField()
    phone      = models.CharField(max_length=30, blank=True, default='')
    message    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f'{self.name} — {self.email}'
