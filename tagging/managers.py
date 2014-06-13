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
    @staticmethod
    def add(obj, **kwargs):
        """Adds the tags matched by kwargs to obj.

        Throws MultipleObjectsReturned exception if lookup
        parameters are not strict enough to provide uniqueness.

        :param obj: Item (generic) instance
        :param **kwargs: Tag lookup parameters
        """
        tag = Tag.objects.get(**kwargs)
        c_type = ContentType.objects.get_for_model(obj)
        TaggedItem.objects.get_or_create(tag_group=tag.tag_group, content_type_id=c_type.id, object_id=obj.id)

    @staticmethod
    def filter(obj, **kwargs):
        """Returns QuerySet of all tags bound with the obj.

        If the optional lang parameter is provided, returns
        only the tags in given language.

        :param obj: Item (generic) instance
        :param **kwargs: Tag lookup parameters
        """
        c_type = ContentType.objects.get_for_model(obj)
        items = TaggedItem.objects.filter(content_type_id=c_type.id, object_id=obj.id).values('tag_group')
        return Tag.objects.filter(tag_group__in=items, **kwargs)

    @staticmethod
    def remove(obj, **kwargs):
        """Removes the tags matched by kwargs from obj.

        Throws MultipleObjectsReturned exception if lookup
        parameters are not strict enough to provide uniqueness.

        :param obj: Item (generic) instance
        :param **kwargs: Tag lookup parameters
        """
        tag = Tag.objects.get(**kwargs)
        c_type = ContentType.objects.get_for_model(obj)
        try:
            tagged = TaggedItem.objects.get(tag_group=tag.tag_group, content_type_id=c_type.id)
            tagged.delete()
        except TaggedItem.DoesNotExist:
            pass
