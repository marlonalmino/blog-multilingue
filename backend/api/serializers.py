from rest_framework import serializers
from blog.models import Post, PostLocale
from taxonomy.models import CategoryLocale, TagLocale
from embeds.models import Embed
from comments.models import Comment
from media.models import MediaAsset


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "slug_base", "status", "published_at", "canonical_url", "is_featured", "author", "cover_media")


class PostLocaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLocale
        fields = ("id", "post", "locale", "title", "summary", "body_md", "body_html", "slug_locale", "seo_title", "seo_description", "og_title", "og_description", "og_image_media", "reading_time_words")


class CategoryLocaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryLocale
        fields = ("id", "category", "locale", "name", "slug_locale", "description")


class TagLocaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagLocale
        fields = ("id", "tag", "locale", "name", "slug_locale")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "post", "user", "parent", "body", "status", "spam_score", "created_at")


class MediaAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaAsset
        fields = ("id", "storage_provider", "path", "mime_type", "width", "height", "checksum", "size_bytes", "metadata", "created_at")


class PostLocaleDetailSerializer(serializers.ModelSerializer):
    categories = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    embeds = serializers.SerializerMethodField()

    class Meta:
        model = PostLocale
        fields = (
            "id", "post", "locale", "title", "summary", "body_md", "body_html", "slug_locale",
            "seo_title", "seo_description", "og_title", "og_description", "og_image_media", "reading_time_words",
            "categories", "tags", "embeds",
        )

    def get_categories(self, obj):
        qs = CategoryLocale.objects.filter(category__postcategory__post=obj.post, locale=obj.locale)
        return [{"name": c.name, "slug": c.slug_locale} for c in qs.distinct()]

    def get_tags(self, obj):
        qs = TagLocale.objects.filter(tag__posttag__post=obj.post, locale=obj.locale)
        return [{"name": t.name, "slug": t.slug_locale} for t in qs.distinct()]

    def get_embeds(self, obj):
        qs = Embed.objects.filter(post_locale=obj).order_by("position")
        return [{"url": e.url, "provider": e.provider_domain.domain, "position": e.position, "metadata": e.metadata} for e in qs]


class FeedItemSerializer(serializers.ModelSerializer):
    cover = serializers.SerializerMethodField()
    published_at = serializers.DateTimeField(source="post.published_at")
    categories = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = PostLocale
        fields = ("id", "post", "locale", "title", "summary", "slug_locale", "cover", "published_at", "categories", "tags")

    def get_cover(self, obj):
        media = obj.post.cover_media
        return media.path if media else None

    def get_categories(self, obj):
        qs = CategoryLocale.objects.filter(category__postcategory__post=obj.post, locale=obj.locale)
        return [{"name": c.name, "slug": c.slug_locale} for c in qs.distinct()]

    def get_tags(self, obj):
        qs = TagLocale.objects.filter(tag__posttag__post=obj.post, locale=obj.locale)
        return [{"name": t.name, "slug": t.slug_locale} for t in qs.distinct()]
