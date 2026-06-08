from .models import VoiceCard, StatItem, FAQItem, UseCaseSlide, HowItWorksStep, DemoBooking, PricingPlan


def dashboard_counts(request):
    if not request.path.startswith('/dashboard/'):
        return {}
    if not (request.user.is_authenticated and request.user.is_staff):
        return {}
    return {
        'nav_vc_count':      VoiceCard.objects.count(),
        'nav_stat_count':    StatItem.objects.count(),
        'nav_faq_count':     FAQItem.objects.count(),
        'nav_uc_count':      UseCaseSlide.objects.count(),
        'nav_hiw_count':     HowItWorksStep.objects.count(),
        'nav_booking_count': DemoBooking.objects.count(),
        'nav_pricing_count': PricingPlan.objects.count(),
    }
