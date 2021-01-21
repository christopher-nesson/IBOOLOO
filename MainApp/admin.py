from django.contrib import admin

from .models import Topic, Theme, Diary


# Register your models here.
@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    pass


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    pass
