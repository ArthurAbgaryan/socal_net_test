from django.contrib import admin
from .models import Action

@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ['user', 'target','verb', 'date_created']
    list_filter = ('date_created',)
    search_fields = ('verb',)
# Register your models here.
