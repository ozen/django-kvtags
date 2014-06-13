from tastypie.resources import ModelResource
from tastypie.constants import ALL

from tagging.models import *


class TagResource(ModelResource):
    class Meta:
        queryset = Tag.objects.all()
        filtering = {
            "tag_group": ALL,
            "key": ALL,
            "value": ALL
        }


class TaggedItemResource(ModelResource):
    class Meta:
        queryset = TaggedItem.objects.all()
        resource_name = 'tagged-item'