from django.contrib import admin
from .models import SiteSettings, VoiceCard, StatItem, FAQItem, UseCaseSlide, HowItWorksStep, ContactSubmission

admin.site.site_header  = "বাংলা Speech AI — Admin"
admin.site.site_title   = "Bangla Speech AI Admin"
admin.site.index_title  = "Content Management"


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Announcement Bar", {"fields": ("announcement_text", "announcement_link_text")}),
        ("Hero Section",     {"fields": ("hero_badge", "hero_title", "hero_title_highlight", "hero_subtitle", "hero_btn_primary", "hero_btn_secondary")}),
        ("Section Headings", {"fields": ("voices_heading", "stats_heading")}),
        ("API Section",      {"fields": ("api_badge", "api_heading", "api_body", "api_features", "api_btn_text")}),
        ("CTA Banner",       {"fields": ("cta_title", "cta_subtitle")}),
    )


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'phone', 'created_at')
    readonly_fields = ('name', 'email', 'phone', 'message', 'created_at')
    ordering      = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(VoiceCard)
class VoiceCardAdmin(admin.ModelAdmin):
    list_display  = ('name', 'duration', 'wave_seed', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering      = ('order',)
    fieldsets = (
        (None, {"fields": ("name", "script_text", "is_active", "order")}),
        ("Audio", {"fields": ("audio_file", "duration", "wave_seed"),
                   "description": "Upload an MP3/WAV for real playback. If no file is uploaded, a simulated animation runs for 'duration' seconds."}),
    )


@admin.register(StatItem)
class StatItemAdmin(admin.ModelAdmin):
    list_display  = ('number', 'label', 'order')
    list_editable = ('order',)
    ordering      = ('order',)


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display  = ('question', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering      = ('order',)


@admin.register(UseCaseSlide)
class UseCaseSlideAdmin(admin.ModelAdmin):
    list_display  = ('title', 'slide_type', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering      = ('order',)


@admin.register(HowItWorksStep)
class HowItWorksStepAdmin(admin.ModelAdmin):
    list_display  = ('step_number', 'title', 'order')
    list_editable = ('order',)
    ordering      = ('order',)
