from django.urls import path, include
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

import snippets.views as views
from rest_framework.urlpatterns import format_suffix_patterns

snippet_list = views.SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

snippet_detail = views.SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

snippet_highlight = views.SnippetViewSet.as_view({
    'get': 'highlight',
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = views.UserViewSet.as_view({
    'get': 'list',
})

user_detail = views.UserViewSet.as_view({
    'get': 'retrieve',
})

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet, basename='snippet')
router.register(r'users', views.UserViewSet, basename='user')
# 첫 인수 = url endpoint, basename은 뭐지?

urlpatterns = [
    path('', include(router.urls)),
]

# urlpatterns = [
#     path('', views.api_root),
#     path('snippets/', snippet_list, name='snippet-list'),
#     path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
#     path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
#     path('users/', user_list, name='user-list'),
#     path('users/<int:pk>/', user_detail, name='user-detail'),
# ]

# urlpatterns = format_suffix_patterns(urlpatterns)
