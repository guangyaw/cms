from django.contrib import admin
from blogs.models import BlogPost, Classification

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publish_time')
    list_filter = ("publish_time", "author")
    search_fields = ("title", "content")
    #raw_id_fields = ("author",)
    #date_hierarchy = "publish_time"
    ordering = ("-publish_time", "author")


class ClassificationAdmin(admin.ModelAdmin):
    list_display = ("class_name", "class_script")


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Classification, ClassificationAdmin)
