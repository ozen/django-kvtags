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


class TagGroup(TimeStamped):
    key = models.CharField(max_length=50, db_index=True)

    def __unicode__(self):
        return u"%s %d" % (self.key, self.pk)


class Tag(TimeStamped):
    """Defines generic tags.

    Provides tag_group and key fields to support intrarelated tags.

    Tags in the same group have the same tag_group value.
    Tags have keys based on their variations in their groups.
    tag_group and key pairs are unique in the table.
    """
    tag_group = models.ForeignKey(TagGroup, related_name='tags')
    key = models.CharField(max_length=50, db_index=True)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return u"%s (%s - %s)" % (self.value, self.key, self.tag_group)

    class Meta:
        unique_together = (('tag_group', 'key'),)


class TaggedItem(TimeStamped):
    """Binds tags with items.

    Uses Django Generic Relations to bind tags with any model.

    Uses tag_group of Tag for referencing to tags (not foreign key)
    to reduce the number of relations, i.e. only one TaggedItem
    exists for several tags in the same group.
    """
    tag_group = models.ForeignKey(TagGroup, related_name='items')
    object_id = models.IntegerField(db_index=True)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together = (('tag_group', 'object_id', 'content_type'),)

    def __unicode__(self):
        return u"%s (%s)" % (self.content_object, self.tag_group)
