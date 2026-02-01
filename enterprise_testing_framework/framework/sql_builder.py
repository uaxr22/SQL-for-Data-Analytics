from .medallion_rules import build_not_null_checks, build_unique_checks


def build_quality_sql(layer_config):
    """Build a list of SQL checks for a single medallion layer."""
    table = layer_config.get("table")
    statements = []
    # Not-null checks keep required columns populated.
    statements.extend(build_not_null_checks(table, layer_config.get("not_null", [])))
    # Unique checks prevent duplicate business keys.
    statements.extend(build_unique_checks(table, layer_config.get("unique", [])))
    return statements


def render_quality_sql(layer_name, layer_config):
    """Render SQL as a runnable script with a header comment."""
    statements = build_quality_sql(layer_config)
    if not statements:
        return f"-- {layer_name} quality checks (no rules configured)"
    header = f"-- {layer_name} quality checks"
    body = ";\n\n".join(statements) + ";"
    return f"{header}\n{body}"
