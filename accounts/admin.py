from django.contrib import admin
from accounts.models import BlogPost, Profile


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_time')
    list_filter = ("author", "publish_time")
    search_fields = ("title", "content")
    ordering = ("-publish_time", "author")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("phone_no", "user")


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Profile, ProfileAdmin)
