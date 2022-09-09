from django.contrib import admin
from . import models



@admin.register(models.Notes)
class NotesAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


