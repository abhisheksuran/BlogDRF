from django.contrib import admin
from core import models

# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Blog)
admin.site.register(models.Tag)
admin.site.register(models.UserComment)
#admin.site.register(models.UserReply)
admin.site.register(models.UserProfile)
