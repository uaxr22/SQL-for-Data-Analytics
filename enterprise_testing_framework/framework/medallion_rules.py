def build_not_null_checks(table, columns):
    """Create SQL statements that count NULLs for each column."""
    return [
        f"SELECT COUNT(*) AS null_{col} FROM {table} WHERE {col} IS NULL"
        for col in columns
    ]


def build_unique_checks(table, columns):
    """Create SQL statements that find duplicate values per column."""
    return [
        (
            "SELECT {col}, COUNT(*) AS dup_count FROM {table} "
            "GROUP BY {col} HAVING COUNT(*) > 1"
        ).format(col=col, table=table)
        for col in columns
    ]
