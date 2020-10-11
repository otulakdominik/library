from django.urls import path, re_path
from django.conf.urls import include
from . import views
from rest_framework import routers
from .viewsets import BookViewSet

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)

app_name = 'books'

urlpatterns = [
    path('list', views.BookListView.as_view(), name='list'),
    path('create', views.BookCreateView.as_view(), name='create'),
    re_path(r'^(?P<pk>\d+)/edit/$', views.BookUpdateView.as_view(), name='edit'),
    re_path(r'^(?P<pk>\d+)/del/$', views.BookDeleteView.as_view(), name='del'),
    path('create_author', views.AuthorCreateView.as_view(), name='create_author'),
    path('create_identifiers', views.IdentifiersCreateView.as_view(), name='create_identifiers'),
    path('search', views.SearchResultsView.as_view(), name='search_results'),
    path('data_search', views.DataSearchResultsView.as_view(), name='data_search_results'),
    path('search_api', views.BookSearchApiGoogle.as_view(), name='search_api'),
    path('api', include(router.urls), name='api'),
]
