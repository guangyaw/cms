from django.contrib.auth.models import User
from django.db import models
from datetime import date
#from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=40, default='', blank=True)


class Classification(models.Model):
    class_name = models.CharField(max_length=40, default='')
    class_script = models.CharField(max_length=100, default='', blank=True)


class BlogPost(models.Model):
    title = models.CharField(max_length=50, default='')
    content = RichTextUploadingField(max_length=300)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    class_item = models.ManyToManyField(Classification)
    publish_time = models.DateField(default=date.today)

    class Meta:
        ordering = ["-publish_time"]

    def __str__(self):
        return self.title
