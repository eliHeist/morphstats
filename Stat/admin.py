from django.contrib import admin

from Stat.models import Service, Stat

# Register your models here.
class InlineService(admin.StackedInline):
    model = Service
    max_num = 3
    extra = 3

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    inlines = [InlineService]