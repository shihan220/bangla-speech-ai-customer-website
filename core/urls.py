from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import dashboard_views as dv

urlpatterns = [
    path('', views.home, name='home'),
    path('book-demo/', views.book_demo, name='book_demo'),
    path('contact-us/', views.contact_us, name='contact_us'),

    # ── Auth ──────────────────────────────────────────────
    path('dashboard/login/', auth_views.LoginView.as_view(
        template_name='dashboard/login.html',
        redirect_authenticated_user=True,
    ), name='db_login'),
    path('dashboard/logout/', auth_views.LogoutView.as_view(
        next_page='/dashboard/login/',
    ), name='db_logout'),

    # ── Dashboard overview ─────────────────────────────────
    path('dashboard/',          dv.db_index,    name='db_index'),
    path('dashboard/settings/',    dv.db_settings,    name='db_settings'),
    path('dashboard/api-section/', dv.db_api_section, name='db_api_section'),
    path('dashboard/hero/',        dv.db_hero,        name='db_hero'),
    path('dashboard/announcement/',dv.db_announcement,name='db_announcement'),
    path('dashboard/cta/',         dv.db_cta_headings,name='db_cta_headings'),

    # ── Voice Cards ────────────────────────────────────────
    path('dashboard/voices/',                                dv.db_voices,       name='db_voices'),
    path('dashboard/voices/new/',                            dv.db_voice_new,    name='db_voice_new'),
    path('dashboard/voices/<int:pk>/edit/',                  dv.db_voice_edit,   name='db_voice_edit'),
    path('dashboard/voices/<int:pk>/delete/',                dv.db_voice_delete, name='db_voice_delete'),
    path('dashboard/voices/<int:pk>/toggle/',                dv.db_voice_toggle, name='db_voice_toggle'),
    path('dashboard/voices/<int:pk>/move/<str:direction>/',  dv.db_voice_move,   name='db_voice_move'),

    # ── Stats ──────────────────────────────────────────────
    path('dashboard/stats/',                               dv.db_stats,      name='db_stats'),
    path('dashboard/stats/new/',                           dv.db_stat_new,   name='db_stat_new'),
    path('dashboard/stats/<int:pk>/edit/',                 dv.db_stat_edit,  name='db_stat_edit'),
    path('dashboard/stats/<int:pk>/delete/',               dv.db_stat_delete,name='db_stat_delete'),
    path('dashboard/stats/<int:pk>/move/<str:direction>/', dv.db_stat_move,  name='db_stat_move'),

    # ── FAQs ───────────────────────────────────────────────
    path('dashboard/faqs/',                               dv.db_faqs,      name='db_faqs'),
    path('dashboard/faqs/new/',                           dv.db_faq_new,   name='db_faq_new'),
    path('dashboard/faqs/<int:pk>/edit/',                 dv.db_faq_edit,  name='db_faq_edit'),
    path('dashboard/faqs/<int:pk>/delete/',               dv.db_faq_delete,name='db_faq_delete'),
    path('dashboard/faqs/<int:pk>/toggle/',               dv.db_faq_toggle,name='db_faq_toggle'),
    path('dashboard/faqs/<int:pk>/move/<str:direction>/', dv.db_faq_move,  name='db_faq_move'),

    # ── Use Cases ──────────────────────────────────────────
    path('dashboard/usecases/',                                dv.db_usecases,       name='db_usecases'),
    path('dashboard/usecases/new/',                            dv.db_usecase_new,    name='db_usecase_new'),
    path('dashboard/usecases/<int:pk>/edit/',                  dv.db_usecase_edit,   name='db_usecase_edit'),
    path('dashboard/usecases/<int:pk>/delete/',                dv.db_usecase_delete, name='db_usecase_delete'),
    path('dashboard/usecases/<int:pk>/toggle/',                dv.db_usecase_toggle, name='db_usecase_toggle'),
    path('dashboard/usecases/<int:pk>/move/<str:direction>/',  dv.db_usecase_move,   name='db_usecase_move'),

    # ── How It Works ───────────────────────────────────────
    path('dashboard/hiw/',                               dv.db_hiw,      name='db_hiw'),
    path('dashboard/hiw/new/',                           dv.db_hiw_new,  name='db_hiw_new'),
    path('dashboard/hiw/<int:pk>/edit/',                 dv.db_hiw_edit, name='db_hiw_edit'),
    path('dashboard/hiw/<int:pk>/delete/',               dv.db_hiw_delete,name='db_hiw_delete'),
    path('dashboard/hiw/<int:pk>/move/<str:direction>/', dv.db_hiw_move, name='db_hiw_move'),

    # ── Pricing Plans ──────────────────────────────────────
    path('dashboard/pricing/',                                dv.db_pricing,        name='db_pricing'),
    path('dashboard/pricing/new/',                            dv.db_pricing_new,    name='db_pricing_new'),
    path('dashboard/pricing/<int:pk>/edit/',                  dv.db_pricing_edit,   name='db_pricing_edit'),
    path('dashboard/pricing/<int:pk>/delete/',                dv.db_pricing_delete, name='db_pricing_delete'),
    path('dashboard/pricing/<int:pk>/toggle/',                dv.db_pricing_toggle, name='db_pricing_toggle'),
    path('dashboard/pricing/<int:pk>/move/<str:direction>/',  dv.db_pricing_move,   name='db_pricing_move'),

    # ── Demo Bookings ──────────────────────────────────────
    path('dashboard/bookings/', dv.db_bookings, name='db_bookings'),

    # ── Contact Submissions ─────────────────────────────────
    path('dashboard/contacts/', dv.db_contacts, name='db_contacts'),
]
