from django.contrib import admin
from accounts.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_no", "api_key", "secret_no")


admin.site.register(Profile, ProfileAdmin)
