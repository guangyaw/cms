from django.contrib import admin
from accounts.models import BlogPost, Profile


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'author')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Profile, ProfileAdmin)