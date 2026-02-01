import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from framework.config_loader import load_config  # noqa: E402


CONFIG_PATH = BASE_DIR / "config" / "sources.json"
SQL_PATHS = {
    "bronze": BASE_DIR / "sql" / "bronze_quality.sql",
    "silver": BASE_DIR / "sql" / "silver_quality.sql",
    "gold": BASE_DIR / "sql" / "gold_quality.sql",
}


class TestSqlQualityRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config(CONFIG_PATH)
        cls.medallion = cls.config["medallion"]

    def _read_sql(self, layer):
        return SQL_PATHS[layer].read_text(encoding="utf-8").lower()

    def test_not_null_checks_covered(self):
        for layer, rules in self.medallion.items():
            sql_text = self._read_sql(layer)
            for column in rules.get("not_null", []):
                self.assertIn(f"{column.lower()} is null", sql_text)

    def test_unique_checks_covered(self):
        for layer in ["bronze", "silver"]:
            rules = self.medallion[layer]
            sql_text = self._read_sql(layer)
            for column in rules.get("unique", []):
                self.assertIn(f"group by {column.lower()}", sql_text)

    def test_range_checks_covered(self):
        for layer, rules in self.medallion.items():
            sql_text = self._read_sql(layer)
            for rule in rules.get("range", []):
                column = rule["column"].lower()
                if rule.get("min") is not None:
                    self.assertIn(f"{column} < {rule['min']}", sql_text)
                if rule.get("max") is not None:
                    self.assertIn(f"{column} > {rule['max']}", sql_text)

    def test_referential_checks_covered(self):
        silver_rules = self.medallion.get("silver", {})
        sql_text = self._read_sql("silver")
        for rule in silver_rules.get("referential", []):
            self.assertIn(rule["parent_table"].lower(), sql_text)
            self.assertIn(rule["child_column"].lower(), sql_text)
            self.assertIn(rule["parent_column"].lower(), sql_text)


if __name__ == "__main__":
    unittest.main()
