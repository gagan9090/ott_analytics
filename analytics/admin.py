from django.contrib import admin

# Register your models here.

from .models import User, Video, WatchSession

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'registration_date')
    search_fields = ('name', 'email')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'duration')
    list_filter = ('genre',)
    search_fields = ('title',)


@admin.register(WatchSession)
class WatchSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'video', 'start_time', 'end_time', 'session_duration', 'device_type', 'is_rewatch')
    list_filter = ('device_type', 'is_rewatch', 'video__genre')
    search_fields = ('user__name', 'video__title')
