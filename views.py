from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from tagging.forms import ImportTagsForm
from tagging.utils import import_tags_csv

from django.utils.translation import ugettext as _
from django.contrib import messages


def import_tags(request):
    """Provides graphical interface to tagging.utils.import_tags_csv"""
    if request.method == 'POST':
        form = ImportTagsForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                import_tags_csv(request.FILES['file'])
                messages.success(request, _("Yahoo! The csv is fucking loaded nigga!"))
            except:
                messages.error(request, _("File is invalid!"))
        else:
            messages.error(request, _("File is invalid!"))
        return HttpResponseRedirect(reverse('tagging_import_tags'))
    else:
        form = ImportTagsForm()
    return render(request,  'import_tags.html', {'form': form})
