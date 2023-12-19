from django.contrib import admin

from support.models import Contact, Service

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    '''Admin View for Contact'''

    list_display = ('name', 'email', 'subject', 'date_sent', 'date_updated', 'is_viewed')
    list_filter = ('date_sent',)
    
    # readonly_fields = ('',)
    search_fields = ('name', 'email', )
    date_hierarchy = 'date_sent'
    ordering = ('-pk',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    '''Admin View for Service'''

    list_display = ('subject',  'slug', 'date_sent', 'date_updated')
    list_filter = ('date_sent',)
    
    search_fields = ('subject',)
    date_hierarchy = 'date_sent'
    ordering = ('-pk',)