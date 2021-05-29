from django.contrib import admin
from .admin import Realtor


class RealtorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'date_hired')
    list_display_list = ('id', 'name')
    search_fields = ('name')
    list_per_page = 25

admin.site.register(Realtor, RealtorAdmin)
