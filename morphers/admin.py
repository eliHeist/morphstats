from django.contrib import admin

from morphers.models import Grade, Level, Morpher, Residence, School

# Register your models here.
admin.site.register(Level)
admin.site.register(Grade)
admin.site.register(Residence)

@admin.register(Morpher)
class MorphAdmin(admin.ModelAdmin):
    list_display = ('name','grade','residence')
    list_filter = ('grade','school','residence')
    search_fields = ('name',)
    

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)