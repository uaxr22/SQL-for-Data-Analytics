def build_not_null_checks(table, columns):
    return [
        f"SELECT COUNT(*) AS null_{col} FROM {table} WHERE {col} IS NULL"
        for col in columns
    ]


def build_unique_checks(table, columns):
    return [
        (
            "SELECT {col}, COUNT(*) AS dup_count FROM {table} "
            "GROUP BY {col} HAVING COUNT(*) > 1"
        ).format(col=col, table=table)
        for col in columns
    ]


def build_range_checks(table, ranges):
    checks = []
    for rule in ranges:
        column = rule["column"]
        minimum = rule.get("min")
        maximum = rule.get("max")
        predicates = []
        if minimum is not None:
            predicates.append(f"{column} < {minimum}")
        if maximum is not None:
            predicates.append(f"{column} > {maximum}")
        if predicates:
            checks.append(
                "SELECT COUNT(*) AS out_of_range_{col} FROM {table} WHERE {pred}".format(
                    col=column, table=table, pred=" OR ".join(predicates)
                )
            )
    return checks


def build_referential_checks(child_table, rules):
    checks = []
    for rule in rules:
        child_column = rule["child_column"]
        parent_table = rule["parent_table"]
        parent_column = rule["parent_column"]
        checks.append(
            (
                "SELECT COUNT(*) AS orphan_{child} FROM {child_table} c "
                "LEFT JOIN {parent_table} p "
                "ON c.{child} = p.{parent} "
                "WHERE p.{parent} IS NULL"
            ).format(
                child=child_column,
                child_table=child_table,
                parent_table=parent_table,
                parent=parent_column,
            )
        )
    return checks
