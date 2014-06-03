from django.db import models
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.contenttypes.models import ContentType
from tagging.models import *


class TagManager(models.Manager):
    """Provides an interface to the tagging system

    Models that use tags should add a TagManager.

    Example:
        from tagging.managers import TagManager

    in the model:
        tags = TagManager()

    when using it:
        <model_class>.tags.get(<model_instance>)
    """
    def add(self, obj, **kwargs):
        """Adds the tags matched by kwargs to obj.

        Throws MultipleObjectsReturned exception if lookup
        paramaters are not strict enough to provide uniqueness.

        :param obj: Item (generic) instance
        :**kwargs: Tag lookup parameters
        """
        tags = Tag.objects.get(**kwargs)
        for tag in tags:
            tagged = TaggedItem(tag_id=tag.tag_id, content_object=obj)
            tagged.save()

    def get(self, obj, lang=None):
        """Returns a list of all tags binded with the obj.

        If the optional lang parameter is provided, returns
        only the tags in given language.

        :param obj: Item (generic) instance
        :param lang: Language code (Optional)
        """
        all_tags = []
        ctype = ContentType.objects.get_for_model(obj)
        for tagged_item in TaggedItem.objects.filter(content_type_id=ctype.id, object_id=obj.id):
            if lang is None:
                all_tags += tagged_item.get_tags()
            else:
                all_tags += tagged_item.get_tags(lang=lang)
        return all_tags

    def remove(self, obj, **kwargs):
        """Removes the tags matched by kwargs to obj.

        Throws MultipleObjectsReturned exception if lookup
        paramaters are not strict enough to provide uniqueness.

        :param obj: Item (generic) instance
        :**kwargs: Tag lookup parameters
        """
        tags = Tag.objects.get(**kwargs)
        for tag in tags:
            tagged = TaggedItem(tag_id=tag.tag_id, content_object=obj)
            tagged.delete()
