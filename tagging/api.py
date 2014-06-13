from tagging.models import *
from tastypie.resources import ModelResource
from tastypie import fields


class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()


class TaggedItemResource(ModelResource):
    class Meta:
        queryset = TaggedItem.objects.all()
