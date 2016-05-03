# -*- coding: iso-8859-1 -*-
from django.contrib import admin
from .models import *
import csv
from django.http import HttpResponse


class UserProfileAdmin(admin.ModelAdmin):
    """The page that allows administrators to add/modify user profiles."""

    list_display = ['user', 'postcode', 'dateOfBirth', 'gender']
    search_fields = ['user']
    readonly_fields = ['user']
    actions = ['download_csv']
    # now the download_csv is an action that the admin can perform

    def download_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="data.csv"'

        CATEGORY_CHOICES = ['Other gender or prefer not to disclose', 'Male', 'Female']

        writer = csv.writer(response)
        writer.writerow(['First name', 'Last name', 'Postcode', 'Date of birth', 'Gender'])
        for obj in UserProfile.objects.all():
            writer.writerow([obj.user.first_name, obj.user.last_name, obj.postcode, obj.dateOfBirth, CATEGORY_CHOICES[obj.gender]])
        return response

    download_csv.short_description = "Download CSV file for selected stats."


class PreferenceAdmin(admin.ModelAdmin):
    pass


class SubPreferenceAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    """The page that allows administrators to add/modify events."""

    list_display = ('name', 'startDate', 'category')
    list_filter = ('startDate',)
    date_hierarchy = 'startDate'
    ordering = ('-startDate',)
    fields = ('name', 'category', 'startDate', 'endDate', 'location', 'info', 'caterTo', 'picture')


class EventCategoryAdmin(admin.ModelAdmin):
    pass


class CafeCatAdmin(admin.ModelAdmin):
    pass


class CafeItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Preference, PreferenceAdmin)
admin.site.register(SubPreference, SubPreferenceAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventCategory, EventCategoryAdmin)
admin.site.register(CafeCategory, CafeCatAdmin)
admin.site.register(CafeItem, CafeItemAdmin)
