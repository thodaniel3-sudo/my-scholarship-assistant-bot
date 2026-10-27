"""Configurable registry of tables the bot may search.

EDIT the column names below to match your actual Supabase schema.
Run scripts/inspect_database.sql in the Supabase SQL Editor to discover them.
"""

SEARCHABLE_TABLES = {
    "universities": {
        "display_name": "Universities",
        "search_columns": ["name"],            # <-- EDIT if your column differs
        "return_columns": ["id", "name"],      # <-- EDIT
        "user_scoped": False,
    },
    "programmes": {
        "display_name": "Programmes",
        "search_columns": ["name"],            # <-- EDIT
        "return_columns": ["id", "name", "university_id"],
        "user_scoped": False,
    },
    "scholarships": {
        "display_name": "Scholarships",
        "search_columns": ["title"],           # <-- EDIT
        "return_columns": ["id", "title"],
        "user_scoped": False,
    },
}