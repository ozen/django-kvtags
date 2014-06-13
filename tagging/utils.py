import unicodecsv

from tagging.models import Tag


def import_tags_csv(csv_file):
    """Imports tags from a csv file to the database.

    A file instance must be provided as an argument.
    File must be opened beforehand.

    The first row of the csv file is for keys.
    Subsequent rows are values.

    :param csv_file: opened csv file instance
    """
    reader = unicodecsv.reader(csv_file, encoding='utf-8')
    keys = reader.next()

    for row in reader:
        tag_group = None
        new_tags = []

        for index, tag_value in enumerate(row):
            if tag_group is None:
                try:
                    obj = Tag.objects.get(key=keys[index], value=tag_value)
                    tag_group = obj.tag_group
                except Tag.DoesNotExist:
                    obj = Tag(key=keys[index], value=tag_value)
                    obj.save()
                    new_tags.append(obj)
                    tag_group = obj.tag_group
            else:
                Tag.objects.get_or_create(tag_group=tag_group, key=keys[index], value=tag_value)

        for new_tag in new_tags:
            new_tag.tag_id = tag_group
            new_tag.save()
