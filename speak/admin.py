from django.contrib import admin
from django.utils.html import format_html

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Record
class RecordAdmin(admin.ModelAdmin):

    def audio_tag(self, obj):
        return format_html('<audio controls="" src="{}"></audio>'.format(obj.audio.url))

    audio_tag.short_description = 'Audio'

    list_display = ('id', 'utterance', 'gender', 'age', 'ethnic', 'dialect', 'count_good', 'count_bad')
    search_fields = ['code', 'utterance', 'gender', 'age', 'ethnic', 'dialect',]
  
admin.site.register(Record, RecordAdmin)


from .models import Utterance
class UtteranceResource(resources.ModelResource):
    class Meta:
        model = Utterance

class UtteranceAdmin(ImportExportModelAdmin):
    list_display = ("code", "text", 'count', 'active')
    list_filter = ("active",)
    search_fields = ['text']
    resource_class = UtteranceResource
admin.site.register(Utterance, UtteranceAdmin)

from .models import Age
class AgeResource(resources.ModelResource):
    class Meta:
        model = Age

class AgeAdmin(ImportExportModelAdmin):
    list_display = ("code", "category", 'detail', 'count')
    resource_class = AgeResource
admin.site.register(Age, AgeAdmin)

from .models import Ethnic
class EthnicResource(resources.ModelResource):    
    class Meta:
        model = Ethnic

class EthnicAdmin(ImportExportModelAdmin):
    list_display = ("code", "category", 'detail', 'count')
    resource_class = EthnicResource
admin.site.register(Ethnic, EthnicAdmin)

from .models import Dialect
class DialectResource(resources.ModelResource):
    class Meta:
        model = Dialect

class DialectAdmin(ImportExportModelAdmin):
    list_display = ("code", "category", 'detail', 'count')
    resource_class = DialectResource
admin.site.register(Dialect, DialectAdmin)

from .models import Gender

class GenderAdmin(admin.ModelAdmin):
    list_display = ("code",  'category', 'count')
admin.site.register(Gender, GenderAdmin)
