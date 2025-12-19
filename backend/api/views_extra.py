from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count
from blog.models import PostLocale, PostStatus
from taxonomy.models import CategoryLocale, TagLocale
from .serializers import FeedItemSerializer, PostLocaleDetailSerializer
import logging
logger = logging.getLogger(__name__)


class FeedView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        locale = request.query_params.get("locale")
        logger.info("FeedView locale=%s user_auth=%s", locale, getattr(request.user, "is_authenticated", False))
        if not locale:
            return Response({"detail": "locale_required"}, status=400)
        qs = PostLocale.objects.select_related("post", "post__cover_media").filter(locale=locale, post__status=PostStatus.PUBLISHED)
        category = request.query_params.get("category")
        tag = request.query_params.get("tag")
        featured = request.query_params.get("featured")
        q = request.query_params.get("q")
        ordering = request.query_params.get("ordering") or "-post__published_at"
        if category:
            qs = qs.filter(post__postcategory__category__locales__slug_locale=category, post__postcategory__category__locales__locale=locale)
        if tag:
            qs = qs.filter(post__posttag__tag__locales__slug_locale=tag, post__posttag__tag__locales__locale=locale)
        if featured in ("true", "1"):
            qs = qs.filter(post__is_featured=True)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q))
        qs = qs.order_by(ordering)
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(qs, request)
        ser = FeedItemSerializer(page, many=True)
        return paginator.get_paginated_response(ser.data)


class PostBySlugView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        locale = request.query_params.get("locale")
        slug = request.query_params.get("slug")
        if not locale or not slug:
            return Response({"detail": "locale_and_slug_required"}, status=400)
        try:
            obj = PostLocale.objects.select_related("post").get(locale=locale, slug_locale=slug)
        except PostLocale.DoesNotExist:
            return Response({"detail": "not_found"}, status=404)
        ser = PostLocaleDetailSerializer(obj)
        return Response(ser.data)


class NavigationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        locale = request.query_params.get("locale")
        logger.info("NavigationView locale=%s", locale)
        if not locale:
            return Response({"detail": "locale_required"}, status=400)
        cats = CategoryLocale.objects.filter(locale=locale).annotate(
            posts_count=Count("category__postcategory", filter=Q(category__postcategory__post__status=PostStatus.PUBLISHED))
        ).order_by("name")
        tags = TagLocale.objects.filter(locale=locale).annotate(
            posts_count=Count("tag__posttag", filter=Q(tag__posttag__post__status=PostStatus.PUBLISHED))
        ).order_by("name")
        return Response({
            "categories": [{"name": c.name, "slug": c.slug_locale, "count": c.posts_count} for c in cats],
            "tags": [{"name": t.name, "slug": t.slug_locale, "count": t.posts_count} for t in tags],
        })


class RelatedView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        locale = request.query_params.get("locale")
        slug = request.query_params.get("slug")
        limit = int(request.query_params.get("limit") or "6")
        if not locale or not slug:
            return Response({"detail": "locale_and_slug_required"}, status=400)
        try:
            current = PostLocale.objects.select_related("post").get(locale=locale, slug_locale=slug)
        except PostLocale.DoesNotExist:
            return Response({"detail": "not_found"}, status=404)
        qs_tags = PostLocale.objects.select_related("post").filter(
            locale=locale,
            post__status=PostStatus.PUBLISHED,
            post__posttag__tag__locales__locale=locale,
            post__posttag__tag__locales__slug_locale__in=list(
                TagLocale.objects.filter(tag__posttag__post=current.post, locale=locale).values_list("slug_locale", flat=True)
            ),
        ).exclude(post=current.post)
        qs_cats = PostLocale.objects.select_related("post").filter(
            locale=locale,
            post__status=PostStatus.PUBLISHED,
            post__postcategory__category__locales__locale=locale,
            post__postcategory__category__locales__slug_locale__in=list(
                CategoryLocale.objects.filter(category__postcategory__post=current.post, locale=locale).values_list("slug_locale", flat=True)
            ),
        ).exclude(post=current.post)
        qs = qs_tags.union(qs_cats).order_by("-post__published_at")[:limit]
        ser = FeedItemSerializer(qs, many=True)
        return Response(ser.data)


class FeaturedView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        locale = request.query_params.get("locale")
        limit = int(request.query_params.get("limit") or "5")
        if not locale:
            return Response({"detail": "locale_required"}, status=400)
        qs = PostLocale.objects.select_related("post", "post__cover_media").filter(
            locale=locale,
            post__status=PostStatus.PUBLISHED,
            post__is_featured=True,
        ).order_by("-post__published_at")[:limit]
        ser = FeedItemSerializer(qs, many=True)
        return Response(ser.data)


class SuggestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        locale = request.query_params.get("locale")
        q = request.query_params.get("q")
        limit = int(request.query_params.get("limit") or "8")
        if not locale or not q:
            return Response({"detail": "locale_and_q_required"}, status=400)
        qs = PostLocale.objects.filter(locale=locale, post__status=PostStatus.PUBLISHED).filter(
            Q(title__icontains=q) | Q(summary__icontains=q)
        ).order_by("-post__published_at")[:limit]
        data = [{"title": x.title, "slug": x.slug_locale} for x in qs]
        return Response(data)
