from django.contrib import admin

from morphers.models import Grade, Level, Morpher, Residence, School

# Register your models here.
admin.site.register(Level)
admin.site.register(Grade)
admin.site.register(Residence)
admin.site.register(School)

class MorphAdmin(admin.ModelAdmin):
    list_filter = ('grade',)
    
admin.site.register(Morpher, MorphAdmin)