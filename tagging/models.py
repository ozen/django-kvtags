from django.db import models
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Tag(models.Model):
    """Defines generic tags.

    Provides tag_id and lang fields with tags to support
    translations into different languages.
    Each translation of a tag is a distinct Tag instance.

    Translations of the same tag have the same tag_id.
    Tags have lang code based on their languages.
    tag_id and lang pairs are unique in the table.
    """
    tag_id = models.IntegerField()
    lang = models.SlugField(db_index=True)
    value = models.TextField()

    def __unicode__(self):
        return self.value

    def save(self, *args, **kwargs):
        if self.tag_id is None:
            # auto increment tag_id if it is not present
            try:
                top = Tag.objects.order_by('-tag_id')[0].tag_id
            except IndexError:
                top = 0
            self.tag_id = top + 1
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('tag_id', 'lang'),)


class TaggedItem(models.Model):
    """Binds Tag with an item.

    Uses Django Generic Relations to bind tags with any model.

    Uses tag_id of Tag to reference to tags (not foreign key)
    to reduce the number of relations, i.e. only one TaggedItem
    exists for several translations of a tag of an item.
    """
    tag_id = models.IntegerField()
    object_id = models.IntegerField(db_index=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    content_object = GenericForeignKey()

    def get_tags(self, **kwargs):
        return Tag.objects.filter(tag_id=self.tag_id, **kwargs)

    def get_tag(self, lang=None):
        if lang is None:
            try:
                return Tag.objects.filter(tag_id=self.tag_id)[0]
            except:
                return None
        else:
            try:
                return Tag.objects.get(tag_id=self.tag_id, lang=lang)
            except:
                return None