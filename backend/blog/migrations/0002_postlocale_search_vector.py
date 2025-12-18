from django.db import migrations
from django.contrib.postgres.operations import CreateExtension
from django.contrib.postgres.search import SearchVectorField


def create_tsvector_trigger(apps, schema_editor):
    schema_editor.execute("""
        CREATE FUNCTION blog_postlocale_tsvector_update() RETURNS trigger AS $$
        begin
            new.search_vector := to_tsvector(
                CASE new.locale
                    WHEN 'pt' THEN 'portuguese'
                    WHEN 'en' THEN 'english'
                    WHEN 'es' THEN 'spanish'
                    ELSE 'simple'
                END,
                coalesce(new.title,'') || ' ' || coalesce(new.body_html,'')
            );
            return new;
        end
        $$ LANGUAGE plpgsql;
    """)
    schema_editor.execute("""
        CREATE TRIGGER blog_postlocale_tsvector_update_trigger
        BEFORE INSERT OR UPDATE OF title, body_html, locale
        ON blog_postlocale
        FOR EACH ROW EXECUTE FUNCTION blog_postlocale_tsvector_update();
    """)
    schema_editor.execute("CREATE INDEX IF NOT EXISTS blog_postlocale_search_vector_gin ON blog_postlocale USING GIN (search_vector)")
    schema_editor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    schema_editor.execute("CREATE EXTENSION IF NOT EXISTS unaccent")
    schema_editor.execute("CREATE INDEX IF NOT EXISTS blog_postlocale_slug_trgm ON blog_postlocale USING GIN (slug_locale gin_trgm_ops)")
    schema_editor.execute("CREATE INDEX IF NOT EXISTS blog_postlocale_title_trgm ON blog_postlocale USING GIN (title gin_trgm_ops)")


def drop_tsvector_trigger(apps, schema_editor):
    schema_editor.execute("DROP INDEX IF EXISTS blog_postlocale_title_trgm")
    schema_editor.execute("DROP INDEX IF EXISTS blog_postlocale_slug_trgm")
    schema_editor.execute("DROP INDEX IF EXISTS blog_postlocale_search_vector_gin")
    schema_editor.execute("DROP TRIGGER IF EXISTS blog_postlocale_tsvector_update_trigger ON blog_postlocale")
    schema_editor.execute("DROP FUNCTION IF EXISTS blog_postlocale_tsvector_update()")


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
    ]
    operations = [
        migrations.AddField(
            model_name='postlocale',
            name='search_vector',
            field=SearchVectorField(null=True),
        ),
        migrations.RunPython(create_tsvector_trigger, drop_tsvector_trigger),
    ]
