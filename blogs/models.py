from django.db import models
from accounts.models import Profile
from datetime import date
#from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Classification(models.Model):
    class_name = models.CharField(max_length=40, default='')
    class_script = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.class_name


class BlogPost(models.Model):
    title = models.CharField(max_length=50, default='')
    content = RichTextUploadingField(max_length=300)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="blog_authors")
    class_item = models.ManyToManyField(Classification)
    publish_time = models.DateField(default=date.today)

    class Meta:
        ordering = ["-publish_time"]

    def __str__(self):
        return self.title