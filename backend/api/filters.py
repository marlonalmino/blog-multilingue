from django_filters import rest_framework as filters
from blog.models import Post, PostLocale
from taxonomy.models import CategoryLocale, TagLocale
from comments.models import Comment
from django.contrib.postgres.search import SearchQuery
from django.db.models import F


class PostFilterSet(filters.FilterSet):
    status = filters.CharFilter(field_name="status", lookup_expr="exact")
    author = filters.NumberFilter(field_name="author_id", lookup_expr="exact")
    is_featured = filters.BooleanFilter(field_name="is_featured")
    published_after = filters.DateTimeFilter(field_name="published_at", lookup_expr="gte")
    published_before = filters.DateTimeFilter(field_name="published_at", lookup_expr="lte")

    class Meta:
        model = Post
        fields = ["status", "author", "is_featured", "published_after", "published_before"]


class PostLocaleFilterSet(filters.FilterSet):
    locale = filters.CharFilter(field_name="locale", lookup_expr="exact")
    slug = filters.CharFilter(field_name="slug_locale", lookup_expr="exact")
    q = filters.CharFilter(method="filter_search")
    category = filters.CharFilter(method="filter_category")
    tag = filters.CharFilter(method="filter_tag")

    class Meta:
        model = PostLocale
        fields = ["locale", "slug", "q", "category", "tag"]

    def filter_search(self, queryset, name, value):
        locale = self.data.get("locale")
        config = "simple"
        if locale == "pt":
            config = "portuguese"
        elif locale == "en":
            config = "english"
        elif locale == "es":
            config = "spanish"
        query = SearchQuery(value, config=config)
        return queryset.filter(search_vector=query)

    def filter_category(self, queryset, name, value):
        locale = self.data.get("locale")
        qs = queryset.filter(
            post__postcategory__category__locales__slug_locale=value
        )
        if locale:
            qs = qs.filter(post__postcategory__category__locales__locale=locale)
        return qs.distinct()

    def filter_tag(self, queryset, name, value):
        locale = self.data.get("locale")
        qs = queryset.filter(
            post__posttag__tag__locales__slug_locale=value
        )
        if locale:
            qs = qs.filter(post__posttag__tag__locales__locale=locale)
        return qs.distinct()


class CategoryLocaleFilterSet(filters.FilterSet):
    locale = filters.CharFilter(field_name="locale", lookup_expr="exact")

    class Meta:
        model = CategoryLocale
        fields = ["locale"]


class TagLocaleFilterSet(filters.FilterSet):
    locale = filters.CharFilter(field_name="locale", lookup_expr="exact")

    class Meta:
        model = TagLocale
        fields = ["locale"]


class CommentFilterSet(filters.FilterSet):
    post = filters.NumberFilter(field_name="post_id", lookup_expr="exact")
    status = filters.CharFilter(field_name="status", lookup_expr="exact")

    class Meta:
        model = Comment
        fields = ["post", "status"]
