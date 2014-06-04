from django.db import models
from tagging.managers import TagManager


class Item(models.Model):
    name = models.CharField(max_length=50)

    objects = models.Manager()
    tags = TagManager()

    def __unicode__(self):
        return self.name