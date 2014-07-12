from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.contenttypes import generic
from tagging.models import *


admin.site.register(Tag)
admin.site.register(TaggedItem)