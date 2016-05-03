# -*- coding: iso-8859-1 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordResetForm
from django.contrib.auth.views import password_change, password_reset, logout
from django.conf.urls.static import static
from stove import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
     url(r'^admin/', include(admin.site.urls)),
     url(r'^admin/demographics/$',views.demographics,name='demographics'),
     url(r'^admin/profiler/$',views.profiler,name='profiler'),
     url(r'^', include('stove.urls')),
     url(r'^accounts/password_change/$', password_change, {'password_change_form': AdminPasswordChangeForm}, name="password_change"),
     url(r'^accounts/password_reset/$', password_reset, {'password_reset_form': PasswordResetForm}, name="password_reset"),
     url(r'^accounts/logout/$', logout, {'next_page': '/'}),
     url(r'^accounts/', include('django.contrib.auth.urls', namespace='auth')),
     url(r'^accounts/', include('django.contrib.auth.urls')),
     url('', include('social.apps.django_app.urls', namespace='social')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

