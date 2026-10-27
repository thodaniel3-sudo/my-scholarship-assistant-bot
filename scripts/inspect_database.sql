-- Run each block in the Supabase SQL Editor. Paste the results back to me.

-- 1. All tables and views
SELECT table_schema, table_name, table_type
FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog','information_schema')
ORDER BY table_schema, table_name;

-- 2. Columns for a specific table (replace YOUR_TABLE)
-- SELECT column_name, data_type, is_nullable, column_default
-- FROM information_schema.columns
-- WHERE table_schema='public' AND table_name='YOUR_TABLE'
-- ORDER BY ordinal_position;

-- 3. Foreign keys
SELECT tc.table_name, kcu.column_name,
       ccu.table_name AS foreign_table_name,
       ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu USING (constraint_name)
JOIN information_schema.constraint_column_usage ccu USING (constraint_name)
WHERE tc.constraint_type='FOREIGN KEY' AND tc.table_schema='public';

-- 4. Approximate row counts
SELECT relname, n_live_tup FROM pg_stat_user_tables ORDER BY n_live_tup DESC;