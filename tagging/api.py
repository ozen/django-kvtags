from tastypie.resources import ModelResource, Resource
from tastypie.constants import ALL
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie import fields

from tagging.models import *


class TagGroupResource(ModelResource):
    tags = fields.ToManyField('tagging.api.TagResource', 'tags', full=True)

    class Meta:
        queryset = TagGroup.objects.all()
        filtering = {
            "key": ALL
        }
        resource_name = 'tag-group'
        excludes = ['created', 'updated']
        include_resource_uri = False


class TagResource(ModelResource):
    # tag_group = fields.ForeignKey(TagGroupResource, 'tag_group')

    class Meta:
        queryset = Tag.objects.all()
        filtering = {
            "tag_group": ALL,
            "key": ALL,
            "value": ALL
        }
        excludes = ['created', 'updated']
        include_resource_uri = False


class TaggedItemResource(ModelResource):
    tag_group = fields.ForeignKey(TagGroupResource, 'tag_group')

    class Meta:
        queryset = TaggedItem.objects.all()
        resource_name = 'tagged-item'