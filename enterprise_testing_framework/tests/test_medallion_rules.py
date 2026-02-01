import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
# Add framework path so tests can import local modules.
sys.path.append(str(BASE_DIR))

from framework.config_loader import load_config  # noqa: E402


CONFIG_PATH = BASE_DIR / "config" / "sources.json"


class TestMedallionRules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load the JSON config once for all tests.
        cls.config = load_config(CONFIG_PATH)
        cls.medallion = cls.config["medallion"]

    def test_layers_present(self):
        # Ensure expected layers exist.
        for layer in ["bronze", "silver", "gold"]:
            self.assertIn(layer, self.medallion)

    def test_tables_configured(self):
        # Every layer must point to a table name.
        for layer, rules in self.medallion.items():
            self.assertIn("table", rules, msg=f"{layer} missing table")

    def test_not_null_rules_present(self):
        # Each layer must list not-null columns.
        for layer, rules in self.medallion.items():
            self.assertTrue(rules.get("not_null"), msg=f"{layer} missing not_null")

    def test_unique_rules_present(self):
        # Unique rules are required for bronze and silver layers.
        for layer in ["bronze", "silver"]:
            self.assertTrue(
                self.medallion[layer].get("unique"),
                msg=f"{layer} missing unique rules",
            )


if __name__ == "__main__":
    unittest.main()
