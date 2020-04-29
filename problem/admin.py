from django.contrib import admin

# Register your models here.
from problem import models

admin.site.register(models.Problem)
admin.site.register(models.ProblemTag)
