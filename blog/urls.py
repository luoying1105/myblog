from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from .feeds import LatestPostsFeed

urlpatterns = [
    # post views
    url(r'^$', views.post_list, name='post_list'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list,
        name='post_list_by_tag'),

    # url(r'^$', views.PostListView.as_view(), name='post_list'),,
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/vote/$',
        views.detai_vote,
        name='vote'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share,
        name='post_share'),

    url(r'^(?P<category_slug>[-\w]+)/$',
        views.post_list,
        name='post_list_by_category'),
    url(r'^feed/$', LatestPostsFeed(), name='post_feed'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
