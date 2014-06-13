# coding=utf-8
from django.test import TestCase
from .models import Item
from tagging.models import *
from tagging.utils import import_tags_csv
from django.core.exceptions import MultipleObjectsReturned
import os


class ImportCSVTestCase(TestCase):
    def test_import_csv(self):
        with open(os.path.join(os.path.dirname(__file__), 'test.csv'), 'rb') as csv_file:
            import_tags_csv(csv_file)
        self.assertEqual(Tag.objects.get(pk=1).tag_group, 1)
        self.assertEqual(Tag.objects.get(pk=2).tag_group, 1)
        self.assertEqual(Tag.objects.get(pk=3).tag_group, 1)
        self.assertEqual(Tag.objects.get(pk=4).tag_group, 2)
        self.assertEqual(Tag.objects.get(pk=5).tag_group, 2)
        self.assertEqual(Tag.objects.get(pk=1).key, 'en')
        self.assertEqual(Tag.objects.get(pk=2).key, 'tr')
        self.assertEqual(Tag.objects.get(pk=3).key, 'fr')
        self.assertEqual(Tag.objects.get(pk=4).key, 'en')
        self.assertEqual(Tag.objects.get(pk=5).key, 'tr')


class AddTagsTestCase(TestCase):
    fixtures = ['test_data1.json']

    def setUp(self):
        self.i = Item.objects.get(pk=1)

    def test_tag_add_ex1(self):
        with self.assertRaises(MultipleObjectsReturned):
            Item.tags.add(self.i, key='en')

    def test_tag_add_ex2(self):
        with self.assertRaises(MultipleObjectsReturned):
            Item.tags.add(self.i, value='mum')

    def test_tag_add(self):
        Item.tags.add(self.i, key='en', value='red')
        ctype = ContentType.objects.get_for_model(self.i)

        tag_group = TaggedItem.objects.filter(content_type_id=ctype.id, object_id=self.i.id)[0].tag_group
        tag = Tag.objects.get(tag_group=tag_group, key='en')
        self.assertEqual(tag.value, 'red')
        tag = Tag.objects.get(tag_group=tag_group, key='tr')
        self.assertEqual(tag.value, u'kırmızı')
        self.assertEqual(len(Item.tags.filter(self.i)), 3)

        # don't add same tag twice
        count = TaggedItem.objects.count()
        Item.tags.add(self.i, key='en', value='red')
        self.assertEqual(TaggedItem.objects.count(), count)

    def tearDown(self):
        del self.i


class RemoveTagsTestCase(TestCase):
    fixtures = ['test_data2.json']

    def setUp(self):
        self.i = Item.objects.get(pk=1)
        # we have to adjust content_type_id fields in test runtime
        ctype = ContentType.objects.get_for_model(Item)
        for tagged in TaggedItem.objects.all():
            tagged.content_type_id = ctype.id
            tagged.save()

    def test_tag_remove_ex1(self):
        with self.assertRaises(MultipleObjectsReturned):
            Item.tags.remove(self.i, key='en')

    def test_tag_remove_ex2(self):
        with self.assertRaises(MultipleObjectsReturned):
            Item.tags.remove(self.i, value='mum')

    def test_tag_remove(self):
        tag_group = Tag.objects.get(key='en', value='mum').tag_group
        Item.tags.remove(self.i, key='en', value='mum')
        self.assertEqual(TaggedItem.objects.filter(tag_group=tag_group).count(), 0)
        Item.tags.remove(self.i, key='en', value='mum')

    def tearDown(self):
        del self.i


class FilterTagsTestCase(TestCase):
    fixtures = ['test_data2.json']

    def setUp(self):
        self.i = Item.objects.get(pk=1)
        self.j = Item.objects.get(pk=2)
        # we have to adjust content_type_id fields in test runtime
        ctype = ContentType.objects.get_for_model(Item)
        for tagged in TaggedItem.objects.all():
            tagged.content_type_id = ctype.id
            tagged.save()

    def test_tag_filter(self):
        self.assertEqual(len(Item.tags.filter(self.i)), 6)
        self.assertEqual(Item.tags.filter(self.i, key='en')[0].value, 'mum')
        self.assertEqual(Item.tags.filter(self.i, key='tr')[1].value, 'mum')
        self.assertEqual(len(Item.tags.filter(self.j)), 6)
        self.assertEqual(Item.tags.filter(self.j, key='en')[0].value, 'red')
        self.assertEqual(Item.tags.filter(self.j, key='tr')[1].value, 'turuncu')

    def tearDown(self):
        del self.i
        del self.j