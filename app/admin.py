from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from app import models as model
from django.contrib.admin.widgets import AutocompleteSelect
from django.db import models
# Register your models here.

@admin.register(model.Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ('stage_name', 'parent', 'slug', 'stage_index')