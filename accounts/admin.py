from django.contrib import admin
from accounts.models import BlogPost, Profile, Classification


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_time')
    list_filter = ("publish_time", "author")
    search_fields = ("title", "content")
    #raw_id_fields = ("author",)
    #date_hierarchy = "publish_time"
    ordering = ("-publish_time", "author")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_no", "api_key", "secret_no")


class ClassificationAdmin(admin.ModelAdmin):
    list_display = ("class_name", "class_script")


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Classification, ClassificationAdmin)
