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

    @staticmethod
    def get_list(obj):
        c_type = ContentType.objects.get_for_model(obj)
        ret = []

        for item in TaggedItem.objects.filter(content_type=c_type, object_id=obj.id).values('tag'):
            tag = Tag.objects.prefetch_related('keyvalues').get(pk=item['tag'])
            ret.append(tag)

        return ret

    def get_serialized_list(self, obj):
        c_type = ContentType.objects.get_for_model(obj)

        if self.CACHE:
            tags = self.CACHE.get('tags')

            if tags is None:
                print "missed cache"
                tags = self.populate_tags_dictionary()
                self.CACHE.set('tags', tags)
            else:
                print "hit cache"
        else:
            tags = self.populate_tags_dictionary()

        ret = []
        for item in TaggedItem.objects.filter(content_type=c_type, object_id=obj.id).values('tag'):
            ret.append(tags[item['tag']])

        return ret

    @staticmethod
    def populate_tags_dictionary():
        tags = {}
        for tag in Tag.objects.select_related().prefetch_related('keyvalues').all():
            obj = {'id': tag.id, 'key': tag.key}
            for key_value in tag.keyvalues.all():
                obj[key_value.key] = key_value.value
            tags[tag.id] = obj
        return tags