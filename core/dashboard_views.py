from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.urls import reverse
from django import forms

from .models import SiteSettings, VoiceCard, StatItem, FAQItem, UseCaseSlide, HowItWorksStep, DemoBooking, PricingPlan, ContactSubmission

# ── Auth guard ───────────────────────────────────────────────
staff_only = user_passes_test(
    lambda u: u.is_active and u.is_staff,
    login_url='/dashboard/login/'
)


# ── Form styling mixin ───────────────────────────────────────
class _Styled:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            w = field.widget
            base = w.attrs.get('class', '')
            if isinstance(w, forms.CheckboxInput):
                w.attrs['class'] = (base + ' db-check').strip()
            elif isinstance(w, forms.Textarea):
                w.attrs['class'] = (base + ' db-input db-textarea').strip()
            elif isinstance(w, (forms.Select, forms.SelectMultiple)):
                w.attrs['class'] = (base + ' db-input db-select').strip()
            elif isinstance(w, forms.ClearableFileInput):
                pass
            else:
                w.attrs['class'] = (base + ' db-input').strip()


# ── Forms ────────────────────────────────────────────────────
class SiteSettingsForm(_Styled, forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['company_name', 'logo_white', 'logo_black', 'favicon', 'contact_email']
        widgets = {
            'logo_white': forms.ClearableFileInput(attrs={'accept': 'image/*,.svg'}),
            'logo_black': forms.ClearableFileInput(attrs={'accept': 'image/*,.svg'}),
            'favicon':    forms.ClearableFileInput(attrs={'accept': 'image/*,.ico,.svg'}),
        }


class HeroSectionForm(_Styled, forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'hero_badge', 'hero_title', 'hero_title_highlight',
            'hero_subtitle', 'hero_btn_primary', 'hero_btn_secondary',
        ]
        widgets = {
            'hero_subtitle': forms.Textarea(attrs={'rows': 3}),
        }


class AnnouncementForm(_Styled, forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ['announcement_text', 'announcement_link_text']


class CtaHeadingsForm(_Styled, forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'voices_heading',
            'usecases_heading', 'usecases_heading_highlight',
            'pricing_badge', 'pricing_heading', 'pricing_sub',
            'stats_heading',
            'cta_title', 'cta_subtitle',
        ]
        widgets = {
            'cta_subtitle': forms.Textarea(attrs={'rows': 3}),
        }


class ApiSectionForm(_Styled, forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'api_badge', 'api_heading', 'api_body',
            'api_features', 'api_btn_text',
            'api_code_lang', 'api_code_content',
        ]
        widgets = {
            'api_body':         forms.Textarea(attrs={'rows': 3}),
            'api_features':     forms.Textarea(attrs={'rows': 5}),
            'api_code_content': forms.Textarea(attrs={'rows': 12, 'style': 'font-family:monospace;font-size:13px;'}),
        }


class VoiceCardForm(_Styled, forms.ModelForm):
    class Meta:
        model = VoiceCard
        fields = ['name', 'script_text', 'audio_file', 'duration', 'wave_seed', 'order', 'is_active']
        widgets = {'script_text': forms.Textarea(attrs={'rows': 3})}


class StatItemForm(_Styled, forms.ModelForm):
    class Meta:
        model = StatItem
        fields = ['number', 'label', 'order']


class FAQItemForm(_Styled, forms.ModelForm):
    class Meta:
        model = FAQItem
        fields = ['question', 'answer', 'order', 'is_active']
        widgets = {'answer': forms.Textarea(attrs={'rows': 4})}


class UseCaseSlideForm(_Styled, forms.ModelForm):
    class Meta:
        model = UseCaseSlide
        fields = ['title', 'description', 'slide_type', 'overlay_text', 'badge_text', 'order', 'is_active']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


class HowItWorksStepForm(_Styled, forms.ModelForm):
    class Meta:
        model = HowItWorksStep
        fields = ['step_number', 'title', 'description', 'order']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


# ── Order helper ─────────────────────────────────────────────
def _move(model, pk, direction):
    items = list(model.objects.order_by('order', 'pk'))
    for i, item in enumerate(items):
        if item.order != i:
            model.objects.filter(pk=item.pk).update(order=i)
    items = list(model.objects.order_by('order', 'pk'))
    idx = next((i for i, x in enumerate(items) if x.pk == pk), None)
    if idx is None:
        return
    if direction == 'up' and idx > 0:
        a, b = items[idx], items[idx - 1]
        a.order, b.order = idx - 1, idx
        a.save(update_fields=['order'])
        b.save(update_fields=['order'])
    elif direction == 'down' and idx < len(items) - 1:
        a, b = items[idx], items[idx + 1]
        a.order, b.order = idx + 1, idx
        a.save(update_fields=['order'])
        b.save(update_fields=['order'])


# ── Overview ─────────────────────────────────────────────────
@staff_only
def db_index(request):
    return render(request, 'dashboard/index.html', {
        'vc_total':   VoiceCard.objects.count(),
        'vc_active':  VoiceCard.objects.filter(is_active=True).count(),
        'stat_count': StatItem.objects.count(),
        'faq_total':  FAQItem.objects.count(),
        'faq_active': FAQItem.objects.filter(is_active=True).count(),
        'uc_total':   UseCaseSlide.objects.count(),
        'uc_active':       UseCaseSlide.objects.filter(is_active=True).count(),
        'hiw_count':       HowItWorksStep.objects.count(),
        'booking_count':  DemoBooking.objects.count(),
        'pricing_count':  PricingPlan.objects.count(),
        'contact_count':  ContactSubmission.objects.count(),
    })


# ── Site Settings ────────────────────────────────────────────
@staff_only
def db_settings(request):
    obj = SiteSettings.get()
    form = SiteSettingsForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Site settings saved successfully.')
        return redirect('db_settings')
    return render(request, 'dashboard/settings.html', {'form': form})


# ── API Section Settings ─────────────────────────────────────
@staff_only
def db_api_section(request):
    obj = SiteSettings.get()
    form = ApiSectionForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'API section saved.')
        return redirect('db_api_section')
    return render(request, 'dashboard/api_section.html', {'form': form})


# ── Hero Section ─────────────────────────────────────────────
@staff_only
def db_hero(request):
    obj = SiteSettings.get()
    form = HeroSectionForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Hero section saved.')
        return redirect('db_hero')
    return render(request, 'dashboard/hero.html', {'form': form})


# ── Announcement Bar ─────────────────────────────────────────
@staff_only
def db_announcement(request):
    obj = SiteSettings.get()
    form = AnnouncementForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Announcement bar saved.')
        return redirect('db_announcement')
    return render(request, 'dashboard/announcement.html', {'form': form})


# ── CTA & Headings ───────────────────────────────────────────
@staff_only
def db_cta_headings(request):
    obj = SiteSettings.get()
    form = CtaHeadingsForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'CTA & headings saved.')
        return redirect('db_cta_headings')
    return render(request, 'dashboard/cta_headings.html', {'form': form})


