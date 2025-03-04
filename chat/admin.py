from django.contrib import admin

# Register your models here.
from .models import Thread, Message


class ThreadAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "updated")


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "sender", "thread", "created", "is_read")
    list_filter = ("is_read",)


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
