from django.contrib import admin
from .models import (User, HealthResults,
                     MobileImages,
                     Processes, Backup,
                     Feedback)


# Register your models here.
admin.site.register(User)
admin.site.register(MobileImages)
admin.site.register(HealthResults)
admin.site.register(Processes)
admin.site.register(Backup)
admin.site.register(Feedback)
# admin.site.register(UserMobile)