# ── Voice Cards ──────────────────────────────────────────────
@staff_only
def db_voices(request):
    return render(request, 'dashboard/voices.html', {
        'voices': VoiceCard.objects.order_by('order', 'pk'),
    })


@staff_only
def db_voice_new(request):
    form = VoiceCardForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Voice card added.')
        return redirect('db_voices')
    return render(request, 'dashboard/form.html', {
        'form': form,
        'form_title': 'Add Voice Card',
        'section_name': 'Voice Cards',
        'cancel_url': reverse('db_voices'),
    })


@staff_only
def db_voice_edit(request, pk):
    obj = get_object_or_404(VoiceCard, pk=pk)
    form = VoiceCardForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Voice card updated.')
        return redirect('db_voices')
    return render(request, 'dashboard/form.html', {
        'form': form, 'obj': obj,
        'form_title': f'Edit — {obj.name}',
        'section_name': 'Voice Cards',
        'cancel_url': reverse('db_voices'),
        'delete_url': reverse('db_voice_delete', args=[pk]),
    })


@require_POST
@staff_only
def db_voice_delete(request, pk):
    get_object_or_404(VoiceCard, pk=pk).delete()
    messages.success(request, 'Voice card deleted.')
    return redirect('db_voices')


@require_POST
@staff_only
def db_voice_toggle(request, pk):
    obj = get_object_or_404(VoiceCard, pk=pk)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active'])
    return redirect('db_voices')


@require_POST
@staff_only
def db_voice_move(request, pk, direction):
    _move(VoiceCard, pk, direction)
    return redirect('db_voices')


