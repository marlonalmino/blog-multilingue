from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Role, UserRole
from taxonomy.models import Category, CategoryLocale, Tag, TagLocale, PostCategory, PostTag
from blog.models import Post, PostLocale, PostStatus, Locale
from comments.models import Comment, CommentStatus
from django.utils.text import slugify
from django.db import transaction
from datetime import datetime, timezone


class Command(BaseCommand):
    help = "Populate initial data: roles, users, taxonomy, posts with translations, comments"

    def add_arguments(self, parser):
        parser.add_argument("--posts", type=int, default=5)

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        roles = ["Admin", "Editor", "Author", "Translator", "Reader"]
        for r in roles:
            Role.objects.get_or_create(name=r)
        admin_email = "admin@example.com"
        admin, created = User.objects.get_or_create(username="admin", defaults={"email": admin_email})
        if created or not admin.password:
            admin.set_password("admin123")
            admin.save()
        UserRole.objects.get_or_create(user=admin, role=Role.objects.get(name="Admin"))
        cat_names = {"pt": ["Tecnologia", "Tutoriais", "Noticias"], "en": ["Technology", "Tutorials", "News"], "es": ["Tecnología", "Tutoriales", "Noticias"]}
        categories = []
        for i in range(3):
            # Use PT as primary key to resolve existing category
            pt_slug = slugify(cat_names[Locale.PT][i])
            existing = CategoryLocale.objects.filter(locale=Locale.PT, slug_locale=pt_slug).first()
            c = existing.category if existing else Category.objects.create()
            for loc in [Locale.PT, Locale.EN, Locale.ES]:
                name = cat_names[loc][i]
                slug = slugify(name)
                CategoryLocale.objects.get_or_create(
                    category=c,
                    locale=loc,
                    slug_locale=slug,
                    defaults={"name": name, "description": ""},
                )
            categories.append(c)
        tag_names = {"pt": ["Django", "Next.js", "PostgreSQL"], "en": ["Django", "Next.js", "PostgreSQL"], "es": ["Django", "Next.js", "PostgreSQL"]}
        tags = []
        for i in range(3):
            # Use EN as primary key for tag resolution
            en_slug = slugify(tag_names[Locale.EN][i])
            existing_tag = TagLocale.objects.filter(locale=Locale.EN, slug_locale=en_slug).first()
            t = existing_tag.tag if existing_tag else Tag.objects.create()
            for loc in [Locale.PT, Locale.EN, Locale.ES]:
                name = tag_names[loc][i]
                slug = slugify(name)
                TagLocale.objects.get_or_create(tag=t, locale=loc, slug_locale=slug, defaults={"name": name})
            tags.append(t)
        posts_count = options["posts"]
        for i in range(posts_count):
            slug_base = f"post-{i+1}"
            post, created_post = Post.objects.get_or_create(
                slug_base=slug_base,
                defaults={
                    "author": admin,
                    "status": PostStatus.PUBLISHED,
                    "published_at": datetime.now(timezone.utc),
                    "canonical_url": "",
                    "is_featured": (i % 2 == 0),
                },
            )
            for loc in [Locale.PT, Locale.EN, Locale.ES]:
                title = f"Post {i+1} {loc}"
                summary = f"Resumo {loc} para {slug_base}" if loc == Locale.PT else f"Summary {loc} for {slug_base}"
                body_md = f"# {title}\n\nConteúdo em {loc}"
                body_html = f"<h1>{title}</h1><p>Conteúdo em {loc}</p>"
                PostLocale.objects.get_or_create(
                    post=post,
                    locale=loc,
                    defaults={
                        "title": title,
                        "summary": summary,
                        "body_md": body_md,
                        "body_html": body_html,
                        "slug_locale": f"{slug_base}-{loc}",
                        "seo_title": title,
                        "seo_description": summary,
                    },
                )
            PostCategory.objects.get_or_create(post=post, category=categories[i % len(categories)])
            PostTag.objects.get_or_create(post=post, tag=tags[i % len(tags)])
            if not Comment.objects.filter(post=post, user=admin, body="Excelente!").exists():
                Comment.objects.create(post=post, user=admin, body="Excelente!", status=CommentStatus.APPROVED)
            if not Comment.objects.filter(post=post, user__isnull=True, body="Comentário aguardando aprovação").exists():
                Comment.objects.create(post=post, user=None, body="Comentário aguardando aprovação", status=CommentStatus.PENDING)
        self.stdout.write(self.style.SUCCESS(f"Seed concluído: {posts_count} posts, categorias/tags e comentários criados"))
