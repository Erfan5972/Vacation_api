from django.contrib import admin

from . import models


admin.site.register(models.Vacation)
admin.site.register(models.VacationResponse)