# ── Stats ────────────────────────────────────────────────────
@staff_only
def db_stats(request):
    return render(request, 'dashboard/stats.html', {
        'stats': StatItem.objects.order_by('order', 'pk'),
    })


@staff_only
def db_stat_new(request):
    form = StatItemForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Stat added.')
        return redirect('db_stats')
    return render(request, 'dashboard/form.html', {
        'form': form,
        'form_title': 'Add Stat',
        'section_name': 'Stats',
        'cancel_url': reverse('db_stats'),
    })


@staff_only
def db_stat_edit(request, pk):
    obj = get_object_or_404(StatItem, pk=pk)
    form = StatItemForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Stat updated.')
        return redirect('db_stats')
    return render(request, 'dashboard/form.html', {
        'form': form, 'obj': obj,
        'form_title': f'Edit Stat — {obj.number}',
        'section_name': 'Stats',
        'cancel_url': reverse('db_stats'),
        'delete_url': reverse('db_stat_delete', args=[pk]),
    })


@require_POST
@staff_only
def db_stat_delete(request, pk):
    get_object_or_404(StatItem, pk=pk).delete()
    messages.success(request, 'Stat deleted.')
    return redirect('db_stats')


@require_POST
@staff_only
def db_stat_move(request, pk, direction):
    _move(StatItem, pk, direction)
    return redirect('db_stats')


# ── FAQs ─────────────────────────────────────────────────────
@staff_only
def db_faqs(request):
    return render(request, 'dashboard/faqs.html', {
        'faqs': FAQItem.objects.order_by('order', 'pk'),
    })


@staff_only
def db_faq_new(request):
    form = FAQItemForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'FAQ added.')
        return redirect('db_faqs')
    return render(request, 'dashboard/form.html', {
        'form': form,
        'form_title': 'Add FAQ',
        'section_name': 'FAQs',
        'cancel_url': reverse('db_faqs'),
    })


@staff_only
def db_faq_edit(request, pk):
    obj = get_object_or_404(FAQItem, pk=pk)
    form = FAQItemForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'FAQ updated.')
        return redirect('db_faqs')
    return render(request, 'dashboard/form.html', {
        'form': form, 'obj': obj,
        'form_title': 'Edit FAQ',
        'section_name': 'FAQs',
        'cancel_url': reverse('db_faqs'),
        'delete_url': reverse('db_faq_delete', args=[pk]),
    })


@require_POST
@staff_only
def db_faq_delete(request, pk):
    get_object_or_404(FAQItem, pk=pk).delete()
    messages.success(request, 'FAQ deleted.')
    return redirect('db_faqs')


@require_POST
@staff_only
def db_faq_toggle(request, pk):
    obj = get_object_or_404(FAQItem, pk=pk)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active'])
    return redirect('db_faqs')


@require_POST
@staff_only
def db_faq_move(request, pk, direction):
    _move(FAQItem, pk, direction)
    return redirect('db_faqs')


# ── Use Cases ────────────────────────────────────────────────
@staff_only
def db_usecases(request):
    return render(request, 'dashboard/usecases.html', {
        'usecases': UseCaseSlide.objects.order_by('order', 'pk'),
    })


@staff_only
def db_usecase_new(request):
    form = UseCaseSlideForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Use case added.')
        return redirect('db_usecases')
    return render(request, 'dashboard/form.html', {
        'form': form,
        'form_title': 'Add Use Case',
        'section_name': 'Use Cases',
        'cancel_url': reverse('db_usecases'),
    })


@staff_only
def db_usecase_edit(request, pk):
    obj = get_object_or_404(UseCaseSlide, pk=pk)
    form = UseCaseSlideForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Use case updated.')
        return redirect('db_usecases')
    return render(request, 'dashboard/form.html', {
        'form': form, 'obj': obj,
        'form_title': f'Edit — {obj.title}',
        'section_name': 'Use Cases',
        'cancel_url': reverse('db_usecases'),
        'delete_url': reverse('db_usecase_delete', args=[pk]),
    })


@require_POST
@staff_only
def db_usecase_delete(request, pk):
    get_object_or_404(UseCaseSlide, pk=pk).delete()
    messages.success(request, 'Use case deleted.')
    return redirect('db_usecases')


@require_POST
@staff_only
def db_usecase_toggle(request, pk):
    obj = get_object_or_404(UseCaseSlide, pk=pk)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active'])
    return redirect('db_usecases')


