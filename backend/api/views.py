from rest_framework import viewsets, permissions
from django.utils import timezone
from blog.models import Post, PostLocale, PostStatus
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

    def get_permissions(self):
        if getattr(self, "action", None) == "create":
            return [permissions.AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = self.request.user if self.request.user and self.request.user.is_authenticated else None
        serializer.save(user=user, status="approved")


class PostManageViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = PostFilterSet

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by("-published_at", "-created_at")

    def perform_create(self, serializer):
        status = serializer.validated_data.get("status")
        published_at = serializer.validated_data.get("published_at")
        if status == PostStatus.PUBLISHED and not published_at:
            serializer.save(author=self.request.user, published_at=timezone.now())
        else:
            serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.author_id != self.request.user.id:
            raise permissions.PermissionDenied("not_owner")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author_id != self.request.user.id:
            raise permissions.PermissionDenied("not_owner")
        instance.delete()


class PostLocaleManageViewSet(viewsets.ModelViewSet):
    serializer_class = PostLocaleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = PostLocaleFilterSet

    def get_queryset(self):
        return PostLocale.objects.select_related("post").filter(post__author=self.request.user).order_by("-post__published_at", "-post__created_at")

    def perform_create(self, serializer):
        post = serializer.validated_data.get("post")
        if not post or post.author_id != self.request.user.id:
            raise permissions.PermissionDenied("not_owner")
        serializer.save()

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.post.author_id != self.request.user.id:
            raise permissions.PermissionDenied("not_owner")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.post.author_id != self.request.user.id:
            raise permissions.PermissionDenied("not_owner")
        instance.delete()


class MediaAssetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MediaAsset.objects.all().order_by("-created_at")
    serializer_class = MediaAssetSerializer
    permission_classes = [permissions.AllowAny]
