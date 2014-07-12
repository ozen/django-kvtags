from django.core.cache import get_cache
from tagging.models import *


class TagManager(models.Manager):
    """Provides an interface to the tagging system"""

    def __init__(self, cache=None):
        super(TagManager, self).__init__()
        if cache:
            self.CACHE = get_cache(cache)
        else:
            self.CACHE = None

    @staticmethod
    def add(obj, **kwargs):
        c_type = ContentType.objects.get_for_model(obj)
        for tag in Tag.objects.filter(**kwargs):
            TaggedItem.objects.get_or_create(tag=tag, content_type=c_type, object_id=obj.id)

    @staticmethod
    def add_by_keyvalue(obj, **kwargs):
        c_type = ContentType.objects.get_for_model(obj)
        for keyvalue in KeyValue.objects.filter(**kwargs):
            TaggedItem.objects.get_or_create(tag=keyvalue.tag, content_type=c_type, object_id=obj.id)

    @staticmethod
    def remove(obj, **kwargs):
        c_type = ContentType.objects.get_for_model(obj)
        for tag in Tag.objects.filter(**kwargs):
            try:
                item = TaggedItem.objects.get(tag=tag, content_type=c_type, object_id=obj.id)
                item.delete()
            except TaggedItem.DoesNotExist:
                pass

    @staticmethod
    def remove_by_keyvalue(obj, **kwargs):
        c_type = ContentType.objects.get_for_model(obj)
        for keyvalue in KeyValue.objects.filter(**kwargs):
            try:
                item = TaggedItem.objects.get(tag=keyvalue.tag, content_type=c_type, object_id=obj.id)
                item.delete()
            except TaggedItem.DoesNotExist:
                pass

    def get_list(self, obj):
        c_type = ContentType.objects.get_for_model(obj)
        tags = []

        for item in TaggedItem.objects.filter(content_type=c_type, object_id=obj.id).values('tag'):
            if self.CACHE:
                tag = self.CACHE.get('tag_%s' % item.tag.pk, None)
                if tag is None:
                    tag = Tag.objects.prefetch_related('keyvalues').get(pk=item.tag.pk)
                    self.CACHE.set('tag_%s' % item.tag.pk, tag)
            else:
                tag = Tag.objects.prefetch_related('keyvalues').get(pk=item.tag.pk)

            tags.append(tag)

        return tags