@require_POST
@staff_only
def db_usecase_move(request, pk, direction):
    _move(UseCaseSlide, pk, direction)
    return redirect('db_usecases')


# ── How It Works ─────────────────────────────────────────────
@staff_only
def db_hiw(request):
    return render(request, 'dashboard/hiw.html', {
        'steps': HowItWorksStep.objects.order_by('order', 'pk'),
    })


@staff_only
def db_hiw_new(request):
    form = HowItWorksStepForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Step added.')
        return redirect('db_hiw')
    return render(request, 'dashboard/form.html', {
        'form': form,
        'form_title': 'Add Step',
        'section_name': 'How It Works',
        'cancel_url': reverse('db_hiw'),
    })


@staff_only
def db_hiw_edit(request, pk):
    obj = get_object_or_404(HowItWorksStep, pk=pk)
    form = HowItWorksStepForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Step updated.')
        return redirect('db_hiw')
    return render(request, 'dashboard/form.html', {
        'form': form, 'obj': obj,
        'form_title': f'Edit Step {obj.step_number}',
        'section_name': 'How It Works',
        'cancel_url': reverse('db_hiw'),
        'delete_url': reverse('db_hiw_delete', args=[pk]),
    })


@require_POST
@staff_only
def db_hiw_delete(request, pk):
    get_object_or_404(HowItWorksStep, pk=pk).delete()
    messages.success(request, 'Step deleted.')
    return redirect('db_hiw')


@require_POST
@staff_only
def db_hiw_move(request, pk, direction):
    _move(HowItWorksStep, pk, direction)
    return redirect('db_hiw')


# ── Pricing Plans ────────────────────────────────────────────
class PricingPlanForm(_Styled, forms.ModelForm):
    class Meta:
        model = PricingPlan
        fields = ['name', 'badge_text', 'price', 'price_period', 'description',
                  'features', 'cta_text', 'cta_url', 'is_featured', 'is_active', 'order']
        widgets = {
            'features': forms.Textarea(attrs={'rows': 8,
                'placeholder': 'One feature per line\ne.g.\n1,000 characters / month\n3 voice styles\nEmail support'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }


@staff_only
def db_pricing(request):
    return render(request, 'dashboard/pricing.html', {
        'plans': PricingPlan.objects.order_by('order', 'pk'),
    })


@staff_only
def db_pricing_new(request):
    form = PricingPlanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Pricing plan added.')
        return redirect('db_pricing')
    return render(request, 'dashboard/form.html', {
        'form': form,
        'form_title': 'Add Pricing Plan',
        'section_name': 'Pricing',
        'cancel_url': reverse('db_pricing'),
    })


@staff_only
def db_pricing_edit(request, pk):
    obj = get_object_or_404(PricingPlan, pk=pk)
    form = PricingPlanForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Pricing plan updated.')
        return redirect('db_pricing')
    return render(request, 'dashboard/form.html', {
        'form': form, 'obj': obj,
        'form_title': f'Edit — {obj.name}',
        'section_name': 'Pricing',
        'cancel_url': reverse('db_pricing'),
        'delete_url': reverse('db_pricing_delete', args=[pk]),
    })


@require_POST
@staff_only
def db_pricing_delete(request, pk):
    get_object_or_404(PricingPlan, pk=pk).delete()
    messages.success(request, 'Pricing plan deleted.')
    return redirect('db_pricing')


@require_POST
@staff_only
def db_pricing_toggle(request, pk):
    obj = get_object_or_404(PricingPlan, pk=pk)
    obj.is_active = not obj.is_active
    obj.save(update_fields=['is_active'])
    return redirect('db_pricing')


@require_POST
@staff_only
def db_pricing_move(request, pk, direction):
    _move(PricingPlan, pk, direction)
    return redirect('db_pricing')


# ── Demo Bookings ────────────────────────────────────────────
@staff_only
def db_bookings(request):
    return render(request, 'dashboard/bookings.html', {
        'bookings': DemoBooking.objects.order_by('-created_at'),
    })


# ── Contact Submissions ───────────────────────────────────────
@staff_only
def db_contacts(request):
    return render(request, 'dashboard/contacts.html', {
        'contacts': ContactSubmission.objects.order_by('-created_at'),
    })
