from django.contrib import admin

from facilitators.models import Facilitator, Tag

# Register your models here.
admin.site.register(Facilitator)
admin.site.register(Tag)