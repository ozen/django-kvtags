===============
django-tagging
===============

Multilingual tagging system for Django.

TagManager
============

django-tagging is meant to be used via TagManager.
First, add TagManager to your model to which you will add tags;

::

    class Fabric(TimeStamped):
        # your stuff
        objects = models.Manager()
        tags = TagManager()


Then use it to add, remove and filter tags.

TODO: methods
--------------


Using API
============

django-tagging supports `tastypie`_.

TagResource
-------------

::

    # urls.py
    from tagging.api import TagResource

    tag_resource = TagResource()

    urlpatterns = patterns('',
        # The normal jazz here...
        (r'^api/', include(tag_resource.urls)),
    )

or

::

    # urls.py
    from tastypie.api import Api
    from tagging.api import TagResource

    your_api = Api(api_name='v1')
    # Your other resources
    your_api.register(TagResource())


    urlpatterns = patterns('',
        # The normal jazz here...
        (r'^api/', include(your_api.urls)),
    )


TaggedItemResource
------------------

TaggedItem has generic relation to your models. If you don't need to resolve the relations,
you can include TaggedItemResource to your API just as you include TagResource.

However, if you want to resolve generic relations, you should create a new class based on
TaggedItemResource by yourself. Then, add the new class to the API as usual.

Example:

::

    # urls.py
    from tagging.api import TaggedItemResource
    from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
    from yourapp.models import Spam, Egg
    from yourapp.api import SpamResource, EggResource

    class MyTaggedItemResource(TaggedItemResource):
        content_object = GenericForeignKeyField({
            Spam: SpamResource,
            Egg: EggResource
        }, 'content_object')



.. _tastypie: https://django-tastypie.readthedocs.org/en/latest/