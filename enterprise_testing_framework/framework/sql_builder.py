from .medallion_rules import (
    build_not_null_checks,
    build_range_checks,
    build_referential_checks,
    build_unique_checks,
)


def build_quality_sql(layer_name, layer_config):
    table = layer_config.get("table")
    statements = []
    statements.extend(build_not_null_checks(table, layer_config.get("not_null", [])))
    statements.extend(build_unique_checks(table, layer_config.get("unique", [])))
    statements.extend(build_range_checks(table, layer_config.get("range", [])))
    if layer_config.get("referential"):
        statements.extend(build_referential_checks(table, layer_config["referential"]))
    return statements


def render_quality_sql(layer_name, layer_config):
    statements = build_quality_sql(layer_name, layer_config)
    if not statements:
        return f"-- {layer_name} quality checks (no rules configured)"
    header = f"-- {layer_name} quality checks"
    body = ";\n\n".join(statements) + ";"
    return f"{header}\n{body}"
