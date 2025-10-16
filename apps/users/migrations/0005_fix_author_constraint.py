# Manual migration to fix constraint name after table rename

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_author_user'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            DO $$
            BEGIN
                -- Drop old constraint if it exists
                IF EXISTS (
                    SELECT 1 FROM pg_constraint 
                    WHERE conname = 'author_profiles_user_id_key'
                ) THEN
                    ALTER TABLE authors DROP CONSTRAINT author_profiles_user_id_key;
                END IF;
                
                -- Create new constraint if it doesn't exist
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint 
                    WHERE conname = 'authors_user_id_key'
                ) THEN
                    ALTER TABLE authors ADD CONSTRAINT authors_user_id_key UNIQUE (user_id);
                END IF;
            END $$;
            """,
            reverse_sql="""
            DO $$
            BEGIN
                -- Drop new constraint if it exists
                IF EXISTS (
                    SELECT 1 FROM pg_constraint 
                    WHERE conname = 'authors_user_id_key'
                ) THEN
                    ALTER TABLE authors DROP CONSTRAINT authors_user_id_key;
                END IF;
                
                -- Restore old constraint if it doesn't exist
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint 
                    WHERE conname = 'author_profiles_user_id_key'
                ) THEN
                    ALTER TABLE authors ADD CONSTRAINT author_profiles_user_id_key UNIQUE (user_id);
                END IF;
            END $$;
            """,
        ),
    ]
