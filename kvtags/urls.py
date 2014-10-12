from django.conf.urls import url
from kvtags import views


urlpatterns = [
    url(r'^import-tags/$', views.import_tags, name='tagging_import_tags'),
]
