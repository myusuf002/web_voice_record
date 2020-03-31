from django.contrib import admin

from .models import Language
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'beam_width', 'lm_alpha', 'lm_beta','active')
    search_fields = ['code', 'name']
  
admin.site.register(Language, LanguageAdmin)
