from django.contrib import admin

from contest import models

admin.site.register(models.Contest)
# admin.site.register(models.Participant)