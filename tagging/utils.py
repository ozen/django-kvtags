from django.core.exceptions import ObjectDoesNotExist
from tagging.models import Tag
import unicodecsv


def import_tags_csv(csv_file):
    """Imports tags from a csv file to the database.

    A file instance must be provided as an argument.
    File must be opened beforehand.

    The first row of the csv file is for language codes.
    Subsequent rows are tags.
    Each row corresponds to a tag with each field is a translation.

    :param csv_file: opened csv file instance
    """
    reader = unicodecsv.reader(csv_file, encoding='utf-8')
    langs = reader.next()

    for row in reader:
        tag_id = None
        new_tags = []

        for index, tag_value in enumerate(row):
            if tag_id is None:
                try:
                    obj = Tag.objects.get(lang=langs[index], value=tag_value)
                    tag_id = obj.tag_id
                except ObjectDoesNotExist:
                    obj = Tag(lang=langs[index], value=tag_value)
                    obj.save()
                    new_tags.append(obj)
                    tag_id = obj.tag_id
            else:
                Tag.objects.get_or_create(tag_id=tag_id, lang=langs[index], value=tag_value)

        for new_tag in new_tags:
            new_tag.tag_id = tag_id
            new_tag.save()
