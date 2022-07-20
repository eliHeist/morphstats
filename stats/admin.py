from django.contrib import admin

from stats.models import Day, Group, Service

# Register your models here.
# admin.site.register(Day)
# admin.site.register(Service)
admin.site.register(Group)

class InlineService(admin.StackedInline):
    model = Service
    max_num = 3

@admin.register(Day)
class SundayStats(admin.ModelAdmin):
    inlines = [InlineService]


# admin.site.register(Day, SundayStats)