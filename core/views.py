from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django import forms

from .models import SiteSettings, VoiceCard, StatItem, FAQItem, UseCaseSlide, HowItWorksStep, DemoBooking, PricingPlan, ContactSubmission


class _DemoForm(forms.ModelForm):
    class Meta:
        model = DemoBooking
        fields = ['full_name', 'company', 'email', 'monthly_volume', 'use_case', 'business_context', 'agreed']

    def clean_full_name(self):
        v = self.cleaned_data.get('full_name', '').strip()
        if not v:
            raise forms.ValidationError('Full name is required.')
        return v

    def clean_use_case(self):
        v = self.cleaned_data.get('use_case', '')
        if not v:
            raise forms.ValidationError('Please select a use case.')
        return v

    def clean_business_context(self):
        v = self.cleaned_data.get('business_context', '').strip()
        if not v:
            raise forms.ValidationError('Please describe your business context.')
        return v

    def clean_agreed(self):
        if not self.cleaned_data.get('agreed'):
            raise forms.ValidationError('You must agree to continue.')
        return True


def home(request):
    context = {
        's':         SiteSettings.get(),
        'voices':    VoiceCard.objects.filter(is_active=True),
        'stats':     StatItem.objects.all(),
        'faqs':      FAQItem.objects.filter(is_active=True),
        'use_cases': UseCaseSlide.objects.filter(is_active=True),
        'hiw_steps':     HowItWorksStep.objects.all(),
        'pricing_plans': PricingPlan.objects.filter(is_active=True).order_by('order'),
    }
    return render(request, 'core/home.html', context)


@require_POST
def book_demo(request):
    form = _DemoForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'ok': True})
    errors = {k: v[0] for k, v in form.errors.items()}
    return JsonResponse({'ok': False, 'errors': errors})


class _ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'message']

    def clean_name(self):
        v = self.cleaned_data.get('name', '').strip()
        if not v:
            raise forms.ValidationError('Name is required.')
        return v

    def clean_message(self):
        v = self.cleaned_data.get('message', '').strip()
        if not v:
            raise forms.ValidationError('Message is required.')
        return v


@require_POST
def contact_us(request):
    form = _ContactForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'ok': True})
    errors = {k: v[0] for k, v in form.errors.items()}
    return JsonResponse({'ok': False, 'errors': errors})
