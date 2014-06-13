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
        """Returns QuerySet of all tags bound with the obj.

        If the optional lang parameter is provided, returns
        only the tags in given language.

        :param obj: Item (generic) instance
        :param lang: Language code (Optional)
        """
        ctype = ContentType.objects.get_for_model(obj)
        items = TaggedItem.objects.filter(content_type_id=ctype.id, object_id=obj.id).values('tag_id')
        if lang is None:
            return Tag.objects.filter(tag_id__in=items)
        else:
            return Tag.objects.filter(tag_id__in=items, lang=lang)

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
