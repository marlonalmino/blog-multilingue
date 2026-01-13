from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.db import transaction
from django.utils import timezone
from accounts.models import Role, UserRole
from taxonomy.models import Category, CategoryLocale, Tag, TagLocale, PostCategory, PostTag
from blog.models import Post, PostLocale, PostStatus, Locale
from comments.models import Comment, CommentStatus
from media.models import MediaAsset
import uuid


class Command(BaseCommand):
    help = "Populate high-quality demo data for screenshots"

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
        authors = [
            ("alice", "alice@example.com"),
            ("bob", "bob@example.com"),
            ("carol", "carol@example.com"),
            ("diego", "diego@example.com"),
        ]
        for username, email in authors:
            u, c = User.objects.get_or_create(username=username, defaults={"email": email})
            if c or not u.password:
                u.set_password("password123")
                u.save()
            UserRole.objects.get_or_create(user=u, role=Role.objects.get(name="Author"))
        cat_data = [
            {"en": ("Web Development", "Frontend, backend, and modern web tooling."), "pt": ("Desenvolvimento Web", "Frontend, backend e ferramentas modernas."), "es": ("Desarrollo Web", "Frontend, backend y herramientas modernas.")},
            {"en": ("Data Engineering", "Pipelines, storage, and data modeling."), "pt": ("Engenharia de Dados", "Pipelines, armazenamento e modelagem de dados."), "es": ("Ingeniería de Datos", "Pipelines, almacenamiento y modelado de datos.")},
            {"en": ("DevOps", "CI/CD, observability, and deployments."), "pt": ("DevOps", "CI/CD, observabilidade e deploy."), "es": ("DevOps", "CI/CD, observabilidad y despliegues.")},
            {"en": ("UI/UX", "Design systems and accessibility."), "pt": ("UI/UX", "Design systems e acessibilidade."), "es": ("UI/UX", "Sistemas de diseño y accesibilidad.")},
        ]
        categories = []
        for entry in cat_data:
            en_name, en_desc = entry["en"]
            en_slug = slugify(en_name)
            existing = CategoryLocale.objects.filter(locale=Locale.EN, slug_locale=en_slug).first()
            c = existing.category if existing else Category.objects.create()
            for loc in [Locale.EN, Locale.PT, Locale.ES]:
                name, desc = entry[loc]
                slug = slugify(name)
                CategoryLocale.objects.get_or_create(
                    category=c,
                    locale=loc,
                    slug_locale=slug,
                    defaults={"name": name, "description": desc},
                )
            categories.append(c)
        tag_names = [
            {"en": "Next.js", "pt": "Next.js", "es": "Next.js"},
            {"en": "Django REST", "pt": "Django REST", "es": "Django REST"},
            {"en": "TypeScript", "pt": "TypeScript", "es": "TypeScript"},
            {"en": "PostgreSQL", "pt": "PostgreSQL", "es": "PostgreSQL"},
            {"en": "Tailwind CSS", "pt": "Tailwind CSS", "es": "Tailwind CSS"},
            {"en": "SEO", "pt": "SEO", "es": "SEO"},
            {"en": "Performance", "pt": "Performance", "es": "Performance"},
            {"en": "Accessibility", "pt": "Acessibilidade", "es": "Accesibilidad"},
        ]
        tags = []
        for item in tag_names:
            en_slug = slugify(item["en"])
            existing_tag = TagLocale.objects.filter(locale=Locale.EN, slug_locale=en_slug).first()
            t = existing_tag.tag if existing_tag else Tag.objects.create()
            for loc in [Locale.EN, Locale.PT, Locale.ES]:
                name = item[loc]
                slug = slugify(name)
                TagLocale.objects.get_or_create(tag=t, locale=loc, slug_locale=slug, defaults={"name": name})
            tags.append(t)
        def _media(path):
            return MediaAsset.objects.get_or_create(
                path=path,
                defaults={"mime_type": "image/jpeg", "width": 1920, "height": 1080, "checksum": uuid.uuid4().hex, "size_bytes": 250000},
            )[0]
        cover1 = _media("/media/demo/cover-modern-seo.jpg")
        cover2 = _media("/media/demo/cover-django-rest.jpg")
        cover3 = _media("/media/demo/cover-typescript-performance.jpg")
        cover4 = _media("/media/demo/cover-postgres-fulltext.jpg")
        cover5 = _media("/media/demo/cover-tailwind-accessibility.jpg")
        cover6 = _media("/media/demo/cover-content-i18n.jpg")
        demo_posts = [
            {
                "slug": "modern-seo-nextjs",
                "covers": cover1,
                "author": "alice",
                "featured": True,
                "locales": {
                    Locale.EN: {
                        "title": "Modern SEO for Next.js Blogs",
                        "summary": "Technical and content strategies to rank better with Next.js.",
                        "body_md": "# Modern SEO\n\nOptimize metadata, performance, and content structure.\n\n- Canonical URLs\n- Open Graph tags\n- Fast LCP",
                        "og_title": "Modern SEO for Next.js Blogs",
                        "og_description": "Strategies for better ranking and rich sharing.",
                    },
                    Locale.PT: {
                        "title": "SEO moderno para blogs em Next.js",
                        "summary": "Técnicas técnicas e de conteúdo para ranquear melhor com Next.js.",
                        "body_md": "# SEO moderno\n\nOtimize metadados, performance e estrutura de conteúdo.\n\n- URLs canônicas\n- Tags Open Graph\n- LCP rápido",
                        "og_title": "SEO moderno para blogs em Next.js",
                        "og_description": "Estratégias para ranqueamento e compartilhamento ricos.",
                    },
                    Locale.ES: {
                        "title": "SEO moderno para blogs en Next.js",
                        "summary": "Estrategias técnicas y de contenido para posicionar mejor con Next.js.",
                        "body_md": "# SEO moderno\n\nOptimiza metadatos, rendimiento y estructura de contenido.\n\n- URLs canónicas\n- Etiquetas Open Graph\n- LCP rápido",
                        "og_title": "SEO moderno para blogs en Next.js",
                        "og_description": "Estrategias para mejor posicionamiento y compartidos ricos.",
                    },
                },
                "cats": [0],
                "tags": ["Next.js", "SEO", "Performance"],
            },
            {
                "slug": "django-rest-best-practices",
                "covers": cover2,
                "author": "bob",
                "featured": True,
                "locales": {
                    Locale.EN: {
                        "title": "Django REST Best Practices",
                        "summary": "Authentication, pagination, filtering, and error handling.",
                        "body_md": "# Best Practices\n\nBuild robust APIs with DRF.\n\n- JWT auth\n- Pagination\n- Filters",
                        "og_title": "Django REST Best Practices",
                        "og_description": "Patterns for reliable and secure APIs.",
                    },
                    Locale.PT: {
                        "title": "Boas práticas com Django REST",
                        "summary": "Autenticação, paginação, filtros e tratamento de erros.",
                        "body_md": "# Boas práticas\n\nConstrua APIs robustas com DRF.\n\n- Autenticação JWT\n- Paginação\n- Filtros",
                        "og_title": "Boas práticas com Django REST",
                        "og_description": "Padrões para APIs confiáveis e seguras.",
                    },
                    Locale.ES: {
                        "title": "Buenas prácticas con Django REST",
                        "summary": "Autenticación, paginación, filtrado y manejo de errores.",
                        "body_md": "# Buenas prácticas\n\nConstruye APIs robustas con DRF.\n\n- JWT\n- Paginación\n- Filtros",
                        "og_title": "Buenas prácticas con Django REST",
                        "og_description": "Patrones para APIs confiables y seguras.",
                    },
                },
                "cats": [0, 2],
                "tags": ["Django REST", "PostgreSQL", "Performance"],
            },
            {
                "slug": "typescript-performance-patterns",
                "covers": cover3,
                "author": "carol",
                "featured": False,
                "locales": {
                    Locale.EN: {
                        "title": "TypeScript Performance Patterns",
                        "summary": "Practical patterns to reduce re-renders and heavy code paths.",
                        "body_md": "# Patterns\n\nMemoization, virtualization, and lean components.\n\n- useMemo\n- windowing\n- code splitting",
                        "og_title": "TypeScript Performance Patterns",
                        "og_description": "Reduce re-renders and improve UX.",
                    },
                    Locale.PT: {
                        "title": "Padrões de performance com TypeScript",
                        "summary": "Padrões práticos para reduzir re-renders e caminhos pesados.",
                        "body_md": "# Padrões\n\nMemoization, virtualização e componentes leves.\n\n- useMemo\n- windowing\n- code splitting",
                        "og_title": "Padrões de performance com TypeScript",
                        "og_description": "Reduza re-renders e melhore UX.",
                    },
                    Locale.ES: {
                        "title": "Patrones de rendimiento con TypeScript",
                        "summary": "Patrones prácticos para reducir re-renderizados y rutas pesadas.",
                        "body_md": "# Patrones\n\nMemoization, virtualización y componentes ligeros.\n\n- useMemo\n- windowing\n- code splitting",
                        "og_title": "Patrones de rendimiento con TypeScript",
                        "og_description": "Mejora UX reduciendo re-renderizados.",
                    },
                },
                "cats": [0],
                "tags": ["TypeScript", "Performance"],
            },
            {
                "slug": "postgres-full-text-search",
                "covers": cover4,
                "author": "diego",
                "featured": True,
                "locales": {
                    Locale.EN: {
                        "title": "PostgreSQL Full‑Text Search for Blogs",
                        "summary": "Language-aware search with tsvector tuned for multilingual posts.",
                        "body_md": "# Full‑Text Search\n\nUse language configs and proper indexing.\n\n- tsvector\n- GIN indexes\n- locale aware",
                        "og_title": "PostgreSQL Full‑Text Search",
                        "og_description": "Language-aware search tuned for content.",
                    },
                    Locale.PT: {
                        "title": "Busca full‑text com PostgreSQL para blogs",
                        "summary": "Busca sensível ao idioma com tsvector para posts multilíngues.",
                        "body_md": "# Busca Full‑Text\n\nUse configurações por idioma e indexação adequada.\n\n- tsvector\n- índices GIN\n- sensível ao locale",
                        "og_title": "Busca Full‑Text com PostgreSQL",
                        "og_description": "Busca ajustada ao conteúdo e idioma.",
                    },
                    Locale.ES: {
                        "title": "Búsqueda full‑text con PostgreSQL para blogs",
                        "summary": "Búsqueda con conocimiento del idioma usando tsvector.",
                        "body_md": "# Búsqueda Full‑Text\n\nConfigs de idioma y buen indexado.\n\n- tsvector\n- índices GIN\n- locale aware",
                        "og_title": "Búsqueda Full‑Text con PostgreSQL",
                        "og_description": "Búsqueda ajustada al contenido multilingüe.",
                    },
                },
                "cats": [1],
                "tags": ["PostgreSQL", "Performance"],
            },
            {
                "slug": "tailwind-accessible-design",
                "covers": cover5,
                "author": "alice",
                "featured": False,
                "locales": {
                    Locale.EN: {
                        "title": "Accessible Design with Tailwind CSS",
                        "summary": "Color contrast, focus states, and semantic components.",
                        "body_md": "# Accessible Design\n\nCompose accessible UI primitives.\n\n- contrast\n- focus\n- landmarks",
                        "og_title": "Accessible Design with Tailwind",
                        "og_description": "Build inclusive interfaces with utility classes.",
                    },
                    Locale.PT: {
                        "title": "Design acessível com Tailwind CSS",
                        "summary": "Contraste de cores, estados de foco e componentes semânticos.",
                        "body_md": "# Design acessível\n\nComponha primitivas de UI acessíveis.\n\n- contraste\n- foco\n- landmarks",
                        "og_title": "Design acessível com Tailwind",
                        "og_description": "Interfaces inclusivas com utilitários.",
                    },
                    Locale.ES: {
                        "title": "Diseño accesible con Tailwind CSS",
                        "summary": "Contraste, estados de foco y componentes semánticos.",
                        "body_md": "# Diseño accesible\n\nCompón primitivas accesibles.\n\n- contraste\n- foco\n- landmarks",
                        "og_title": "Diseño accesible con Tailwind",
                        "og_description": "Interfaces inclusivas con utilidades.",
                    },
                },
                "cats": [3],
                "tags": ["Tailwind CSS", "Accessibility"],
            },
            {
                "slug": "content-localization-i18n",
                "covers": cover6,
                "author": "bob",
                "featured": False,
                "locales": {
                    Locale.EN: {
                        "title": "Content Localization and i18n",
                        "summary": "Organize translations, slugs per locale, and SEO metadata.",
                        "body_md": "# i18n\n\nStructure multi-locale content and routing.\n\n- locale slugs\n- SEO per locale\n- translation flow",
                        "og_title": "Content Localization and i18n",
                        "og_description": "Structure multi-locale content effectively.",
                    },
                    Locale.PT: {
                        "title": "Localização de conteúdo e i18n",
                        "summary": "Organize traduções, slugs por idioma e metadados de SEO.",
                        "body_md": "# i18n\n\nEstruture conteúdo multi-locale e roteamento.\n\n- slugs por idioma\n- SEO por locale\n- fluxo de tradução",
                        "og_title": "Localização de conteúdo e i18n",
                        "og_description": "Estruture conteúdo multi-língue com eficiência.",
                    },
                    Locale.ES: {
                        "title": "Localización de contenido e i18n",
                        "summary": "Organiza traducciones, slugs por idioma y metadatos SEO.",
                        "body_md": "# i18n\n\nEstructura contenido multi-locale y enrutado.\n\n- slugs por idioma\n- SEO por locale\n- flujo de traducción",
                        "og_title": "Localización de contenido e i18n",
                        "og_description": "Estructura contenido multilingüe de forma eficaz.",
                    },
                },
                "cats": [0],
                "tags": ["Next.js", "SEO", "Django REST"],
            },
        ]
        users_map = {u.username: u for u in User.objects.filter(username__in=[d["author"] for d in demo_posts])}
        tag_map = {}
        for t in tags:
            tl = TagLocale.objects.filter(tag=t, locale=Locale.EN).first()
            if tl:
                tag_map[tl.name] = t
        for data in demo_posts:
            post, created_post = Post.objects.get_or_create(
                slug_base=data["slug"],
                defaults={
                    "author": users_map.get(data["author"], admin),
                    "status": PostStatus.PUBLISHED,
                    "published_at": timezone.now(),
                    "cover_media": data["covers"],
                    "canonical_url": "",
                    "is_featured": data["featured"],
                },
            )
            for loc, vals in data["locales"].items():
                title = vals["title"]
                summary = vals["summary"]
                body_md = vals["body_md"]
                lines = [ln.strip() for ln in body_md.splitlines()]
                bullets = [ln[2:].strip() for ln in lines if ln.startswith("- ")]
                ul = "".join([f"<li>{b}</li>" for b in bullets])
                body_html = f"<h1>{title}</h1><p>{summary}</p>" + (f"<ul>{ul}</ul>" if ul else "")
                slug_loc = slugify(title)
                PostLocale.objects.update_or_create(
                    post=post,
                    locale=loc,
                    defaults={
                        "title": title,
                        "summary": summary,
                        "body_md": body_md,
                        "body_html": body_html,
                        "slug_locale": slug_loc,
                        "seo_title": title,
                        "seo_description": summary,
                        "og_title": vals["og_title"],
                        "og_description": vals["og_description"],
                        "og_image_media": data["covers"],
                    },
                )
            for ci in data["cats"]:
                PostCategory.objects.get_or_create(post=post, category=categories[ci])
            for tag_name in data["tags"]:
                t = tag_map.get(tag_name)
                if t:
                    PostTag.objects.get_or_create(post=post, tag=t)
            c1 = Comment.objects.create(post=post, user=admin, body="Excelente conteúdo. Vou aplicar no próximo projeto.", status=CommentStatus.APPROVED)
            c2 = Comment.objects.create(post=post, user=users_map.get("alice"), body="Gostei das dicas práticas, especialmente sobre SEO.", status=CommentStatus.APPROVED)
            Comment.objects.create(post=post, user=users_map.get("bob"), parent=c1, body="Concordo, os exemplos são objetivos.", status=CommentStatus.APPROVED)
