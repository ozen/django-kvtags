import unicodecsv

from tagging.models import *


def import_tags_csv(csv_file):
    """Imports tags from a csv file to the database.

    A file instance must be provided as an argument.
    File must be opened beforehand.

    The first row of the csv file is for keys.
    Subsequent rows are values.

    :param csv_file: opened csv file instance
    """
    reader = unicodecsv.reader(csv_file, encoding='utf-8')
    group_key = reader.next()[0]
    tag_keys = reader.next()

    for row in reader:
        tag_group = None
        new_tags = []

        for index, tag_value in enumerate(row):
            if tag_group is None:
                try:
                    tag = Tag.objects.get(key=tag_keys[index], value=tag_value, tag_group__key=group_key)
                    tag_group = tag.tag_group
                except Tag.DoesNotExist:
                    obj = Tag(key=tag_keys[index], value=tag_value)
                    new_tags.append(obj)
            else:
                Tag.objects.get_or_create(tag_group=tag_group, key=tag_keys[index], value=tag_value)

        if tag_group is None:
            tag_group = TagGroup.objects.create(key=group_key)

        for new_tag in new_tags:
            new_tag.tag_group = tag_group
            new_tag.save()
