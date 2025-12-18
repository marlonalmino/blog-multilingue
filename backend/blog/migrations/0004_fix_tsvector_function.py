from django.db import migrations


def replace_tsvector_function(apps, schema_editor):
    schema_editor.execute("""
        CREATE OR REPLACE FUNCTION blog_postlocale_tsvector_update() RETURNS trigger AS $$
        begin
            new.search_vector := to_tsvector(
                (CASE new.locale
                    WHEN 'pt' THEN 'portuguese'
                    WHEN 'en' THEN 'english'
                    WHEN 'es' THEN 'spanish'
                    ELSE 'simple'
                END)::regconfig,
                coalesce(new.title,'') || ' ' || coalesce(new.body_html,'')
            );
            return new;
        end
        $$ LANGUAGE plpgsql;
    """)


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0003_alter_postlocale_search_vector'),
    ]
    operations = [
        migrations.RunPython(replace_tsvector_function),
    ]
