from rest_framework import viewsets, permissions
from blog.models import Post, PostLocale
from taxonomy.models import CategoryLocale, TagLocale
from comments.models import Comment
from media.models import MediaAsset
from .serializers import (
    PostSerializer, PostLocaleSerializer, PostLocaleDetailSerializer,
    CategoryLocaleSerializer, TagLocaleSerializer,
    CommentSerializer, MediaAssetSerializer
)
from .filters import (
    PostFilterSet, PostLocaleFilterSet,
    CategoryLocaleFilterSet, TagLocaleFilterSet,
    CommentFilterSet
)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Post.objects.all().order_by("-published_at")
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = PostFilterSet

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get("status")
        locale = self.request.query_params.get("locale")
        author = self.request.query_params.get("author")
        is_featured = self.request.query_params.get("is_featured")
        if status:
            qs = qs.filter(status=status)
        if author:
            qs = qs.filter(author_id=author)
        if is_featured in ("true", "1"):
            qs = qs.filter(is_featured=True)
        if locale:
            qs = qs.prefetch_related("locales").filter(locales__locale=locale)
        return qs


class PostLocaleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PostLocale.objects.select_related("post").all().order_by("-post__published_at")
    permission_classes = [permissions.AllowAny]
    filterset_class = PostLocaleFilterSet

    def get_serializer_class(self):
        if getattr(self, "action", None) == "retrieve":
            return PostLocaleDetailSerializer
        return PostLocaleSerializer


class CategoryLocaleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoryLocale.objects.select_related("category").all()
    serializer_class = CategoryLocaleSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = CategoryLocaleFilterSet


class TagLocaleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TagLocale.objects.select_related("tag").all()
    serializer_class = TagLocaleSerializer
    permission_classes = [permissions.AllowAny]
    filterset_class = TagLocaleFilterSet


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related("post", "user").all().order_by("created_at")
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_class = CommentFilterSet


class MediaAssetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MediaAsset.objects.all().order_by("-created_at")
    serializer_class = MediaAssetSerializer
    permission_classes = [permissions.AllowAny]
