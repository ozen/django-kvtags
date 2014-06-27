from tagging.models import *


class TagManager(models.Manager):
    """Provides an interface to the tagging system

    Models that use tags should add a TagManager.
    """

    @staticmethod
    def add(obj, **kwargs):
        """Adds the tags matched by kwargs to obj along with their groups.

        Throws MultipleObjectsReturned exception if lookup
        parameters are not strict enough to provide uniqueness.

        :param obj: Item (generic) instance
        :param **kwargs: Tag lookup parameters
        """
        tag = Tag.objects.get(**kwargs)
        c_type = ContentType.objects.get_for_model(obj)
        TaggedItem.objects.get_or_create(tag_group=tag.tag_group, content_type=c_type, object_id=obj.id)

    @staticmethod
    def add_group(obj, **kwargs):
        """Adds the tag groups matched by kwargs to obj.

        Throws MultipleObjectsReturned exception if lookup
        parameters are not strict enough to provide uniqueness.

        :param obj: Item (generic) instance
        :param **kwargs: TagGroup lookup parameters
        """
        group = TagGroup.objects.get(**kwargs)
        c_type = ContentType.objects.get_for_model(obj)
        TaggedItem.objects.get_or_create(tag_group=group, content_type=c_type, object_id=obj.id)


    @staticmethod
    def filter_tags(obj, **kwargs):
        """Returns QuerySet of tags bound with the obj.

        :param obj: Item (generic) instance
        :param **kwargs: Tag lookup parameters
        """
        c_type = ContentType.objects.get_for_model(obj)
        groups = TaggedItem.objects.filter(content_type=c_type, object_id=obj.id).values('tag_group')
        return Tag.objects.filter(tag_group__in=groups, **kwargs)

    @staticmethod
    def filter_groups(obj, **kwargs):
        """Returns QuerySet of groups bound with the obj.

        :param obj: Item (generic) instance
        :param **kwargs: TagGroup lookup parameters
        """
        c_type = ContentType.objects.get_for_model(obj)
        groups = TaggedItem.objects.filter(content_type=c_type, object_id=obj.id).values('tag_group')
        return TagGroup.objects.filter(pk__in=groups, **kwargs)

    @staticmethod
    def remove(obj, **kwargs):
        """Removes the tags matched by kwargs from obj along with their groups.

        Throws MultipleObjectsReturned exception if lookup
        parameters are not strict enough to provide uniqueness.

        :param obj: Item (generic) instance
        :param **kwargs: Tag lookup parameters
        """
        tag = Tag.objects.get(**kwargs)
        c_type = ContentType.objects.get_for_model(obj)
        try:
            tagged = TaggedItem.objects.get(tag_group=tag.tag_group, content_type=c_type)
            tagged.delete()
        except TaggedItem.DoesNotExist:
            pass

    @staticmethod
    def remove_group(obj, **kwargs):
        """Removes the tags matched by kwargs from obj along with their groups.

        Throws MultipleObjectsReturned exception if lookup
        parameters are not strict enough to provide uniqueness.

        :param obj: Item (generic) instance
        :param **kwargs: TagGroup lookup parameters
        """
        group = TagGroup.objects.get(**kwargs)
        c_type = ContentType.objects.get_for_model(obj)
        try:
            tagged = TaggedItem.objects.get(tag_group=tag_group, content_type=c_type)
            tagged.delete()
        except TaggedItem.DoesNotExist:
            pass