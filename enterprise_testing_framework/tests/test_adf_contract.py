import sys
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
# Add framework path so tests can import local modules.
sys.path.append(str(BASE_DIR))

from framework.adf_contract import (  # noqa: E402
    find_failure_handler,
    get_activity_names,
    get_copy_activity_inputs,
    get_parameters,
    get_pipeline_name,
    load_pipeline,
)
from framework.config_loader import load_config  # noqa: E402


CONFIG_PATH = BASE_DIR / "config" / "sources.json"
PIPELINE_PATH = BASE_DIR / "adf" / "pipeline_multiple_sources.json"


class TestAdfContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load config and pipeline once for all tests.
        cls.config = load_config(CONFIG_PATH)
        cls.pipeline = load_pipeline(PIPELINE_PATH)
        cls.adf_config = cls.config["adf"]

    def test_pipeline_name(self):
        # Pipeline name must match the expected contract.
        self.assertEqual(
            get_pipeline_name(self.pipeline),
            self.adf_config["pipeline_name"],
        )

    def test_required_parameters(self):
        # Required parameters must exist in the pipeline definition.
        pipeline_params = set(get_parameters(self.pipeline))
        for param in self.adf_config["parameters"]:
            self.assertIn(param, pipeline_params)

    def test_expected_sources_present(self):
        # Each expected source should have a Copy activity and dataset.
        activity_names = set(get_activity_names(self.pipeline))
        copy_inputs = get_copy_activity_inputs(self.pipeline)
        for source in self.adf_config["expected_sources"]:
            self.assertIn(source["activity"], activity_names)
            self.assertIn(source["dataset"], copy_inputs.get(source["activity"], []))

    def test_failure_handler_present(self):
        # Ensure the pipeline contains a failure handling step.
        handler = find_failure_handler(self.pipeline)
        self.assertIsNotNone(handler)


if __name__ == "__main__":
    unittest.main()
