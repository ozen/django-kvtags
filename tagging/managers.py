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
        parameters are not strict enough to provide uniqueness.

        :param obj: Item (generic) instance
        :param **kwargs: Tag lookup parameters
        """
        tag = Tag.objects.get(**kwargs)
        tagged = TaggedItem(tag_id=tag.tag_id, content_object=obj)
        tagged.save()

    def filter(self, obj, lang=None):
        """Returns a list of all tags bound with the obj.

        Attention: Does NOT return a QuerySet

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
        """Removes the tags matched by kwargs from obj.

        Throws MultipleObjectsReturned exception if lookup
        parameters are not strict enough to provide uniqueness.

        :param obj: Item (generic) instance
        :param **kwargs: Tag lookup parameters
        """
        tag = Tag.objects.get(**kwargs)
        ctype = ContentType.objects.get_for_model(obj)
        tagged = TaggedItem.objects.get(tag_id=tag.tag_id, content_type_id=ctype.id)
        tagged.delete()
