from django.db import models
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now


class TimeStamped(models.Model):
    """Provides created and updated timestamps on models."""

    created = models.DateTimeField(null=True, editable=False)
    updated = models.DateTimeField(null=True, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        _now = now()
        self.updated = _now
        if not self.id:
            self.created = _now
        super(TimeStamped, self).save(*args, **kwargs)


class Tag(TimeStamped):
    """Defines generic tags.

    Provides tag_group and key fields to support intra-related tags.

    Tags in the same group have the same tag_group value.
    Tags have keys based on their variations in their groups.
    tag_group and key pairs are unique in the table.
    """
    tag_group = models.IntegerField()
    key = models.SlugField(db_index=True)
    value = models.TextField()

    def __unicode__(self):
        return self.value

    def save(self, *args, **kwargs):
        if self.tag_group is None:
            # auto increment tag_group if it is not present
            try:
                top = Tag.objects.order_by('-tag_group')[0].tag_group
            except IndexError:
                top = 0
            self.tag_group = top + 1
        super(Tag, self).save(*args, **kwargs)

    class Meta:
        unique_together = (('tag_group', 'key'),)


class TaggedItem(TimeStamped):
    """Binds tags with items.

    Uses Django Generic Relations to bind tags with any model.

    Uses tag_group of Tag for referencing to tags (not foreign key)
    to reduce the number of relations, i.e. only one TaggedItem
    exists for several tags in the same group.
    """
    tag_group = models.IntegerField()
    object_id = models.IntegerField(db_index=True, null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    content_object = GenericForeignKey()

    class Meta:
        unique_together = (('tag_group', 'object_id', 'content_type'),)
