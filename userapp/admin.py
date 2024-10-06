from django.contrib import admin

# Register your models here.
from userapp.models import *


class PeopleAdmin(admin.ModelAdmin):
    list_display=("username","email","password","confirm_password")

class Url_linkAdmin(admin.ModelAdmin):
    list_display=("user","original_url","short_code","short_url","qr_code_url","visit_count","created_at")

admin.site.register(Short_url,Url_linkAdmin)
admin.site.register(People,PeopleAdmin)