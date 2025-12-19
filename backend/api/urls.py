from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, PostLocaleViewSet,
    CategoryLocaleViewSet, TagLocaleViewSet,
    CommentViewSet, MediaAssetViewSet,
    PostManageViewSet, PostLocaleManageViewSet
)
from .auth_views import LoginView, RefreshView, LogoutView, MeView, CsrfTokenView, RegisterView
from .views_media import MediaUploadView
from .views_extra import FeedView, PostBySlugView, NavigationView, RelatedView, FeaturedView, SuggestView

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'post-locales', PostLocaleViewSet, basename='post-locales')
router.register(r'my-posts', PostManageViewSet, basename='my-posts')
router.register(r'my-post-locales', PostLocaleManageViewSet, basename='my-post-locales')
router.register(r'categories', CategoryLocaleViewSet, basename='categories')
router.register(r'tags', TagLocaleViewSet, basename='tags')
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'media', MediaAssetViewSet, basename='media')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login', LoginView.as_view()),
    path('auth/register', RegisterView.as_view()),
    path('auth/refresh', RefreshView.as_view()),
    path('auth/logout', LogoutView.as_view()),
    path('auth/me', MeView.as_view()),
    path('auth/csrf-token', CsrfTokenView.as_view()),
    path('media/upload', MediaUploadView.as_view()),
    path('feed', FeedView.as_view()),
    path('post', PostBySlugView.as_view()),
    path('navigation', NavigationView.as_view()),
    path('related', RelatedView.as_view()),
    path('featured', FeaturedView.as_view()),
    path('suggest', SuggestView.as_view()),
]
