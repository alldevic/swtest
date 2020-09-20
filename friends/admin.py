from django.contrib import admin

from .models import Invite


@admin.register(Invite)
class InviteAdmin(admin.ModelAdmin):
    readonly_fields = ("date_created", "date_confirmed")
    list_display = ('pk', 'from_user', 'to_user', 'confirmed')
    search_fields = ('from_user', 'to_user')
    list_filter = ('from_user', 'to_user')
