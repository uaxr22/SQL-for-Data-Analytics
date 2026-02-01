import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR))

from framework.config_loader import load_config  # noqa: E402


CONFIG_PATH = BASE_DIR / "config" / "sources.json"


class TestMedallionRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_config(CONFIG_PATH)
        cls.medallion = cls.config["medallion"]

    def test_layers_present(self):
        for layer in ["bronze", "silver", "gold"]:
            self.assertIn(layer, self.medallion)

    def test_tables_configured(self):
        for layer, rules in self.medallion.items():
            self.assertIn("table", rules, msg=f"{layer} missing table")

    def test_not_null_rules_present(self):
        for layer, rules in self.medallion.items():
            self.assertTrue(rules.get("not_null"), msg=f"{layer} missing not_null")

    def test_unique_rules_present(self):
        for layer in ["bronze", "silver"]:
            self.assertTrue(
                self.medallion[layer].get("unique"),
                msg=f"{layer} missing unique rules",
            )

    def test_range_rules_valid(self):
        for layer, rules in self.medallion.items():
            for rule in rules.get("range", []):
                minimum = rule.get("min")
                maximum = rule.get("max")
                if minimum is not None and maximum is not None:
                    self.assertLessEqual(minimum, maximum)

    def test_referential_rules_have_columns(self):
        for rule in self.medallion.get("silver", {}).get("referential", []):
            self.assertIn("child_column", rule)
            self.assertIn("parent_table", rule)
            self.assertIn("parent_column", rule)


if __name__ == "__main__":
    unittest.main()
