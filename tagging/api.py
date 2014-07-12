from tastypie.resources import ModelResource, Resource
from tastypie.constants import ALL
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie import fields
from tagging.models import *


class TagResource(ModelResource):
    keyvalues = fields.ToManyField('tagging.api.KeyValueResource', 'keyvalues', full=True)

    class Meta:
        queryset = Tag.objects.all()
        filtering = {
            "key": ALL
        }
        resource_name = 'tag'
        excludes = ['created', 'updated']
        include_resource_uri = False


class KeyValueResource(ModelResource):
    class Meta:
        queryset = KeyValue.objects.all()
        filtering = {
            "tag": ALL,
            "key": ALL,
            "value": ALL
        }
        resource_name = 'keyvalue'
        include_resource_uri = False


class TaggedItemResource(ModelResource):
    tag = fields.ForeignKey(TagResource, 'tag')

    class Meta:
        queryset = TaggedItem.objects.all()
        resource_name = 'tagged-item'